import { useState, useRef, useCallback } from 'react'
import { fetchEventSource } from '@microsoft/fetch-event-source'
import MarkdownIt from 'markdown-it'
import { useGlobalState } from '@/store'
import { saveHistory, type HistoryMetadata } from '@/utils/divinationHistory'
import { getDivinationOption } from '@/config/constants'
import { logger } from '@/utils/logger'
import { toast } from 'sonner'

const API_BASE = import.meta.env.VITE_API_BASE || ''
const IS_TAURI = import.meta.env.VITE_IS_TAURI || ''
const md = new MarkdownIt()

// 打字机效果配置
const TYPEWRITER_CHUNK_SIZE = 3  // 每次显示的字符数
const TYPEWRITER_DELAY = 25      // 每次显示的间隔（ms）

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

  // 打字机效果函数
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
      onUpdate(md.render(currentText))
      
      // 添加延迟
      if (i + TYPEWRITER_CHUNK_SIZE < chars.length) {
        await new Promise(resolve => setTimeout(resolve, TYPEWRITER_DELAY))
      }
    }
    
    // 确保最终显示完整内容
    if (!typewriterRef.current.cancelled) {
      onUpdate(md.render(fullText))
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
      // 取消之前的打字机效果
      typewriterRef.current.cancelled = true
      
      setLoading(true)
      setResultLoading(true)
      setStreaming(false)
      setResult('')
      setShowDrawer(true)

      const headers: Record<string, string> = {
        Authorization: `Bearer ${jwt || 'xxx'}`,
        'Content-Type': 'application/json',
      }

      const requestBody = {
        ...params,
        prompt_type: promptType,
      }

      // 判断使用哪种模式
      const useCustomApi = customOpenAISettings.enable && customOpenAISettings.apiKey

      if (useCustomApi) {
        // ========== 自定义 API 模式：使用 SSE 流式 ==========
        headers['x-api-key'] = customOpenAISettings.apiKey
        headers['x-api-url'] = customOpenAISettings.baseUrl
        headers['x-api-model'] = customOpenAISettings.model

        let tmpResultBuffer = ''
        let firstChunk = true

        await fetchEventSource(`${API_BASE}/api/divination`, {
          method: 'POST',
          body: JSON.stringify(requestBody),
          headers,
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
            if (msg.event === 'FatalError') {
              throw new Error(msg.data)
            }
            if (!msg.data || msg.data === '[DONE]') {
              return
            }
            try {
              const parsed = JSON.parse(msg.data)
              if (typeof parsed === 'object' && parsed !== null && parsed.error) {
                setResult(`错误: ${parsed.error}`)
                return
              }
              const newContent = typeof parsed === 'string' ? parsed : String(parsed)
              tmpResultBuffer += newContent
              setResult(md.render(tmpResultBuffer))

              if (firstChunk) {
                firstChunk = false
                setResultLoading(false)
                setLoading(false)
              }
            } catch {
              if (msg.data && !msg.data.startsWith('[')) {
                tmpResultBuffer += msg.data
                setResult(md.render(tmpResultBuffer))
                if (firstChunk) {
                  firstChunk = false
                  setResultLoading(false)
                  setLoading(false)
                }
              }
            }
          },
          onclose() {
            setStreaming(false)
            saveToHistory(params, tmpResultBuffer)
          },
          onerror(err) {
            setResult(`占卜失败: ${err.message}`)
            setStreaming(false)
            throw new Error(`占卜失败: ${err.message}`)
          },
        })
      } else {
        // ========== 预设模式：JSON 响应 + 打字机效果 ==========
        if (IS_TAURI) {
          setResult('请在设置中配置 API BASE URL 和 API KEY')
          setResultLoading(false)
          setLoading(false)
          return
        }

        const response = await fetch(`${API_BASE}/api/divination`, {
          method: 'POST',
          headers,
          body: JSON.stringify(requestBody),
        })

        if (!response.ok) {
          const errorText = await response.text()
          throw new Error(`请求失败: ${response.status} ${errorText}`)
        }

        const data: DivinationResponse = await response.json()
        
        if (!data.success || !data.content) {
          throw new Error(data.error || 'AI返回内容为空')
        }

        // 开始打字机效果
        setResultLoading(false)
        setLoading(false)
        setStreaming(true)

        await typewriterEffect(data.content, setResult)
        
        setStreaming(false)
        saveToHistory(params, data.content)
      }
    } catch (error: unknown) {
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
  }
}
