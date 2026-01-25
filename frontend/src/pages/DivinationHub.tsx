import { Suspense, lazy } from 'react'
import { useSmoothScroll, useScrollSpy } from '@/hooks'
import { DIVINATION_OPTIONS } from '@/config/constants'
import { SectionAd } from '@/components/AdUnit'

const TarotModule = lazy(() => import('@/pages/divination/TarotPage'))
const XiaoLiuRenModule = lazy(() => import('@/pages/divination/XiaoLiuRenPage'))
const BirthdayModule = lazy(() => import('@/pages/divination/BirthdayPage'))
const NewNameModule = lazy(() => import('@/pages/divination/NewNamePage'))
const NameModule = lazy(() => import('@/pages/divination/NamePage'))
const DreamModule = lazy(() => import('@/pages/divination/DreamPage'))
const PlumFlowerModule = lazy(() => import('@/pages/divination/PlumFlowerPage'))
const FateModule = lazy(() => import('@/pages/divination/FatePage'))
const ChouqianModule = lazy(() => import('@/pages/Chouqian'))
const LiuyaoModule = lazy(() => import('@/features/liuyao'))
const LaohuangliModule = lazy(() => import('@/pages/divination/LaohuangliPage'))
const ZodiacModule = lazy(() => import('@/pages/divination/ZodiacPage'))
const DailyFortuneModule = lazy(() => import('@/pages/divination/DailyFortunePage'))
const MonthlyFortuneModule = lazy(() => import('@/pages/divination/MonthlyFortunePage'))

const moduleMap: Record<string, React.LazyExoticComponent<React.ComponentType<any>>> = {
    tarot: TarotModule,
    xiaoliu: XiaoLiuRenModule,
    birthday: BirthdayModule,
    new_name: NewNameModule,
    name: NameModule,
    dream: DreamModule,
    plum_flower: PlumFlowerModule,
    fate: FateModule,
    chouqian: ChouqianModule,
    liuyao: LiuyaoModule,
    laohuangli: LaohuangliModule,
    zodiac: ZodiacModule,
    daily: DailyFortuneModule,
    monthly: MonthlyFortuneModule,
}

const LoadingFallback = () => (
    <div className="flex items-center justify-center py-12">
        <div className="text-center space-y-4">
            <div className="animate-spin rounded-full h-10 w-10 border-2 border-muted border-t-foreground mx-auto"></div>
            <p className="text-sm text-muted-foreground">加载中...</p>
        </div>
    </div>
)

export default function DivinationHub() {
    const { scrollToAnchor } = useSmoothScroll()
    const sectionIds = DIVINATION_OPTIONS.map(opt => opt.key)
    const activeSection = useScrollSpy(sectionIds)

    return (
        <div className="space-y-8">
            {/* Hero Banner */}
            <section className="text-center py-12 md:py-16">
                <h1 className="text-4xl md:text-5xl font-bold mb-4 text-foreground">
                    占卜中心
                </h1>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                    融合传统智慧与人工智能，探索命运的奥秘
                </p>
            </section>

            {/* Sticky Tab Navigation */}
            <div className="sticky top-16 z-40 bg-background/95 backdrop-blur-sm border-b border-border -mx-4 px-4 md:-mx-6 md:px-6">
                <div className="flex items-center gap-1 overflow-x-auto scrollbar-hide py-3">
                    {DIVINATION_OPTIONS.map((option) => {
                        const Icon = option.icon
                        const isActive = activeSection === option.key
                        return (
                            <button
                                key={option.key}
                                onClick={() => scrollToAnchor(option.key)}
                                className={`
                                    flex items-center gap-2 px-4 py-2 rounded-md whitespace-nowrap transition-colors text-sm font-medium
                                    ${isActive
                                        ? 'bg-primary text-primary-foreground'
                                        : 'hover:bg-accent text-muted-foreground'
                                    }
                                `}
                            >
                                <Icon className="h-4 w-4" />
                                <span>{option.label}</span>
                            </button>
                        )
                    })}
                </div>
            </div>

            {/* Divination Modules */}
            <div className="space-y-12">
                {DIVINATION_OPTIONS.map((option) => {
                    const ModuleComponent = moduleMap[option.key]
                    if (!ModuleComponent) return null

                    return (
                        <section
                            key={option.key}
                            id={option.key}
                            className="scroll-mt-32"
                        >
                            {/* Section Header */}
                            <div className="flex items-center mb-6">
                                <div className="flex-1 h-px bg-border"></div>
                                <div className="flex items-center gap-2 mx-4">
                                    {option.icon && <option.icon className="h-5 w-5 text-muted-foreground" />}
                                    <h2 className="text-xl font-semibold text-foreground">{option.title}</h2>
                                </div>
                                <div className="flex-1 h-px bg-border"></div>
                            </div>
                            <p className="text-center text-muted-foreground text-sm mb-6">{option.description}</p>

                            {/* Module Card */}
                            <div className="rounded-xl border border-border bg-card p-6 md:p-8">
                                <Suspense fallback={<LoadingFallback />}>
                                    <ModuleComponent />
                                </Suspense>
                            </div>
                        </section>
                    )
                })}
            </div>

            {/* 广告位 - 在运势科普前 */}
            <SectionAd className="my-8" />

            {/* Knowledge Section */}
            <section id="knowledge" className="scroll-mt-32 py-12">
                <div className="flex items-center mb-8">
                    <div className="flex-1 h-px bg-border"></div>
                    <h2 className="text-xl font-semibold mx-4 text-foreground">运势科普</h2>
                    <div className="flex-1 h-px bg-border"></div>
                </div>
                <p className="text-center text-muted-foreground text-sm mb-8">了解各种占卜方式的起源与含义</p>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {[
                        { title: '塔罗牌', desc: '探索内心，洞察未来可能性的西方占卜工具' },
                        { title: '生辰八字', desc: '揭示命运轨迹的传统命理学方法' },
                        { title: '小六壬', desc: '简便快捷的六神预测术' },
                        { title: '梅花易数', desc: '基于易经的古老占卜方法' },
                        { title: '周公解梦', desc: '解读梦境含义的传统智慧' },
                        { title: '姓名五格', desc: '分析姓名对运势影响的命理系统' },
                    ].map((item, i) => (
                        <div key={i} className="p-5 rounded-xl border border-border bg-card hover:border-muted-foreground transition-colors">
                            <h3 className="text-base font-semibold mb-2 text-foreground">{item.title}</h3>
                            <p className="text-sm text-muted-foreground leading-relaxed">{item.desc}</p>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    )
}
