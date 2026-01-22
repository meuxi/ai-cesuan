import { useTranslation } from 'react-i18next'
import { Label } from '@/components/ui/label'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { getDivinationOption } from '@/config/constants'
import { Button } from '@/components/ui/button'
import { Sparkles } from 'lucide-react'

const CONFIG = getDivinationOption('fate')!

export default function FatePage() {
  const { t } = useTranslation()
  const [fate, setFate] = useLocalStorage('fate_body', {
    name1: '',
    name2: '',
  })
  const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
    useDivination('fate')

  const handleSubmit = () => {
    onSubmit({
      prompt: `${fate.name1} ${fate.name2}`,
      fate: fate,
    })
  }

  return (
    <DivinationCardHeader
      title={t('fate.title')}
      description={t('fate.description')}
      icon={CONFIG.icon}
      divinationType="fate"
    >
      <div className="max-w-2xl mx-auto w-full">
        <div className="space-y-5">
          <div className="p-4 bg-secondary rounded-lg border border-border">
            <h4 className="font-medium text-foreground">{t('fate.slogan')}</h4>
            <p className="text-sm text-muted-foreground mt-2">
              {t('fate.tip')}
            </p>
          </div>
          <div>
            <Label className="text-sm font-medium text-foreground">{t('fate.name1')}</Label>
            <input
              value={fate.name1}
              onChange={(e) => setFate({ ...fate, name1: e.target.value })}
              maxLength={40}
              className="w-full px-3 py-2 mt-2 text-sm border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            />
          </div>
          <div>
            <Label className="text-sm font-medium text-foreground">{t('fate.name2')}</Label>
            <input
              value={fate.name2}
              onChange={(e) => setFate({ ...fate, name2: e.target.value })}
              maxLength={40}
              className="w-full px-3 py-2 mt-2 text-sm border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            />
          </div>
        </div>

        {!result && !loading && (
          <div className="mt-6">
            <Button
              onClick={handleSubmit}
              disabled={!fate.name1.trim() || !fate.name2.trim() || loading}
              className="w-full h-12"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              {t('fate.predict')}
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
