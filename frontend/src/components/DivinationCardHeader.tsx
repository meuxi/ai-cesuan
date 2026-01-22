import { ReactNode } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { ArrowLeft, LucideIcon, History } from 'lucide-react'

interface DivinationCardHeaderProps {
  /** 页面标题 */
  title: string
  /** 页面描述/副标题 */
  description: string
  /** 卡片内容区域 */
  children: ReactNode
  /** 返回按钮点击回调，默认返回到市场首页 */
  onBack?: () => void
  /** 标题图标 */
  icon?: LucideIcon
  /** 占卜类型，用于历史记录导航（可选，如果不提供则不显示历史按钮） */
  divinationType?: string
}

/**
 * 占卜页面通用卡片头部组件 - FateMaster 风格
 */
export function DivinationCardHeader({
  title,
  description,
  children,
  onBack,
  icon: Icon,
  divinationType,
}: DivinationCardHeaderProps) {
  const navigate = useNavigate()
  const { t } = useTranslation()

  const handleBack = () => {
    if (onBack) {
      onBack()
    } else {
      navigate('/')
    }
  }

  return (
    <div className="space-y-6">
      {/* 顶部导航栏 */}
      <div className="flex items-center justify-between">
        <button
          onClick={handleBack}
          className="flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          {t('common.back')}
        </button>

        {divinationType && (
          <button
            onClick={() => navigate(`/history/${divinationType}`)}
            className="flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            <History className="h-4 w-4" />
            {t('common.history')}
          </button>
        )}
      </div>

      {/* 标题区域 */}
      <div className="text-center py-6">
        <div className="flex items-center justify-center gap-3 mb-3">
          {Icon && (
            <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center">
              <Icon className="w-5 h-5 text-muted-foreground" />
            </div>
          )}
          <h1 className="text-3xl md:text-4xl font-bold text-foreground">
            {title}
          </h1>
        </div>
        <p className="text-muted-foreground">
          {description}
        </p>
      </div>

      {/* 内容卡片 */}
      <div className="rounded-xl border border-border bg-card p-4 md:p-6">
        {children}
      </div>
    </div>
  )
}
