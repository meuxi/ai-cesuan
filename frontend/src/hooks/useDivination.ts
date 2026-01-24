import { useState, useRef, useCallback, useEffect, useMemo } from 'react'
import { fetchEventSource } from '@microsoft/fetch-event-source'
import { useGlobalState } from '@/store'
import { saveHistory, type HistoryMetadata } from '@/utils/divinationHistory'
import { getDivinationOption } from '@/config/constants'
import { logger } from '@/utils/logger'
import { toast } from 'sonner'
import { createThrottledUpdater } from '@/utils/streamFetch'

const API_BASE = import.meta.env.VITE_API_BASE || ''
const IS_TAURI = import.meta.env.VITE_IS_TAURI || ''

// 打字机效果配置
const TYPEWRITER_CHUNK_SIZE = 3  // 每次显示的字符数
const TYPEWRITER_DELAY = 25      // 每次显示的间隔（ms）

// 流式渲染节流配置
const STREAM_THROTTLE_DELAY = 16  // 约 60fps

// 内存保护：最大缓冲区大小（约 250KB）
const MAX_BUFFER_SIZE = 250000

/**
 * 解析 SSE 数据
 * 支持后端统一的错误格式: { type: "error", code: "ERROR_CODE", message: "..." }
 */
interface SSEParseResult {
  type: 'content' | 'error' | 'done' | 'skip'
  content?: string
  error?: { code: string; message: string }
}

function parseSSEData(data: string): SSEParseResult {
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

// 占卜请求参数类型
interface DivinationParams {
  prompt?: string
  question?: string
  userName?: string
  name?: string
  birthday?: string
  gender?: string
  num1?: number
  num2?: number
  cards?: Array<{
    position: string
    name: string
    code: string
    isReversed: boolean
    meaning?: string
  }>
  spread?: { code: string; name: string }
  master?: { id: string; name: string; prompt?: string; gamePrompt?: string }
  [key: string]: unknown  // 允许其他动态属性
}

// JSON 响应类型
interface DivinationResponse {
  success: boolean
  content?: string
  error?: string
  model?: string
  latency_ms?: number
}

export function useDivination(promptType: string) {
  const { jwt, customOpenAISettings } = useGlobalState()
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)
  const [resultLoading, setResultLoading] = useState(false)
  const [streaming, setStreaming] = useState(false)
  const [showDrawer, setShowDrawer] = useState(false)
  
  // 用于取消打字机效果
  const typewriterRef = useRef<{ cancelled: boolean }>({ cancelled: false })
  
  // 用于取消流式请求（AbortController）
  const abortControllerRef = useRef<AbortController | null>(null)
  
  // 取消当前请求的函数
  const cancelRequest = useCallback(() => {
    // 取消流式请求
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
    // 取消打字机效果
    typewriterRef.current.cancelled = true
    setStreaming(false)
    setLoading(false)
    setResultLoading(false)
  }, [])
  
  // 流式渲染的节流更新器（避免高频更新导致 UI 卡顿）
  // 直接传递原始文本，由 ResultDisplay 组件负责 Markdown 渲染
  const throttledUpdater = useMemo(
    () => createThrottledUpdater((text: string) => {
      setResult(text)  // 传递原始文本，避免重复解析
    }, STREAM_THROTTLE_DELAY),
    []
  )
  
  // 组件卸载时自动取消请求，防止内存泄漏
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
        abortControllerRef.current = null
      }
      typewriterRef.current.cancelled = true
      throttledUpdater.cancel()
    }
  }, [throttledUpdater])

  // 打字机效果函数
  // 传递原始文本，由 ResultDisplay 组件负责 Markdown 渲染
  const typewriterEffect = useCallback(async (
    fullText: string,
    onUpdate: (text: string) => void
  ) => {
    typewriterRef.current.cancelled = false
    const chars = fullText.split('')
    let currentText = ''
    
    for (let i = 0; i < chars.length; i += TYPEWRITER_CHUNK_SIZE) {
      if (typewriterRef.current.cancelled) break
      
      const chunk = chars.slice(i, i + TYPEWRITER_CHUNK_SIZE).join('')
      currentText += chunk
      onUpdate(currentText)  // 传递原始文本
      
      // 添加延迟
      if (i + TYPEWRITER_CHUNK_SIZE < chars.length) {
        await new Promise(resolve => setTimeout(resolve, TYPEWRITER_DELAY))
      }
    }
    
    // 确保最终显示完整内容
    if (!typewriterRef.current.cancelled) {
      onUpdate(fullText)  // 传递原始文本
    }
    
    return fullText
  }, [])

  // 保存历史记录
  const saveToHistory = useCallback((params: DivinationParams, resultText: string) => {
    if (!resultText || !promptType) return
    
    const config = getDivinationOption(promptType)
    if (!config) return
    
    const metadata: HistoryMetadata = {
      userName: params.userName || params.name,
      question: params.prompt || params.question,
    }

    // 塔罗牌特定数据
    if (params.cards) {
      metadata.cards = params.cards.map(c => ({
        position: c.position,
        name: c.name,
        code: c.code,
        isReversed: c.isReversed
      }))
      metadata.spread = params.spread
      metadata.master = params.master ? { id: params.master.id, name: params.master.name } : undefined
    }

    // 八字/紫微相关数据
    if (params.birthday) {
      metadata.birthday = params.birthday
      metadata.gender = params.gender
    }

    // 梅花易数
    if (params.num1 !== undefined || params.num2 !== undefined) {
      metadata.numbers = [params.num1, params.num2].filter(n => n !== undefined)
    }

    // 构建prompt摘要
    let promptSummary = params.prompt || ''
    if (!promptSummary && params.cards) {
      promptSummary = params.cards.map(c =>
        `${c.name}${c.isReversed ? '(逆位)' : ''}`
      ).join(', ')
    }

    saveHistory({
      type: promptType,
      title: config.title,
      prompt: promptSummary,
      result: resultText,
      metadata,
    })
  }, [promptType])

  const onSubmit = async (params: DivinationParams) => {
    try {
      // 取消之前的请求和打字机效果
      cancelRequest()
      
      // 创建新的 AbortController
      abortControllerRef.current = new AbortController()
      
      setLoading(true)
      setResultLoading(true)
      setStreaming(false)
      setResult('')
      setShowDrawer(true)

      // Tauri 模式下需要自定义 API 配置
      if (IS_TAURI && !(customOpenAISettings.enable && customOpenAISettings.apiKey)) {
        setResult('请在设置中配置 API BASE URL 和 API KEY')
        setResultLoading(false)
        setLoading(false)
        return
      }

      // 构建请求头
      const headers: Record<string, string> = {
        Authorization: `Bearer ${jwt || 'xxx'}`,
        'Content-Type': 'application/json',
      }

      // 如果使用自定义 API，添加相应的头部
      const useCustomApi = customOpenAISettings.enable && customOpenAISettings.apiKey
      if (useCustomApi) {
        headers['x-api-key'] = customOpenAISettings.apiKey
        headers['x-api-url'] = customOpenAISettings.baseUrl
        headers['x-api-model'] = customOpenAISettings.model
      }

      const requestBody = {
        ...params,
        prompt_type: promptType,
      }

      // ========== 统一的 SSE 流式处理（去重后的代码） ==========
      let tmpResultBuffer = ''
      let firstChunk = true

      await fetchEventSource(`${API_BASE}/api/divination`, {
        method: 'POST',
        body: JSON.stringify(requestBody),
        headers,
        signal: abortControllerRef.current.signal,
        
        async onopen(response) {
          const contentType = response.headers.get('content-type') || ''
          if (response.ok && contentType.includes('text/event-stream')) {
            setStreaming(true)
            return
          } else if (response.status >= 400) {
            throw new Error(`${response.status} ${await response.text()}`)
          } else if (!response.ok) {
            throw new Error(`响应状态异常: ${response.status}`)
          }
        },
        
        onmessage(msg) {
          // 处理致命错误事件
          if (msg.event === 'FatalError') {
            throw new Error(msg.data)
          }
          
          // 使用统一的解析函数处理 SSE 数据
          const result = parseSSEData(msg.data)
          
          switch (result.type) {
            case 'done':
            case 'skip':
              return
              
            case 'error':
              // 显示错误信息
              setResult(`错误 [${result.error?.code}]: ${result.error?.message}`)
              setStreaming(false)
              return
              
            case 'content':
              // 内存保护：检查缓冲区大小
              if (tmpResultBuffer.length > MAX_BUFFER_SIZE) {
                logger.warn('响应内容过长，已达到缓冲区限制')
                return
              }
              
              tmpResultBuffer += result.content || ''
              // 使用节流更新，避免高频渲染导致 UI 卡顿
              throttledUpdater.update(tmpResultBuffer)
              
              // 首次收到数据时更新加载状态
              if (firstChunk) {
                firstChunk = false
                setResultLoading(false)
                setLoading(false)
              }
              break
          }
        },
        
        onclose() {
          abortControllerRef.current = null
          // 刷新节流缓冲区，确保显示完整内容
          throttledUpdater.flush()
          // 最终确保显示完整结果
          setResult(tmpResultBuffer)
          setStreaming(false)
          saveToHistory(params, tmpResultBuffer)
        },
        
        onerror(err) {
          // 忽略用户主动取消的错误
          if (err.name === 'AbortError') {
            logger.debug('用户取消了请求')
            return
          }
          setResult(`占卜失败: ${err.message}`)
          setStreaming(false)
          throw new Error(`占卜失败: ${err.message}`)
        },
      })
    } catch (error: unknown) {
      // 忽略用户主动取消的错误
      if (error instanceof Error && error.name === 'AbortError') {
        logger.debug('用户取消了请求')
        return
      }
      
      logger.error(error)
      const errorMessage = error instanceof Error ? error.message : String(error)
      const userFriendlyMsg = errorMessage.includes('rate_limit')
        ? '请求过于频繁，请稍后再试（约1分钟）'
        : errorMessage.includes('API')
          ? 'API配置错误，请检查设置'
          : errorMessage || '占卜失败，请检查网络后重试'
      setResult(userFriendlyMsg)
      toast.error(userFriendlyMsg)
      setStreaming(false)
    } finally {
      setLoading(false)
      setResultLoading(false)
      abortControllerRef.current = null
    }
  }

  return {
    result,
    loading,
    resultLoading,
    streaming,
    showDrawer,
    setShowDrawer,
    onSubmit,
    cancelRequest,  // 暴露取消请求函数
  }
}
