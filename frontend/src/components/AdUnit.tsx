/**
 * Google AdSense 广告单元组件
 * 支持延迟加载、响应式尺寸、内容流插入
 * 
 * 配置说明：
 * 1. 在 Google AdSense 后台创建广告单元后获取 slot ID
 * 2. 将下方的 "YOUR_XXX_SLOT" 替换为实际的广告位 slot ID
 * 3. data-ad-client 已配置为项目的 AdSense 发布商 ID
 * 
 * 使用示例：
 * <AdUnit slot="1234567890" format="auto" />
 * <InArticleAd /> - 文章内嵌广告
 * <ResponsiveAd /> - 响应式广告
 */

import { useEffect, useRef, useState } from 'react'
import { logger } from '@/utils/logger'

interface AdUnitProps {
    slot: string
    format?: 'auto' | 'fluid' | 'rectangle' | 'horizontal' | 'vertical'
    responsive?: boolean
    className?: string
    lazyLoad?: boolean
    lazyOffset?: number
}

declare global {
    interface Window {
        adsbygoogle: any[]
    }
}

// 默认的AdSense发布商ID（可通过环境变量 VITE_AD_CLIENT 覆盖）
const DEFAULT_AD_CLIENT = 'ca-pub-1821747886980667'

// 获取 AdSense 发布商 ID：优先使用环境变量，否则使用默认值
function getAdClient(): string {
    const envAdClient = import.meta.env.VITE_AD_CLIENT
    if (envAdClient && envAdClient !== '' && !envAdClient.includes('VITE_')) {
        return envAdClient
    }
    return DEFAULT_AD_CLIENT
}

export function AdUnit({
    slot,
    format = 'auto',
    responsive = true,
    className = '',
    lazyLoad = true,
    lazyOffset = 200
}: AdUnitProps) {
    const adRef = useRef<HTMLDivElement>(null)
    const [isVisible, setIsVisible] = useState(!lazyLoad)
    const [adLoaded, setAdLoaded] = useState(false)

    // 使用环境变量配置的 ad_client，否则使用默认值
    const adClient = getAdClient()

    useEffect(() => {
        if (!lazyLoad) {
            setIsVisible(true)
            return
        }

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        setIsVisible(true)
                        observer.disconnect()
                    }
                })
            },
            {
                rootMargin: `${lazyOffset}px`,
                threshold: 0
            }
        )

        if (adRef.current) {
            observer.observe(adRef.current)
        }

        return () => observer.disconnect()
    }, [lazyLoad, lazyOffset])

    useEffect(() => {
        if (!isVisible || adLoaded) return

        const loadAd = () => {
            try {
                if (window.adsbygoogle && adRef.current) {
                    (window.adsbygoogle = window.adsbygoogle || []).push({})
                    setAdLoaded(true)
                }
            } catch (error) {
                logger.warn('AdSense loading error:', error)
            }
        }

        const timer = setTimeout(loadAd, 100)
        return () => clearTimeout(timer)
    }, [isVisible, adLoaded])

    // 根据格式返回对应的 Tailwind 类（移动端友好）
    const getFormatClass = (): string => {
        switch (format) {
            case 'rectangle':
                // 移动端自适应，桌面端保持最小尺寸
                return 'w-full md:min-w-[300px] min-h-[250px]'
            case 'horizontal':
                // 移动端全宽，桌面端保持横幅尺寸
                return 'w-full md:min-w-[728px] min-h-[90px]'
            case 'vertical':
                // 侧边栏广告仅桌面端显示，所以可以保持固定尺寸
                return 'min-w-[160px] min-h-[600px]'
            case 'fluid':
                return 'w-full'
            default:
                return 'w-full'
        }
    }

    // 判断是否使用自动广告（slot 为 auto 或空时）
    const isAutoAd = !slot || slot === 'auto'

    return (
        <div
            ref={adRef}
            className={`ad-container overflow-hidden ${getFormatClass()} ${className}`}
        >
            {isVisible && (
                <ins
                    className="adsbygoogle block"
                    data-ad-client={adClient}
                    // 自动广告不需要 slot，手动广告需要具体 slot ID
                    {...(!isAutoAd && { 'data-ad-slot': slot })}
                    data-ad-format={format}
                    data-full-width-responsive={responsive ? 'true' : 'false'}
                />
            )}
        </div>
    )
}

/**
 * 内容区广告 - 适合放在文章/结果内容之间
 * 移动端友好，自动响应式调整
 */
export function ContentAd({ className = '' }: { className?: string }) {
    return (
        <div className={`w-full my-6 ${className}`}>
            <div className="relative">
                {/* 广告标识 - 小巧不突兀 */}
                <div className="text-center text-[10px] text-muted-foreground/60 mb-1">广告</div>
                <AdUnit
                    slot="auto"
                    format="auto"
                    responsive={true}
                    lazyLoad={true}
                    className="rounded-lg overflow-hidden max-w-full"
                />
            </div>
        </div>
    )
}

/**
 * 结果页广告 - 放在占卜结果下方
 * 有适当间距，不影响阅读
 */
export function ResultAd({ className = '' }: { className?: string }) {
    return (
        <div className={`w-full mt-8 pt-6 border-t border-border/50 ${className}`}>
            <div className="text-center text-[10px] text-muted-foreground/50 mb-2">— 广告 —</div>
            <AdUnit
                slot="auto"
                format="fluid"
                responsive={true}
                lazyLoad={true}
                className="rounded-lg overflow-hidden"
            />
        </div>
    )
}

/**
 * 页面分隔广告 - 放在页面模块之间
 * 有明显分隔，视觉上独立
 */
export function SectionAd({ className = '' }: { className?: string }) {
    return (
        <div className={`w-full py-4 ${className}`}>
            <div className="max-w-2xl mx-auto">
                <div className="text-center text-[10px] text-muted-foreground/50 mb-1">广告</div>
                <AdUnit
                    slot="auto"
                    format="auto"
                    responsive={true}
                    lazyLoad={true}
                    className="rounded-lg overflow-hidden"
                />
            </div>
        </div>
    )
}

/**
 * 文章内嵌广告 - 适合长文内容
 */
export function InArticleAd({ className = '' }: { className?: string }) {
    return (
        <div className={`my-6 ${className}`}>
            <div className="text-center text-[10px] text-muted-foreground/50 mb-1">广告</div>
            <AdUnit
                slot="auto"
                format="fluid"
                lazyLoad={true}
                className="rounded-lg overflow-hidden"
            />
        </div>
    )
}

/**
 * 侧边栏广告 - 仅桌面端显示
 */
export function SidebarAd({ className = '' }: { className?: string }) {
    return (
        <div className={`hidden lg:block sticky top-24 ${className}`}>
            <div className="text-center text-[10px] text-muted-foreground/50 mb-1">广告</div>
            <AdUnit
                slot="auto"
                format="vertical"
                responsive={false}
                lazyLoad={true}
            />
        </div>
    )
}

/**
 * 横幅广告 - 页面顶部/底部
 */
export function BannerAd({ className = '' }: { className?: string }) {
    return (
        <div className={`w-full ${className}`}>
            <AdUnit
                slot="auto"
                format="horizontal"
                responsive={true}
                lazyLoad={true}
            />
        </div>
    )
}

/**
 * 响应式广告 - 通用场景
 */
export function ResponsiveAd({ className = '' }: { className?: string }) {
    return (
        <div className={`w-full my-4 ${className}`}>
            <AdUnit
                slot="auto"
                format="auto"
                responsive={true}
                lazyLoad={true}
            />
        </div>
    )
}
