import { Eye, Loader2, ArrowRight } from 'lucide-react'

interface DivinationActionBarProps {
  hasResult: boolean
  loading: boolean
  onToggleResult: () => void
  onSubmit: () => void
}

export function DivinationActionBar({
  hasResult,
  loading,
  onToggleResult,
  onSubmit,
}: DivinationActionBarProps) {
  return (
    <div className="flex gap-3 justify-center pt-6">
      <button
        onClick={onToggleResult}
        className="inline-flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-medium border border-input rounded-md bg-background text-muted-foreground hover:bg-accent transition-colors disabled:opacity-50 flex-1 md:flex-initial md:min-w-[140px]"
        disabled={!hasResult}
      >
        <Eye className="h-4 w-4" />
        查看结果
      </button>
      <button
        onClick={onSubmit}
        disabled={loading}
        className="inline-flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-semibold bg-primary text-primary-foreground hover:bg-primary/90 rounded-md transition-colors disabled:opacity-50 flex-1 md:flex-initial md:min-w-[140px]"
      >
        {loading ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" />
            占卜中
          </>
        ) : (
          <>
            开始占卜
            <ArrowRight className="h-4 w-4" />
          </>
        )}
      </button>
    </div>
  )
}
