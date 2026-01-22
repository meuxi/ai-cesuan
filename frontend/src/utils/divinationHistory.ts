import { logger } from './logger'

/**
 * 历史记录元数据接口 - 用于存储不同占卜类型的特定数据
 */
export interface HistoryMetadata {
  // 通用字段
  userName?: string           // 用户名/求测者姓名
  question?: string           // 所问问题

  // 塔罗牌
  cards?: Array<{
    position: string
    name: string
    code: string
    isReversed: boolean
  }>
  spread?: { code: string; name: string }
  master?: { id: string; name: string }

  // 八字/紫微/合婚相关
  birthday?: string           // 生日
  gender?: string             // 性别
  lunarDate?: string          // 农历日期
  fourPillars?: string        // 四柱

  // 抽签相关
  qianType?: string           // 签类型 (guanyin/guandi等)
  qianNumber?: number         // 签号
  signTitle?: string          // 签文标题

  // 六爻相关
  hexagram?: string           // 卦象
  yaos?: number[]             // 爻位

  // 梅花易数
  upperGua?: string           // 上卦
  lowerGua?: string           // 下卦
  numbers?: number[]          // 起卦数字

  // 小六壬
  monthGod?: string           // 月神
  dayGod?: string             // 日神  
  hourGod?: string            // 时神

  // 其他扩展字段
  [key: string]: unknown
}

/**
 * 占卜历史记录项接口
 */
export interface DivinationHistoryItem {
  id: string                  // 唯一标识
  type: string                // 占卜类型
  title: string               // 显示标题
  prompt: string              // 用户输入/问题摘要
  result: string              // AI解读结果 (markdown格式)
  timestamp: number           // 时间戳
  metadata?: HistoryMetadata  // 扩展元数据
}

/**
 * 保存历史记录的参数接口
 */
export interface SaveHistoryParams {
  type: string
  title: string
  prompt: string
  result: string
  metadata?: HistoryMetadata
}

const HISTORY_KEY_PREFIX = 'divination_history_'
const MAX_HISTORY_COUNT = 20  // 每种类型最多保存20条

/**
 * 生成唯一ID
 * 使用时间戳 + 随机数确保唯一性，避免竞态条件
 */
function generateUniqueId(): string {
  const timestamp = Date.now()
  const random = Math.random().toString(36).substring(2, 9)
  return `${timestamp}-${random}`
}

/**
 * 获取指定类型的历史记录
 */
export function getHistoryByType(type: string): DivinationHistoryItem[] {
  try {
    const data = localStorage.getItem(`${HISTORY_KEY_PREFIX}${type}`)
    if (!data) return []
    return JSON.parse(data)
  } catch (error) {
    logger.error('Failed to get history:', error)
    return []
  }
}

/**
 * 获取所有类型的历史记录（合并并按时间排序）
 */
export function getHistory(): DivinationHistoryItem[] {
  try {
    const allHistory: DivinationHistoryItem[] = []

    // 遍历 localStorage 获取所有历史记录
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key && key.startsWith(HISTORY_KEY_PREFIX)) {
        const data = localStorage.getItem(key)
        if (data) {
          const items = JSON.parse(data) as DivinationHistoryItem[]
          allHistory.push(...items)
        }
      }
    }

    // 按时间倒序排序
    return allHistory.sort((a, b) => b.timestamp - a.timestamp)
  } catch (error) {
    logger.error('Failed to get history:', error)
    return []
  }
}

/**
 * 保存历史记录（按类型分开保存）
 */
export function saveHistory(params: SaveHistoryParams): void {
  try {
    const history = getHistoryByType(params.type)
    const timestamp = Date.now()

    // 使用统一的时间戳和生成的唯一ID
    const newItem: DivinationHistoryItem = {
      id: generateUniqueId(),
      type: params.type,
      title: params.title,
      prompt: params.prompt,
      result: params.result,
      timestamp,
      metadata: params.metadata,
    }

    // 添加到开头
    history.unshift(newItem)

    // 每个类型保留最近20条
    const limitedHistory = history.slice(0, MAX_HISTORY_COUNT)

    localStorage.setItem(`${HISTORY_KEY_PREFIX}${params.type}`, JSON.stringify(limitedHistory))
    logger.log(`History saved: ${params.type} - ${params.title}`)
  } catch (error) {
    logger.error('Failed to save history:', error)
  }
}

/**
 * 删除指定历史记录
 */
export function deleteHistoryItem(id: string, type: string): void {
  try {
    const history = getHistoryByType(type)
    const filtered = history.filter(item => item.id !== id)
    localStorage.setItem(`${HISTORY_KEY_PREFIX}${type}`, JSON.stringify(filtered))
  } catch (error) {
    logger.error('Failed to delete history item:', error)
  }
}

/**
 * 清空所有历史记录
 */
export function clearHistory(): void {
  try {
    const keysToRemove: string[] = []
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key && key.startsWith(HISTORY_KEY_PREFIX)) {
        keysToRemove.push(key)
      }
    }
    keysToRemove.forEach(key => localStorage.removeItem(key))
  } catch (error) {
    logger.error('Failed to clear history:', error)
  }
}
