/**
 * 运限对比面板
 * 支持多流年/多大限对比分析
 * 参考 mingpan 实现
 */

import { useState, useMemo } from 'react'
import { Plus, X, ArrowLeftRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
import type { ZiweiResult, EnhancedPalace } from '@/types/ziwei'
import { YearlyCalculator } from '@/services/ziwei/YearlyCalculator'
import { MutagenCore } from '@/services/ziwei/MutagenCore'

interface HoroscopeComparePanelProps {
    data: ZiweiResult
    onHighlight?: (palaceIndexes: number[]) => void
}

interface CompareItem {
    id: string
    type: 'yearly' | 'decade'
    year?: number
    decadeIndex?: number
    heavenlyStem: string
    earthlyBranch: string
    palaceIndex: number
    palaceName: string
    mutagen: { lu: string; quan: string; ke: string; ji: string }
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

// 四化徽章
function MutagenBadges({ mutagen }: { mutagen: { lu: string; quan: string; ke: string; ji: string } }) {
    const items = [
        { key: 'lu', label: '禄', star: mutagen.lu, color: 'bg-green-500/20 text-green-600' },
        { key: 'quan', label: '权', star: mutagen.quan, color: 'bg-red-500/20 text-red-600' },
        { key: 'ke', label: '科', star: mutagen.ke, color: 'bg-blue-500/20 text-blue-600' },
        { key: 'ji', label: '忌', star: mutagen.ji, color: 'bg-purple-500/20 text-purple-600' },
    ]

    return (
        <div className="grid grid-cols-2 gap-1 text-[10px]">
            {items.map(item => (
                <div key={item.key} className={`px-1.5 py-0.5 rounded ${item.color}`}>
                    <span className="font-medium">{item.label}</span>
                    <span className="ml-1">{item.star || '-'}</span>
                </div>
            ))}
        </div>
    )
}

// 对比项卡片
function CompareItemCard({
    item,
    onRemove,
    palaces
}: {
    item: CompareItem
    onRemove: () => void
    palaces: EnhancedPalace[]
}) {
    const palace = palaces[item.palaceIndex]

    return (
        <Card className="relative min-w-[180px] flex-shrink-0">
            <button
                onClick={onRemove}
                className="absolute top-1 right-1 p-1 rounded-full hover:bg-destructive/10 text-muted-foreground hover:text-destructive"
            >
                <X className="w-3 h-3" />
            </button>

            <CardHeader className="p-3 pb-2">
                <CardTitle className="text-sm flex items-center gap-2">
                    <Badge variant={item.type === 'yearly' ? 'default' : 'secondary'} className="text-xs">
                        {item.type === 'yearly' ? '流年' : '大限'}
                    </Badge>
                    <span className={getStemColor(item.heavenlyStem)}>{item.heavenlyStem}</span>
                    <span className={getBranchColor(item.earthlyBranch)}>{item.earthlyBranch}</span>
                    {item.year && <span className="text-muted-foreground text-xs">({item.year})</span>}
                </CardTitle>
            </CardHeader>

            <CardContent className="p-3 pt-0 space-y-2">
                <div className="text-xs">
                    <span className="text-muted-foreground">命宫：</span>
                    <span className="font-medium">{palace?.name || item.palaceName}</span>
                </div>

                <div>
                    <div className="text-xs text-muted-foreground mb-1">四化</div>
                    <MutagenBadges mutagen={item.mutagen} />
                </div>
            </CardContent>
        </Card>
    )
}

export function HoroscopeComparePanel({ data, onHighlight }: HoroscopeComparePanelProps) {
    const [compareItems, setCompareItems] = useState<CompareItem[]>([])
    const [showYearPicker, setShowYearPicker] = useState(false)

    const currentYear = new Date().getFullYear()

    // 可选年份范围
    const yearOptions = useMemo(() => {
        const years: number[] = []
        for (let y = currentYear - 5; y <= currentYear + 10; y++) {
            years.push(y)
        }
        return years
    }, [currentYear])

    // 添加流年对比项
    const addYearlyItem = (year: number) => {
        const existing = compareItems.find(item => item.type === 'yearly' && item.year === year)
        if (existing) return

        const { stem, branch } = YearlyCalculator.getYearStemBranch(year)
        const palaceIndex = data.palaces.findIndex(p => p.earthlyBranch === branch)
        const mutagen = MutagenCore.getMutagen(stem)

        const newItem: CompareItem = {
            id: `yearly-${year}`,
            type: 'yearly',
            year,
            heavenlyStem: stem,
            earthlyBranch: branch,
            palaceIndex: palaceIndex !== -1 ? palaceIndex : 0,
            palaceName: data.palaces[palaceIndex]?.name || '',
            mutagen: {
                lu: mutagen.lu || '',
                quan: mutagen.quan || '',
                ke: mutagen.ke || '',
                ji: mutagen.ji || ''
            }
        }

        setCompareItems([...compareItems, newItem])
        setShowYearPicker(false)
    }

    // 添加大限对比项
    const addDecadeItem = (decadeIndex: number) => {
        const existing = compareItems.find(item => item.type === 'decade' && item.decadeIndex === decadeIndex)
        if (existing) return

        const decade = data.decades?.[decadeIndex]
        if (!decade) return

        const mutagen = MutagenCore.getMutagen(decade.heavenlyStem)

        const newItem: CompareItem = {
            id: `decade-${decadeIndex}`,
            type: 'decade',
            decadeIndex,
            heavenlyStem: decade.heavenlyStem,
            earthlyBranch: decade.earthlyBranch,
            palaceIndex: decade.palaceIndex,
            palaceName: decade.palaceName,
            mutagen: {
                lu: mutagen.lu || '',
                quan: mutagen.quan || '',
                ke: mutagen.ke || '',
                ji: mutagen.ji || ''
            }
        }

        setCompareItems([...compareItems, newItem])
    }

    // 移除对比项
    const removeItem = (id: string) => {
        setCompareItems(compareItems.filter(item => item.id !== id))
    }

    // 高亮所有对比项的宫位
    const highlightAll = () => {
        const indexes = compareItems.map(item => item.palaceIndex)
        onHighlight?.(indexes)
    }

    // 四化对比分析
    const mutagenComparison = useMemo(() => {
        if (compareItems.length < 2) return null

        const comparison: Record<string, { star: string; sources: string[] }[]> = {
            lu: [],
            quan: [],
            ke: [],
            ji: []
        }

        compareItems.forEach(item => {
            const label = item.type === 'yearly' ? `${item.year}年` : `${item.decadeIndex! + 1}限`

            if (item.mutagen.lu) {
                const existing = comparison.lu.find(c => c.star === item.mutagen.lu)
                if (existing) {
                    existing.sources.push(label)
                } else {
                    comparison.lu.push({ star: item.mutagen.lu, sources: [label] })
                }
            }
            if (item.mutagen.quan) {
                const existing = comparison.quan.find(c => c.star === item.mutagen.quan)
                if (existing) {
                    existing.sources.push(label)
                } else {
                    comparison.quan.push({ star: item.mutagen.quan, sources: [label] })
                }
            }
            if (item.mutagen.ke) {
                const existing = comparison.ke.find(c => c.star === item.mutagen.ke)
                if (existing) {
                    existing.sources.push(label)
                } else {
                    comparison.ke.push({ star: item.mutagen.ke, sources: [label] })
                }
            }
            if (item.mutagen.ji) {
                const existing = comparison.ji.find(c => c.star === item.mutagen.ji)
                if (existing) {
                    existing.sources.push(label)
                } else {
                    comparison.ji.push({ star: item.mutagen.ji, sources: [label] })
                }
            }
        })

        return comparison
    }, [compareItems])

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between">
                <h3 className="text-sm font-medium flex items-center gap-2">
                    <ArrowLeftRight className="w-4 h-4" />
                    运限对比
                </h3>
                <div className="flex gap-2">
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setShowYearPicker(!showYearPicker)}
                    >
                        <Plus className="w-3 h-3 mr-1" />
                        添加流年
                    </Button>
                    {compareItems.length > 0 && (
                        <Button variant="outline" size="sm" onClick={highlightAll}>
                            高亮宫位
                        </Button>
                    )}
                </div>
            </div>

            {/* 年份选择器 */}
            {showYearPicker && (
                <div className="p-3 bg-secondary/50 rounded-lg">
                    <div className="text-xs text-muted-foreground mb-2">选择流年</div>
                    <div className="flex flex-wrap gap-2">
                        {yearOptions.map(year => {
                            const { stem, branch } = YearlyCalculator.getYearStemBranch(year)
                            const isSelected = compareItems.some(item => item.type === 'yearly' && item.year === year)
                            return (
                                <button
                                    key={year}
                                    onClick={() => addYearlyItem(year)}
                                    disabled={isSelected}
                                    className={`px-2 py-1 rounded text-xs transition-colors ${isSelected
                                        ? 'bg-primary/20 text-primary cursor-not-allowed'
                                        : 'bg-background hover:bg-primary/10 border border-border'
                                        }`}
                                >
                                    <span className={getStemColor(stem)}>{stem}</span>
                                    <span className={getBranchColor(branch)}>{branch}</span>
                                    <span className="text-muted-foreground ml-1">({year})</span>
                                </button>
                            )
                        })}
                    </div>
                </div>
            )}

            {/* 大限快速添加 */}
            {data.decades && data.decades.length > 0 && (
                <div className="p-3 bg-secondary/30 rounded-lg">
                    <div className="text-xs text-muted-foreground mb-2">快速添加大限</div>
                    <div className="flex flex-wrap gap-2">
                        {data.decades.slice(0, 8).map((decade, index) => {
                            const isSelected = compareItems.some(item => item.type === 'decade' && item.decadeIndex === index)
                            return (
                                <button
                                    key={index}
                                    onClick={() => addDecadeItem(index)}
                                    disabled={isSelected}
                                    className={`px-2 py-1 rounded text-xs transition-colors ${isSelected
                                        ? 'bg-purple-500/20 text-purple-600 cursor-not-allowed'
                                        : 'bg-background hover:bg-purple-500/10 border border-border'
                                        }`}
                                >
                                    <span className={getStemColor(decade.heavenlyStem)}>{decade.heavenlyStem}</span>
                                    <span className={getBranchColor(decade.earthlyBranch)}>{decade.earthlyBranch}</span>
                                    <span className="text-muted-foreground ml-1">({decade.startAge}岁)</span>
                                </button>
                            )
                        })}
                    </div>
                </div>
            )}

            {/* 对比项列表 */}
            {compareItems.length > 0 && (
                <ScrollArea className="w-full">
                    <div className="flex gap-3 pb-2">
                        {compareItems.map(item => (
                            <CompareItemCard
                                key={item.id}
                                item={item}
                                onRemove={() => removeItem(item.id)}
                                palaces={data.palaces}
                            />
                        ))}
                    </div>
                </ScrollArea>
            )}

            {/* 四化对比分析 */}
            {mutagenComparison && (
                <Card>
                    <CardHeader className="p-3 pb-2">
                        <CardTitle className="text-sm">四化对比分析</CardTitle>
                    </CardHeader>
                    <CardContent className="p-3 pt-0">
                        <div className="grid grid-cols-2 gap-3 text-xs">
                            {Object.entries(mutagenComparison).map(([key, items]) => {
                                const colors: Record<string, string> = {
                                    lu: 'bg-green-50 dark:bg-green-950/30 border-green-200',
                                    quan: 'bg-red-50 dark:bg-red-950/30 border-red-200',
                                    ke: 'bg-blue-50 dark:bg-blue-950/30 border-blue-200',
                                    ji: 'bg-purple-50 dark:bg-purple-950/30 border-purple-200'
                                }
                                const labels: Record<string, string> = { lu: '化禄', quan: '化权', ke: '化科', ji: '化忌' }

                                return (
                                    <div key={key} className={`p-2 rounded border ${colors[key]}`}>
                                        <div className="font-medium mb-1">{labels[key]}</div>
                                        {items.length > 0 ? (
                                            <div className="space-y-1">
                                                {items.map((item, idx) => (
                                                    <div key={idx} className="flex justify-between">
                                                        <span>{item.star}</span>
                                                        <span className="text-muted-foreground">
                                                            {item.sources.join('、')}
                                                            {item.sources.length > 1 && (
                                                                <Badge variant="outline" className="ml-1 text-[8px] px-1">重叠</Badge>
                                                            )}
                                                        </span>
                                                    </div>
                                                ))}
                                            </div>
                                        ) : (
                                            <div className="text-muted-foreground">-</div>
                                        )}
                                    </div>
                                )
                            })}
                        </div>

                        {/* 重叠四化提示 */}
                        {Object.values(mutagenComparison).some(items => items.some(i => i.sources.length > 1)) && (
                            <div className="mt-3 p-2 bg-amber-50 dark:bg-amber-950/30 rounded text-xs text-amber-700 dark:text-amber-300">
                                ⚠️ 检测到四化重叠，这表示在不同运限中同一星曜多次化同一种四化，能量加倍！
                            </div>
                        )}
                    </CardContent>
                </Card>
            )}

            {compareItems.length === 0 && (
                <div className="text-center text-sm text-muted-foreground py-8">
                    点击上方按钮添加流年或大限进行对比分析
                </div>
            )}
        </div>
    )
}

export default HoroscopeComparePanel
