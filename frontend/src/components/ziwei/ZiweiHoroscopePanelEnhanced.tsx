/**
 * 紫微斗数运限面板组件 - 增强版
 * 融合 MingAI-master 和 iztro-hook 的优点
 * 特性：
 * - 使用 iztro 前端计算精确运限
 * - 显示大限/流年四化
 * - 层级联动（选大限→显示对应流年）
 * - 五行颜色着色
 */

import { useState, useMemo, useEffect, useCallback, forwardRef, useImperativeHandle } from 'react'
import { useTranslation } from 'react-i18next'
import type { ZiweiResult, DecadeInfo } from '@/types/ziwei'
import type { HoroscopeHighlight, HoroscopeInfo } from './ZiweiChartGrid'
import { ziweiHoroscopeService, type MutagenInfo, type DecadalDetail, type YearlyDetail, type MonthlyDetail, type DailyDetail, type HourlyDetail } from '@/services/ziweiHoroscopeService'
import { MinorLimitCalculator, type MinorLimitInfo } from '@/services/ziwei/MinorLimitCalculator'

// 日期切换类型
export type HoroscopeScope = 'decadal' | 'yearly' | 'monthly' | 'daily' | 'hourly'

// 暴露给父组件的方法
export interface ZiweiHoroscopePanelRef {
    handleDateChange: (scope: HoroscopeScope, delta: number) => void
}

interface ZiweiHoroscopePanelProps {
    data: ZiweiResult
    onHighlightChange?: (highlight: HoroscopeHighlight) => void
    onHoroscopeInfoChange?: (info: HoroscopeInfo) => void
    onDateChange?: (scope: HoroscopeScope, delta: number) => void  // 日期切换回调（供中宫快捷按钮使用）
}

// 五行颜色映射：天干
function getStemColor(stem: string): string {
    switch (stem) {
        case '甲': case '乙': return 'text-green-500'
        case '丙': case '丁': return 'text-red-500'
        case '戊': case '己': return 'text-amber-500'
        case '庚': case '辛': return 'text-yellow-400'
        case '壬': case '癸': return 'text-blue-500'
        default: return 'text-foreground'
    }
}

// 五行颜色映射：地支
function getBranchColor(branch: string): string {
    const map: Record<string, string> = {
        '寅': 'text-green-500', '卯': 'text-green-500',
        '巳': 'text-red-500', '午': 'text-red-500',
        '辰': 'text-amber-500', '戌': 'text-amber-500', '丑': 'text-amber-500', '未': 'text-amber-500',
        '申': 'text-yellow-400', '酉': 'text-yellow-400',
        '亥': 'text-blue-500', '子': 'text-blue-500'
    }
    return map[branch] || 'text-foreground'
}

// 四化徽章组件
function MutagenBadge({ mutagen, compact = false }: { mutagen?: MutagenInfo; compact?: boolean }) {
    if (!mutagen) return null

    const items = [
        { key: 'lu', label: '禄', star: mutagen.lu, color: 'bg-green-500/20 text-green-600 dark:text-green-400' },
        { key: 'quan', label: '权', star: mutagen.quan, color: 'bg-red-500/20 text-red-600 dark:text-red-400' },
        { key: 'ke', label: '科', star: mutagen.ke, color: 'bg-blue-500/20 text-blue-600 dark:text-blue-400' },
        { key: 'ji', label: '忌', star: mutagen.ji, color: 'bg-purple-500/20 text-purple-600 dark:text-purple-400' },
    ]

    if (compact) {
        return (
            <div className="flex gap-0.5 flex-wrap">
                {items.map(item => item.star && (
                    <span key={item.key} className={`px-1 py-0.5 rounded text-[8px] ${item.color}`}>
                        {item.label}
                    </span>
                ))}
            </div>
        )
    }

    return (
        <div className="grid grid-cols-2 gap-1 text-[9px]">
            {items.map(item => (
                <div key={item.key} className={`px-1.5 py-0.5 rounded ${item.color}`}>
                    <span className="font-medium">{item.label}</span>
                    <span className="ml-1">{item.star || '-'}</span>
                </div>
            ))}
        </div>
    )
}

// 区块标题组件
function SectionHeader({
    title,
    color,
    isActive,
    onToggle,
    subtitle
}: {
    title: string
    color: string
    isActive: boolean
    onToggle: () => void
    subtitle?: string
}) {
    return (
        <button
            onClick={onToggle}
            className={`w-full py-2 px-3 flex items-center justify-between rounded-t-lg transition-colors ${isActive ? `${color} text-white` : 'bg-secondary/50 hover:bg-secondary'
                }`}
        >
            <div className="flex items-center gap-2">
                <span className="font-medium text-sm">{title}</span>
                {subtitle && <span className="text-xs opacity-80">{subtitle}</span>}
            </div>
            <span className="text-xs">{isActive ? '●' : '○'}</span>
        </button>
    )
}

export const ZiweiHoroscopePanelEnhanced = forwardRef<ZiweiHoroscopePanelRef, ZiweiHoroscopePanelProps>(
    function ZiweiHoroscopePanelEnhanced({ data, onHighlightChange, onHoroscopeInfoChange, onDateChange }, ref) {
    const { t } = useTranslation()
    // 初始化服务
    const [serviceReady, setServiceReady] = useState(false)

    // 选中状态
    const [selectedDecadeIndex, setSelectedDecadeIndex] = useState<number | null>(null)
    const [selectedYear, setSelectedYear] = useState<number | null>(null)
    const [selectedMonth, setSelectedMonth] = useState<number | null>(null)
    const [selectedDay, setSelectedDay] = useState<number | null>(null)
    const [selectedHour, setSelectedHour] = useState<number | null>(null)
    const [selectedMinorAge, setSelectedMinorAge] = useState<number | null>(null)

    // 激活状态
    const [decadalActive, setDecadalActive] = useState(false)
    const [yearlyActive, setYearlyActive] = useState(false)
    const [monthlyActive, setMonthlyActive] = useState(false)
    const [dailyActive, setDailyActive] = useState(false)
    const [hourlyActive, setHourlyActive] = useState(false)
    const [minorLimitActive, setMinorLimitActive] = useState(false)

    // 展开状态（用于显示四化详情）
    const [showDecadalMutagen, setShowDecadalMutagen] = useState(false)
    const [showYearlyMutagen, setShowYearlyMutagen] = useState(false)

    const today = useMemo(() => new Date(), [])
    const currentYear = today.getFullYear()
    const currentMonth = today.getMonth() + 1
    const currentDay = today.getDate()

    // 当前查看的年月
    const viewYear = selectedYear ?? currentYear
    const viewMonth = selectedMonth ?? currentMonth

    // 初始化 iztro 服务
    useEffect(() => {
        if (data.solarDate) {
            // 从solarDate解析时辰
            const hourBranch = data.basicInfo.fourPillars.hour.branch
            const branchToIndex: Record<string, number> = {
                '子': 0, '丑': 1, '寅': 2, '卯': 3, '辰': 4, '巳': 5,
                '午': 6, '未': 7, '申': 8, '酉': 9, '戌': 10, '亥': 11
            }
            const timeIndex = branchToIndex[hourBranch] ?? 0

            const success = ziweiHoroscopeService.initialize({
                solarDate: data.solarDate,
                timeIndex,
                gender: data.gender === 'male' ? '男' : '女'
            })
            setServiceReady(success)
        }
    }, [data.solarDate, data.basicInfo.fourPillars.hour.branch, data.gender])

    // 获取大限列表（带四化）
    const decadeList = useMemo<DecadalDetail[]>(() => {
        if (serviceReady) {
            return ziweiHoroscopeService.getDecadalList()
        }
        // 降级使用原始数据
        return data.decades?.map((d, i) => ({
            index: i,
            startAge: d.startAge,
            endAge: d.endAge,
            heavenlyStem: d.heavenlyStem,
            earthlyBranch: d.earthlyBranch,
            palaceName: d.palaceName,
            palaceIndex: d.palaceIndex
        })) || []
    }, [serviceReady, data.decades])

    // 当前大限
    const currentDecade = useMemo(() => {
        const age = currentYear - data.birthYear + 1
        return decadeList.find(d => d.startAge <= age && age <= d.endAge)
    }, [decadeList, currentYear, data.birthYear])

    // 选中的大限
    const selectedDecade = useMemo(() => {
        if (selectedDecadeIndex === null) return currentDecade
        return decadeList[selectedDecadeIndex]
    }, [selectedDecadeIndex, decadeList, currentDecade])

    // 流年列表（使用iztro精确计算）
    const yearlyList = useMemo<YearlyDetail[]>(() => {
        if (!selectedDecade) return []

        if (serviceReady) {
            return ziweiHoroscopeService.getYearlyListInDecade(selectedDecade.startAge, selectedDecade.endAge)
        }

        // 降级：简单计算
        const startYear = data.birthYear + selectedDecade.startAge - 1
        const endYear = data.birthYear + selectedDecade.endAge - 1
        const years: YearlyDetail[] = []
        const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

        for (let year = startYear; year <= endYear; year++) {
            const stemIndex = (year - 4) % 10
            const branchIndex = (year - 4) % 12
            years.push({
                year,
                heavenlyStem: stems[stemIndex],
                earthlyBranch: branches[branchIndex],
                palaceIndex: branchIndex,
                palaceName: ''
            })
        }
        return years
    }, [selectedDecade, serviceReady, data.birthYear])

    // 流月列表
    const monthlyList = useMemo<MonthlyDetail[]>(() => {
        if (serviceReady) {
            return ziweiHoroscopeService.getMonthlyList(viewYear)
        }
        // 降级
        const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        const months: MonthlyDetail[] = []

        for (let m = 1; m <= 12; m++) {
            const branchIndex = (m + 1) % 12
            months.push({
                month: m,
                heavenlyStem: stems[(m - 1) % 10],
                earthlyBranch: branches[branchIndex],
                palaceIndex: branchIndex,
                palaceName: ''
            })
        }
        return months
    }, [viewYear, serviceReady])

    // 流日列表
    const dailyList = useMemo<DailyDetail[]>(() => {
        if (serviceReady) {
            return ziweiHoroscopeService.getDailyList(viewYear, viewMonth)
        }
        // 降级
        const daysInMonth = new Date(viewYear, viewMonth, 0).getDate()
        const days: DailyDetail[] = []
        const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

        for (let d = 1; d <= daysInMonth; d++) {
            const baseDate = new Date(1900, 0, 31)
            const targetDate = new Date(viewYear, viewMonth - 1, d)
            const diffDays = Math.floor((targetDate.getTime() - baseDate.getTime()) / (1000 * 60 * 60 * 24))
            days.push({
                day: d,
                heavenlyStem: stems[(diffDays + 10) % 10],
                earthlyBranch: branches[(diffDays + 12) % 12],
                palaceIndex: (diffDays + 12) % 12,
                palaceName: ''
            })
        }
        return days
    }, [viewYear, viewMonth, serviceReady])

    // 流时列表（当选中日期时）
    const hourlyList = useMemo<HourlyDetail[]>(() => {
        if (!selectedDay || !serviceReady) return []
        return ziweiHoroscopeService.getHourlyList(viewYear, viewMonth, selectedDay)
    }, [viewYear, viewMonth, selectedDay, serviceReady])

    // 小限列表（当前大限范围内）
    const minorLimitList = useMemo<MinorLimitInfo[]>(() => {
        if (!selectedDecade || !data.palaces) return []

        const yearBranch = data.basicInfo.fourPillars.year.branch
        const gender = data.gender as 'male' | 'female'

        return MinorLimitCalculator.calculateRange(
            data.birthYear,
            data.birthYear + selectedDecade.startAge - 1,
            data.birthYear + selectedDecade.endAge - 1,
            yearBranch,
            gender,
            data.palaces
        )
    }, [selectedDecade, data.palaces, data.basicInfo.fourPillars.year.branch, data.gender, data.birthYear])

    // 当前小限
    const currentMinorLimit = useMemo(() => {
        const currentAge = currentYear - data.birthYear + 1
        return minorLimitList.find(m => m.age === currentAge)
    }, [minorLimitList, currentYear, data.birthYear])

    // 选中的小限
    const selectedMinorLimit = useMemo(() => {
        if (selectedMinorAge === null) return currentMinorLimit
        return minorLimitList.find(m => m.age === selectedMinorAge)
    }, [selectedMinorAge, minorLimitList, currentMinorLimit])

    // 更新高亮信息
    const updateHighlight = useCallback(() => {
        const highlight: HoroscopeHighlight = {}
        const info: HoroscopeInfo = {}

        if (decadalActive && selectedDecade) {
            highlight.decadalIndex = selectedDecade.palaceIndex
            info.decadal = {
                heavenlyStem: selectedDecade.heavenlyStem,
                startAge: selectedDecade.startAge,
                palaceNames: selectedDecade.palaceNames
            }
        }

        if (yearlyActive && selectedYear !== null) {
            const yearInfo = yearlyList.find(y => y.year === selectedYear)
            if (yearInfo) {
                highlight.yearlyIndex = yearInfo.palaceIndex
                info.yearly = {
                    heavenlyStem: yearInfo.heavenlyStem,
                    palaceIndex: yearInfo.palaceIndex,
                    palaceNames: yearInfo.palaceNames
                }
            }
        }

        if (monthlyActive && selectedMonth !== null) {
            const monthInfo = monthlyList.find(m => m.month === selectedMonth)
            if (monthInfo) {
                highlight.monthlyIndex = monthInfo.palaceIndex
                info.monthly = {
                    heavenlyStem: monthInfo.heavenlyStem,
                    palaceIndex: monthInfo.palaceIndex,
                    palaceNames: monthInfo.palaceNames
                }
            }
        }

        if (dailyActive && selectedDay !== null) {
            const dayInfo = dailyList.find(d => d.day === selectedDay)
            if (dayInfo) {
                highlight.dailyIndex = dayInfo.palaceIndex
                info.daily = {
                    heavenlyStem: dayInfo.heavenlyStem,
                    palaceIndex: dayInfo.palaceIndex,
                    palaceNames: dayInfo.palaceNames
                }
            }
        }

        // 流时高亮
        if (hourlyActive && selectedHour !== null) {
            const hourInfo = hourlyList.find(h => h.hour === selectedHour)
            if (hourInfo) {
                highlight.hourlyIndex = hourInfo.palaceIndex
                info.hourly = {
                    heavenlyStem: hourInfo.heavenlyStem,
                    palaceIndex: hourInfo.palaceIndex,
                    palaceNames: hourInfo.palaceNames
                }
            }
        }

        // 小限高亮
        if (minorLimitActive && selectedMinorLimit) {
            highlight.minorLimitIndex = selectedMinorLimit.palaceIndex
            info.minorLimit = {
                age: selectedMinorLimit.age,
                palaceIndex: selectedMinorLimit.palaceIndex
            }
        }

        onHighlightChange?.(highlight)
        onHoroscopeInfoChange?.(info)
    }, [
        decadalActive, yearlyActive, monthlyActive, dailyActive, hourlyActive, minorLimitActive,
        selectedDecade, selectedYear, selectedMonth, selectedDay, selectedHour, selectedMinorLimit,
        yearlyList, monthlyList, dailyList, hourlyList,
        onHighlightChange, onHoroscopeInfoChange
    ])

    useEffect(() => {
        updateHighlight()
    }, [updateHighlight])

    // 处理大限选择
    const handleDecadeSelect = (index: number) => {
        if (selectedDecadeIndex === index && decadalActive) {
            setDecadalActive(false)
            setSelectedDecadeIndex(null)
            // 清除下级选择
            setYearlyActive(false)
            setSelectedYear(null)
            setMonthlyActive(false)
            setSelectedMonth(null)
            setDailyActive(false)
            setSelectedDay(null)
        } else {
            setSelectedDecadeIndex(index)
            setDecadalActive(true)
        }
    }

    // 处理流年选择
    const handleYearSelect = (year: number) => {
        if (selectedYear === year && yearlyActive) {
            setYearlyActive(false)
            setSelectedYear(null)
            setMonthlyActive(false)
            setSelectedMonth(null)
            setDailyActive(false)
            setSelectedDay(null)
        } else {
            setSelectedYear(year)
            setYearlyActive(true)
        }
    }

    // 处理流月选择
    const handleMonthSelect = (month: number) => {
        if (selectedMonth === month && monthlyActive) {
            setMonthlyActive(false)
            setSelectedMonth(null)
            setDailyActive(false)
            setSelectedDay(null)
        } else {
            setSelectedMonth(month)
            setMonthlyActive(true)
        }
    }

    // 处理流日选择
    const handleDaySelect = (day: number) => {
        if (selectedDay === day && dailyActive) {
            setDailyActive(false)
            setSelectedDay(null)
            setHourlyActive(false)
            setSelectedHour(null)
        } else {
            setSelectedDay(day)
            setDailyActive(true)
        }
    }

    // 处理流时选择
    const handleHourSelect = (hour: number) => {
        if (selectedHour === hour && hourlyActive) {
            setHourlyActive(false)
            setSelectedHour(null)
        } else {
            setSelectedHour(hour)
            setHourlyActive(true)
        }
    }

    // 处理小限选择
    const handleMinorLimitSelect = (age: number) => {
        if (selectedMinorAge === age && minorLimitActive) {
            setMinorLimitActive(false)
            setSelectedMinorAge(null)
        } else {
            setSelectedMinorAge(age)
            setMinorLimitActive(true)
        }
    }

    // 获取选中流年的详细信息
    const selectedYearlyDetail = useMemo(() => {
        if (!selectedYear) return null
        return yearlyList.find(y => y.year === selectedYear) || null
    }, [selectedYear, yearlyList])

    // 处理中宫快捷日期切换（供外部调用）
    const handleDateChange = useCallback((scope: HoroscopeScope, delta: number) => {
        const currentYear = new Date().getFullYear()

        switch (scope) {
            case 'decadal': {
                // 大限切换：delta 为 ±10 年
                const newYear = (selectedYear || currentYear) + delta
                const newDecadeIndex = decadeList.findIndex(d =>
                    newYear >= (data.birthYear || 2000) + d.startAge - 1 &&
                    newYear <= (data.birthYear || 2000) + d.endAge - 1
                )
                if (newDecadeIndex >= 0) {
                    setSelectedDecadeIndex(newDecadeIndex)
                    setDecadalActive(true)
                    // 同时更新流年
                    setSelectedYear(newYear)
                    setYearlyActive(true)
                }
                break
            }
            case 'yearly': {
                // 流年切换
                const newYear = (selectedYear || currentYear) + delta
                if (newYear >= (data.birthYear || 1900) && newYear <= currentYear + 10) {
                    setSelectedYear(newYear)
                    setYearlyActive(true)
                    // 重置下级
                    setSelectedMonth(null)
                    setSelectedDay(null)
                    setSelectedHour(null)
                }
                break
            }
            case 'monthly': {
                // 流月切换
                let newMonth = (selectedMonth || new Date().getMonth() + 1) + delta
                let year = selectedYear || currentYear
                if (newMonth > 12) { newMonth = 1; year++ }
                if (newMonth < 1) { newMonth = 12; year-- }
                setSelectedYear(year)
                setSelectedMonth(newMonth)
                setYearlyActive(true)
                setMonthlyActive(true)
                setSelectedDay(null)
                setSelectedHour(null)
                break
            }
            case 'daily': {
                // 流日切换
                const today = new Date()
                const baseDate = selectedDay
                    ? new Date(selectedYear || today.getFullYear(), (selectedMonth || today.getMonth() + 1) - 1, selectedDay)
                    : today
                baseDate.setDate(baseDate.getDate() + delta)
                setSelectedYear(baseDate.getFullYear())
                setSelectedMonth(baseDate.getMonth() + 1)
                setSelectedDay(baseDate.getDate())
                setYearlyActive(true)
                setMonthlyActive(true)
                setDailyActive(true)
                setSelectedHour(null)
                break
            }
            case 'hourly': {
                // 流时切换 (0-11 时辰索引)
                let newHour = (selectedHour ?? Math.floor(new Date().getHours() / 2)) + delta
                if (newHour > 11) newHour = 0
                if (newHour < 0) newHour = 11
                setSelectedHour(newHour)
                setHourlyActive(true)
                break
            }
        }

        // 通知外部
        onDateChange?.(scope, delta)
    }, [selectedYear, selectedMonth, selectedDay, selectedHour, decadeList, data.birthYear, onDateChange])

    // 通过 ref 暴露日期切换方法供外部使用（替代 window 全局对象）
    useImperativeHandle(ref, () => ({
        handleDateChange
    }), [handleDateChange])

    return (
        <div className="space-y-3">
            {/* 大限 */}
            <div className="rounded-lg border border-border overflow-hidden">
                <SectionHeader
                    title={t('ziwei.horoscopePanel.decadal')}
                    color="bg-purple-500"
                    isActive={decadalActive}
                    onToggle={() => {
                        if (decadalActive) {
                            setDecadalActive(false)
                            setSelectedDecadeIndex(null)
                        } else if (currentDecade) {
                            setDecadalActive(true)
                            setSelectedDecadeIndex(decadeList.indexOf(currentDecade))
                        }
                    }}
                    subtitle={currentDecade ? `${t('ziwei.horoscopePanel.currentAge')}：${currentDecade.startAge}-${currentDecade.endAge}${t('ziwei.horoscopePanel.age')}` : undefined}
                />
                <div className="p-3 bg-background">
                    <div className="flex gap-2 overflow-x-auto pb-2">
                        {decadeList.slice(0, 10).map((decade, index) => {
                            const isSelected = decadalActive && selectedDecadeIndex === index
                            const isCurrent = decade === currentDecade
                            return (
                                <button
                                    key={index}
                                    onClick={() => handleDecadeSelect(index)}
                                    className={`flex-shrink-0 p-2 rounded-lg text-center transition-all min-w-[60px] ${isSelected
                                        ? 'bg-purple-500 text-white shadow-md'
                                        : isCurrent
                                            ? 'bg-purple-100 dark:bg-purple-900/30 border-2 border-purple-400'
                                            : 'bg-secondary/50 border border-border hover:border-purple-300'
                                        }`}
                                >
                                    <div className="text-sm font-bold flex flex-col items-center leading-tight">
                                        <span className={isSelected ? '' : getStemColor(decade.heavenlyStem)}>
                                            {decade.heavenlyStem}
                                        </span>
                                        <span className={isSelected ? '' : getBranchColor(decade.earthlyBranch)}>
                                            {decade.earthlyBranch}
                                        </span>
                                    </div>
                                    <div className={`text-[10px] ${isSelected ? 'text-white/90' : 'text-muted-foreground'}`}>
                                        {decade.palaceName}
                                    </div>
                                    <div className={`text-[10px] ${isSelected ? 'text-white/70' : 'text-muted-foreground'}`}>
                                        {decade.startAge}{t('ziwei.horoscopePanel.age')}
                                    </div>
                                </button>
                            )
                        })}
                    </div>

                    {/* 大限四化显示 */}
                    {decadalActive && selectedDecade?.mutagen && (
                        <div className="mt-2 p-2 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                            <div className="flex items-center justify-between mb-1">
                                <span className="text-xs font-medium text-purple-700 dark:text-purple-300">
                                    {t('ziwei.mutagen.decadal')} ({selectedDecade.heavenlyStem})
                                </span>
                                <button
                                    onClick={() => setShowDecadalMutagen(!showDecadalMutagen)}
                                    className="text-[10px] text-purple-500"
                                >
                                    {showDecadalMutagen ? t('ziwei.horoscopePanel.collapse') : t('ziwei.horoscopePanel.expand')}
                                </button>
                            </div>
                            {showDecadalMutagen ? (
                                <MutagenBadge mutagen={selectedDecade.mutagen} />
                            ) : (
                                <MutagenBadge mutagen={selectedDecade.mutagen} compact />
                            )}
                        </div>
                    )}
                </div>
            </div>

            {/* 流年 */}
            <div className="rounded-lg border border-border overflow-hidden">
                <SectionHeader
                    title={t('ziwei.horoscopePanel.yearly')}
                    color="bg-blue-500"
                    isActive={yearlyActive}
                    onToggle={() => {
                        if (yearlyActive) {
                            setYearlyActive(false)
                            setSelectedYear(null)
                        } else {
                            setYearlyActive(true)
                            setSelectedYear(currentYear)
                        }
                    }}
                    subtitle={selectedDecade ? `${selectedDecade.startAge}${t('ziwei.horoscopePanel.age')} ${t('ziwei.horoscopePanel.decadal')}` : undefined}
                />
                <div className="p-3 bg-background">
                    {yearlyList.length > 0 ? (
                        <>
                            <div className="flex gap-2 overflow-x-auto pb-2">
                                {yearlyList.map((yearInfo) => {
                                    const isSelected = yearlyActive && selectedYear === yearInfo.year
                                    const isCurrent = yearInfo.year === currentYear
                                    return (
                                        <button
                                            key={yearInfo.year}
                                            onClick={() => handleYearSelect(yearInfo.year)}
                                            className={`flex-shrink-0 p-2 rounded-lg text-center transition-all min-w-[55px] ${isSelected
                                                ? 'bg-blue-500 text-white shadow-md'
                                                : isCurrent
                                                    ? 'bg-blue-100 dark:bg-blue-900/30 border-2 border-blue-400'
                                                    : 'bg-secondary/50 border border-border hover:border-blue-300'
                                                }`}
                                        >
                                            <div className="text-sm font-bold flex flex-col items-center leading-tight">
                                                <span className={isSelected ? '' : getStemColor(yearInfo.heavenlyStem)}>
                                                    {yearInfo.heavenlyStem}
                                                </span>
                                                <span className={isSelected ? '' : getBranchColor(yearInfo.earthlyBranch)}>
                                                    {yearInfo.earthlyBranch}
                                                </span>
                                            </div>
                                            <div className={`text-[10px] ${isSelected ? 'text-white/90' : 'text-muted-foreground'}`}>
                                                {yearInfo.year}
                                            </div>
                                        </button>
                                    )
                                })}
                            </div>

                            {/* 流年四化显示 */}
                            {yearlyActive && selectedYearlyDetail?.mutagen && (
                                <div className="mt-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                                    <div className="flex items-center justify-between mb-1">
                                        <span className="text-xs font-medium text-blue-700 dark:text-blue-300">
                                            {t('ziwei.mutagen.yearly')} ({selectedYearlyDetail.heavenlyStem})
                                        </span>
                                        <button
                                            onClick={() => setShowYearlyMutagen(!showYearlyMutagen)}
                                            className="text-[10px] text-blue-500"
                                        >
                                            {showYearlyMutagen ? t('ziwei.horoscopePanel.collapse') : t('ziwei.horoscopePanel.expand')}
                                        </button>
                                    </div>
                                    {showYearlyMutagen ? (
                                        <MutagenBadge mutagen={selectedYearlyDetail.mutagen} />
                                    ) : (
                                        <MutagenBadge mutagen={selectedYearlyDetail.mutagen} compact />
                                    )}
                                </div>
                            )}
                        </>
                    ) : (
                        <div className="text-xs text-muted-foreground text-center py-2">
                            {t('ziwei.horoscopePanel.selectDecadal')}
                        </div>
                    )}
                </div>
            </div>

            {/* 流月 */}
            <div className="rounded-lg border border-border overflow-hidden">
                <SectionHeader
                    title={t('ziwei.horoscopePanel.monthly')}
                    color="bg-green-500"
                    isActive={monthlyActive}
                    onToggle={() => {
                        if (monthlyActive) {
                            setMonthlyActive(false)
                            setSelectedMonth(null)
                        } else {
                            setMonthlyActive(true)
                            setSelectedMonth(currentMonth)
                        }
                    }}
                    subtitle={`${viewYear}年`}
                />
                <div className="p-3 bg-background">
                    <div className="flex gap-2 overflow-x-auto pb-2">
                        {monthlyList.map((monthInfo) => {
                            const isSelected = monthlyActive && selectedMonth === monthInfo.month
                            const isCurrent = monthInfo.month === currentMonth && viewYear === currentYear
                            return (
                                <button
                                    key={monthInfo.month}
                                    onClick={() => handleMonthSelect(monthInfo.month)}
                                    className={`flex-shrink-0 p-2 rounded-lg text-center transition-all min-w-[50px] ${isSelected
                                        ? 'bg-green-500 text-white shadow-md'
                                        : isCurrent
                                            ? 'bg-green-100 dark:bg-green-900/30 border-2 border-green-400'
                                            : 'bg-secondary/50 border border-border hover:border-green-300'
                                        }`}
                                >
                                    <div className="text-sm font-bold flex flex-col items-center leading-tight">
                                        <span className={isSelected ? '' : getStemColor(monthInfo.heavenlyStem)}>
                                            {monthInfo.heavenlyStem}
                                        </span>
                                        <span className={isSelected ? '' : getBranchColor(monthInfo.earthlyBranch)}>
                                            {monthInfo.earthlyBranch}
                                        </span>
                                    </div>
                                    <div className={`text-[10px] ${isSelected ? 'text-white/90' : 'text-muted-foreground'}`}>
                                        {monthInfo.month}月
                                    </div>
                                </button>
                            )
                        })}
                    </div>
                </div>
            </div>

            {/* 流日 */}
            <div className="rounded-lg border border-border overflow-hidden">
                <SectionHeader
                    title={t('ziwei.horoscopePanel.daily')}
                    color="bg-orange-500"
                    isActive={dailyActive}
                    onToggle={() => {
                        if (dailyActive) {
                            setDailyActive(false)
                            setSelectedDay(null)
                        } else {
                            setDailyActive(true)
                            setSelectedDay(currentDay)
                        }
                    }}
                    subtitle={`${viewYear}年${viewMonth}月`}
                />
                <div className="p-3 bg-background">
                    <div className="grid grid-cols-7 gap-1">
                        {dailyList.map((dayInfo) => {
                            const isSelected = dailyActive && selectedDay === dayInfo.day
                            const isCurrent = dayInfo.day === currentDay && viewMonth === currentMonth && viewYear === currentYear
                            return (
                                <button
                                    key={dayInfo.day}
                                    onClick={() => handleDaySelect(dayInfo.day)}
                                    className={`p-1 rounded text-center transition-all ${isSelected
                                        ? 'bg-orange-500 text-white shadow-md'
                                        : isCurrent
                                            ? 'bg-orange-100 dark:bg-orange-900/30 border-2 border-orange-400'
                                            : 'bg-secondary/50 border border-border hover:border-orange-300'
                                        }`}
                                >
                                    <div className="text-xs font-bold flex flex-col items-center leading-tight">
                                        <span className={isSelected ? '' : getStemColor(dayInfo.heavenlyStem)}>
                                            {dayInfo.heavenlyStem}
                                        </span>
                                        <span className={isSelected ? '' : getBranchColor(dayInfo.earthlyBranch)}>
                                            {dayInfo.earthlyBranch}
                                        </span>
                                    </div>
                                    <div className={`text-[9px] ${isSelected ? 'text-white/90' : 'text-muted-foreground'}`}>
                                        {dayInfo.day}日
                                    </div>
                                </button>
                            )
                        })}
                    </div>
                </div>
            </div>

            {/* 流时 - 选择流年后即可显示 */}
            {selectedYear && yearlyActive && (
                <div className="rounded-lg border border-border overflow-hidden">
                    <SectionHeader
                        title={t('ziwei.horoscopePanel.hourly')}
                        color="bg-cyan-500"
                        isActive={hourlyActive}
                        onToggle={() => {
                            if (hourlyActive) {
                                setHourlyActive(false)
                                setSelectedHour(null)
                            } else {
                                const currentHour = Math.floor(new Date().getHours() / 2) % 12
                                setHourlyActive(true)
                                setSelectedHour(currentHour)
                            }
                        }}
                        subtitle={`${viewYear}年${viewMonth}月${selectedDay}日`}
                    />
                    <div className="p-3 bg-background">
                        <div className="grid grid-cols-6 gap-1">
                            {hourlyList.map((hourInfo) => {
                                const isSelected = hourlyActive && selectedHour === hourInfo.hour
                                const currentHour = Math.floor(new Date().getHours() / 2) % 12
                                const isCurrent = hourInfo.hour === currentHour && selectedDay === currentDay && viewMonth === currentMonth && viewYear === currentYear
                                return (
                                    <button
                                        key={hourInfo.hour}
                                        onClick={() => handleHourSelect(hourInfo.hour)}
                                        className={`p-1.5 rounded text-center transition-all ${isSelected
                                            ? 'bg-cyan-500 text-white shadow-md'
                                            : isCurrent
                                                ? 'bg-cyan-100 dark:bg-cyan-900/30 border-2 border-cyan-400'
                                                : 'bg-secondary/50 border border-border hover:border-cyan-300'
                                            }`}
                                    >
                                        <div className="text-xs font-bold flex flex-col items-center leading-tight">
                                            <span className={isSelected ? '' : getStemColor(hourInfo.heavenlyStem)}>
                                                {hourInfo.heavenlyStem}
                                            </span>
                                            <span className={isSelected ? '' : getBranchColor(hourInfo.earthlyBranch)}>
                                                {hourInfo.earthlyBranch}
                                            </span>
                                        </div>
                                        <div className={`text-[9px] ${isSelected ? 'text-white/90' : 'text-muted-foreground'}`}>
                                            {hourInfo.hourName}时
                                        </div>
                                    </button>
                                )
                            })}
                        </div>
                        {hourlyList.length === 0 && (
                            <div className="text-center text-muted-foreground text-sm py-2">
                                加载流时数据中...
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* 小限 */}
            <div className="rounded-lg border border-border overflow-hidden">
                <SectionHeader
                    title="小限"
                    color="bg-pink-500"
                    isActive={minorLimitActive}
                    onToggle={() => {
                        if (minorLimitActive) {
                            setMinorLimitActive(false)
                            setSelectedMinorAge(null)
                        } else if (currentMinorLimit) {
                            setMinorLimitActive(true)
                            setSelectedMinorAge(currentMinorLimit.age)
                        }
                    }}
                    subtitle={selectedDecade ? `${selectedDecade.startAge}-${selectedDecade.endAge}岁` : '请先选大限'}
                />
                <div className="p-3 bg-background">
                    {minorLimitList.length > 0 ? (
                        <div className="flex gap-2 overflow-x-auto pb-2">
                            {minorLimitList.map((minor) => {
                                const isSelected = minorLimitActive && selectedMinorAge === minor.age
                                const isCurrent = minor === currentMinorLimit
                                return (
                                    <button
                                        key={minor.age}
                                        onClick={() => handleMinorLimitSelect(minor.age)}
                                        className={`flex-shrink-0 p-2 rounded-lg text-center transition-all min-w-[55px] ${isSelected
                                            ? 'bg-pink-500 text-white shadow-md'
                                            : isCurrent
                                                ? 'bg-pink-100 dark:bg-pink-900/30 border-2 border-pink-400'
                                                : 'bg-secondary/50 border border-border hover:border-pink-300'
                                            }`}
                                    >
                                        <div className="text-sm font-bold flex flex-col items-center leading-tight">
                                            <span className={isSelected ? '' : getStemColor(minor.heavenlyStem)}>
                                                {minor.heavenlyStem}
                                            </span>
                                            <span className={isSelected ? '' : getBranchColor(minor.earthlyBranch)}>
                                                {minor.earthlyBranch}
                                            </span>
                                        </div>
                                        <div className={`text-[10px] ${isSelected ? 'text-white/90' : 'text-muted-foreground'}`}>
                                            {minor.age}岁
                                        </div>
                                        <div className={`text-[9px] ${isSelected ? 'text-white/70' : 'text-muted-foreground/70'}`}>
                                            {minor.year}
                                        </div>
                                    </button>
                                )
                            })}
                        </div>
                    ) : (
                        <div className="text-xs text-muted-foreground text-center py-2">
                            请先选择大限查看对应小限
                        </div>
                    )}

                    {/* 小限宫位信息 */}
                    {minorLimitActive && selectedMinorLimit && (
                        <div className="mt-2 p-2 bg-pink-50 dark:bg-pink-900/20 rounded-lg">
                            <div className="text-xs text-pink-700 dark:text-pink-300">
                                <span className="font-medium">{selectedMinorLimit.age}岁小限</span>
                                <span className="ml-2">
                                    在 <span className="font-bold">{data.palaces[selectedMinorLimit.palaceIndex]?.name || ''}</span> 宫
                                </span>
                                <span className="ml-2 text-pink-500">
                                    ({selectedMinorLimit.heavenlyStem}{selectedMinorLimit.earthlyBranch}年)
                                </span>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* 图例说明 */}
            <div className="p-3 bg-secondary/30 rounded-lg">
                <div className="text-xs text-muted-foreground mb-2">颜色说明</div>
                <div className="flex flex-wrap gap-3 text-xs">
                    <span className="flex items-center gap-1">
                        <span className="w-3 h-3 rounded bg-purple-500"></span>
                        大限
                    </span>
                    <span className="flex items-center gap-1">
                        <span className="w-3 h-3 rounded bg-pink-500"></span>
                        小限
                    </span>
                    <span className="flex items-center gap-1">
                        <span className="w-3 h-3 rounded bg-blue-500"></span>
                        流年
                    </span>
                    <span className="flex items-center gap-1">
                        <span className="w-3 h-3 rounded bg-green-500"></span>
                        流月
                    </span>
                    <span className="flex items-center gap-1">
                        <span className="w-3 h-3 rounded bg-orange-500"></span>
                        流日
                    </span>
                </div>
                <div className="flex flex-wrap gap-2 mt-2 text-xs">
                    <span className="flex items-center gap-1">
                        <span className="px-1 bg-green-500/20 text-green-600 rounded text-[9px]">禄</span>
                        化禄
                    </span>
                    <span className="flex items-center gap-1">
                        <span className="px-1 bg-red-500/20 text-red-600 rounded text-[9px]">权</span>
                        化权
                    </span>
                    <span className="flex items-center gap-1">
                        <span className="px-1 bg-blue-500/20 text-blue-600 rounded text-[9px]">科</span>
                        化科
                    </span>
                    <span className="flex items-center gap-1">
                        <span className="px-1 bg-purple-500/20 text-purple-600 rounded text-[9px]">忌</span>
                        化忌
                    </span>
                </div>
            </div>
        </div>
    )
})
