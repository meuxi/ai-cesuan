import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { Label } from '@/components/ui/label'
import { Sparkles, Calendar, Calculator, Loader2, RotateCcw } from 'lucide-react'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import { QimenGrid, QimenTimeInfo, type GongData } from '@/components/qimen'
import { motion } from 'framer-motion'

const API_BASE = import.meta.env.VITE_API_BASE || ''

interface QimenResult {
  time_info: {
    solar_date: string
    lunar_date: string
    jie_qi: string
    sizhu: { year: string; month: string; day: string; hour: string }
  }
  pan_info: {
    description: string
    yin_yang: string
    ju_shu: number
  }
  jiugong: GongData[]
}

export default function QimenPage() {
  const { t } = useTranslation()
  const [year, setYear] = useState(new Date().getFullYear())
  const [month, setMonth] = useState(new Date().getMonth() + 1)
  const [day, setDay] = useState(new Date().getDate())
  const [hour, setHour] = useState(new Date().getHours())
  const [minute, setMinute] = useState(new Date().getMinutes())
  const [panType, setPanType] = useState('时盘')
  const [panStyle, setPanStyle] = useState('转盘')
  const [qimenData, setQimenData] = useState<QimenResult | null>(null)
  const [paipanLoading, setPaipanLoading] = useState(false)

  const { result, loading, resultLoading, streaming, onSubmit } =
    useDivination('qimen')

  // 步骤1：排盘
  const handlePaipan = async () => {
    if (!year || !month || !day || hour === undefined) {
      toast.error('请填写完整的起盘时间')
      return
    }

    try {
      setPaipanLoading(true)
      const response = await fetch(`${API_BASE}/api/qimen/paipan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          year, month, day, hour, minute, 
          pan_type: panType,
          pan_style: panStyle 
        })
      })

      if (!response.ok) {
        throw new Error('排盘失败')
      }

      const data = await response.json()
      setQimenData(data)
    } catch (error: any) {
      toast.error(error.message || '排盘失败，请重试')
    } finally {
      setPaipanLoading(false)
    }
  }

  // 重置
  const handleReset = () => {
    setQimenData(null)
  }

  // 步骤2：AI分析
  const handleAIAnalysis = () => {
    onSubmit({
      prompt: `奇门遁甲排盘：${qimenData?.pan_info?.description}`,
      qimen_data: qimenData
    })
  }

  return (
    <DivinationCardHeader
      title={t('qimen.title')}
      description={t('qimen.description')}
      icon={Sparkles}
      divinationType="qimen"
    >
      <div className="max-w-4xl mx-auto w-full">
        {/* 起盘表单 */}
        <div className="space-y-4 mb-6">
          <h3 className="text-lg font-semibold flex items-center gap-2 text-foreground">
            <Calendar className="h-5 w-5 text-muted-foreground" />
            起盘时间
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div>
              <Label className="block mb-2 text-sm font-medium text-foreground">年份</Label>
              <input
                type="number"
                className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                value={year}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setYear(Number(e.target.value))}
              />
            </div>
            <div>
              <Label className="block mb-2 text-sm font-medium text-foreground">月份</Label>
              <input
                type="number"
                className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                value={month}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setMonth(Number(e.target.value))}
                min={1}
                max={12}
              />
            </div>
            <div>
              <Label className="block mb-2 text-sm font-medium text-foreground">日期</Label>
              <input
                type="number"
                className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                value={day}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setDay(Number(e.target.value))}
                min={1}
                max={31}
              />
            </div>
            <div>
              <Label className="block mb-2 text-sm font-medium text-foreground">时</Label>
              <input
                type="number"
                className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                value={hour}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setHour(Number(e.target.value))}
                min={0}
                max={23}
              />
            </div>
            <div>
              <Label className="block mb-2 text-sm font-medium text-foreground">分</Label>
              <input
                type="number"
                className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                value={minute}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setMinute(Number(e.target.value))}
                min={0}
                max={59}
              />
            </div>
            <div>
              <Label className="block mb-2 text-sm font-medium text-foreground">盘式</Label>
              <select
                className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                value={panType}
                onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setPanType(e.target.value)}
              >
                <option value="时盘">{t('qimen.hourlyChart')}</option>
                <option value="日盘">{t('qimen.dailyChart')}</option>
                <option value="月盘">{t('qimen.monthlyChart')}</option>
                <option value="年盘">{t('qimen.yearlyChart')}</option>
              </select>
            </div>
            <div>
              <Label className="block mb-2 text-sm font-medium text-foreground">盘型</Label>
              <select
                className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                value={panStyle}
                onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setPanStyle(e.target.value)}
              >
                <option value="转盘">{t('qimen.rotating')}</option>
                <option value="飞盘">{t('qimen.flying')}</option>
              </select>
            </div>
          </div>
        </div>

        {/* 排盘结果展示 - 使用新组件 */}
        {qimenData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl p-6 border border-border bg-card/80 backdrop-blur-sm space-y-6 mb-6"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary" />
                排盘结果
              </h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleReset}
                className="text-muted-foreground hover:text-foreground"
              >
                <RotateCcw className="w-4 h-4 mr-1" />
                重新起盘
              </Button>
            </div>

            {/* 时间信息 - 使用新组件 */}
            {qimenData.time_info && qimenData.pan_info && (
              <QimenTimeInfo
                timeInfo={qimenData.time_info}
                panInfo={qimenData.pan_info}
              />
            )}

            {/* 九宫格 - 使用新组件 */}
            {qimenData.jiugong && (
              <div className="space-y-3">
                <h4 className="font-medium text-foreground text-center">九宫布局</h4>
                <QimenGrid jiugong={qimenData.jiugong} />
              </div>
            )}
          </motion.div>
        )}

        {/* 步骤1：排盘按钮 */}
        {!qimenData && (
          <div className="mt-6">
            <Button
              onClick={handlePaipan}
              disabled={paipanLoading}
              className="w-full h-12"
            >
              {paipanLoading ? (
                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />正在排盘...</>
              ) : (
                <><Calculator className="w-4 h-4 mr-2" />开始排盘</>
              )}
            </Button>
          </div>
        )}

        {/* 步骤2：AI分析按钮 */}
        {qimenData && !result && !loading && (
          <div className="mt-4">
            <Button
              onClick={handleAIAnalysis}
              disabled={loading}
              className="w-full h-12"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              开始 AI 分析
            </Button>
          </div>
        )}

        {/* 步骤3：AI分析结果 */}
        <InlineResult
          result={result}
          loading={resultLoading}
          streaming={streaming}
          title={t('qimen.aiAnalysis')}
        />
      </div>
    </DivinationCardHeader>
  )
}
