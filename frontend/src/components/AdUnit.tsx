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
import { useGlobalState } from '@/store'

interface AdUnitProps {
    slot: string
    format?: 'auto' | 'fluid' | 'rectangle' | 'horizontal' | 'vertical'
    responsive?: boolean
    className?: string
    style?: React.CSSProperties
    lazyLoad?: boolean
    lazyOffset?: number
}

declare global {
    interface Window {
        adsbygoogle: any[]
    }
}

// 默认的AdSense发布商ID（可通过后端配置覆盖）
const DEFAULT_AD_CLIENT = 'ca-pub-1821747886980667'

export function AdUnit({
    slot,
    format = 'auto',
    responsive = true,
    className = '',
    style,
    lazyLoad = true,
    lazyOffset = 200
}: AdUnitProps) {
    const adRef = useRef<HTMLDivElement>(null)
    const [isVisible, setIsVisible] = useState(!lazyLoad)
    const [adLoaded, setAdLoaded] = useState(false)
    const { settings } = useGlobalState()

    // 优先使用后端配置的ad_client，否则使用默认值
    const adClient = settings.ad_client || DEFAULT_AD_CLIENT

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

    const getFormatStyle = (): React.CSSProperties => {
        switch (format) {
            case 'rectangle':
                return { minWidth: '300px', minHeight: '250px' }
            case 'horizontal':
                return { minWidth: '728px', minHeight: '90px' }
            case 'vertical':
                return { minWidth: '160px', minHeight: '600px' }
            case 'fluid':
                return { width: '100%' }
            default:
                return {}
        }
    }

    return (
        <div
            ref={adRef}
            className={`ad-container overflow-hidden ${className}`}
            style={{
                ...getFormatStyle(),
                ...style
            }}
        >
            {isVisible && (
                <ins
                    className="adsbygoogle"
                    style={{ display: 'block', ...style }}
                    data-ad-client={adClient}
                    data-ad-slot={slot}
                    data-ad-format={format}
                    data-full-width-responsive={responsive ? 'true' : 'false'}
                />
            )}
        </div>
    )
}

export function InArticleAd({ className = '' }: { className?: string }) {
    return (
        <div className={`my-6 ${className}`}>
            <div className="text-center text-xs text-muted-foreground mb-1">广告</div>
            <AdUnit
                slot="YOUR_IN_ARTICLE_SLOT"
                format="fluid"
                lazyLoad={true}
                className="rounded-lg overflow-hidden"
            />
        </div>
    )
}

export function SidebarAd({ className = '' }: { className?: string }) {
    return (
        <div className={`sticky top-20 ${className}`}>
            <div className="text-center text-xs text-muted-foreground mb-1">广告</div>
            <AdUnit
                slot="YOUR_SIDEBAR_SLOT"
                format="vertical"
                responsive={false}
                lazyLoad={true}
                style={{ minWidth: '160px', minHeight: '600px' }}
            />
        </div>
    )
}

export function BannerAd({ className = '' }: { className?: string }) {
    return (
        <div className={`w-full ${className}`}>
            <AdUnit
                slot="YOUR_BANNER_SLOT"
                format="horizontal"
                responsive={true}
                lazyLoad={true}
            />
        </div>
    )
}

export function ResponsiveAd({ className = '' }: { className?: string }) {
    return (
        <div className={`w-full my-4 ${className}`}>
            <AdUnit
                slot="YOUR_RESPONSIVE_SLOT"
                format="auto"
                responsive={true}
                lazyLoad={true}
            />
        </div>
    )
}
