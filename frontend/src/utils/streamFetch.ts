/**
 * 原生 SSE 流式请求工具
 * 参考 MingAI-master 项目的设计，使用原生 fetch + ReadableStream
 * 替代 @microsoft/fetch-event-source，更轻量、更可控
 * 
 * 功能：
 * - 原生 fetch + ReadableStream 处理 SSE
 * - 统一的错误格式解析（支持后端 SSEErrorCode）
 * - 可选的重连机制
 * - 内存保护
 */

import { logger } from './logger'

// 内存保护：最大缓冲区大小（约 250KB）
export const MAX_BUFFER_SIZE = 250000

/**
 * SSE 解析结果类型
 */
export interface SSEParseResult {
  type: 'content' | 'error' | 'done' | 'skip'
  content?: string
  error?: { code: string; message: string }
}

/**
 * 解析 SSE 数据
 * 支持后端统一的错误格式: { type: "error", code: "ERROR_CODE", message: "..." }
 */
export function parseSSEData(data: string): SSEParseResult {
  if (!data || data === '[DONE]') {
    return { type: 'done' }
  }

  try {
    const parsed = JSON.parse(data)
    
    // 检查是否是统一的错误格式
    if (typeof parsed === 'object' && parsed !== null) {
      if (parsed.type === 'error') {
        return { 
          type: 'error', 
          error: { code: parsed.code || 'UNKNOWN', message: parsed.message || '未知错误' }
        }
      }
      // 兼容旧的错误格式
      if (parsed.error) {
        return { 
          type: 'error', 
          error: { code: 'LEGACY_ERROR', message: parsed.error }
        }
      }
    }
    
    // 普通内容
    const content = typeof parsed === 'string' ? parsed : String(parsed)
    return { type: 'content', content }
  } catch {
    // JSON 解析失败，直接作为文本内容
    if (data && !data.startsWith('[')) {
      return { type: 'content', content: data }
    }
    return { type: 'skip' }
  }
}

export interface StreamOptions {
  /** 收到每个数据块时的回调（累积的完整内容） */
  onChunk: (content: string) => void
  /** 发生错误时的回调 */
  onError?: (error: Error) => void
  /** 流结束时的回调 */
  onDone?: () => void
  /** 首次收到数据时的回调 */
  onFirstChunk?: () => void
  /** AbortController 的 signal，用于取消请求 */
  signal?: AbortSignal
}

export interface StreamFetchOptions extends Omit<RequestInit, 'body'> {
  /** 请求体（会自动 JSON.stringify） */
  body?: object | string
}

/**
 * 带重连机制的流式请求选项
 */
export interface StreamFetchWithRetryOptions extends StreamOptions {
  /** 最大重试次数（默认 3） */
  maxRetries?: number
  /** 重试延迟（毫秒，默认 1000） */
  retryDelay?: number
  /** 判断错误是否可重试的函数 */
  isRetryable?: (error: Error) => boolean
}

/**
 * 默认的可重试错误判断函数
 */
export function defaultIsRetryable(error: Error): boolean {
  const msg = error.message.toLowerCase()
  // 网络错误、超时、fetch 失败等可以重试
  return (
    msg.includes('network') ||
    msg.includes('timeout') ||
    msg.includes('fetch') ||
    msg.includes('failed to fetch') ||
    msg.includes('connection') ||
    msg.includes('ETIMEDOUT') ||
    msg.includes('ECONNREFUSED')
  )
}

/**
 * 发起流式请求并处理 SSE 数据
 * 
 * @param url - 请求地址
 * @param fetchOptions - fetch 选项
 * @param streamOptions - 流处理选项
 * 
 * @example
 * ```ts
 * await streamFetch(
 *   '/api/divination',
 *   {
 *     method: 'POST',
 *     body: { prompt: '今日运势', prompt_type: 'daily' },
 *     headers: { 'x-api-key': 'xxx' },
 *     signal: abortController.signal,
 *   },
 *   {
 *     onChunk: (content) => setResult(prev => prev + content),
 *     onError: (err) => toast.error(err.message),
 *     onDone: () => setStreaming(false),
 *     onFirstChunk: () => setLoading(false),
 *   }
 * )
 * ```
 */
export async function streamFetch(
  url: string,
  fetchOptions: StreamFetchOptions,
  streamOptions: StreamOptions
): Promise<void> {
  const { onChunk, onError, onDone, onFirstChunk, signal } = streamOptions

  // 处理请求体
  const body = typeof fetchOptions.body === 'object'
    ? JSON.stringify(fetchOptions.body)
    : fetchOptions.body

  // 合并默认 headers
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...fetchOptions.headers,
  }

  // 累积的完整内容（用于传递给 onChunk）
  let accumulatedContent = ''

  try {
    const response = await fetch(url, {
      ...fetchOptions,
      body,
      headers,
      signal,
    })

    // 检查响应状态
    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`HTTP ${response.status}: ${errorText}`)
    }

    // 检查是否是 SSE 响应
    const contentType = response.headers.get('content-type') || ''
    if (!contentType.includes('text/event-stream')) {
      // 不是 SSE，可能是 JSON 响应
      const data = await response.json()
      if (data.success && data.content) {
        onFirstChunk?.()
        onChunk(data.content)
        onDone?.()
        return
      } else {
        throw new Error(data.error || '响应格式错误')
      }
    }

    // 处理 SSE 流
    const reader = response.body!.getReader()
    const decoder = new TextDecoder()
    let lineBuffer = ''
    let isFirstChunk = true

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        // 解码并追加到缓冲区
        lineBuffer += decoder.decode(value, { stream: true })

        // 按行分割处理
        const lines = lineBuffer.split('\n')
        // 最后一行可能不完整，保留到下次处理
        lineBuffer = lines.pop() || ''

        for (const line of lines) {
          // 跳过空行和非数据行
          if (!line.startsWith('data: ')) continue

          const data = line.slice(6).trim()
          
          // 使用统一的解析函数
          const result = parseSSEData(data)

          switch (result.type) {
            case 'done':
              onDone?.()
              return
              
            case 'error':
              onError?.(new Error(`[${result.error?.code}] ${result.error?.message}`))
              return
              
            case 'content':
              // 内存保护检查
              if (accumulatedContent.length > MAX_BUFFER_SIZE) {
                logger.warn('[streamFetch] 内容超出缓冲区限制，停止累积')
                continue
              }
              
              accumulatedContent += result.content || ''
              
              // 首次收到数据
              if (isFirstChunk) {
                isFirstChunk = false
                onFirstChunk?.()
              }
              
              // 传递累积的完整内容
              onChunk(accumulatedContent)
              break
              
            case 'skip':
              // 跳过无效数据
              break
          }
        }
      }

      // 流正常结束
      onDone?.()
    } catch (err) {
      // 重新抛出，让外层处理
      throw err
    }
  } catch (err) {
    // 处理取消请求
    if (err instanceof Error && err.name === 'AbortError') {
      // 用户主动取消，静默处理
      return
    }

    // 其他错误
    if (onError) {
      onError(err instanceof Error ? err : new Error(String(err)))
    } else {
      throw err
    }
  }
}

/**
 * 带重连机制的流式请求
 * 当发生可重试的错误时，自动进行重连
 * 
 * @param url - 请求地址
 * @param fetchOptions - fetch 选项
 * @param streamOptions - 流处理选项（包含重试配置）
 */
export async function streamFetchWithRetry(
  url: string,
  fetchOptions: StreamFetchOptions,
  streamOptions: StreamFetchWithRetryOptions
): Promise<void> {
  const {
    maxRetries = 3,
    retryDelay = 1000,
    isRetryable = defaultIsRetryable,
    onError,
    ...baseOptions
  } = streamOptions

  let retryCount = 0
  let lastError: Error | null = null

  while (retryCount <= maxRetries) {
    try {
      await streamFetch(url, fetchOptions, {
        ...baseOptions,
        onError: (err) => {
          // 暂存错误，等待判断是否重试
          lastError = err
          throw err
        },
      })
      return // 成功则退出
    } catch (error) {
      const err = error instanceof Error ? error : new Error(String(error))
      
      // 用户取消不重试
      if (err.name === 'AbortError') {
        return
      }

      // 检查是否可重试
      if (retryCount < maxRetries && isRetryable(err)) {
        retryCount++
        logger.warn(
          `[streamFetchWithRetry] 请求失败，${retryDelay * retryCount}ms后重试 (${retryCount}/${maxRetries}):`,
          err.message
        )
        await new Promise(resolve => setTimeout(resolve, retryDelay * retryCount))
        continue
      }

      // 不可重试或已耗尽重试次数
      if (onError) {
        onError(err)
      } else {
        throw err
      }
      return
    }
  }
}

/**
 * 创建一个带节流的流式更新函数
 * 避免高频更新导致的性能问题
 * 
 * @param updateFn - 实际的更新函数
 * @param delay - 节流延迟（毫秒），默认 16ms ≈ 60fps
 */
export function createThrottledUpdater(
  updateFn: (text: string) => void,
  delay = 16
): {
  update: (text: string) => void
  flush: () => void
  cancel: () => void
} {
  let buffer = ''
  let timeoutId: ReturnType<typeof setTimeout> | null = null
  let lastUpdate = 0

  const flush = () => {
    if (buffer) {
      updateFn(buffer)
    }
    if (timeoutId) {
      clearTimeout(timeoutId)
      timeoutId = null
    }
  }

  const cancel = () => {
    if (timeoutId) {
      clearTimeout(timeoutId)
      timeoutId = null
    }
    buffer = ''
  }

  const update = (text: string) => {
    buffer = text
    const now = Date.now()
    const elapsed = now - lastUpdate

    if (elapsed >= delay) {
      // 距离上次更新已超过延迟时间，立即更新
      lastUpdate = now
      updateFn(buffer)
    } else if (!timeoutId) {
      // 设置定时器，在延迟后更新
      timeoutId = setTimeout(() => {
        lastUpdate = Date.now()
        updateFn(buffer)
        timeoutId = null
      }, delay - elapsed)
    }
  }

  return { update, flush, cancel }
}
