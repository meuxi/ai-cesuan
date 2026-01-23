/**
 * 八字合婚页面
 * 基于完整八字（年月日时）进行合婚分析
 */

import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Label } from '@/components/ui/label'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { toast } from 'sonner'
import { Heart, Users, Calculator, Sparkles, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'

const API_BASE = import.meta.env.VITE_API_BASE || ''

interface PersonBazi {
    year: string
    month: string
    day: string
    hour: string
    full: string
    wuxing_count: Record<string, number>
    dominant_wuxing: string
}

interface PersonInfo {
    name: string
    birth: string
    bazi: PersonBazi
}

interface Dimension {
    name: string
    score: number
    description: string
}

interface Conflict {
    title: string
    severity: string
    description: string
    suggestion: string
}

interface HehunResult {
    success: boolean
    male: PersonInfo
    female: PersonInfo
    overall_score: number
    level: string
    level_color: string
    dimensions: Dimension[]
    conflicts: Conflict[]
}

interface PersonInput {
    name: string
    year: number
    month: number
    day: number
    hour: number
}

const currentYear = new Date().getFullYear()

export default function HehunPage() {
    const { t } = useTranslation()
    const [male, setMale] = useLocalStorage<PersonInput>('hehun_male', {
        name: '男方',
        year: 1995,
        month: 1,
        day: 1,
        hour: 12,
    })
    const [female, setFemale] = useLocalStorage<PersonInput>('hehun_female', {
        name: '女方',
        year: 1997,
        month: 1,
        day: 1,
        hour: 12,
    })
    const [hehunData, setHehunData] = useState<HehunResult | null>(null)
    const [calcLoading, setCalcLoading] = useState(false)

    const { result, loading, resultLoading, streaming, onSubmit } = useDivination('hehun')

    const handleCalculate = async () => {
        if (!male.year || !male.month || !male.day || !female.year || !female.month || !female.day) {
            toast.error('请填写完整的出生信息')
            return
        }

        try {
            setCalcLoading(true)
            const response = await fetch(`${API_BASE}/api/hehun/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    male: { ...male, gender: '男' },
                    female: { ...female, gender: '女' },
                    hepan_type: 'love',
                }),
            })

            if (!response.ok) throw new Error('合婚计算失败')
            const data = await response.json()
            setHehunData(data)
        } catch (error: unknown) {
            const message = error instanceof Error ? error.message : '合婚计算失败'
            toast.error(message)
        } finally {
            setCalcLoading(false)
        }
    }

    const handleAIAnalysis = () => {
        onSubmit({
            prompt: '八字合婚分析',
            hehun_data: hehunData,
        })
    }

    const handleReset = () => {
        setHehunData(null)
    }

    const getScoreColor = (score: number) => {
        if (score >= 75) return 'text-green-600 dark:text-green-400'
        if (score >= 55) return 'text-yellow-600 dark:text-yellow-400'
        return 'text-red-600 dark:text-red-400'
    }

    const renderPersonInput = (
        person: PersonInput,
        setPerson: (p: PersonInput) => void,
        label: string,
        icon: string
    ) => (
        <div className="p-4 bg-secondary rounded-lg border border-border">
            <div className="flex items-center gap-2 mb-3">
                <span className="text-xl">{icon}</span>
                <Label className="text-foreground font-medium">{label}</Label>
            </div>
            <div className="space-y-3">
                <div className="grid grid-cols-4 gap-2">
                    <div className="col-span-2">
                        <Label className="text-xs text-muted-foreground">年</Label>
                        <input
                            type="number"
                            min="1900"
                            max={currentYear}
                            value={person.year}
                            onChange={(e) => setPerson({ ...person, year: parseInt(e.target.value) || 1990 })}
                            className="w-full px-2 py-1.5 text-sm border border-input rounded-md bg-background text-foreground"
                        />
                    </div>
                    <div>
                        <Label className="text-xs text-muted-foreground">月</Label>
                        <select
                            value={person.month}
                            onChange={(e) => setPerson({ ...person, month: parseInt(e.target.value) })}
                            className="w-full px-2 py-1.5 text-sm border border-input rounded-md bg-background text-foreground"
                        >
                            {Array.from({ length: 12 }, (_, i) => (
                                <option key={i + 1} value={i + 1}>{i + 1}月</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <Label className="text-xs text-muted-foreground">日</Label>
                        <select
                            value={person.day}
                            onChange={(e) => setPerson({ ...person, day: parseInt(e.target.value) })}
                            className="w-full px-2 py-1.5 text-sm border border-input rounded-md bg-background text-foreground"
                        >
                            {Array.from({ length: 31 }, (_, i) => (
                                <option key={i + 1} value={i + 1}>{i + 1}日</option>
                            ))}
                        </select>
                    </div>
                </div>
                <div>
                    <Label className="text-xs text-muted-foreground">时辰</Label>
                    <select
                        value={person.hour}
                        onChange={(e) => setPerson({ ...person, hour: parseInt(e.target.value) })}
                        className="w-full px-2 py-1.5 text-sm border border-input rounded-md bg-background text-foreground"
                    >
                        <option value={0}>子时 (23:00-01:00)</option>
                        <option value={1}>丑时 (01:00-03:00)</option>
                        <option value={3}>寅时 (03:00-05:00)</option>
                        <option value={5}>卯时 (05:00-07:00)</option>
                        <option value={7}>辰时 (07:00-09:00)</option>
                        <option value={9}>巳时 (09:00-11:00)</option>
                        <option value={11}>午时 (11:00-13:00)</option>
                        <option value={13}>未时 (13:00-15:00)</option>
                        <option value={15}>申时 (15:00-17:00)</option>
                        <option value={17}>酉时 (17:00-19:00)</option>
                        <option value={19}>戌时 (19:00-21:00)</option>
                        <option value={21}>亥时 (21:00-23:00)</option>
                    </select>
                </div>
            </div>
            {hehunData && (
                <div className="mt-3 p-2 bg-background rounded border border-border">
                    <div className="text-xs text-muted-foreground mb-1">八字</div>
                    <div className="font-medium text-foreground text-sm">
                        {label === '男方信息' ? hehunData.male?.bazi?.full : hehunData.female?.bazi?.full}
                    </div>
                    <div className="text-xs text-muted-foreground mt-1">
                        主五行：{label === '男方信息' ? hehunData.male?.bazi?.dominant_wuxing : hehunData.female?.bazi?.dominant_wuxing}
                    </div>
                </div>
            )}
        </div>
    )

    return (
        <DivinationCardHeader
            title={t('hehun.title')}
            description={t('hehun.description')}
            icon={Heart}
            divinationType="hehun"
        >
            <div className="max-w-3xl mx-auto w-full">
                <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {renderPersonInput(male, setMale, '男方信息', '👨')}
                        {renderPersonInput(female, setFemale, '女方信息', '👩')}
                    </div>

                    {hehunData && (
                        <div className="p-6 bg-card rounded-xl border border-border">
                            <div className="flex justify-between items-center mb-4">
                                <h3 className="text-lg font-semibold text-foreground">合婚结果</h3>
                                <Button variant="ghost" size="sm" onClick={handleReset}>重新计算</Button>
                            </div>

                            <div className="flex justify-center mb-6">
                                <div className="text-center">
                                    <div className={`text-5xl font-bold ${getScoreColor(hehunData.overall_score)}`}>
                                        {hehunData.overall_score}
                                    </div>
                                    <div className={`text-lg font-medium mt-1 ${getScoreColor(hehunData.overall_score)}`}>
                                        {hehunData.level}
                                    </div>
                                </div>
                            </div>

                            <div className="h-3 bg-secondary rounded-full overflow-hidden mb-6">
                                <div
                                    className={`h-full transition-all duration-500 ${hehunData.overall_score >= 75 ? 'bg-green-500' :
                                            hehunData.overall_score >= 55 ? 'bg-yellow-500' : 'bg-red-500'
                                        }`}
                                    style={{ width: `${hehunData.overall_score}%` }}
                                />
                            </div>

                            {hehunData.dimensions && hehunData.dimensions.length > 0 && (
                                <div className="space-y-3 mb-4">
                                    <h4 className="text-sm font-medium text-muted-foreground">维度分析</h4>
                                    {hehunData.dimensions.map((dim, idx) => (
                                        <div key={idx} className="flex items-center justify-between p-2 bg-secondary rounded">
                                            <span className="text-sm text-foreground">{dim.name}</span>
                                            <div className="flex items-center gap-2">
                                                <div className="w-24 h-2 bg-background rounded-full overflow-hidden">
                                                    <div
                                                        className="h-full bg-primary"
                                                        style={{ width: `${dim.score}%` }}
                                                    />
                                                </div>
                                                <span className="text-sm font-medium w-8">{dim.score}</span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}

                            {hehunData.conflicts && hehunData.conflicts.length > 0 && (
                                <div className="space-y-2">
                                    <h4 className="text-sm font-medium text-muted-foreground">注意事项</h4>
                                    {hehunData.conflicts.map((conflict, idx) => (
                                        <div key={idx} className="p-3 bg-destructive/10 rounded border border-destructive/20">
                                            <div className="font-medium text-sm text-destructive">{conflict.title}</div>
                                            <div className="text-xs text-muted-foreground mt-1">{conflict.description}</div>
                                            <div className="text-xs text-foreground mt-1">💡 {conflict.suggestion}</div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {!hehunData && (
                    <div className="mt-6">
                        <Button onClick={handleCalculate} disabled={calcLoading} className="w-full h-12">
                            {calcLoading ? (
                                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />正在计算...</>
                            ) : (
                                <><Calculator className="w-4 h-4 mr-2" />开始合婚计算</>
                            )}
                        </Button>
                    </div>
                )}

                {hehunData && !result && !loading && (
                    <div className="mt-4">
                        <Button onClick={handleAIAnalysis} disabled={loading} className="w-full h-12">
                            <Sparkles className="w-4 h-4 mr-2" />
                            AI 深度分析
                        </Button>
                    </div>
                )}

                <InlineResult result={result} loading={resultLoading} streaming={streaming} title={t('hehun.aiAnalysis')} />
            </div>
        </DivinationCardHeader>
    )
}
