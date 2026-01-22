/**
 * 占卜结果展示组件
 * 统一的AI分析结果展示界面
 */

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Copy, Check, Share2, Download, ChevronDown, ChevronUp, Sparkles } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useTranslation } from 'react-i18next'
import ReactMarkdown from 'react-markdown'

interface ResultDisplayProps {
  /** 结果内容（支持Markdown） */
  result: string | null
  /** 是否正在加载 */
  loading?: boolean
  /** 是否流式输出 */
  streaming?: boolean
  /** 结果标题 */
  title?: string
  /** 自定义类名 */
  className?: string
  /** 是否可收起 */
  collapsible?: boolean
  /** 默认是否收起 */
  defaultCollapsed?: boolean
  /** 复制成功回调 */
  onCopy?: () => void
  /** 分享回调 */
  onShare?: () => void
  /** 下载回调 */
  onDownload?: () => void
}

export function ResultDisplay({
  result,
  loading = false,
  streaming = false,
  title,
  className,
  collapsible = false,
  defaultCollapsed = false,
  onCopy,
  onShare,
  onDownload
}: ResultDisplayProps) {
  const { i18n } = useTranslation()
  const [copied, setCopied] = useState(false)
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed)
  const contentRef = useRef<HTMLDivElement>(null)

  // 自动滚动到最新内容（流式输出时）
  useEffect(() => {
    if (streaming && contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight
    }
  }, [result, streaming])

  // 复制功能
  const handleCopy = async () => {
    if (!result) return
    try {
      await navigator.clipboard.writeText(result)
      setCopied(true)
      onCopy?.()
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  // 如果没有结果且不在加载，不显示
  if (!result && !loading) return null

  const defaultTitle = i18n.language === 'en' ? 'AI Analysis' : 'AI 分析结果'

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className={cn(
        'rounded-xl border border-border bg-card overflow-hidden',
        className
      )}
    >
      {/* 头部 */}
      <div className={cn(
        'flex items-center justify-between px-4 py-3',
        'bg-gradient-to-r from-primary/10 via-primary/5 to-transparent',
        'border-b border-border'
      )}>
        <div className="flex items-center gap-2">
          <motion.div
            animate={loading || streaming ? { rotate: 360 } : { rotate: 0 }}
            transition={{ duration: 2, repeat: loading || streaming ? Infinity : 0, ease: 'linear' }}
          >
            <Sparkles className={cn(
              'w-5 h-5',
              loading || streaming ? 'text-primary' : 'text-muted-foreground'
            )} />
          </motion.div>
          <h3 className="font-semibold text-foreground">
            {title || defaultTitle}
          </h3>
          {streaming && (
            <span className="text-xs px-2 py-0.5 bg-primary/20 text-primary rounded-full animate-pulse">
              {i18n.language === 'en' ? 'Generating...' : '生成中...'}
            </span>
          )}
        </div>
        
        {/* 操作按钮 */}
        <div className="flex items-center gap-1">
          {result && !loading && (
            <>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={handleCopy}
                className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                title={i18n.language === 'en' ? 'Copy' : '复制'}
              >
                {copied ? (
                  <Check className="w-4 h-4 text-green-500" />
                ) : (
                  <Copy className="w-4 h-4" />
                )}
              </motion.button>
              
              {onShare && (
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={onShare}
                  className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                  title={i18n.language === 'en' ? 'Share' : '分享'}
                >
                  <Share2 className="w-4 h-4" />
                </motion.button>
              )}
              
              {onDownload && (
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={onDownload}
                  className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                  title={i18n.language === 'en' ? 'Download' : '下载'}
                >
                  <Download className="w-4 h-4" />
                </motion.button>
              )}
            </>
          )}
          
          {collapsible && result && (
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
            >
              {isCollapsed ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronUp className="w-4 h-4" />
              )}
            </motion.button>
          )}
        </div>
      </div>

      {/* 内容区域 */}
      <AnimatePresence>
        {(!collapsible || !isCollapsed) && (
          <motion.div
            initial={collapsible ? { height: 0 } : false}
            animate={{ height: 'auto' }}
            exit={{ height: 0 }}
            className="overflow-hidden"
          >
            <div
              ref={contentRef}
              className={cn(
                'p-4 overflow-y-auto',
                'prose prose-sm dark:prose-invert max-w-none',
                'prose-headings:text-foreground prose-p:text-foreground/90',
                'prose-strong:text-foreground prose-a:text-primary'
              )}
              style={{ maxHeight: '500px' }}
            >
              {loading && !result ? (
                <LoadingSkeleton />
              ) : (
                <ReactMarkdown>
                  {result || ''}
                </ReactMarkdown>
              )}
              
              {/* 流式输出光标 */}
              {streaming && (
                <motion.span
                  className="inline-block w-2 h-5 bg-primary ml-1"
                  animate={{ opacity: [1, 0] }}
                  transition={{ duration: 0.5, repeat: Infinity }}
                />
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

// 加载骨架
function LoadingSkeleton() {
  return (
    <div className="space-y-3 animate-pulse">
      {[100, 85, 95, 75, 90].map((width, i) => (
        <div 
          key={i}
          className="h-4 bg-muted rounded"
          style={{ width: `${width}%` }}
        />
      ))}
    </div>
  )
}

// 简洁版结果显示（用于内嵌场景）
interface InlineResultDisplayProps {
  result: string | null
  loading?: boolean
  streaming?: boolean
}

export function InlineResultDisplay({ result, loading, streaming }: InlineResultDisplayProps) {
  if (!result && !loading) return null

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="mt-4 p-4 rounded-lg bg-secondary/50 border border-border"
    >
      {loading && !result ? (
        <div className="flex items-center gap-2 text-muted-foreground">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          >
            <Sparkles className="w-4 h-4" />
          </motion.div>
          <span className="text-sm">正在分析...</span>
        </div>
      ) : (
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown>{result || ''}</ReactMarkdown>
          {streaming && (
            <motion.span
              className="inline-block w-1.5 h-4 bg-primary ml-0.5"
              animate={{ opacity: [1, 0] }}
              transition={{ duration: 0.5, repeat: Infinity }}
            />
          )}
        </div>
      )}
    </motion.div>
  )
}
