import { useMemo } from 'react'
import { useTranslation } from 'react-i18next'
import { FiveElementsChart } from '@/components/bazi/FiveElementsChart'

// 天干五行映射
const TIANGAN_WUXING: Record<string, string> = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

// 地支五行映射
const DIZHI_WUXING: Record<string, string> = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

type FiveElement = '木' | '火' | '土' | '金' | '水'

interface BaziData {
    sizhu?: Record<string, string | undefined>
    nayin?: Record<string, string | undefined>
    dizhi_cang?: Record<string, string[]>
    xunkong?: Record<string, string>
    lunar_info?: {
        lunar_year?: number
        lunar_month?: number
        lunar_day?: number
        year_cn?: string
        month_cn?: string
        day_cn?: string
        zodiac?: string
        [key: string]: unknown
    }
    [key: string]: unknown
}

interface BaziDisplayProps {
    data: BaziData | null
    loading?: boolean
}

export function BaziDisplay({ data, loading }: BaziDisplayProps) {
    const { t, i18n } = useTranslation()
    const isEnglish = i18n.language === 'en'

    // 计算五行统计
    const fiveElements = useMemo(() => {
        const counts: Record<FiveElement, number> = { '木': 0, '火': 0, '土': 0, '金': 0, '水': 0 }
        
        if (!data?.sizhu) return counts
        
        const { sizhu, dizhi_cang } = data
        
        // 统计天干地支
        ;['year', 'month', 'day', 'hour'].forEach(pillar => {
            const gz = sizhu[pillar]
            if (gz && gz.length >= 2) {
                const tg = gz[0]
                const dz = gz[1]
                
                // 天干五行
                if (TIANGAN_WUXING[tg]) {
                    counts[TIANGAN_WUXING[tg] as FiveElement]++
                }
                
                // 地支五行
                if (DIZHI_WUXING[dz]) {
                    counts[DIZHI_WUXING[dz] as FiveElement]++
                }
            }
            
            // 藏干五行
            const canggan = dizhi_cang?.[pillar]
            if (canggan && Array.isArray(canggan)) {
                canggan.forEach((cg: string) => {
                    if (TIANGAN_WUXING[cg]) {
                        counts[TIANGAN_WUXING[cg] as FiveElement]++
                    }
                })
            }
        })
        
        return counts
    }, [data])

    if (loading) {
        return (
            <div className="flat-card p-4 mb-4">
                <div className="text-center text-muted-foreground">
                    {isEnglish ? 'Calculating...' : '正在排盘...'}
                </div>
            </div>
        )
    }

    if (!data) {
        return null
    }

    const { sizhu, nayin, dizhi_cang, xunkong, lunar_info } = data

    return (
        <div className="flat-card p-4 mb-4 bg-card border border-border">
            <h3 className="text-lg font-semibold mb-3 text-foreground">
                📊 {isEnglish ? 'BaZi Chart Result' : '八字排盘结果'}
            </h3>

            {/* 农历信息 */}
            {lunar_info && (
                <div className="mb-4 p-3 bg-secondary rounded-lg">
                    <div className="text-sm">
                        <span className="font-medium">{isEnglish ? 'Lunar: ' : '农历：'}</span>
                        {lunar_info.year_cn} {lunar_info.month_cn}{lunar_info.day_cn}
                        <span className="ml-3">
                            <span className="font-medium">{isEnglish ? 'Zodiac: ' : '生肖：'}</span>
                            {lunar_info.zodiac}
                        </span>
                    </div>
                </div>
            )}

            {/* 四柱八字 */}
            <div className="grid grid-cols-4 gap-2 mb-4">
                {['year', 'month', 'day', 'hour'].map((pillar, index) => (
                    <div
                        key={pillar}
                        className="text-center p-3 bg-secondary rounded-lg border border-border"
                    >
                        <div className="text-xs text-muted-foreground mb-1">
                            {isEnglish 
                                ? ['Year', 'Month', 'Day', 'Hour'][index]
                                : ['年柱', '月柱', '日柱', '时柱'][index]
                            }
                        </div>
                        <div className="text-2xl font-bold text-foreground">
                            {sizhu?.[pillar] || '--'}
                        </div>
                        <div className="text-xs text-muted-foreground mt-1">
                            {nayin?.[pillar] || ''}
                        </div>
                    </div>
                ))}
            </div>

            {/* 五行分布图 */}
            <div className="mb-4 p-3 bg-secondary rounded-lg">
                <div className="font-medium mb-2 text-sm">
                    {isEnglish ? '🎯 Five Elements Distribution' : '🎯 五行分布'}
                </div>
                <FiveElementsChart elements={fiveElements} />
            </div>

            {/* 详细信息折叠 */}
            <details className="mt-3">
                <summary className="cursor-pointer text-sm font-medium text-foreground hover:underline">
                    {isEnglish ? 'View Details' : '查看详细信息'}
                </summary>
                <div className="mt-3 space-y-3 text-sm">
                    {/* 地支藏干 */}
                    <div className="p-3 bg-secondary rounded">
                        <div className="font-medium mb-2">
                            {isEnglish ? 'Hidden Stems:' : '地支藏干：'}
                        </div>
                        <div className="grid grid-cols-4 gap-2">
                            {['year', 'month', 'day', 'hour'].map((pillar, idx) => (
                                <div key={pillar} className="text-center">
                                    <div className="text-xs text-muted-foreground">
                                        {isEnglish 
                                            ? ['Yr', 'Mo', 'Da', 'Hr'][idx]
                                            : ['年', '月', '日', '时'][idx]
                                        }
                                    </div>
                                    <div>{dizhi_cang?.[pillar]?.join(' ') || '--'}</div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* 旬空 */}
                    <div className="p-3 bg-secondary rounded">
                        <div className="font-medium mb-2">
                            {isEnglish ? 'Void Branches:' : '旬空：'}
                        </div>
                        <div className="grid grid-cols-4 gap-2">
                            {['year', 'month', 'day', 'hour'].map((pillar, idx) => (
                                <div key={pillar} className="text-center">
                                    <div className="text-xs text-muted-foreground">
                                        {isEnglish 
                                            ? ['Yr', 'Mo', 'Da', 'Hr'][idx]
                                            : ['年', '月', '日', '时'][idx]
                                        }
                                    </div>
                                    <div>{xunkong?.[pillar] || '--'}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </details>

            <div className="mt-3 text-xs text-muted-foreground text-center">
                ✨ {isEnglish 
                    ? 'AI will provide professional analysis based on this data'
                    : 'AI将基于以上精确数据进行专业解读'
                }
            </div>
        </div>
    )
}
