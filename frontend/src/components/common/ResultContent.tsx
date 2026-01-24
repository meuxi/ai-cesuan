/**
 * 统一的结果内容渲染组件
 * 
 * 抽取 ResultDrawer、InlineResult、ResultDisplay 的公共渲染逻辑，
 * 包括：加载状态、内容渲染、流式光标等。
 */

import { memo, forwardRef, ReactNode } from 'react'
import { motion } from 'framer-motion'
import { Sparkles } from 'lucide-react'
import DOMPurify from 'dompurify'
import ReactMarkdown from 'react-markdown'
import { cn } from '@/lib/utils'

// ========== 加载状态组件 ==========

export interface LoadingIndicatorProps {
  /** 主文本 */
  text?: string
  /** 副文本 */
  subText?: string
  /** 尺寸: sm | md | lg */
  size?: 'sm' | 'md' | 'lg'
  /** 自定义类名 */
  className?: string
}

export const LoadingIndicator = memo(function LoadingIndicator({
  text = '正在占卜中...',
  subText,
  size = 'md',
  className
}: LoadingIndicatorProps) {
  const sizeConfig = {
    sm: { spinner: 'h-6 w-6', text: 'text-sm', subText: 'text-xs' },
    md: { spinner: 'h-8 w-8', text: 'text-base', subText: 'text-sm' },
    lg: { spinner: 'h-10 w-10', text: 'text-lg', subText: 'text-sm' }
  }

  const config = sizeConfig[size]

  return (
    <div className={cn('flex flex-col items-center justify-center space-y-3', className)}>
      <div className={cn(
        'animate-spin rounded-full border-2 border-muted border-t-primary',
        config.spinner
      )} />
      <div className="text-center space-y-1">
        <p className={cn('font-medium text-foreground', config.text)}>{text}</p>
        {subText && (
          <p className={cn('text-muted-foreground', config.subText)}>{subText}</p>
        )}
      </div>
    </div>
  )
})

// ========== 流式光标组件 ==========

export interface StreamingCursorProps {
  /** 光标样式变体 */
  variant?: 'block' | 'line'
  /** 自定义类名 */
  className?: string
}

export const StreamingCursor = memo(function StreamingCursor({
  variant = 'line',
  className
}: StreamingCursorProps) {
  const baseClass = variant === 'block' 
    ? 'w-2 h-5 bg-primary' 
    : 'w-1 h-5 bg-foreground rounded-sm'

  return (
    <motion.span
      className={cn('inline-flex ml-1 align-middle', baseClass, className)}
      animate={{ opacity: [1, 0] }}
      transition={{ duration: 0.5, repeat: Infinity }}
    />
  )
})

// ========== 骨架加载组件 ==========

export interface LoadingSkeletonProps {
  /** 行数 */
  lines?: number
  /** 自定义类名 */
  className?: string
}

export const LoadingSkeleton = memo(function LoadingSkeleton({
  lines = 5,
  className
}: LoadingSkeletonProps) {
  const widths = [100, 85, 95, 75, 90, 80, 70, 88, 92, 78]
  
  return (
    <div className={cn('space-y-3 animate-pulse', className)}>
      {Array.from({ length: lines }).map((_, i) => (
        <div 
          key={i}
          className="h-4 bg-muted rounded"
          style={{ width: `${widths[i % widths.length]}%` }}
        />
      ))}
    </div>
  )
})

// ========== Markdown 内容渲染组件 ==========

export interface MarkdownContentProps {
  /** Markdown 文本内容 */
  content: string
  /** 是否流式输出中 */
  streaming?: boolean
  /** 自定义类名 */
  className?: string
}

export const MarkdownContent = memo(function MarkdownContent({
  content,
  streaming = false,
  className
}: MarkdownContentProps) {
  return (
    <div className={cn(
      'prose prose-sm dark:prose-invert max-w-none',
      'prose-headings:text-foreground prose-p:text-foreground/90',
      'prose-strong:text-foreground prose-a:text-primary',
      className
    )}>
      <ReactMarkdown>{content}</ReactMarkdown>
      {streaming && <StreamingCursor variant="block" />}
    </div>
  )
})

// ========== HTML 内容渲染组件（带 sanitize） ==========

export interface HtmlContentProps {
  /** HTML 内容（会自动 sanitize） */
  content: string
  /** 是否流式输出中 */
  streaming?: boolean
  /** 元素 ID（用于截图等操作） */
  id?: string
  /** 自定义类名 */
  className?: string
}

export const HtmlContent = memo(function HtmlContent({
  content,
  streaming = false,
  id,
  className
}: HtmlContentProps) {
  return (
    <div id={id} className={cn(streaming && 'streaming-content', className)}>
      <div
        className={cn(
          'prose prose-neutral max-w-none dark:prose-invert',
          'prose-headings:font-semibold prose-headings:text-foreground',
          'prose-p:text-muted-foreground prose-p:leading-relaxed',
          'prose-li:text-muted-foreground'
        )}
        dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(content) }}
      />
      {streaming && <StreamingCursor variant="line" />}
    </div>
  )
})

// ========== 统一的结果内容组件 ==========

export interface ResultContentProps {
  /** 结果内容 */
  result: string | null
  /** 是否加载中 */
  loading?: boolean
  /** 是否流式输出中 */
  streaming?: boolean
  /** 内容类型: html | markdown */
  contentType?: 'html' | 'markdown'
  /** 加载状态配置 */
  loadingConfig?: {
    text?: string
    subText?: string
    size?: 'sm' | 'md' | 'lg'
  }
  /** 元素 ID */
  id?: string
  /** 自定义类名 */
  className?: string
  /** 操作区域插槽 */
  actions?: ReactNode
  /** ref 转发 */
  ref?: React.Ref<HTMLDivElement>
}

export const ResultContent = memo(forwardRef<HTMLDivElement, ResultContentProps>(
  function ResultContent({
    result,
    loading = false,
    streaming = false,
    contentType = 'html',
    loadingConfig,
    id,
    className,
    actions
  }, ref) {
    // 加载中且无内容
    if (loading && !result) {
      return (
        <div ref={ref} className={cn('py-8', className)}>
          <LoadingIndicator
            text={loadingConfig?.text ?? '正在占卜中...'}
            subText={loadingConfig?.subText ?? 'AI 正在为您解读'}
            size={loadingConfig?.size ?? 'md'}
          />
        </div>
      )
    }

    // 无内容
    if (!result) {
      return null
    }

    // 渲染内容
    return (
      <div ref={ref} className={className}>
        {contentType === 'markdown' ? (
          <MarkdownContent
            content={result}
            streaming={streaming}
          />
        ) : (
          <HtmlContent
            content={result}
            streaming={streaming}
            id={id}
          />
        )}
        {/* 操作按钮区域 */}
        {!streaming && actions}
      </div>
    )
  }
))

// ========== 带旋转图标的加载指示器 ==========

export interface SpinnerLoadingProps {
  text?: string
  className?: string
}

export const SpinnerLoading = memo(function SpinnerLoading({
  text = '正在分析...',
  className
}: SpinnerLoadingProps) {
  return (
    <div className={cn('flex items-center gap-2 text-muted-foreground', className)}>
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      >
        <Sparkles className="w-4 h-4" />
      </motion.div>
      <span className="text-sm">{text}</span>
    </div>
  )
})
