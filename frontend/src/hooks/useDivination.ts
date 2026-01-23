import { useState } from 'react'
import { fetchEventSource, EventStreamContentType } from '@microsoft/fetch-event-source'
import MarkdownIt from 'markdown-it'
import { useGlobalState } from '@/store'
import { saveHistory, type HistoryMetadata } from '@/utils/divinationHistory'
import { getDivinationOption } from '@/config/constants'
import { logger } from '@/utils/logger'
import { toast } from 'sonner'

const API_BASE = import.meta.env.VITE_API_BASE || ''
const IS_TAURI = import.meta.env.VITE_IS_TAURI || ''
const md = new MarkdownIt()

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
  cards?: Array<{ name: string; isReversed: boolean }>
  spread?: string
  master?: { id: string; name: string }
  [key: string]: unknown  // 允许其他动态属性
}

export function useDivination(promptType: string) {
  const { jwt, customOpenAISettings } = useGlobalState()
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)
  const [resultLoading, setResultLoading] = useState(false)
  const [streaming, setStreaming] = useState(false)
  const [showDrawer, setShowDrawer] = useState(false)

  const onSubmit = async (params: DivinationParams) => {
    try {
      setLoading(true)
      setResultLoading(true)
      setStreaming(false)
      setResult('')
      setShowDrawer(true)

      let tmpResultBuffer = ''
      let firstChunk = true

      const headers: Record<string, string> = {
        Authorization: `Bearer ${jwt || 'xxx'}`,
        'Content-Type': 'application/json',
      }

      if (customOpenAISettings.enable) {
        headers['x-api-key'] = customOpenAISettings.apiKey
        headers['x-api-url'] = customOpenAISettings.baseUrl
        headers['x-api-model'] = customOpenAISettings.model
      } else if (IS_TAURI) {
        setResult('请在设置中配置 API BASE URL 和 API KEY')
        setResultLoading(false)
        return
      }

      await fetchEventSource(`${API_BASE}/api/divination`, {
        method: 'POST',
        body: JSON.stringify({
          ...params,
          prompt_type: promptType,
        }),
        headers,
        async onopen(response) {
          if (response.ok && response.headers.get('content-type') === EventStreamContentType) {
            setStreaming(true)
            return
          } else if (response.status >= 400) {
            throw new Error(`${response.status} ${await response.text()}`)
          }
        },
        onmessage(msg) {
          if (msg.event === 'FatalError') {
            throw new Error(msg.data)
          }
          if (!msg.data) {
            return
          }
          try {
            const newContent = JSON.parse(msg.data)
            tmpResultBuffer += newContent
            setResult(md.render(tmpResultBuffer))

            // 收到第一个词立即结束加载状态
            if (firstChunk) {
              firstChunk = false
              setResultLoading(false)
              setLoading(false)
            }
          } catch (error) {
            logger.error(error)
          }
        },
        onclose() {
          setStreaming(false)
          // 保存历史记录（仅当有结果时）
          if (tmpResultBuffer && promptType) {
            const config = getDivinationOption(promptType)
            if (config) {
              // 构建metadata
              const metadata: HistoryMetadata = {
                userName: params.userName || params.name,
                question: params.prompt || params.question,
              }

              // 塔罗牌特定数据
              if (params.cards) {
                metadata.cards = params.cards
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
                promptSummary = params.cards.map((c: { name: string; isReversed: boolean }) =>
                  `${c.name}${c.isReversed ? '(逆位)' : ''}`
                ).join(', ')
              }

              saveHistory({
                type: promptType,
                title: config.title,
                prompt: promptSummary,
                result: tmpResultBuffer,
                metadata,
              })
            }
          }
        },
        onerror(err) {
          setResult(`占卜失败: ${err.message}`)
          setStreaming(false)
          throw new Error(`占卜失败: ${err.message}`)
        },
      })
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
      setStreaming(false)
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
