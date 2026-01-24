import { useState, useEffect, useMemo, memo, useCallback } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Trash2, Calendar } from 'lucide-react'
import { getHistoryByType, deleteHistoryItem, DivinationHistoryItem } from '@/utils/divinationHistory'
import { ResultDrawer } from '@/components/ResultDrawer'
import { toast } from 'sonner'
import { getDivinationOption } from '@/config/constants'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'
import { formatRelativeTime } from '@/utils/dateUtils'

const md = new MarkdownIt()

// 安全渲染 Markdown：先渲染再 sanitize，防止 XSS
const safeRenderMarkdown = (content: string): string => {
  return DOMPurify.sanitize(md.render(content))
}

// 使用统一的日期格式化工具
const formatDate = formatRelativeTime

// ========== 列表项组件（使用 React.memo 优化重渲染） ==========
interface HistoryItemProps {
  item: DivinationHistoryItem
  onView: (item: DivinationHistoryItem) => void
  onDelete: (id: string) => void
}

const HistoryItem = memo(function HistoryItem({ item, onView, onDelete }: HistoryItemProps) {
  const handleClick = useCallback(() => {
    onView(item)
  }, [item, onView])

  const handleDelete = useCallback((e: React.MouseEvent) => {
    e.stopPropagation()
    onDelete(item.id)
  }, [item.id, onDelete])

  return (
    <div
      className="p-4 rounded-lg border border-border hover:border-muted-foreground cursor-pointer transition-colors group"
      onClick={handleClick}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs px-2 py-1 rounded-md bg-muted text-muted-foreground font-medium">
              {item.title}
            </span>
            <span className="text-xs text-muted-foreground">
              {formatDate(item.timestamp)}
            </span>
          </div>
          <p className="text-sm text-muted-foreground truncate">
            {item.prompt}
          </p>
          {/* 显示metadata中的额外信息 */}
          {item.metadata && (
            <div className="flex flex-wrap gap-2 mt-2">
              {item.metadata.userName && (
                <span className="text-xs px-1.5 py-0.5 rounded bg-secondary text-secondary-foreground">
                  {item.metadata.userName}
                </span>
              )}
              {item.metadata.qianNumber && (
                <span className="text-xs px-1.5 py-0.5 rounded bg-secondary text-secondary-foreground">
                  第{item.metadata.qianNumber}签
                </span>
              )}
              {item.metadata.birthday && (
                <span className="text-xs px-1.5 py-0.5 rounded bg-secondary text-secondary-foreground">
                  {item.metadata.birthday}
                </span>
              )}
              {item.metadata.cards && item.metadata.cards.length > 0 && (
                <span className="text-xs px-1.5 py-0.5 rounded bg-secondary text-secondary-foreground">
                  {item.metadata.cards.length}张牌
                </span>
              )}
            </div>
          )}
        </div>
        <button
          className="shrink-0 h-8 w-8 p-0 text-muted-foreground hover:text-destructive rounded-md transition-colors flex items-center justify-center"
          onClick={handleDelete}
          aria-label="删除记录"
        >
          <Trash2 className="h-4 w-4" />
        </button>
      </div>
    </div>
  )
})

export default function HistoryPage() {
  const navigate = useNavigate()
  const { type } = useParams<{ type: string }>()
  const [history, setHistory] = useState<DivinationHistoryItem[]>([])
  const [selectedItem, setSelectedItem] = useState<DivinationHistoryItem | null>(null)
  const [showDrawer, setShowDrawer] = useState(false)

  // 获取占卜配置
  const divinationConfig = type ? getDivinationOption(type) : null

  useEffect(() => {
    loadHistory()
  }, [type])

  const loadHistory = () => {
    if (type) {
      setHistory(getHistoryByType(type))
    }
  }

  const handleClearAll = () => {
    if (confirm('确定要清空所有历史记录吗？') && type) {
      // 清空该类型的所有记录
      const allHistory = getHistoryByType(type)
      allHistory.forEach(item => deleteHistoryItem(item.id, type))
      loadHistory()
      toast.success('已清空所有历史记录')
    }
  }

  // 使用 useCallback 稳定回调引用，避免子组件不必要的重渲染
  const handleViewResult = useCallback((item: DivinationHistoryItem) => {
    setSelectedItem(item)
    setShowDrawer(true)
  }, [])

  const handleDeleteItem = useCallback((id: string) => {
    if (type) {
      deleteHistoryItem(id, type)
      loadHistory()
      toast.success('已删除')
    }
  }, [type])

  // 将 markdown 安全渲染成 HTML（使用 DOMPurify 防止 XSS）
  const renderedResult = useMemo(() => {
    if (!selectedItem) return ''
    return safeRenderMarkdown(selectedItem.result)
  }, [selectedItem])

  return (
    <div className="space-y-6">
      {/* 返回按钮 */}
      <button
        onClick={() => navigate(`/divination/${type}`)}
        className="flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        返回
      </button>

      {/* 标题区域 */}
      <div className="text-center py-6">
        <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
          {divinationConfig?.title || '历史记录'}
        </h1>
        <p className="text-muted-foreground">
          最近 {history.length} 条占卜记录
        </p>
      </div>

      {/* 内容卡片 */}
      <div className="rounded-xl border border-border bg-card p-6">
        {history.length > 0 && (
          <div className="flex justify-end mb-4">
            <button
              onClick={handleClearAll}
              className="inline-flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-muted-foreground hover:text-destructive transition-colors"
            >
              <Trash2 className="h-4 w-4" />
              清空所有
            </button>
          </div>
        )}

        {history.length === 0 ? (
          <div className="text-center py-16 text-muted-foreground">
            <Calendar className="h-16 w-16 mx-auto mb-4 opacity-30" />
            <p className="font-medium">暂无历史记录</p>
            <p className="text-sm mt-2">开始占卜后会自动保存记录</p>
          </div>
        ) : (
          <div className="space-y-3">
            {history.map((item) => (
              <HistoryItem
                key={item.id}
                item={item}
                onView={handleViewResult}
                onDelete={handleDeleteItem}
              />
            ))}
          </div>
        )}
      </div>

      {/* 结果抽屉 */}
      {selectedItem && (
        <ResultDrawer
          show={showDrawer}
          onClose={() => setShowDrawer(false)}
          result={renderedResult}
          loading={false}
          streaming={false}
        />
      )}
    </div>
  )
}
