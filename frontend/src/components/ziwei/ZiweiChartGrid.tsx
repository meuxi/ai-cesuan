/**
 * 紫微斗数命盘组件
 * 参考MingAI-master实现三方四正连线、颜色区分、运限高亮等功能
 */

import { useState, useCallback, useMemo } from 'react'
import { useTranslation } from 'react-i18next'
import { Eye, EyeOff, Copy, Check, Sparkles } from 'lucide-react'
import type { ZiweiResult, EnhancedPalace, StarWithMutagen } from '@/types/ziwei'
import { PalaceDetailDialog } from './PalaceDetailDialog'
import { MutagenCore } from '@/services/ziwei/MutagenCore'
import './iztro-style.css'

// 运限高亮类型
export interface HoroscopeHighlight {
    decadalIndex?: number    // 大限宫位索引
    yearlyIndex?: number     // 流年宫位索引
    monthlyIndex?: number    // 流月宫位索引
    dailyIndex?: number      // 流日宫位索引
    hourlyIndex?: number     // 流时宫位索引
    minorLimitIndex?: number // 小限宫位索引
}

// 运限信息类型
export interface HoroscopeInfo {
    decadal?: { heavenlyStem: string; startAge: number; palaceNames?: string[] }
    yearly?: { heavenlyStem: string; palaceIndex: number; palaceNames?: string[] }
    monthly?: { heavenlyStem: string; palaceIndex: number; palaceNames?: string[] }
    daily?: { heavenlyStem: string; palaceIndex: number; palaceNames?: string[] }
    hourly?: { heavenlyStem: string; palaceIndex: number; palaceNames?: string[] }
    minorLimit?: { age: number; palaceIndex: number }
}

// 飞星信息类型
export interface FlyingStarInfo {
    sourcePalace: number      // 源宫位索引
    sourceStem: string        // 源宫天干
    targets: {                // 飞化目标
        lu: { star: string; palaceIndex: number } | null
        quan: { star: string; palaceIndex: number } | null
        ke: { star: string; palaceIndex: number } | null
        ji: { star: string; palaceIndex: number } | null
    }
}

// 日期切换类型
type HoroscopeScope = 'decadal' | 'yearly' | 'monthly' | 'daily' | 'hourly'

interface ZiweiChartGridProps {
    data: ZiweiResult
    onPalaceSelect?: (index: number) => void
    horoscopeHighlight?: HoroscopeHighlight  // 运限高亮
    horoscopeInfo?: HoroscopeInfo            // 运限信息
    onHoroscopeDateChange?: (scope: HoroscopeScope, delta: number) => void  // 快捷切换回调
}

// 三方四正计算
function getSanFangSiZheng(palaceIndex: number): number[] {
    const sanFang = [(palaceIndex + 4) % 12, (palaceIndex + 8) % 12]
    const siZheng = (palaceIndex + 6) % 12
    return [palaceIndex, ...sanFang, siZheng]
}

// 五行颜色映射：天干对应五行
function getStemColor(stem: string): string {
    switch (stem) {
        case '甲': case '乙': return 'text-green-500'  // 木
        case '丙': case '丁': return 'text-red-500'    // 火
        case '戊': case '己': return 'text-amber-500'  // 土
        case '庚': case '辛': return 'text-yellow-400' // 金
        case '壬': case '癸': return 'text-blue-500'   // 水
        default: return 'text-foreground'
    }
}

// 地支五行颜色
function getBranchColor(branch: string): string {
    const map: Record<string, string> = {
        '寅': 'text-green-500', '卯': 'text-green-500',  // 木
        '巳': 'text-red-500', '午': 'text-red-500',      // 火
        '辰': 'text-amber-500', '戌': 'text-amber-500', '丑': 'text-amber-500', '未': 'text-amber-500', // 土
        '申': 'text-yellow-400', '酉': 'text-yellow-400', // 金
        '亥': 'text-blue-500', '子': 'text-blue-500'     // 水
    }
    return map[branch] || 'text-foreground'
}

// 从 CSS 变量获取颜色（用于 SVG 渲染）
function getCSSVarColor(varName: string, fallback: string): string {
    if (typeof window === 'undefined') return fallback;
    const value = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
    if (!value) return fallback;
    const [h, s, l] = value.split(' ').map(v => v.trim());
    if (h && s && l) return `hsl(${h}, ${s}, ${l})`;
    return fallback;
}

// 星曜亮度颜色和标签 - 使用 CSS 变量
function getBrightnessInfo(brightness?: string): { color: string; label: string; hexColor: string } {
    switch (brightness) {
        case '庙': return { color: 'text-red-600 font-bold', label: '庙', hexColor: getCSSVarColor('--star-miao', 'hsl(0, 72%, 51%)') }
        case '旺': return { color: 'text-orange-500 font-semibold', label: '旺', hexColor: getCSSVarColor('--star-wang', 'hsl(25, 95%, 53%)') }
        case '得': return { color: 'text-amber-600 font-medium', label: '得', hexColor: getCSSVarColor('--star-de', 'hsl(32, 95%, 44%)') }
        case '利': return { color: 'text-green-600', label: '利', hexColor: getCSSVarColor('--star-li', 'hsl(142, 76%, 36%)') }
        case '平': return { color: 'text-slate-600', label: '平', hexColor: getCSSVarColor('--star-ping', 'hsl(215, 16%, 47%)') }
        case '不': return { color: 'text-blue-500', label: '不', hexColor: getCSSVarColor('--star-bu', 'hsl(217, 91%, 60%)') }
        case '陷': return { color: 'text-purple-500 opacity-80', label: '陷', hexColor: getCSSVarColor('--star-xian', 'hsl(271, 81%, 56%)') }
        default: return { color: 'text-foreground', label: '', hexColor: getCSSVarColor('--star-default', 'hsl(215, 16%, 57%)') }
    }
}

// 四化颜色
function getMutagenColor(mutagen: string): string {
    if (mutagen.includes('禄')) return 'text-green-500'
    if (mutagen.includes('权')) return 'text-red-500'
    if (mutagen.includes('科')) return 'text-blue-500'
    if (mutagen.includes('忌')) return 'text-purple-500'
    return 'text-foreground'
}

// 飞星背景颜色
function getFlyingStarBgColor(type: 'lu' | 'quan' | 'ke' | 'ji'): string {
    switch (type) {
        case 'lu': return 'bg-green-500/30 ring-2 ring-green-500'
        case 'quan': return 'bg-red-500/30 ring-2 ring-red-500'
        case 'ke': return 'bg-blue-500/30 ring-2 ring-blue-500'
        case 'ji': return 'bg-purple-500/30 ring-2 ring-purple-500'
    }
}

// 地支到索引映射
const BRANCH_TO_INDEX: Record<string, number> = {
    '子': 0, '丑': 1, '寅': 2, '卯': 3, '辰': 4, '巳': 5,
    '午': 6, '未': 7, '申': 8, '酉': 9, '戌': 10, '亥': 11
}

// 宫位在网格中的位置映射
const POSITION_MAP: Record<number, { row: number; col: number }> = {
    5: { row: 0, col: 0 }, 6: { row: 0, col: 1 }, 7: { row: 0, col: 2 }, 8: { row: 0, col: 3 },
    4: { row: 1, col: 0 }, 9: { row: 1, col: 3 },
    3: { row: 2, col: 0 }, 10: { row: 2, col: 3 },
    2: { row: 3, col: 0 }, 1: { row: 3, col: 1 }, 0: { row: 3, col: 2 }, 11: { row: 3, col: 3 },
}

// 六煞星名单（参考MingAI）
const MINOR_MALEFIC_STARS = new Set(['擎羊', '陀羅', '擎羊', '陀罗', '火星', '鈴星', '铃星', '地空', '地劫'])

// 运限四化信息类型
interface HoroscopeMutagenItem {
    scope: 'decadal' | 'yearly' | 'monthly' | 'daily' | 'hourly'
    type: '禄' | '权' | '科' | '忌'
}

// 运限四化颜色配置
const HOROSCOPE_MUTAGEN_COLORS: Record<string, string> = {
    decadal: 'bg-purple-500',   // 大限紫色
    yearly: 'bg-blue-500',      // 流年蓝色
    monthly: 'bg-green-500',    // 流月绿色
    daily: 'bg-orange-500',     // 流日橙色
    hourly: 'bg-cyan-500'       // 流时青色
}

const HOROSCOPE_SCOPE_LABELS: Record<string, string> = {
    decadal: '限',
    yearly: '年',
    monthly: '月',
    daily: '日',
    hourly: '时'
}

// 星曜组件 - 参考官方react-iztro的Izstar实现
function Izstar({ star, selfMutagen, horoscopeMutagens }: {
    star: StarWithMutagen;
    selfMutagen?: string;
    horoscopeMutagens?: HoroscopeMutagenItem[];
}) {
    const isMajor = star.type === 'major'
    const isMinor = star.type === 'minor'
    const isAuxiliary = star.type === 'auxiliary'
    const isMinorMalefic = isMinor && MINOR_MALEFIC_STARS.has(star.name)

    // 星曜类型样式（参考官方CSS）
    const starTypeClass = isMajor ? 'iztro-star-major'
        : isMinorMalefic ? 'iztro-star-tough'
            : isMinor ? 'iztro-star-soft'
                : 'iztro-star-adjective'

    // 四化颜色样式
    const getMutagenClass = (mutagen: string) => {
        if (mutagen.includes('禄')) return 'mutagen-0'  // 禄
        if (mutagen.includes('权')) return 'mutagen-1'  // 权
        if (mutagen.includes('科')) return 'mutagen-2'  // 科
        if (mutagen.includes('忌')) return 'mutagen-3'  // 忌
        return ''
    }

    return (
        <div className={`iztro-star ${starTypeClass}`}>
            <span className={`star-name ${selfMutagen ? `self-mutagen-${getMutagenClass(selfMutagen)}` : ''}`}>
                {star.name}
            </span>
            {star.brightness && (
                <i className="iztro-star-brightness">{star.brightness}</i>
            )}
            {star.mutagen?.map((m, i) => (
                <span key={i} className={`iztro-star-mutagen ${getMutagenClass(m)}`}>{m}</span>
            ))}
            {horoscopeMutagens?.map((item, idx) => (
                <span key={`${item.scope}-${idx}`} className={`iztro-star-mutagen mutagen-${item.scope}`}>
                    {item.type}
                </span>
            ))}
        </div>
    )
}

// 运限高亮颜色配置
const HOROSCOPE_COLORS = {
    decadal: { border: 'border-purple-500', bg: 'bg-purple-500/10', ring: 'ring-purple-500/30', text: 'text-purple-500' },
    minorLimit: { border: 'border-pink-500', bg: 'bg-pink-500/10', ring: 'ring-pink-500/30', text: 'text-pink-500' },
    yearly: { border: 'border-blue-500', bg: 'bg-blue-500/10', ring: 'ring-blue-500/30', text: 'text-blue-500' },
    monthly: { border: 'border-green-500', bg: 'bg-green-500/10', ring: 'ring-green-500/30', text: 'text-green-500' },
    hourly: { border: 'border-cyan-500', bg: 'bg-cyan-500/10', ring: 'ring-cyan-500/30', text: 'text-cyan-500' },
    daily: { border: 'border-orange-500', bg: 'bg-orange-500/10', ring: 'ring-orange-500/30', text: 'text-orange-500' },
}

// 宫位卡片组件 - 优化布局和显示效果
function PalaceCard({
    palace,
    palaceIndex,
    isSelected,
    isMingGong,
    isSanFangSiZheng,
    highlightTypes,
    flowInfo,
    showAdjStars,
    flyingStarTypes,
    isFlyingSource,
    isHoverPreview,
    dynamicPalaceNames,
    horoscopeMutagens,
    horoscopeStars,
    taichiPalaceName,
    onPalaceNameClick,
    onStemClick,
    onStemHover,
    onStemLeave,
    onClick,
    onDoubleClick
}: {
    palace: EnhancedPalace
    palaceIndex: number
    isSelected: boolean
    isMingGong: boolean
    isSanFangSiZheng: boolean
    highlightTypes: string[]  // 运限高亮类型 ['decadal', 'yearly', 'monthly', 'daily']
    flowInfo?: { decadal?: { stem: string; ages: string }; yearly?: string; monthly?: string; daily?: string; hourly?: string }
    dynamicPalaceNames?: { decadal?: string; yearly?: string; monthly?: string; daily?: string; hourly?: string }  // 运限重排宫名
    horoscopeMutagens?: Record<string, HoroscopeMutagenItem[]>  // 星耀名 -> 运限四化列表
    horoscopeStars?: { decadal?: StarWithMutagen[]; yearly?: StarWithMutagen[] }  // 流耀（大限/流年）
    taichiPalaceName?: string  // 太极点宫名
    onPalaceNameClick?: () => void  // 宫名点击（太极点切换）
    showAdjStars: boolean
    flyingStarTypes: ('lu' | 'quan' | 'ke' | 'ji')[]  // 飞星高亮类型
    isFlyingSource: boolean  // 是否为飞星源宫
    isHoverPreview?: boolean  // 是否为悬停预览模式
    onStemClick?: (e: React.MouseEvent) => void  // 宫干点击
    onStemHover?: () => void  // 宫干悬停
    onStemLeave?: () => void  // 宫干离开
    onClick: () => void
    onDoubleClick?: () => void
}) {
    // 计算边框和背景样式
    const getBorderClass = () => {
        if (isSelected) return 'border-primary ring-2 ring-primary/30 bg-primary/5'

        // 多重运限高亮 - 按优先级显示
        if (highlightTypes.length > 0) {
            const primary = highlightTypes[0] as keyof typeof HOROSCOPE_COLORS
            const colors = HOROSCOPE_COLORS[primary]
            return `${colors.border} ring-2 ${colors.ring} ${colors.bg}`
        }

        // 飞星高亮
        if (flyingStarTypes.length > 0) {
            const colors = {
                lu: 'border-green-500 ring-2 ring-green-500/40 bg-green-500/10',
                quan: 'border-red-500 ring-2 ring-red-500/40 bg-red-500/10',
                ke: 'border-blue-500 ring-2 ring-blue-500/40 bg-blue-500/10',
                ji: 'border-purple-500 ring-2 ring-purple-500/40 bg-purple-500/10'
            }
            return colors[flyingStarTypes[0]]
        }

        // 飞星源宫高亮
        if (isFlyingSource) return 'border-amber-500 ring-2 ring-amber-500/40 bg-amber-500/10'

        if (isSanFangSiZheng) return 'border-orange-600/50 bg-orange-600/5'
        if (isMingGong) return 'border-amber-500/50 bg-amber-500/5'
        return 'border-border/60 hover:border-border'
    }

    // 过滤显示的辅星（杂曜）
    const displayMinorStars = showAdjStars
        ? palace.minorStars
        : palace.minorStars.filter(s => s.type !== 'auxiliary')

    // 计算自化信息：宫干四化飞入本宫星耀
    const getSelfMutagen = (starName: string): string | undefined => {
        const stem = palace.heavenlyStem
        const mutagen = MutagenCore.getMutagen(stem)
        const normalizedName = MutagenCore.normalizeStarName(starName)

        if (mutagen.lu && MutagenCore.normalizeStarName(mutagen.lu) === normalizedName) return '禄'
        if (mutagen.quan && MutagenCore.normalizeStarName(mutagen.quan) === normalizedName) return '权'
        if (mutagen.ke && MutagenCore.normalizeStarName(mutagen.ke) === normalizedName) return '科'
        if (mutagen.ji && MutagenCore.normalizeStarName(mutagen.ji) === normalizedName) return '忌'
        return undefined
    }

    // 获取三方四正样式
    const getPalaceClass = () => {
        if (isSelected) return 'focused-palace'
        if (isSanFangSiZheng) return 'surrounded-palace'
        return ''
    }

    return (
        <div
            onClick={onClick}
            onDoubleClick={onDoubleClick}
            className={`iztro-palace iztro-astrolabe-theme-default ${getPalaceClass()} ${getBorderClass()} cursor-pointer`}
        >
            {/* 主星区 - 参考官方react-iztro */}
            <div className="iztro-palace-major">
                {palace.majorStars.map((star, idx) => (
                    <Izstar
                        key={`major-${idx}`}
                        star={star}
                        selfMutagen={getSelfMutagen(star.name)}
                        horoscopeMutagens={horoscopeMutagens?.[MutagenCore.normalizeStarName(star.name)]}
                    />
                ))}
            </div>

            {/* 辅星区 */}
            <div className="iztro-palace-minor">
                {displayMinorStars.map((star, idx) => (
                    <Izstar
                        key={`minor-${idx}`}
                        star={star}
                        selfMutagen={getSelfMutagen(star.name)}
                        horoscopeMutagens={horoscopeMutagens?.[MutagenCore.normalizeStarName(star.name)]}
                    />
                ))}
            </div>

            {/* 杂曜区 */}
            <div className="iztro-palace-adj">
                <div>
                    {showAdjStars && palace.adjStars?.slice(5).map((star, idx) => (
                        <Izstar key={`adj2-${idx}`} star={{ ...star, type: 'auxiliary' as const }} />
                    ))}
                </div>
                <div>
                    {showAdjStars && palace.adjStars?.slice(0, 5).map((star, idx) => (
                        <Izstar key={`adj1-${idx}`} star={{ ...star, type: 'auxiliary' as const }} />
                    ))}
                </div>
            </div>

            {/* 流耀区 */}
            <div className="iztro-palace-horo-star">
                <div className="stars">
                    {horoscopeStars?.decadal?.map((star, idx) => (
                        <Izstar key={`dec-${idx}`} star={star} />
                    ))}
                </div>
                <div className="stars">
                    {horoscopeStars?.yearly?.map((star, idx) => (
                        <Izstar key={`yr-${idx}`} star={star} />
                    ))}
                </div>
            </div>

            {/* 运限宫名区 */}
            <div className="iztro-palace-fate">
                {highlightTypes.map(type => {
                    const labels: Record<string, string> = { decadal: '限', yearly: '年', monthly: '月', daily: '日', hourly: '时' }
                    return (
                        <span key={type} className={`iztro-palace-${type}-active`}>
                            {labels[type]}
                        </span>
                    )
                })}
            </div>

            {/* 底部信息区 - 参考官方react-iztro */}
            <div className="iztro-palace-footer">
                {/* 左侧12神 */}
                <div>
                    <div className="iztro-palace-lft24">
                        <div>{palace.extras?.changsheng12}</div>
                        <div>{palace.extras?.boshi12}</div>
                    </div>
                    <div className="iztro-palace-name" onClick={(e) => { e.stopPropagation(); onPalaceNameClick?.() }}>
                        <span className="iztro-palace-name-wrapper">
                            {palace.name}
                            {taichiPalaceName && (
                                <span className="iztro-palace-name-taichi">
                                    {taichiPalaceName === '命宮' ? '☯' : taichiPalaceName}
                                </span>
                            )}
                        </span>
                        {palace.isBodyPalace && (
                            <span className="iztro-palace-name-body">·身宫</span>
                        )}
                    </div>
                </div>

                {/* 中间大限/小限 */}
                <div>
                    <div className="iztro-palace-scope">
                        <div className="iztro-palace-scope-age">
                            {palace.extras?.ages?.slice(0, 7).join(' ')}
                        </div>
                        <div className="iztro-palace-scope-decadal">
                            {palace.decadeInfo?.startAge} - {palace.decadeInfo?.endAge}
                        </div>
                    </div>
                    <div className="iztro-palace-dynamic-name">
                        {dynamicPalaceNames?.decadal && (
                            <span className="iztro-palace-dynamic-name-decadal">{dynamicPalaceNames.decadal}</span>
                        )}
                        {dynamicPalaceNames?.yearly && (
                            <span className="iztro-palace-dynamic-name-yearly">{dynamicPalaceNames.yearly}</span>
                        )}
                        {dynamicPalaceNames?.monthly && (
                            <span className="iztro-palace-dynamic-name-monthly">{dynamicPalaceNames.monthly}</span>
                        )}
                    </div>
                </div>

                {/* 右侧12神和干支 */}
                <div>
                    <div className="iztro-palace-rgt24">
                        <div>{palace.extras?.suiqian12}</div>
                        <div>{palace.extras?.jiangqian12}</div>
                    </div>
                    <div
                        className={`iztro-palace-gz ${isFlyingSource ? 'iztro-palace-gz-active' : ''}`}
                        onClick={onStemClick}
                        onMouseEnter={onStemHover}
                        onMouseLeave={onStemLeave}
                    >
                        <span>{palace.heavenlyStem}{palace.earthlyBranch}</span>
                    </div>
                </div>
            </div>


            {/* 小限年龄 */}
            {palace.extras?.ages && palace.extras.ages.length > 0 && (
                <div className="absolute bottom-0.5 left-1 text-[6px] text-blue-400/80">
                    {palace.extras.ages.slice(0, 2).join(',')}
                </div>
            )}
        </div>
    )
}

export function ZiweiChartGrid({ data, onPalaceSelect, horoscopeHighlight = {}, horoscopeInfo, onHoroscopeDateChange }: ZiweiChartGridProps) {
    const { t } = useTranslation()
    const [selectedPalace, setSelectedPalace] = useState<number | null>(null)
    const [detailPalace, setDetailPalace] = useState<EnhancedPalace | null>(null)
    const [showDetail, setShowDetail] = useState(false)
    const [showAdjStars, setShowAdjStars] = useState(true)  // 杂曜显隐
    const [copied, setCopied] = useState(false)
    const [flyingStar, setFlyingStar] = useState<FlyingStarInfo | null>(null)  // 飞星状态（点击）
    const [hoverFlyingStar, setHoverFlyingStar] = useState<FlyingStarInfo | null>(null)  // 飞星状态（悬停预览）
    const [taichiPoint, setTaichiPoint] = useState<number>(-1)  // 太极点（-1表示原盘）

    // 找命宫索引
    const mingGongIndex = data.palaces.findIndex(p => p.name === '命宮' || p.name === '命宫')

    // 太极点切换：重新排列宫名
    const PALACE_NAMES = ['命宮', '兄弟', '夫妻', '子女', '财帛', '疾厄', '迁移', '交友', '官禄', '田宅', '福德', '父母']
    const getTaichiPalaceName = useCallback((palaceIndex: number): string | undefined => {
        if (taichiPoint < 0) return undefined
        const offset = (palaceIndex - taichiPoint + 12) % 12
        return PALACE_NAMES[offset]
    }, [taichiPoint])

    const toggleTaichiPoint = useCallback((index: number) => {
        setTaichiPoint(prev => prev === index ? -1 : index)
    }, [])

    // 计算飞星信息：点击宫干时，计算四化飞出位置
    const calculateFlyingStar = useCallback((palaceIndex: number, stem: string) => {
        const mutagen = MutagenCore.getMutagen(stem)
        if (!mutagen.lu && !mutagen.quan && !mutagen.ke && !mutagen.ji) return null

        // 查找每个四化星所在宫位
        const findStarPalace = (starName: string): { star: string; palaceIndex: number } | null => {
            if (!starName) return null
            for (let i = 0; i < data.palaces.length; i++) {
                const palace = data.palaces[i]
                // 在主星中查找
                const majorStar = palace.majorStars.find(s =>
                    MutagenCore.normalizeStarName(s.name) === starName || s.name === starName
                )
                if (majorStar) return { star: starName, palaceIndex: i }
                // 在辅星中查找（文昌文曲左辅右弼等）
                const minorStar = palace.minorStars.find(s =>
                    MutagenCore.normalizeStarName(s.name) === starName || s.name === starName
                )
                if (minorStar) return { star: starName, palaceIndex: i }
            }
            return null
        }

        return {
            sourcePalace: palaceIndex,
            sourceStem: stem,
            targets: {
                lu: mutagen.lu ? findStarPalace(mutagen.lu) : null,
                quan: mutagen.quan ? findStarPalace(mutagen.quan) : null,
                ke: mutagen.ke ? findStarPalace(mutagen.ke) : null,
                ji: mutagen.ji ? findStarPalace(mutagen.ji) : null
            }
        }
    }, [data.palaces])

    // 处理宫干悬停（预览飞星）
    const handleStemHover = useCallback((palaceIndex: number, stem: string) => {
        // 如果已经点击锁定了飞星，不显示悬停预览
        if (flyingStar) return
        const info = calculateFlyingStar(palaceIndex, stem)
        setHoverFlyingStar(info)
    }, [flyingStar, calculateFlyingStar])

    // 处理宫干离开
    const handleStemLeave = useCallback(() => {
        setHoverFlyingStar(null)
    }, [])

    // 处理宫干点击
    const handleStemClick = useCallback((palaceIndex: number, stem: string, e: React.MouseEvent) => {
        e.stopPropagation()
        if (flyingStar?.sourcePalace === palaceIndex) {
            setFlyingStar(null)  // 取消飞星
        } else {
            const info = calculateFlyingStar(palaceIndex, stem)
            setFlyingStar(info)
        }
    }, [flyingStar, calculateFlyingStar])

    // 获取宫位的飞星高亮类型（支持点击和悬停）
    const getFlyingStarHighlight = useCallback((palaceIndex: number): ('lu' | 'quan' | 'ke' | 'ji')[] => {
        // 优先使用点击锁定的飞星，否则使用悬停预览
        const activeFlyingStar = flyingStar || hoverFlyingStar
        if (!activeFlyingStar) return []
        const types: ('lu' | 'quan' | 'ke' | 'ji')[] = []
        if (activeFlyingStar.targets.lu?.palaceIndex === palaceIndex) types.push('lu')
        if (activeFlyingStar.targets.quan?.palaceIndex === palaceIndex) types.push('quan')
        if (activeFlyingStar.targets.ke?.palaceIndex === palaceIndex) types.push('ke')
        if (activeFlyingStar.targets.ji?.palaceIndex === palaceIndex) types.push('ji')
        return types
    }, [flyingStar, hoverFlyingStar])

    // 判断是否为飞星源宫（支持点击和悬停）
    const isFlyingSourcePalace = useCallback((palaceIndex: number): boolean => {
        const activeFlyingStar = flyingStar || hoverFlyingStar
        return activeFlyingStar?.sourcePalace === palaceIndex
    }, [flyingStar, hoverFlyingStar])

    // 三方四正宫位 - 支持运限命宫
    // 优先使用运限命宫（大限>流年），否则使用选中宫位
    const sanFangSiZhengSource = useMemo(() => {
        // 如果有选中运限，从运限命宫出发
        if (horoscopeInfo?.decadal?.palaceNames) {
            const mingIndex = horoscopeInfo.decadal.palaceNames.findIndex(n => n === '命宮' || n === '命宫')
            if (mingIndex >= 0) return { index: mingIndex, type: 'decadal' as const }
        }
        if (horoscopeInfo?.yearly?.palaceNames) {
            const mingIndex = horoscopeInfo.yearly.palaceNames.findIndex(n => n === '命宮' || n === '命宫')
            if (mingIndex >= 0) return { index: mingIndex, type: 'yearly' as const }
        }
        // 默认使用选中宫位
        if (selectedPalace !== null) return { index: selectedPalace, type: 'selected' as const }
        return null
    }, [horoscopeInfo, selectedPalace])

    const sanFangSiZhengIndexes = sanFangSiZhengSource ? getSanFangSiZheng(sanFangSiZhengSource.index) : []

    // 根据地支获取宫位
    const getPalaceByBranch = (branchIndex: number) => {
        const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        const branch = branches[branchIndex]
        return data.palaces.find(p => p.earthlyBranch === branch)
    }

    // 获取宫位高亮类型（多色支持）
    const getHighlightTypes = (palaceIndex: number): string[] => {
        const types: string[] = []
        if (horoscopeHighlight.decadalIndex === palaceIndex) types.push('decadal')
        if (horoscopeHighlight.minorLimitIndex === palaceIndex) types.push('minorLimit')
        if (horoscopeHighlight.yearlyIndex === palaceIndex) types.push('yearly')
        if (horoscopeHighlight.monthlyIndex === palaceIndex) types.push('monthly')
        if (horoscopeHighlight.dailyIndex === palaceIndex) types.push('daily')
        if (horoscopeHighlight.hourlyIndex === palaceIndex) types.push('hourly')
        return types
    }

    // 获取宫位的流年流月信息
    const getFlowInfoForPalace = (palaceIndex: number) => {
        if (!horoscopeInfo) return undefined
        const flowInfo: { decadal?: { stem: string; ages: string }; minorLimit?: string; yearly?: string; monthly?: string; daily?: string; hourly?: string } = {}

        if (horoscopeInfo.decadal && horoscopeHighlight.decadalIndex === palaceIndex) {
            flowInfo.decadal = { stem: horoscopeInfo.decadal.heavenlyStem, ages: `${horoscopeInfo.decadal.startAge}岁` }
        }
        if (horoscopeInfo.minorLimit && horoscopeHighlight.minorLimitIndex === palaceIndex) {
            flowInfo.minorLimit = `${horoscopeInfo.minorLimit.age}岁`
        }
        if (horoscopeInfo.yearly && horoscopeInfo.yearly.palaceIndex === palaceIndex) {
            flowInfo.yearly = horoscopeInfo.yearly.heavenlyStem
        }
        if (horoscopeInfo.monthly && horoscopeInfo.monthly.palaceIndex === palaceIndex) {
            flowInfo.monthly = horoscopeInfo.monthly.heavenlyStem
        }
        if (horoscopeInfo.daily && horoscopeInfo.daily.palaceIndex === palaceIndex) {
            flowInfo.daily = horoscopeInfo.daily.heavenlyStem
        }
        if (horoscopeInfo.hourly && horoscopeInfo.hourly.palaceIndex === palaceIndex) {
            flowInfo.hourly = horoscopeInfo.hourly.heavenlyStem
        }

        return Object.keys(flowInfo).length > 0 ? flowInfo : undefined
    }

    // 计算宫位内所有星耀的运限四化（多层叠加）
    const getHoroscopeMutagensForPalace = useCallback((palaceIndex: number): Record<string, HoroscopeMutagenItem[]> | undefined => {
        if (!horoscopeInfo) return undefined

        const result: Record<string, HoroscopeMutagenItem[]> = {}
        const MUTAGEN_TYPES: ('禄' | '权' | '科' | '忌')[] = ['禄', '权', '科', '忌']

        // 添加运限四化
        const addMutagen = (scope: 'decadal' | 'yearly' | 'monthly' | 'daily' | 'hourly', stem: string | undefined) => {
            if (!stem) return
            const mutagen = MutagenCore.getMutagen(stem)
            if (!mutagen) return

            const stars = [mutagen.lu, mutagen.quan, mutagen.ke, mutagen.ji]
            stars.forEach((starName, idx) => {
                if (starName) {
                    const normalizedName = MutagenCore.normalizeStarName(starName)
                    if (!result[normalizedName]) result[normalizedName] = []
                    result[normalizedName].push({ scope, type: MUTAGEN_TYPES[idx] })
                }
            })
        }

        // 按层级添加运限四化
        if (horoscopeInfo.decadal) addMutagen('decadal', horoscopeInfo.decadal.heavenlyStem)
        if (horoscopeInfo.yearly) addMutagen('yearly', horoscopeInfo.yearly.heavenlyStem)
        if (horoscopeInfo.monthly) addMutagen('monthly', horoscopeInfo.monthly.heavenlyStem)
        if (horoscopeInfo.daily) addMutagen('daily', horoscopeInfo.daily.heavenlyStem)
        if (horoscopeInfo.hourly) addMutagen('hourly', horoscopeInfo.hourly.heavenlyStem)

        return Object.keys(result).length > 0 ? result : undefined
    }, [horoscopeInfo])

    // 获取宫位的运限重排宫名（叠宫显示）
    const getDynamicPalaceNames = (palaceIndex: number) => {
        if (!horoscopeInfo) return undefined
        const names: { decadal?: string; yearly?: string; monthly?: string; daily?: string; hourly?: string } = {}

        // 大限宫名：从大限命宫视角重排
        if (horoscopeInfo.decadal?.palaceNames && horoscopeInfo.decadal.palaceNames[palaceIndex]) {
            names.decadal = horoscopeInfo.decadal.palaceNames[palaceIndex]
        }
        // 流年宫名
        if (horoscopeInfo.yearly?.palaceNames && horoscopeInfo.yearly.palaceNames[palaceIndex]) {
            names.yearly = horoscopeInfo.yearly.palaceNames[palaceIndex]
        }
        // 流月宫名
        if (horoscopeInfo.monthly?.palaceNames && horoscopeInfo.monthly.palaceNames[palaceIndex]) {
            names.monthly = horoscopeInfo.monthly.palaceNames[palaceIndex]
        }
        // 流日宫名
        if (horoscopeInfo.daily?.palaceNames && horoscopeInfo.daily.palaceNames[palaceIndex]) {
            names.daily = horoscopeInfo.daily.palaceNames[palaceIndex]
        }
        // 流时宫名
        if (horoscopeInfo.hourly?.palaceNames && horoscopeInfo.hourly.palaceNames[palaceIndex]) {
            names.hourly = horoscopeInfo.hourly.palaceNames[palaceIndex]
        }

        return Object.keys(names).length > 0 ? names : undefined
    }

    // 生成命盘文字版本（用于复制）- 增强版，包含运限信息
    const generateChartText = useCallback(() => {
        const lines: string[] = []
        lines.push('【紫微斗数命盘】')
        lines.push(`阳历：${data.solarDate}`)
        lines.push(`农历：${data.lunarDate.year}年${Math.abs(data.lunarDate.month)}月${data.lunarDate.day}日`)
        lines.push(`四柱：${data.basicInfo.fourPillars.year.stem}${data.basicInfo.fourPillars.year.branch} ${data.basicInfo.fourPillars.month.stem}${data.basicInfo.fourPillars.month.branch} ${data.basicInfo.fourPillars.day.stem}${data.basicInfo.fourPillars.day.branch} ${data.basicInfo.fourPillars.hour.stem}${data.basicInfo.fourPillars.hour.branch}`)
        lines.push(`命主：${data.basicInfo.soul}  身主：${data.basicInfo.body}`)
        lines.push(`五行局：${data.basicInfo.fiveElement}`)
        lines.push(`属相：${data.basicInfo.zodiac}  星座：${data.basicInfo.constellation}`)
        lines.push('')

        // 本命四化
        if (data.mutagenInfo?.natal) {
            lines.push('【本命四化】')
            lines.push(`化禄：${data.mutagenInfo.natal.lu || '-'}  化权：${data.mutagenInfo.natal.quan || '-'}  化科：${data.mutagenInfo.natal.ke || '-'}  化忌：${data.mutagenInfo.natal.ji || '-'}`)
            lines.push('')
        }

        lines.push('【十二宫位】')

        data.palaces.forEach((palace) => {
            const bodyMark = palace.isBodyPalace ? '（身宫）' : ''
            const majorStars = palace.majorStars.map(s => {
                let str = s.name
                if (s.brightness) str += s.brightness
                if (s.mutagen?.length) str += `化${s.mutagen.join('')}`
                return str
            }).join('、') || '无主星'
            const minorStars = palace.minorStars.map(s => s.name + (s.brightness || '')).join('、')
            // 杂曜（参考MingAI）
            const adjStars = palace.adjStars?.map((s: { name: string }) => s.name).join('、')
            lines.push(`${palace.name}${bodyMark}（${palace.heavenlyStem}${palace.earthlyBranch}）`)
            lines.push(`  主星：${majorStars}`)
            if (minorStars) lines.push(`  辅星：${minorStars}`)
            if (adjStars) lines.push(`  杂曜：${adjStars}`)
        })

        // 大限信息
        if (data.decades && data.decades.length > 0) {
            lines.push('')
            lines.push('【大限排列】')
            data.decades.forEach(d => {
                lines.push(`${d.startAge}-${d.endAge}岁 ${d.heavenlyStem}${d.earthlyBranch} ${d.palaceName}`)
            })
        }

        // 当前运限高亮信息
        if (horoscopeInfo) {
            lines.push('')
            lines.push('【当前选中运限】')
            if (horoscopeInfo.decadal) {
                lines.push(`大限：${horoscopeInfo.decadal.heavenlyStem} (${horoscopeInfo.decadal.startAge}岁起)`)
            }
            if (horoscopeInfo.yearly) {
                lines.push(`流年：${horoscopeInfo.yearly.heavenlyStem}`)
            }
            if (horoscopeInfo.monthly) {
                lines.push(`流月：${horoscopeInfo.monthly.heavenlyStem}`)
            }
            if (horoscopeInfo.daily) {
                lines.push(`流日：${horoscopeInfo.daily.heavenlyStem}`)
            }
        }

        // 四化分布汇总（参考MingAI的ziwei-to-text.ts）
        lines.push('')
        lines.push('【四化分布】')
        const mutagenMap: Record<string, string[]> = {
            '禄': [], '权': [], '科': [], '忌': []
        }

        data.palaces.forEach((palace) => {
            ;[...palace.majorStars, ...palace.minorStars].forEach(star => {
                star.mutagen?.forEach(m => {
                    const key = m.replace(/[本限年月日]/g, '')  // 去掉前缀如"本"、"限"等
                    if (mutagenMap[key]) {
                        mutagenMap[key].push(`${star.name}(${palace.name})`)
                    }
                })
            })
        })

        Object.entries(mutagenMap).forEach(([key, stars]) => {
            if (stars.length > 0) {
                lines.push(`化${key}：${stars.join('、')}`)
            }
        })

        return lines.join('\n')
    }, [data, horoscopeInfo])

    // 复制命盘
    const handleCopy = async () => {
        const text = generateChartText()
        await navigator.clipboard.writeText(text)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    // 网格布局
    const gridLayout = [
        [5, 6, 7, 8],
        [4, -1, -1, 9],
        [3, -1, -1, 10],
        [2, 1, 0, 11],
    ]

    // 计算连线锚点
    const getAnchorPoint = (pos: { row: number; col: number }) => {
        const cellSize = 25
        const padding = 2
        const isTop = pos.row === 0
        const isBottom = pos.row === 3
        const isLeft = pos.col === 0
        const isRight = pos.col === 3
        const centerX = (pos.col + 0.5) * cellSize
        const centerY = (pos.row + 0.5) * cellSize

        if ((isTop && isLeft) || (isTop && isRight) || (isBottom && isLeft) || (isBottom && isRight)) {
            const x = isLeft ? (pos.col + 1) * cellSize - padding : pos.col * cellSize + padding
            const y = isTop ? (pos.row + 1) * cellSize - padding : pos.row * cellSize + padding
            return { x, y }
        }

        if (isTop) return { x: centerX, y: (pos.row + 1) * cellSize - padding }
        if (isBottom) return { x: centerX, y: pos.row * cellSize + padding }
        if (isLeft) return { x: (pos.col + 1) * cellSize - padding, y: centerY }
        if (isRight) return { x: pos.col * cellSize + padding, y: centerY }

        return { x: centerX, y: centerY }
    }

    const handlePalaceClick = (index: number) => {
        setSelectedPalace(selectedPalace === index ? null : index)
        onPalaceSelect?.(index)
    }

    const handlePalaceDoubleClick = (palace: EnhancedPalace) => {
        setDetailPalace(palace)
        setShowDetail(true)
    }

    return (
        <div className="w-full relative">
            {/* 工具栏 */}
            <div className="flex justify-between items-center gap-2 mb-2">
                {/* 飞星信息显示 */}
                {flyingStar && (
                    <div className="flex items-center gap-2 px-3 py-1.5 bg-amber-500/10 rounded-lg text-xs">
                        <Sparkles className="w-3 h-3 text-amber-500" />
                        <span className="text-amber-600 dark:text-amber-400 font-medium">
                            {flyingStar.sourceStem}{t('ziwei.flyingStar.title')}:
                        </span>
                        <span className="flex gap-1">
                            {flyingStar.targets.lu && <span className="text-green-500">{t('ziwei.flyingStar.lu')}→{flyingStar.targets.lu.star}</span>}
                            {flyingStar.targets.quan && <span className="text-red-500">{t('ziwei.flyingStar.quan')}→{flyingStar.targets.quan.star}</span>}
                            {flyingStar.targets.ke && <span className="text-blue-500">{t('ziwei.flyingStar.ke')}→{flyingStar.targets.ke.star}</span>}
                            {flyingStar.targets.ji && <span className="text-purple-500">{t('ziwei.flyingStar.ji')}→{flyingStar.targets.ji.star}</span>}
                        </span>
                        <button
                            onClick={() => setFlyingStar(null)}
                            className="ml-2 text-muted-foreground hover:text-foreground"
                        >
                            ✕
                        </button>
                    </div>
                )}
                <div className="flex gap-2 ml-auto">
                    <button
                        onClick={handleCopy}
                        className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs transition-colors ${copied
                            ? 'bg-green-500/10 text-green-500'
                            : 'bg-secondary text-muted-foreground hover:bg-secondary/80'
                            }`}
                    >
                        {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                        {copied ? t('ziwei.copied') : t('ziwei.copyChart')}
                    </button>
                    <button
                        onClick={() => setShowAdjStars(!showAdjStars)}
                        className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs transition-colors ${showAdjStars
                            ? 'bg-primary/10 text-primary'
                            : 'bg-secondary text-muted-foreground hover:bg-secondary/80'
                            }`}
                    >
                        {showAdjStars ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
                        {showAdjStars ? t('ziwei.hideAuxStars') : t('ziwei.showAuxStars')}
                    </button>
                </div>
            </div>
            {/* 三方四正连线SVG层 - 支持运限命宫 */}
            {sanFangSiZhengSource && (
                <svg
                    className="absolute inset-0 w-full h-full pointer-events-none z-10"
                    style={{ aspectRatio: '4/4' }}
                >
                    {(() => {
                        const sourcePalaceData = data.palaces[sanFangSiZhengSource.index]
                        if (!sourcePalaceData) return null

                        const sourceBranch = BRANCH_TO_INDEX[sourcePalaceData.earthlyBranch]
                        const sourcePos = POSITION_MAP[sourceBranch]
                        if (!sourcePos) return null

                        const startPoint = getAnchorPoint(sourcePos)

                        // 根据来源类型设置线条颜色（参考 react-iztro 配色）
                        const lineColor = sanFangSiZhengSource.type === 'decadal'
                            ? '#1890ff'  // 大限蓝色 (--iztro-color-decadal)
                            : sanFangSiZhengSource.type === 'yearly'
                                ? '#813359'  // 流年紫红色 (--iztro-color-yearly)
                                : '#d4380d'  // 默认橙红色 (--iztro-color-awesome)

                        return sanFangSiZhengIndexes.map((palaceIdx, i) => {
                            if (palaceIdx === sanFangSiZhengSource.index) return null
                            const palaceData = data.palaces[palaceIdx]
                            if (!palaceData) return null

                            const branch = BRANCH_TO_INDEX[palaceData.earthlyBranch]
                            const targetPos = POSITION_MAP[branch]
                            if (!targetPos) return null

                            const to = getAnchorPoint(targetPos)

                            return (
                                <line
                                    key={i}
                                    x1={`${startPoint.x}%`}
                                    y1={`${startPoint.y}%`}
                                    x2={`${to.x}%`}
                                    y2={`${to.y}%`}
                                    stroke={lineColor}
                                    strokeWidth="2"
                                    strokeOpacity="0.6"
                                    strokeDasharray="4,2"
                                />
                            )
                        })
                    })()}
                </svg>
            )}

            {/* 命盘网格 */}
            <div className="grid grid-cols-4 gap-1">
                {gridLayout.map((row, rowIdx) =>
                    row.map((branchIdx, colIdx) => {
                        // 中间区域
                        if (branchIdx === -1) {
                            if (rowIdx === 1 && colIdx === 1) {
                                return (
                                    <div
                                        key={`center-${rowIdx}-${colIdx}`}
                                        className="col-span-2 row-span-2 p-2 rounded-lg bg-gradient-to-br from-secondary/30 to-background/80 border border-border/50"
                                    >
                                        <div className="h-full flex flex-col justify-center space-y-1.5">
                                            {/* 四柱 - 优化显示 */}
                                            <div className="grid grid-cols-4 gap-0.5 text-center">
                                                {['year', 'month', 'day', 'hour'].map((key) => {
                                                    const pillar = data.basicInfo.fourPillars[key as keyof typeof data.basicInfo.fourPillars]
                                                    const labels = { year: '年柱', month: '月柱', day: '日柱', hour: '时柱' }
                                                    return (
                                                        <div key={key} className="bg-background/50 rounded p-1">
                                                            <div className="text-muted-foreground text-[8px] mb-0.5">
                                                                {labels[key as keyof typeof labels]}
                                                            </div>
                                                            <div className="text-sm font-bold leading-tight">
                                                                <span className={getStemColor(pillar.stem)}>{pillar.stem}</span>
                                                            </div>
                                                            <div className="text-sm font-bold leading-tight">
                                                                <span className={getBranchColor(pillar.branch)}>{pillar.branch}</span>
                                                            </div>
                                                        </div>
                                                    )
                                                })}
                                            </div>

                                            {/* 日期信息 */}
                                            <div className="text-center text-[10px] text-muted-foreground space-y-0.5">
                                                <div>阳历: {data.solarDate}</div>
                                                <div>农历: {data.lunarDate.year}年{Math.abs(data.lunarDate.month)}月{data.lunarDate.day}日</div>
                                            </div>

                                            {/* 命理信息 */}
                                            <div className="grid grid-cols-2 gap-1 text-[10px]">
                                                <div className="text-center">
                                                    <span className="text-muted-foreground">属相:</span>
                                                    <span className="ml-1 font-medium">{data.basicInfo.zodiac}</span>
                                                </div>
                                                <div className="text-center">
                                                    <span className="text-muted-foreground">星座:</span>
                                                    <span className="ml-1 font-medium">{data.basicInfo.constellation}</span>
                                                </div>
                                            </div>

                                            <div className="grid grid-cols-2 gap-1 text-[10px]">
                                                <div className="text-center">
                                                    <span className="text-muted-foreground">命主:</span>
                                                    <span className="ml-1 text-purple-500 font-semibold">{data.basicInfo.soul}</span>
                                                </div>
                                                <div className="text-center">
                                                    <span className="text-muted-foreground">身主:</span>
                                                    <span className="ml-1 text-amber-600 font-semibold">{data.basicInfo.body}</span>
                                                </div>
                                            </div>

                                            {/* 命宫/身宫地支 - 参考MingAI */}
                                            <div className="grid grid-cols-2 gap-1 text-[10px]">
                                                <div className="text-center">
                                                    <span className="text-muted-foreground">命宫:</span>
                                                    <span className="ml-1 text-primary font-semibold">
                                                        {data.palaces.find(p => p.name === '命宮' || p.name === '命宫')?.earthlyBranch || '-'}
                                                    </span>
                                                </div>
                                                <div className="text-center">
                                                    <span className="text-muted-foreground">身宫:</span>
                                                    <span className="ml-1 text-amber-500 font-semibold">
                                                        {data.palaces.find(p => p.isBodyPalace)?.earthlyBranch || '-'}
                                                    </span>
                                                </div>
                                            </div>

                                            {/* 五行局 */}
                                            <div className="text-center">
                                                <span className="px-2 py-0.5 rounded-full bg-primary/15 text-primary text-[10px] font-semibold">
                                                    {data.basicInfo.fiveElement}
                                                </span>
                                            </div>

                                            {/* 快捷切换按钮 */}
                                            {onHoroscopeDateChange && (
                                                <div className="mt-1 space-y-1">
                                                    {/* 大限/流年切换 */}
                                                    <div className="flex items-center justify-center gap-1">
                                                        <button
                                                            onClick={() => onHoroscopeDateChange('decadal', -10)}
                                                            className="px-1.5 py-0.5 text-[8px] rounded bg-purple-500/20 text-purple-600 hover:bg-purple-500/30 transition-colors"
                                                            title="前10年"
                                                        >
                                                            ◀10年
                                                        </button>
                                                        <button
                                                            onClick={() => onHoroscopeDateChange('yearly', -1)}
                                                            className="px-1.5 py-0.5 text-[8px] rounded bg-blue-500/20 text-blue-600 hover:bg-blue-500/30 transition-colors"
                                                            title="上一年"
                                                        >
                                                            ◀年
                                                        </button>
                                                        <button
                                                            onClick={() => onHoroscopeDateChange('yearly', 1)}
                                                            className="px-1.5 py-0.5 text-[8px] rounded bg-blue-500/20 text-blue-600 hover:bg-blue-500/30 transition-colors"
                                                            title="下一年"
                                                        >
                                                            年▶
                                                        </button>
                                                        <button
                                                            onClick={() => onHoroscopeDateChange('decadal', 10)}
                                                            className="px-1.5 py-0.5 text-[8px] rounded bg-purple-500/20 text-purple-600 hover:bg-purple-500/30 transition-colors"
                                                            title="后10年"
                                                        >
                                                            10年▶
                                                        </button>
                                                    </div>
                                                    {/* 流月/流日/流时切换 */}
                                                    <div className="flex items-center justify-center gap-1">
                                                        <button
                                                            onClick={() => onHoroscopeDateChange('monthly', -1)}
                                                            className="px-1.5 py-0.5 text-[8px] rounded bg-green-500/20 text-green-600 hover:bg-green-500/30 transition-colors"
                                                            title="上一月"
                                                        >
                                                            ◀月
                                                        </button>
                                                        <button
                                                            onClick={() => onHoroscopeDateChange('daily', -1)}
                                                            className="px-1.5 py-0.5 text-[8px] rounded bg-orange-500/20 text-orange-600 hover:bg-orange-500/30 transition-colors"
                                                            title="上一日"
                                                        >
                                                            ◀日
                                                        </button>
                                                        <button
                                                            onClick={() => onHoroscopeDateChange('daily', 1)}
                                                            className="px-1.5 py-0.5 text-[8px] rounded bg-orange-500/20 text-orange-600 hover:bg-orange-500/30 transition-colors"
                                                            title="下一日"
                                                        >
                                                            日▶
                                                        </button>
                                                        <button
                                                            onClick={() => onHoroscopeDateChange('monthly', 1)}
                                                            className="px-1.5 py-0.5 text-[8px] rounded bg-green-500/20 text-green-600 hover:bg-green-500/30 transition-colors"
                                                            title="下一月"
                                                        >
                                                            月▶
                                                        </button>
                                                    </div>
                                                    {/* 流时切换 */}
                                                    <div className="flex items-center justify-center gap-1">
                                                        <button
                                                            onClick={() => onHoroscopeDateChange('hourly', -1)}
                                                            className="px-1.5 py-0.5 text-[8px] rounded bg-cyan-500/20 text-cyan-600 hover:bg-cyan-500/30 transition-colors"
                                                            title="上一时"
                                                        >
                                                            ◀时
                                                        </button>
                                                        <span className="text-[8px] text-muted-foreground px-1">时辰</span>
                                                        <button
                                                            onClick={() => onHoroscopeDateChange('hourly', 1)}
                                                            className="px-1.5 py-0.5 text-[8px] rounded bg-cyan-500/20 text-cyan-600 hover:bg-cyan-500/30 transition-colors"
                                                            title="下一时"
                                                        >
                                                            时▶
                                                        </button>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                )
                            }
                            return null
                        }

                        const palace = getPalaceByBranch(branchIdx)
                        if (!palace) return null

                        const palaceIndex = data.palaces.indexOf(palace)
                        const highlightTypes = getHighlightTypes(palaceIndex)
                        const flowInfo = getFlowInfoForPalace(palaceIndex)
                        const flyingTypes = getFlyingStarHighlight(palaceIndex)
                        const dynamicNames = getDynamicPalaceNames(palaceIndex)
                        const horoscopeMutagens = getHoroscopeMutagensForPalace(palaceIndex)

                        return (
                            <PalaceCard
                                key={`palace-${branchIdx}`}
                                palace={palace}
                                palaceIndex={palaceIndex}
                                isSelected={selectedPalace === palaceIndex}
                                isMingGong={palaceIndex === mingGongIndex}
                                isSanFangSiZheng={sanFangSiZhengIndexes.includes(palaceIndex) && selectedPalace !== palaceIndex}
                                highlightTypes={highlightTypes}
                                flowInfo={flowInfo}
                                dynamicPalaceNames={dynamicNames}
                                horoscopeMutagens={horoscopeMutagens}
                                showAdjStars={showAdjStars}
                                flyingStarTypes={flyingTypes}
                                isFlyingSource={isFlyingSourcePalace(palaceIndex)}
                                isHoverPreview={!flyingStar && hoverFlyingStar?.sourcePalace === palaceIndex}
                                onStemClick={(e) => handleStemClick(palaceIndex, palace.heavenlyStem, e)}
                                onStemHover={() => handleStemHover(palaceIndex, palace.heavenlyStem)}
                                onStemLeave={handleStemLeave}
                                onClick={() => handlePalaceClick(palaceIndex)}
                                onDoubleClick={() => handlePalaceDoubleClick(palace)}
                            />
                        )
                    })
                )}
            </div>

            {/* 宫位详情弹窗 */}
            <PalaceDetailDialog
                palace={detailPalace}
                open={showDetail}
                onOpenChange={setShowDetail}
            />
        </div>
    )
}
