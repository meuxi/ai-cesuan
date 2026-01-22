import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { Solar } from 'lunar-javascript'
import { logger } from '@/utils/logger'
import SEOHead, { SEO_CONFIG } from '@/components/SEOHead'
import { Label } from '@/components/ui/label'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { getDivinationOption } from '@/config/constants'
import { toast } from 'sonner'
import { BaziDisplay } from '@/components/BaziDisplay'
import { DaYunYearlyPanel } from '@/components/bazi/DaYunYearlyPanel'
import { Button } from '@/components/ui/button'
import { Calculator, Sparkles, Loader2 } from 'lucide-react'

const CONFIG = getDivinationOption('birthday')!
const API_BASE = import.meta.env.VITE_API_BASE || ''

export default function BirthdayPage() {
  const { t } = useTranslation()
  const [birthday, setBirthday] = useLocalStorage('birthday', '2000-08-17T00:00')
  const [lunarBirthday, setLunarBirthday] = useState('')
  const [baziData, setBaziData] = useState<any>(null)
  const [baziLoading, setBaziLoading] = useState(false)
  const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
    useDivination('birthday')

  const computeLunarBirthday = (birthdayStr: string) => {
    try {
      const date = new Date(birthdayStr)
      const solar = Solar.fromYmdHms(
        date.getFullYear(),
        date.getMonth() + 1,
        date.getDate(),
        date.getHours(),
        date.getMinutes(),
        date.getSeconds()
      )
      setLunarBirthday(solar.getLunar().toFullString())
    } catch (error) {
      logger.error('农历转换失败:', error)
      setLunarBirthday(t('birthday.conversionFailed'))
    }
  }

  useEffect(() => {
    computeLunarBirthday(birthday)
  }, [birthday])

  // 步骤1：计算八字
  const handleCalculateBazi = async () => {
    const date = new Date(birthday)
    try {
      setBaziLoading(true)
      const response = await fetch(`${API_BASE}/api/bazi/paipan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          year: date.getFullYear(),
          month: date.getMonth() + 1,
          day: date.getDate(),
          hour: date.getHours(),
          minute: date.getMinutes(),
        }),
      })

      if (!response.ok) {
        throw new Error('排盘失败')
      }

      const baziResult = await response.json()
      setBaziData(baziResult)
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : '排盘失败，请重试'
      toast.error(message)
      logger.error('排盘错误:', error)
    } finally {
      setBaziLoading(false)
    }
  }

  // 步骤2：AI分析
  const handleAIAnalysis = () => {
    const date = new Date(birthday)
    const formattedBirthday = date.getFullYear() + '-' +
      String(date.getMonth() + 1).padStart(2, '0') + '-' +
      String(date.getDate()).padStart(2, '0') + ' ' +
      String(date.getHours()).padStart(2, '0') + ':' +
      String(date.getMinutes()).padStart(2, '0') + ':' +
      String(date.getSeconds()).padStart(2, '0')

    onSubmit({
      prompt: formattedBirthday,
      birthday: formattedBirthday,
      lunar_birthday: lunarBirthday,
      bazi_data: baziData,
    })
  }

  return (
    <DivinationCardHeader
      title={t('birthday.title')}
      description={t('birthday.description')}
      icon={CONFIG.icon}
      divinationType="birthday"
    >
      <div className="max-w-2xl mx-auto w-full">
        <div className="space-y-5">
          <div>
            <Label className="block mb-2 text-sm font-medium text-foreground">{t('birthday.birthDate')}</Label>
            <input
              type="datetime-local"
              value={birthday}
              onChange={(e) => setBirthday(e.target.value)}
              className="px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            />
          </div>
          <div>
            <Label className="text-sm font-medium text-foreground">{t('birthday.lunar')}</Label>
            <p className="text-sm mt-2 text-muted-foreground">{lunarBirthday}</p>
          </div>
        </div>

        {/* 步骤1：计算八字按钮 */}
        {!baziData && (
          <div className="mt-6">
            <Button
              onClick={handleCalculateBazi}
              disabled={baziLoading}
              className="w-full h-12"
            >
              {baziLoading ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('birthday.calculating')}</>
              ) : (
                <><Calculator className="w-4 h-4 mr-2" />{t('birthday.calculateBazi')}</>
              )}
            </Button>
          </div>
        )}

        {/* 步骤2：排盘结果展示 + AI分析按钮 */}
        {baziData && (
          <>
            <BaziDisplay data={baziData} loading={baziLoading} />
            
            {/* 大运流年面板 */}
            <DaYunYearlyPanel 
              birthYear={new Date(birthday).getFullYear()}
              startAge={baziData?.dayun_start_age || 5}
            />

            {/* AI分析按钮 */}
            {!result && !loading && (
              <div className="mt-4">
                <Button
                  onClick={handleAIAnalysis}
                  disabled={loading}
                  className="w-full h-12"
                  variant="default"
                >
                  <Sparkles className="w-4 h-4 mr-2" />
                  {t('birthday.startAIAnalysis')}
                </Button>
              </div>
            )}
          </>
        )}

        {/* 步骤3：AI分析结果内嵌展示 */}
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
