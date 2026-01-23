import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { logger } from '@/utils/logger'
import { Star, Heart, Briefcase, TrendingUp, Activity, Calendar, Users } from 'lucide-react'
import { ZodiacIcon } from '@/components/ZodiacIcons'

const API_BASE = import.meta.env.VITE_API_BASE || ''

const ZODIACS = [
    { name: '白羊座', symbol: '♈', dates: '3.21-4.19' },
    { name: '金牛座', symbol: '♉', dates: '4.20-5.20' },
    { name: '双子座', symbol: '♊', dates: '5.21-6.20' },
    { name: '巨蟹座', symbol: '♋', dates: '6.21-7.22' },
    { name: '狮子座', symbol: '♌', dates: '7.23-8.22' },
    { name: '处女座', symbol: '♍', dates: '8.23-9.22' },
    { name: '天秤座', symbol: '♎', dates: '9.23-10.22' },
    { name: '天蝎座', symbol: '♏', dates: '10.23-11.21' },
    { name: '射手座', symbol: '♐', dates: '11.22-12.21' },
    { name: '摩羯座', symbol: '♑', dates: '12.22-1.19' },
    { name: '水瓶座', symbol: '♒', dates: '1.20-2.18' },
    { name: '双鱼座', symbol: '♓', dates: '2.19-3.20' },
]

interface FortuneData {
    zodiac: string
    date: string
    scores: {
        overall: number
        love: number
        career: number
        wealth: number
        health: number
    }
    lucky_number: number[]
    lucky_color: string
    advice: string[]
}

interface CompatibilityData {
    zodiac1: string
    zodiac2: string
    overall_score: number
    scores: {
        love: number
        friendship: number
        work: number
        communication: number
    }
    rating: string
    advice: string[]
}

type TabType = 'fortune' | 'compatibility' | 'info'

export default function ZodiacPage() {
    const { t } = useTranslation()
    const [activeTab, setActiveTab] = useState<TabType>('fortune')
    const [selectedZodiac, setSelectedZodiac] = useState<string>('白羊座')
    const [selectedZodiac2, setSelectedZodiac2] = useState<string>('狮子座')
    const [fortune, setFortune] = useState<FortuneData | null>(null)
    const [compatibility, setCompatibility] = useState<CompatibilityData | null>(null)
    const [zodiacInfo, setZodiacInfo] = useState<any>(null)
    const [loading, setLoading] = useState(false)

    const fetchDailyFortune = async (zodiac: string) => {
        setLoading(true)
        try {
            const res = await fetch(`${API_BASE}/api/zodiac/fortune/daily/${encodeURIComponent(zodiac)}`)
            if (res.ok) {
                const data = await res.json()
                setFortune(data)
            }
        } catch (e) {
            logger.error('获取运势失败:', e)
        } finally {
            setLoading(false)
        }
    }

    const fetchCompatibility = async (z1: string, z2: string) => {
        setLoading(true)
        try {
            const res = await fetch(
                `${API_BASE}/api/zodiac/compatibility?zodiac1=${encodeURIComponent(z1)}&zodiac2=${encodeURIComponent(z2)}`
            )
            if (res.ok) {
                const data = await res.json()
                setCompatibility(data)
            }
        } catch (e) {
            logger.error('获取配对失败:', e)
        } finally {
            setLoading(false)
        }
    }

    const fetchZodiacInfo = async (zodiac: string) => {
        setLoading(true)
        try {
            const res = await fetch(`${API_BASE}/api/zodiac/info/${encodeURIComponent(zodiac)}`)
            if (res.ok) {
                const data = await res.json()
                setZodiacInfo(data)
            }
        } catch (e) {
            logger.error('获取星座信息失败:', e)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        if (activeTab === 'fortune') {
            fetchDailyFortune(selectedZodiac)
        } else if (activeTab === 'compatibility') {
            fetchCompatibility(selectedZodiac, selectedZodiac2)
        } else if (activeTab === 'info') {
            fetchZodiacInfo(selectedZodiac)
        }
    }, [activeTab, selectedZodiac, selectedZodiac2])

    const scoreItems = [
        { key: 'overall', label: t('zodiac.overall'), icon: Star, color: 'text-yellow-500' },
        { key: 'love', label: t('zodiac.love'), icon: Heart, color: 'text-pink-500' },
        { key: 'career', label: t('zodiac.career'), icon: Briefcase, color: 'text-blue-500' },
        { key: 'wealth', label: t('zodiac.wealth'), icon: TrendingUp, color: 'text-green-500' },
        { key: 'health', label: t('zodiac.health'), icon: Activity, color: 'text-red-500' },
    ]

    return (
        <div className="space-y-6">
            <div className="max-w-2xl mx-auto">
                <h1 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-6">
                    {t('zodiac.title')}
                </h1>

                {/* Tab切换 */}
                <div className="flex gap-2 mb-6 justify-center flex-wrap">
                    {[
                        { id: 'fortune', label: t('zodiac.dailyFortune'), icon: Calendar },
                        { id: 'compatibility', label: t('zodiac.compatibility'), icon: Users },
                        { id: 'info', label: t('zodiac.info'), icon: Star },
                    ].map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id as TabType)}
                            className={`flex items-center gap-1.5 px-4 py-2 rounded-md text-sm font-medium transition-colors ${activeTab === tab.id
                                ? 'bg-primary text-primary-foreground'
                                : 'bg-secondary text-secondary-foreground hover:bg-accent'
                                }`}
                        >
                            <tab.icon className="w-4 h-4" />
                            {tab.label}
                        </button>
                    ))}
                </div>

                {/* 星座选择器 */}
                <div className="grid grid-cols-4 sm:grid-cols-6 gap-2 mb-6">
                    {ZODIACS.map((z) => (
                        <button
                            key={z.name}
                            onClick={() => setSelectedZodiac(z.name)}
                            className={`flex flex-col items-center p-2 rounded-xl transition-all duration-300 ${selectedZodiac === z.name
                                ? 'bg-gradient-to-br from-primary/20 to-primary/10 ring-2 ring-primary shadow-lg scale-105'
                                : 'bg-secondary/50 text-secondary-foreground hover:bg-accent hover:scale-102 border border-border/50 hover:border-primary/30'
                                }`}
                        >
                            <ZodiacIcon zodiac={z.name} size={36} className="transition-transform duration-300 hover:scale-110" />
                            <span className={`text-xs mt-1 font-medium ${selectedZodiac === z.name ? 'text-primary' : ''}`}>
                                {z.name.replace('座', '')}
                            </span>
                        </button>
                    ))}
                </div>

                {/* 配对时显示第二个星座选择器 */}
                {activeTab === 'compatibility' && (
                    <div className="mb-6">
                        <p className="text-muted-foreground text-center text-sm mb-2">{t('zodiac.selectPairZodiac')}</p>
                        <div className="grid grid-cols-4 sm:grid-cols-6 gap-2">
                            {ZODIACS.map((z) => (
                                <button
                                    key={z.name}
                                    onClick={() => setSelectedZodiac2(z.name)}
                                    className={`flex flex-col items-center p-2 rounded-xl transition-all duration-300 ${selectedZodiac2 === z.name
                                        ? 'bg-gradient-to-br from-pink-500/20 to-pink-500/10 ring-2 ring-pink-500 shadow-lg scale-105'
                                        : 'bg-secondary/50 text-secondary-foreground hover:bg-accent hover:scale-102 border border-border/50 hover:border-pink-500/30'
                                        }`}
                                >
                                    <ZodiacIcon zodiac={z.name} size={36} className="transition-transform duration-300 hover:scale-110" />
                                    <span className={`text-xs mt-1 font-medium ${selectedZodiac2 === z.name ? 'text-pink-500' : ''}`}>
                                        {z.name.replace('座', '')}
                                    </span>
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* 内容区域 */}
                {loading ? (
                    <div className="flex justify-center py-12">
                        <div className="animate-spin rounded-full h-10 w-10 border-2 border-muted border-t-foreground" />
                    </div>
                ) : (
                    <div className="rounded-xl border border-border bg-card p-6">
                        {/* 今日运势 */}
                        {activeTab === 'fortune' && fortune && (
                            <div className="space-y-6">
                                <div className="text-center">
                                    <h2 className="text-xl font-bold text-foreground">{fortune.zodiac}</h2>
                                    <p className="text-muted-foreground text-sm">{fortune.date}</p>
                                </div>

                                <div className="space-y-4">
                                    {scoreItems.map((item) => {
                                        const score = fortune.scores[item.key as keyof typeof fortune.scores]
                                        return (
                                            <div key={item.key} className="space-y-1">
                                                <div className="flex items-center justify-between text-sm">
                                                    <div className="flex items-center gap-2">
                                                        <item.icon className={`w-4 h-4 ${item.color}`} />
                                                        <span className="text-foreground">{item.label}</span>
                                                    </div>
                                                    <span className="text-foreground font-bold">{score}{t('zodiac.score')}</span>
                                                </div>
                                                <div className="h-2 bg-secondary rounded-full overflow-hidden">
                                                    <div
                                                        style={{ width: `${score}%` }}
                                                        className={`h-full rounded-full transition-all duration-500 ${score >= 80 ? 'bg-chart-2' : score >= 60 ? 'bg-chart-4' : 'bg-destructive'}`}
                                                    />
                                                </div>
                                            </div>
                                        )
                                    })}
                                </div>

                                <div className="grid grid-cols-2 gap-4 pt-4 border-t border-border">
                                    <div className="text-center">
                                        <p className="text-muted-foreground text-xs">{t('zodiac.luckyNumber')}</p>
                                        <p className="text-foreground font-bold">{fortune.lucky_number?.join(', ')}</p>
                                    </div>
                                    <div className="text-center">
                                        <p className="text-muted-foreground text-xs">{t('zodiac.luckyColor')}</p>
                                        <p className="text-foreground font-bold">{fortune.lucky_color}</p>
                                    </div>
                                </div>

                                {fortune.advice && fortune.advice.length > 0 && (
                                    <div className="pt-4 border-t border-border">
                                        <p className="text-muted-foreground text-xs mb-2">{t('zodiac.todayAdvice')}</p>
                                        <ul className="space-y-1">
                                            {fortune.advice.map((a, i) => (
                                                <li key={i} className="text-foreground text-sm">• {a}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* 星座配对 */}
                        {activeTab === 'compatibility' && compatibility && (
                            <div className="space-y-6">
                                <div className="text-center">
                                    <div className="flex items-center justify-center gap-4">
                                        <ZodiacIcon zodiac={compatibility.zodiac1} size={48} className="drop-shadow-lg" />
                                        <Heart className="w-8 h-8 text-pink-500 animate-pulse" />
                                        <ZodiacIcon zodiac={compatibility.zodiac2} size={48} className="drop-shadow-lg" />
                                    </div>
                                    <p className="text-foreground mt-3 font-medium">
                                        {compatibility.zodiac1} & {compatibility.zodiac2}
                                    </p>
                                </div>

                                <div className="text-center">
                                    <div className="text-5xl font-bold text-foreground">
                                        {compatibility.overall_score}{t('zodiac.score')}
                                    </div>
                                    <p className="text-muted-foreground mt-1">{compatibility.rating}</p>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    {[
                                        { key: 'love', label: t('zodiac.loveIndex') },
                                        { key: 'friendship', label: t('zodiac.friendshipIndex') },
                                        { key: 'work', label: t('zodiac.workIndex') },
                                        { key: 'communication', label: t('zodiac.communicationIndex') },
                                    ].map((item) => (
                                        <div key={item.key} className="bg-secondary rounded-lg p-3 text-center">
                                            <p className="text-muted-foreground text-xs">{item.label}</p>
                                            <p className="text-foreground font-bold text-lg">
                                                {compatibility.scores[item.key as keyof typeof compatibility.scores]}{t('zodiac.score')}
                                            </p>
                                        </div>
                                    ))}
                                </div>

                                {compatibility.advice && compatibility.advice.length > 0 && (
                                    <div className="pt-4 border-t border-border">
                                        <p className="text-muted-foreground text-xs mb-2">{t('zodiac.pairAdvice')}</p>
                                        <ul className="space-y-1">
                                            {compatibility.advice.map((a, i) => (
                                                <li key={i} className="text-foreground text-sm">• {a}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* 星座详情 */}
                        {activeTab === 'info' && zodiacInfo && (
                            <div className="space-y-6">
                                <div className="text-center">
                                    <div className="flex justify-center mb-2">
                                        <ZodiacIcon zodiac={zodiacInfo.name} size={72} className="drop-shadow-xl" />
                                    </div>
                                    <h2 className="text-xl font-bold text-foreground mt-2">{zodiacInfo.name}</h2>
                                    <p className="text-muted-foreground">{zodiacInfo.english}</p>
                                    <p className="text-muted-foreground text-sm">{zodiacInfo.date_range}</p>
                                </div>

                                <div className="grid grid-cols-3 gap-4 text-center">
                                    <div className="bg-secondary rounded-lg p-3">
                                        <p className="text-muted-foreground text-xs">{t('zodiac.element')}</p>
                                        <p className="text-foreground font-bold">{zodiacInfo.element}象</p>
                                    </div>
                                    <div className="bg-secondary rounded-lg p-3">
                                        <p className="text-muted-foreground text-xs">{t('zodiac.quality')}</p>
                                        <p className="text-foreground font-bold">{zodiacInfo.quality}</p>
                                    </div>
                                    <div className="bg-secondary rounded-lg p-3">
                                        <p className="text-muted-foreground text-xs">{t('zodiac.ruler')}</p>
                                        <p className="text-foreground font-bold">{zodiacInfo.ruler}</p>
                                    </div>
                                </div>

                                <div className="space-y-4">
                                    <div>
                                        <p className="text-muted-foreground text-xs mb-2">{t('zodiac.traits')}</p>
                                        <div className="flex flex-wrap gap-2">
                                            {zodiacInfo.traits?.map((t: string, i: number) => (
                                                <span key={i} className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full text-sm">
                                                    {t}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    <div>
                                        <p className="text-muted-foreground text-xs mb-2">{t('zodiac.strengths')}</p>
                                        <div className="flex flex-wrap gap-2">
                                            {zodiacInfo.strengths?.map((s: string, i: number) => (
                                                <span key={i} className="px-3 py-1 bg-chart-2/20 text-chart-2 rounded-full text-sm">
                                                    {s}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    <div>
                                        <p className="text-muted-foreground text-xs mb-2">{t('zodiac.weaknesses')}</p>
                                        <div className="flex flex-wrap gap-2">
                                            {zodiacInfo.weaknesses?.map((w: string, i: number) => (
                                                <span key={i} className="px-3 py-1 bg-destructive/20 text-destructive rounded-full text-sm">
                                                    {w}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}
