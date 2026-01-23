import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { Label } from '@/components/ui/label'
import { Compass, Calendar, Calculator, Sparkles, Loader2 } from 'lucide-react'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'

const API_BASE = import.meta.env.VITE_API_BASE || ''

interface DaliurenResult {
    time_info: {
        solar_date: string
        lunar_date: string
        jie_qi: string
        sizhu: { year: string; month: string; day: string; hour: string }
    }
    tiandi_pan: {
        tian_pan: string[]
        di_pan: string[]
    }
    sike: Array<{
        name: string
        tian: string
        di: string
        liuqin: string
    }>
    sanchuan: Array<{
        name: string
        zhi: string
        wuxing: string
        liuqin: string
    }>
    tianjiang: Array<{
        zhi: string
        jiang: string
        wuxing: string
    }>
}

export default function DaliurenPage() {
    const { t } = useTranslation()
    const [year, setYear] = useState(new Date().getFullYear())
    const [month, setMonth] = useState(new Date().getMonth() + 1)
    const [day, setDay] = useState(new Date().getDate())
    const [hour, setHour] = useState(new Date().getHours())
    const [minute, setMinute] = useState(new Date().getMinutes())
    const [liurenData, setLiurenData] = useState<DaliurenResult | null>(null)
    const [paipanLoading, setPaipanLoading] = useState(false)

    const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
        useDivination('daliuren')

    // 步骤1：排盘
    const handlePaipan = async () => {
        if (!year || !month || !day || hour === undefined) {
            toast.error('请填写完整的起盘时间')
            return
        }

        try {
            setPaipanLoading(true)
            const response = await fetch(`${API_BASE}/api/daliuren/paipan`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ year, month, day, hour, minute })
            })

            if (!response.ok) {
                throw new Error('排盘失败')
            }

            const data = await response.json()
            setLiurenData(data)
        } catch (error: any) {
            toast.error(error.message || '排盘失败，请重试')
        } finally {
            setPaipanLoading(false)
        }
    }

    // 步骤2：AI分析
    const handleAIAnalysis = () => {
        onSubmit({
            prompt: `大六壬排盘：${liurenData?.time_info?.solar_date}`,
            daliuren_data: liurenData
        })
    }

    return (
        <DivinationCardHeader
            title={t('daliuren.title')}
            description={t('daliuren.description')}
            icon={Compass}
            divinationType="daliuren"
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
                    </div>
                </div>

                {/* 排盘结果展示 */}
                {liurenData && (
                    <div className="rounded-xl p-6 border border-border bg-card space-y-6 mb-6">
                        <h3 className="text-lg font-semibold text-foreground">排盘结果</h3>

                        {/* 时间信息 */}
                        {liurenData.time_info && (
                            <div className="space-y-2">
                                <h4 className="font-medium text-foreground">时间信息</h4>
                                <div className="grid grid-cols-2 gap-2 text-sm text-muted-foreground">
                                    <div>公历：{liurenData.time_info.solar_date}</div>
                                    <div>农历：{liurenData.time_info.lunar_date}</div>
                                    <div>节气：{liurenData.time_info.jie_qi}</div>
                                    <div className="col-span-2">
                                        四柱：{liurenData.time_info.sizhu?.year} {liurenData.time_info.sizhu?.month} {liurenData.time_info.sizhu?.day} {liurenData.time_info.sizhu?.hour}
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* 四课 */}
                        {liurenData.sike && (
                            <div className="space-y-2">
                                <h4 className="font-medium text-foreground">四课</h4>
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                    {liurenData.sike.map((ke, idx) => (
                                        <div key={idx} className="border border-border rounded-lg p-3 bg-secondary">
                                            <div className="text-center font-bold text-sm mb-2 text-foreground">{ke.name}</div>
                                            <div className="text-center space-y-1">
                                                <div className="text-foreground">天: {ke.tian}</div>
                                                <div className="text-muted-foreground">地: {ke.di}</div>
                                            </div>
                                            <div className="text-xs text-muted-foreground mt-2 text-center">
                                                {ke.liuqin}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* 三传 */}
                        {liurenData.sanchuan && (
                            <div className="space-y-2">
                                <h4 className="font-medium text-foreground">三传</h4>
                                <div className="grid grid-cols-3 gap-3">
                                    {liurenData.sanchuan.map((chuan, idx) => (
                                        <div key={idx} className="border border-border rounded-lg p-4 bg-secondary text-center">
                                            <div className="font-bold mb-2 text-foreground">{chuan.name}</div>
                                            <div className="text-2xl text-foreground mb-1">{chuan.zhi}</div>
                                            <div className="text-sm text-muted-foreground">{chuan.wuxing}</div>
                                            <div className="text-xs text-muted-foreground mt-1">{chuan.liuqin}</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* 十二天将 */}
                        {liurenData.tianjiang && (
                            <div className="space-y-2">
                                <h4 className="font-medium text-foreground">十二天将</h4>
                                <div className="grid grid-cols-3 md:grid-cols-4 gap-2 text-xs">
                                    {liurenData.tianjiang.map((tj, idx) => (
                                        <div key={idx} className="border border-border rounded p-2 text-center bg-secondary">
                                            <div className="font-bold text-foreground">{tj.jiang}</div>
                                            <div className="text-foreground">{tj.zhi}</div>
                                            <div className="text-muted-foreground">{tj.wuxing}</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* 步骤1：排盘按钮 */}
                {!liurenData && (
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
                {liurenData && !result && !loading && (
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
                    title={t('daliuren.aiAnalysis')}
                />
            </div>
        </DivinationCardHeader>
    )
}
