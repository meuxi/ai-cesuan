/**
 * 日志工具封装
 * 
 * 开发环境：输出完整日志
 * 生产环境：屏蔽 log/debug，仅保留 error/warn（且可配置）
 * 
 * 使用方式：
 * import { logger } from '@/utils/logger';
 * logger.error('错误信息', error);
 * logger.warn('警告信息');
 * logger.log('普通日志');  // 生产环境不输出
 * logger.debug('调试日志'); // 生产环境不输出
 */

const isDev = import.meta.env.DEV;

// 生产环境是否输出警告日志（可通过URL参数开启调试）
const enableProdLogs = typeof window !== 'undefined' && 
  new URLSearchParams(window.location.search).has('debug');

/**
 * 格式化日志前缀
 */
const formatPrefix = (level: string): string => {
  const timestamp = new Date().toISOString().slice(11, 23);
  return `[${timestamp}] [${level.toUpperCase()}]`;
};

export const logger = {
  /**
   * 错误日志 - 始终输出
   * 用于记录异常和错误情况
   */
  error: (...args: unknown[]) => {
    console.error(formatPrefix('error'), ...args);
    // 生产环境可接入日志服务（如Sentry）
    // if (!isDev) sendToLogService('error', args);
  },

  /**
   * 警告日志 - 生产环境可选输出
   * 用于记录潜在问题
   */
  warn: (...args: unknown[]) => {
    if (isDev || enableProdLogs) {
      console.warn(formatPrefix('warn'), ...args);
    }
  },

  /**
   * 普通日志 - 仅开发环境
   * 用于一般信息记录
   */
  log: (...args: unknown[]) => {
    if (isDev || enableProdLogs) {
      console.log(formatPrefix('info'), ...args);
    }
  },

  /**
   * 调试日志 - 仅开发环境
   * 用于详细调试信息
   */
  debug: (...args: unknown[]) => {
    if (isDev || enableProdLogs) {
      console.debug(formatPrefix('debug'), ...args);
    }
  },

  /**
   * 分组日志 - 仅开发环境
   * 用于组织相关日志
   */
  group: (label: string) => {
    if (isDev || enableProdLogs) {
      console.group(label);
    }
  },

  groupEnd: () => {
    if (isDev || enableProdLogs) {
      console.groupEnd();
    }
  },

  /**
   * 表格日志 - 仅开发环境
   * 用于展示结构化数据
   */
  table: (data: unknown) => {
    if (isDev || enableProdLogs) {
      console.table(data);
    }
  },
};

// 默认导出
export default logger;
