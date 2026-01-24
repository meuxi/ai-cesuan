import { X } from 'lucide-react'
import { useRef, useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import ResultActions from '@/components/ResultActions'
import { ResultContent } from '@/components/common'

interface ResultDrawerProps {
  show: boolean
  onClose: () => void
  result: string
  loading: boolean
  streaming: boolean
  title?: string
}

export function ResultDrawer({ show, onClose, result, loading, streaming, title = '占卜结果' }: ResultDrawerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [isAnimating, setIsAnimating] = useState(false)

  // 控制入场动画
  useEffect(() => {
    if (show) {
      requestAnimationFrame(() => {
        setIsAnimating(true)
      })
    } else {
      setIsAnimating(false)
    }
  }, [show])

  // 自动滚动到底部
  useEffect(() => {
    if (result && containerRef.current) {
      const timeoutId = setTimeout(() => {
        if (containerRef.current) {
          containerRef.current.scrollTop = containerRef.current.scrollHeight
        }
      }, 100)
      return () => clearTimeout(timeoutId)
    }
  }, [result])

  if (!show) return null

  const drawerContent = (
    <div className="fixed inset-0 z-50">
      {/* 背景遮罩 */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      ></div>
      {/* 抽屉容器 */}
      <div
        className="fixed inset-x-0 bottom-0 z-50 h-[80vh] rounded-t-2xl border-t border-border bg-card shadow-2xl transition-transform duration-300 ease-out"
        style={{
          transform: isAnimating ? 'translateY(0)' : 'translateY(100%)',
        }}
      >
        {/* 头部 */}
        <div className="flex items-center justify-between border-b border-border px-6 py-4">
          <h3 className="text-lg font-semibold text-foreground">占卜结果</h3>
          <button
            onClick={onClose}
            className="rounded-md p-2 hover:bg-accent transition-colors"
            aria-label="关闭"
          >
            <X className="h-5 w-5 text-muted-foreground" />
          </button>
        </div>
        {/* 内容区域 */}
        <div
          ref={containerRef}
          className="overflow-y-auto p-6 h-[calc(80vh-4rem)]"
        >
          <ResultContent
            result={result}
            loading={loading}
            streaming={streaming}
            contentType="html"
            id="divination-result"
            loadingConfig={{
              text: '正在占卜中...',
              subText: '请稍候，AI 正在为您解读',
              size: 'lg'
            }}
            className={loading ? 'h-full flex items-center justify-center' : ''}
            actions={
              <ResultActions
                result={result.replace(/<[^>]*>/g, '')}
                title={title}
                elementId="divination-result"
              />
            }
          />
        </div>
      </div>
    </div>
  )

  return createPortal(drawerContent, document.body)
}
