/**
 * 八字大运流年面板
 * 显示大运和对应的10个流年
 */

import { useState, useMemo } from 'react'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, ChevronUp, Calendar, Star, TrendingUp } from 'lucide-react'
import { cn } from '@/lib/utils'

// 天干地支
const STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
const BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

// 五行颜色
const WUXING_COLORS: Record<string, string> = {
    '木': 'text-green-500',
    '火': 'text-red-500',
    '土': 'text-amber-500',
    '金': 'text-yellow-400',
    '水': 'text-blue-500',
}

// 天干五行
const STEM_WUXING: Record<string, string> = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
}

// 地支五行
const BRANCH_WUXING: Record<string, string> = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
    '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
    '戌': '土', '亥': '水',
}

interface DaYun {
    ganZhi: string
    startAge: number
    endAge: number
    startYear: number
}

interface DaYunYearlyPanelProps {
    birthYear: number
    startAge?: number  // 起运年龄，默认根据性别和日干计算
    gender?: 'male' | 'female'
    dayMaster?: string  // 日主
}

// 计算年份的干支
function getYearGanZhi(year: number): string {
    const stemIndex = (year - 4) % 10
    const branchIndex = (year - 4) % 12
    return STEMS[stemIndex] + BRANCHES[branchIndex]
}

// 计算大运
function calculateDaYun(
    birthYear: number,
    startAge: number = 5,
    count: number = 8
): DaYun[] {
    const result: DaYun[] = []
    
    // 简化计算：根据出生年份推算
    // 实际应用需要根据月柱和性别/日干阴阳来确定大运顺逆
    const birthGanZhi = getYearGanZhi(birthYear)
    const birthStemIndex = STEMS.indexOf(birthGanZhi[0])
    const birthBranchIndex = BRANCHES.indexOf(birthGanZhi[1])
    
    for (let i = 0; i < count; i++) {
        const age = startAge + i * 10
        const stemIndex = (birthStemIndex + i + 1) % 10
        const branchIndex = (birthBranchIndex + i + 1) % 12
        
        result.push({
            ganZhi: STEMS[stemIndex] + BRANCHES[branchIndex],
            startAge: age,
            endAge: age + 9,
            startYear: birthYear + age - 1,
        })
    }
    
    return result
}

// 计算流年
function calculateLiuNian(startYear: number, count: number = 10): { year: number; ganZhi: string }[] {
    const result: { year: number; ganZhi: string }[] = []
    
    for (let i = 0; i < count; i++) {
        const year = startYear + i
        result.push({
            year,
            ganZhi: getYearGanZhi(year),
        })
    }
    
    return result
}

export function DaYunYearlyPanel({
    birthYear,
    startAge = 5,
    gender = 'male',
    dayMaster,
}: DaYunYearlyPanelProps) {
    const { i18n } = useTranslation()
    const isEnglish = i18n.language === 'en'
    
    const [expandedDaYun, setExpandedDaYun] = useState<number | null>(null)
    const currentYear = new Date().getFullYear()
    const currentAge = currentYear - birthYear + 1
    
    // 计算大运列表
    const daYunList = useMemo(() => 
        calculateDaYun(birthYear, startAge, 8),
        [birthYear, startAge]
    )
    
    // 当前大运
    const currentDaYun = useMemo(() => 
        daYunList.find(d => d.startAge <= currentAge && currentAge <= d.endAge),
        [daYunList, currentAge]
    )
    
    // 自动展开当前大运
    useState(() => {
        if (currentDaYun) {
            const idx = daYunList.indexOf(currentDaYun)
            if (idx >= 0) setExpandedDaYun(idx)
        }
    })
    
    const toggleExpand = (index: number) => {
        setExpandedDaYun(expandedDaYun === index ? null : index)
    }
    
    return (
        <div className="flat-card p-4 mb-4 bg-card border border-border">
            <h3 className="text-lg font-semibold mb-3 text-foreground flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                {isEnglish ? 'Fortune Periods & Yearly Fortune' : '大运流年'}
            </h3>
            
            <div className="text-xs text-muted-foreground mb-4 flex items-center gap-4">
                <span>
                    <Calendar className="w-3 h-3 inline mr-1" />
                    {isEnglish ? `Current Age: ${currentAge}` : `虚岁：${currentAge}岁`}
                </span>
                {currentDaYun && (
                    <span>
                        <Star className="w-3 h-3 inline mr-1" />
                        {isEnglish ? `Current Period: ${currentDaYun.ganZhi}` : `当前大运：${currentDaYun.ganZhi}`}
                    </span>
                )}
            </div>
            
            {/* 大运列表 */}
            <div className="space-y-2">
                {daYunList.map((daYun, index) => {
                    const isExpanded = expandedDaYun === index
                    const isCurrent = currentDaYun === daYun
                    const liuNianList = calculateLiuNian(daYun.startYear, 10)
                    const stem = daYun.ganZhi[0]
                    const branch = daYun.ganZhi[1]
                    const stemWuxing = STEM_WUXING[stem]
                    const branchWuxing = BRANCH_WUXING[branch]
                    
                    return (
                        <div
                            key={index}
                            className={cn(
                                'border rounded-lg overflow-hidden transition-colors',
                                isCurrent ? 'border-primary bg-primary/5' : 'border-border'
                            )}
                        >
                            {/* 大运标题栏 */}
                            <button
                                onClick={() => toggleExpand(index)}
                                className={cn(
                                    'w-full px-4 py-3 flex items-center justify-between text-left transition-colors',
                                    isExpanded ? 'bg-secondary' : 'hover:bg-secondary/50'
                                )}
                            >
                                <div className="flex items-center gap-4">
                                    <div className="text-center min-w-[60px]">
                                        <div className={cn('text-xl font-bold', WUXING_COLORS[stemWuxing])}>
                                            {stem}
                                        </div>
                                        <div className={cn('text-xl font-bold', WUXING_COLORS[branchWuxing])}>
                                            {branch}
                                        </div>
                                    </div>
                                    <div>
                                        <div className="text-sm font-medium">
                                            {daYun.startAge}-{daYun.endAge}{isEnglish ? ' yrs' : '岁'}
                                        </div>
                                        <div className="text-xs text-muted-foreground">
                                            {daYun.startYear}-{daYun.startYear + 9}
                                        </div>
                                    </div>
                                    {isCurrent && (
                                        <span className="text-xs px-2 py-0.5 rounded bg-primary text-primary-foreground">
                                            {isEnglish ? 'Current' : '当前'}
                                        </span>
                                    )}
                                </div>
                                
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <span className="text-xs">
                                        {isEnglish ? 'View yearly' : '查看流年'}
                                    </span>
                                    {isExpanded ? (
                                        <ChevronUp className="w-4 h-4" />
                                    ) : (
                                        <ChevronDown className="w-4 h-4" />
                                    )}
                                </div>
                            </button>
                            
                            {/* 流年展开内容 */}
                            <AnimatePresence>
                                {isExpanded && (
                                    <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <div className="px-4 pb-4 pt-2 border-t border-border/50">
                                            <div className="text-xs text-muted-foreground mb-2">
                                                {isEnglish ? '10 Yearly Fortunes:' : '十年流年：'}
                                            </div>
                                            <div className="grid grid-cols-5 gap-2">
                                                {liuNianList.map((liuNian) => {
                                                    const lnStem = liuNian.ganZhi[0]
                                                    const lnBranch = liuNian.ganZhi[1]
                                                    const isCurrYear = liuNian.year === currentYear
                                                    const age = liuNian.year - birthYear + 1
                                                    
                                                    return (
                                                        <div
                                                            key={liuNian.year}
                                                            className={cn(
                                                                'text-center p-2 rounded border transition-colors',
                                                                isCurrYear
                                                                    ? 'border-primary bg-primary/10'
                                                                    : 'border-border/50 hover:bg-secondary/50'
                                                            )}
                                                        >
                                                            <div className="text-xs text-muted-foreground">
                                                                {liuNian.year}
                                                            </div>
                                                            <div className="font-bold">
                                                                <span className={WUXING_COLORS[STEM_WUXING[lnStem]]}>
                                                                    {lnStem}
                                                                </span>
                                                                <span className={WUXING_COLORS[BRANCH_WUXING[lnBranch]]}>
                                                                    {lnBranch}
                                                                </span>
                                                            </div>
                                                            <div className="text-xs text-muted-foreground">
                                                                {age}{isEnglish ? 'y' : '岁'}
                                                            </div>
                                                        </div>
                                                    )
                                                })}
                                            </div>
                                        </div>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </div>
                    )
                })}
            </div>
            
            <div className="mt-3 text-xs text-muted-foreground text-center">
                💡 {isEnglish 
                    ? 'Click each period to view the corresponding 10 yearly fortunes'
                    : '点击大运可查看对应的10个流年'
                }
            </div>
        </div>
    )
}

export default DaYunYearlyPanel
