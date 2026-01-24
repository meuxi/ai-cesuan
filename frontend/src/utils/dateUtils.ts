/**
 * 日期格式化工具函数
 * 
 * 统一的日期格式化逻辑，避免在多个组件中重复实现
 */

/**
 * 格式化为相对时间（如"刚刚"、"5分钟前"、"3天前"）
 * 
 * @param timestamp - Unix 时间戳（毫秒）
 * @returns 格式化的相对时间字符串
 */
export const formatRelativeTime = (timestamp: number): string => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`

  return date.toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * 格式化为短日期时间（如"今日 14:30"、"1月15日 10:00"）
 * 
 * @param timestamp - Unix 时间戳（毫秒）
 * @returns 格式化的日期时间字符串
 */
export const formatShortDateTime = (timestamp: number): string => {
  const d = new Date(timestamp)
  const now = new Date()
  const isToday = d.toDateString() === now.toDateString()
  const hours = d.getHours().toString().padStart(2, '0')
  const minutes = d.getMinutes().toString().padStart(2, '0')
  const month = d.getMonth() + 1
  const day = d.getDate()

  if (isToday) {
    return `今日 ${hours}:${minutes}`
  }
  return `${month}月${day}日 ${hours}:${minutes}`
}

/**
 * 格式化为完整日期时间（如"2025-01-15 14:30:00"）
 * 
 * @param timestamp - Unix 时间戳（毫秒）
 * @returns 格式化的完整日期时间字符串
 */
export const formatFullDateTime = (timestamp: number): string => {
  const d = new Date(timestamp)
  const year = d.getFullYear()
  const month = (d.getMonth() + 1).toString().padStart(2, '0')
  const day = d.getDate().toString().padStart(2, '0')
  const hours = d.getHours().toString().padStart(2, '0')
  const minutes = d.getMinutes().toString().padStart(2, '0')
  const seconds = d.getSeconds().toString().padStart(2, '0')

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

/**
 * 格式化为日期（如"2025-01-15"）
 * 
 * @param timestamp - Unix 时间戳（毫秒）或 Date 对象
 * @returns 格式化的日期字符串
 */
export const formatDate = (timestamp: number | Date): string => {
  const d = timestamp instanceof Date ? timestamp : new Date(timestamp)
  const year = d.getFullYear()
  const month = (d.getMonth() + 1).toString().padStart(2, '0')
  const day = d.getDate().toString().padStart(2, '0')

  return `${year}-${month}-${day}`
}

/**
 * 格式化为中文日期（如"2025年1月15日"）
 * 
 * @param timestamp - Unix 时间戳（毫秒）或 Date 对象
 * @returns 格式化的中文日期字符串
 */
export const formatChineseDate = (timestamp: number | Date): string => {
  const d = timestamp instanceof Date ? timestamp : new Date(timestamp)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}
