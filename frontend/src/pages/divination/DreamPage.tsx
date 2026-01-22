import { useTranslation } from 'react-i18next'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import SEOHead, { SEO_CONFIG } from '@/components/SEOHead'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { getDivinationOption } from '@/config/constants'
import { Button } from '@/components/ui/button'
import { Sparkles } from 'lucide-react'

const CONFIG = getDivinationOption('dream')!

export default function DreamPage() {
  const { t } = useTranslation()
  const [prompt, setPrompt] = useLocalStorage('dream_prompt', '')
  const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
    useDivination('dream')

  const handleSubmit = () => {
    onSubmit({
      prompt: prompt,
    })
  }

  return (
    <DivinationCardHeader
      title={t('dream.title')}
      description={t('dream.description')}
      icon={CONFIG.icon}
      divinationType="dream"
    >
      <div className="max-w-2xl mx-auto w-full">
        <div>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder={t('dream.dreamPlaceholder')}
            maxLength={40}
            rows={3}
            className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 resize-none"
          />
          <p className="text-xs text-muted-foreground mt-2">
            {t('dream.dreamTip')}
          </p>
        </div>

        {/* AI分析按钮 */}
        {!result && !loading && (
          <div className="mt-6">
            <Button
              onClick={handleSubmit}
              disabled={!prompt.trim() || loading}
              className="w-full h-12"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              {t('dream.startInterpret')}
            </Button>
          </div>
        )}

        {/* AI分析结果 */}
        <InlineResult
          result={result}
          loading={resultLoading}
          streaming={streaming}
          title={CONFIG.title}
        />
      </div>
    </DivinationCardHeader>
  )
}
