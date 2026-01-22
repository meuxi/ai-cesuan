import { useTranslation } from 'react-i18next'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { getDivinationOption } from '@/config/constants'
import { Button } from '@/components/ui/button'
import { Sparkles } from 'lucide-react'

const CONFIG = getDivinationOption('name')!

export default function NamePage() {
  const { t } = useTranslation()
  const [prompt, setPrompt] = useLocalStorage('name_prompt', '')
  const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
    useDivination('name')

  const handleSubmit = () => {
    onSubmit({
      prompt: prompt,
    })
  }

  return (
    <DivinationCardHeader
      title={t('name.title')}
      description={t('name.description')}
      icon={CONFIG.icon}
      divinationType="name"
    >
      <div className="max-w-2xl mx-auto w-full">
        <div>
          <input
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder={t('name.namePlaceholder')}
            maxLength={10}
            className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          />
          <p className="text-xs text-muted-foreground mt-2">
            {t('name.nameTip')}
          </p>
        </div>

        {!result && !loading && (
          <div className="mt-6">
            <Button
              onClick={handleSubmit}
              disabled={!prompt.trim() || loading}
              className="w-full h-12"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              {t('name.startAnalysis')}
            </Button>
          </div>
        )}

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
