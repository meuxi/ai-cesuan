/**
 * 紫微斗数运限面板组件
 * 参考 MingAI-master 实现大限、流年、流月、流日选择和高亮功能
 */

import { useState, useMemo, useEffect, useCallback } from 'react'
import type { ZiweiResult, DecadeInfo } from '@/types/ziwei'
import type { HoroscopeHighlight, HoroscopeInfo } from './ZiweiChartGrid'

interface ZiweiHoroscopePanelProps {
    data: ZiweiResult
    onHighlightChange?: (highlight: HoroscopeHighlight) => void
    onHoroscopeInfoChange?: (info: HoroscopeInfo) => void
}

// 五行颜色映射
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

// 地支列表
const BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

// 天干列表
const STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

// 根据年份计算天干地支
function getYearGanZhi(year: number): { stem: string; branch: string } {
    const stemIndex = (year - 4) % 10
    const branchIndex = (year - 4) % 12
    return {
        stem: STEMS[stemIndex],
        branch: BRANCHES[branchIndex]
    }
}

// 根据月份计算天干地支（需要年干）
function getMonthGanZhi(year: number, month: number): { stem: string; branch: string } {
    const yearStem = STEMS[(year - 4) % 10]
    const yearStemIndex = STEMS.indexOf(yearStem)

    // 月支固定：正月寅、二月卯...
    const branchIndex = (month + 1) % 12

    // 月干计算：年干决定月干起始
    const monthStemStart = (yearStemIndex % 5) * 2
    const stemIndex = (monthStemStart + month - 1) % 10

    return {
        stem: STEMS[stemIndex],
        branch: BRANCHES[branchIndex]
    }
}

// 区块标题组件
function SectionHeader({
    title,
    color,
    isActive,
    onToggle
}: {
    title: string
    color: string
    isActive: boolean
    onToggle: () => void
}) {
    return (
        <button
            onClick={onToggle}
            className={`w-full py-2 px-3 flex items-center justify-between rounded-t-lg transition-colors ${isActive ? `${color} text-white` : 'bg-secondary/50 hover:bg-secondary'
                }`}
        >
            <span className="font-medium text-sm">{title}</span>
            <span className="text-xs">{isActive ? '点击取消' : '点击选择'}</span>
        </button>
    )
}

export function ZiweiHoroscopePanel({ data, onHighlightChange, onHoroscopeInfoChange }: ZiweiHoroscopePanelProps) {
    // 选中状态
    const [selectedDecadeIndex, setSelectedDecadeIndex] = useState<number | null>(null)
    const [selectedYear, setSelectedYear] = useState<number | null>(null)
    const [selectedMonth, setSelectedMonth] = useState<number | null>(null)
    const [selectedDay, setSelectedDay] = useState<number | null>(null)

    // 激活状态
    const [decadalActive, setDecadalActive] = useState(false)
    const [yearlyActive, setYearlyActive] = useState(false)
    const [monthlyActive, setMonthlyActive] = useState(false)
    const [dailyActive, setDailyActive] = useState(false)

    const today = useMemo(() => new Date(), [])
    const currentYear = today.getFullYear()
    const currentMonth = today.getMonth() + 1
    const currentDay = today.getDate()

    // 当前查看的年月
    const viewYear = selectedYear ?? currentYear
    const viewMonth = selectedMonth ?? currentMonth

    // 获取大限列表
    const decadeList = useMemo(() => data.decades || [], [data.decades])

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

    // 计算流年列表（当前大限内的年份）
    const yearlyList = useMemo(() => {
        if (!selectedDecade) return []
        const startYear = data.birthYear + selectedDecade.startAge - 1
        const endYear = data.birthYear + selectedDecade.endAge - 1
        const years: { year: number; stem: string; branch: string; palaceIndex: number }[] = []

        for (let year = startYear; year <= endYear; year++) {
            const ganZhi = getYearGanZhi(year)
            // 流年命宫位置 = 根据流年地支确定
            const branchIndex = BRANCHES.indexOf(ganZhi.branch)
            years.push({
                year,
                stem: ganZhi.stem,
                branch: ganZhi.branch,
                palaceIndex: branchIndex
            })
        }
        return years
    }, [selectedDecade, data.birthYear])

    // 计算流月列表（12个月）
    const monthlyList = useMemo(() => {
        const months: { month: number; stem: string; branch: string; palaceIndex: number }[] = []
        for (let m = 1; m <= 12; m++) {
            const ganZhi = getMonthGanZhi(viewYear, m)
            const branchIndex = BRANCHES.indexOf(ganZhi.branch)
            months.push({
                month: m,
                stem: ganZhi.stem,
                branch: ganZhi.branch,
                palaceIndex: branchIndex
            })
        }
        return months
    }, [viewYear])

    // 计算流日列表
    const dailyList = useMemo(() => {
        const daysInMonth = new Date(viewYear, viewMonth, 0).getDate()
        const days: { day: number; stem: string; branch: string; palaceIndex: number }[] = []

        for (let d = 1; d <= daysInMonth; d++) {
            // 简化的日干支计算
            const baseDate = new Date(1900, 0, 31) // 甲子日
            const targetDate = new Date(viewYear, viewMonth - 1, d)
            const diffDays = Math.floor((targetDate.getTime() - baseDate.getTime()) / (1000 * 60 * 60 * 24))
            const stemIndex = diffDays % 10
            const branchIndex = diffDays % 12

            days.push({
                day: d,
                stem: STEMS[(stemIndex + 10) % 10],
                branch: BRANCHES[(branchIndex + 12) % 12],
                palaceIndex: (branchIndex + 12) % 12
            })
        }
        return days
    }, [viewYear, viewMonth])

    // 更新高亮信息
    const updateHighlight = useCallback(() => {
        const highlight: HoroscopeHighlight = {}
        const info: HoroscopeInfo = {}

        if (decadalActive && selectedDecade) {
            highlight.decadalIndex = selectedDecade.palaceIndex
            info.decadal = {
                heavenlyStem: selectedDecade.heavenlyStem,
                startAge: selectedDecade.startAge
            }
        }

        if (yearlyActive && selectedYear !== null) {
            const yearInfo = yearlyList.find(y => y.year === selectedYear)
            if (yearInfo) {
                highlight.yearlyIndex = yearInfo.palaceIndex
                info.yearly = {
                    heavenlyStem: yearInfo.stem,
                    palaceIndex: yearInfo.palaceIndex
                }
            }
        }

        if (monthlyActive && selectedMonth !== null) {
            const monthInfo = monthlyList.find(m => m.month === selectedMonth)
            if (monthInfo) {
                highlight.monthlyIndex = monthInfo.palaceIndex
                info.monthly = {
                    heavenlyStem: monthInfo.stem,
                    palaceIndex: monthInfo.palaceIndex
                }
            }
        }

        if (dailyActive && selectedDay !== null) {
            const dayInfo = dailyList.find(d => d.day === selectedDay)
            if (dayInfo) {
                highlight.dailyIndex = dayInfo.palaceIndex
                info.daily = {
                    heavenlyStem: dayInfo.stem,
                    palaceIndex: dayInfo.palaceIndex
                }
            }
        }

        onHighlightChange?.(highlight)
        onHoroscopeInfoChange?.(info)
    }, [
        decadalActive, yearlyActive, monthlyActive, dailyActive,
        selectedDecade, selectedYear, selectedMonth, selectedDay,
        yearlyList, monthlyList, dailyList,
        onHighlightChange, onHoroscopeInfoChange
    ])

    // 状态变化时更新高亮
    useEffect(() => {
        updateHighlight()
    }, [updateHighlight])

    // 处理大限选择
    const handleDecadeSelect = (index: number) => {
        if (selectedDecadeIndex === index && decadalActive) {
            setDecadalActive(false)
            setSelectedDecadeIndex(null)
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
        } else {
            setSelectedDay(day)
            setDailyActive(true)
        }
    }

    return (
        <div className="space-y-3">
            {/* 大限 */}
            <div className="rounded-lg border border-border overflow-hidden">
                <SectionHeader
                    title="大限"
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
                />
                <div className="p-3 bg-background">
                    {currentDecade && (
                        <div className="text-xs text-muted-foreground mb-2">
                            当前: {currentDecade.palaceName} ({currentDecade.startAge}-{currentDecade.endAge}岁)
                        </div>
                    )}
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
                                                ? 'bg-purple-100 dark:bg-purple-900/30 border border-purple-300'
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
                                        {decade.startAge}岁
                                    </div>
                                </button>
                            )
                        })}
                    </div>
                </div>
            </div>

            {/* 流年 */}
            <div className="rounded-lg border border-border overflow-hidden">
                <SectionHeader
                    title="流年"
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
                />
                <div className="p-3 bg-background">
                    <div className="text-xs text-muted-foreground mb-2">
                        {selectedDecade ? `${selectedDecade.startAge}岁 大限内的流年` : '选择大限查看流年'}
                    </div>
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
                                                ? 'bg-blue-100 dark:bg-blue-900/30 border border-blue-300'
                                                : 'bg-secondary/50 border border-border hover:border-blue-300'
                                        }`}
                                >
                                    <div className="text-sm font-bold flex flex-col items-center leading-tight">
                                        <span className={isSelected ? '' : getStemColor(yearInfo.stem)}>
                                            {yearInfo.stem}
                                        </span>
                                        <span className={isSelected ? '' : getBranchColor(yearInfo.branch)}>
                                            {yearInfo.branch}
                                        </span>
                                    </div>
                                    <div className={`text-[10px] ${isSelected ? 'text-white/90' : 'text-muted-foreground'}`}>
                                        {yearInfo.year}
                                    </div>
                                </button>
                            )
                        })}
                    </div>
                </div>
            </div>

            {/* 流月 */}
            <div className="rounded-lg border border-border overflow-hidden">
                <SectionHeader
                    title="流月"
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
                />
                <div className="p-3 bg-background">
                    <div className="text-xs text-muted-foreground mb-2">
                        {viewYear}年 12个月
                    </div>
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
                                                ? 'bg-green-100 dark:bg-green-900/30 border border-green-300'
                                                : 'bg-secondary/50 border border-border hover:border-green-300'
                                        }`}
                                >
                                    <div className="text-sm font-bold flex flex-col items-center leading-tight">
                                        <span className={isSelected ? '' : getStemColor(monthInfo.stem)}>
                                            {monthInfo.stem}
                                        </span>
                                        <span className={isSelected ? '' : getBranchColor(monthInfo.branch)}>
                                            {monthInfo.branch}
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
                    title="流日"
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
                />
                <div className="p-3 bg-background">
                    <div className="text-xs text-muted-foreground mb-2">
                        {viewYear}年{viewMonth}月 {dailyList.length}天
                    </div>
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
                                                ? 'bg-orange-100 dark:bg-orange-900/30 border border-orange-300'
                                                : 'bg-secondary/50 border border-border hover:border-orange-300'
                                        }`}
                                >
                                    <div className="text-xs font-bold flex flex-col items-center leading-tight">
                                        <span className={isSelected ? '' : getStemColor(dayInfo.stem)}>
                                            {dayInfo.stem}
                                        </span>
                                        <span className={isSelected ? '' : getBranchColor(dayInfo.branch)}>
                                            {dayInfo.branch}
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

            {/* 图例说明 */}
            <div className="p-3 bg-secondary/30 rounded-lg">
                <div className="text-xs text-muted-foreground mb-2">颜色说明</div>
                <div className="flex flex-wrap gap-2 text-xs">
                    <span className="flex items-center gap-1">
                        <span className="w-3 h-3 rounded bg-purple-500"></span>
                        大限
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
            </div>
        </div>
    )
}
