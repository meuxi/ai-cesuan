import { useTranslation } from 'react-i18next'
import { Label } from '@/components/ui/label'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { getDivinationOption } from '@/config/constants'
import { Button } from '@/components/ui/button'
import { Sparkles } from 'lucide-react'

const CONFIG = getDivinationOption('plum_flower')!

export default function PlumFlowerPage() {
  const { t } = useTranslation()
  const [plumFlower, setPlumFlower] = useLocalStorage('plum_flower', {
    num1: 0,
    num2: 0,
  })
  const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
    useDivination('plum_flower')

  const handleSubmit = () => {
    onSubmit({
      prompt: `${plumFlower.num1} ${plumFlower.num2}`,
      plum_flower: plumFlower,
    })
  }

  return (
    <DivinationCardHeader
      title={t('plumFlower.title')}
      description={t('plumFlower.description')}
      icon={CONFIG.icon}
      divinationType="plum_flower"
    >
      <div className="max-w-2xl mx-auto w-full">
        <div className="space-y-5">
          <div className="p-4 bg-secondary rounded-lg border border-border">
            <p className="text-sm text-foreground">{t('plumFlower.inputTip')}</p>
          </div>
          <div>
            <Label className="text-sm font-medium text-foreground">{t('plumFlower.number1')}</Label>
            <input
              type="number"
              min={0}
              max={1000}
              value={plumFlower.num1}
              onChange={(e) =>
                setPlumFlower({ ...plumFlower, num1: parseInt(e.target.value) || 0 })
              }
              className="w-full px-3 py-2 mt-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            />
          </div>
          <div>
            <Label className="text-sm font-medium text-foreground">{t('plumFlower.number2')}</Label>
            <input
              type="number"
              min={0}
              max={1000}
              value={plumFlower.num2}
              onChange={(e) =>
                setPlumFlower({ ...plumFlower, num2: parseInt(e.target.value) || 0 })
              }
              className="w-full px-3 py-2 mt-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            />
          </div>
        </div>

        {!result && !loading && (
          <div className="mt-6">
            <Button
              onClick={handleSubmit}
              disabled={loading}
              className="w-full h-12"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              {t('plumFlower.startDivination')}
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
