/**
 * SEO 头部组件
 * 用于动态设置页面的 title、description 和 OpenGraph 标签
 */

import { useEffect } from 'react'

interface SEOHeadProps {
    title?: string
    description?: string
    keywords?: string
    ogImage?: string
    ogType?: 'website' | 'article'
    canonicalUrl?: string
    noIndex?: boolean
}

const BASE_TITLE = 'AI 占卜 - 智能命理解析'
const BASE_DESCRIPTION = 'AI智能占卜平台，提供塔罗牌、生辰八字、紫微斗数、周公解梦、姓名测算等专业命理服务，结合传统文化与人工智能技术'
const BASE_URL = 'https://divination.app.awsl.uk'

export default function SEOHead({
    title,
    description = BASE_DESCRIPTION,
    keywords,
    ogImage = '/android-chrome-512x512.png',
    ogType = 'website',
    canonicalUrl,
    noIndex = false
}: SEOHeadProps) {
    const fullTitle = title ? `${title} | ${BASE_TITLE}` : BASE_TITLE

    useEffect(() => {
        document.title = fullTitle

        const updateMeta = (name: string, content: string, isProperty = false) => {
            const attr = isProperty ? 'property' : 'name'
            let meta = document.querySelector(`meta[${attr}="${name}"]`) as HTMLMetaElement
            if (!meta) {
                meta = document.createElement('meta')
                meta.setAttribute(attr, name)
                document.head.appendChild(meta)
            }
            meta.content = content
        }

        updateMeta('description', description)
        if (keywords) {
            updateMeta('keywords', keywords)
        }

        updateMeta('og:title', fullTitle, true)
        updateMeta('og:description', description, true)
        updateMeta('og:type', ogType, true)
        updateMeta('og:image', ogImage.startsWith('http') ? ogImage : `${BASE_URL}${ogImage}`, true)
        updateMeta('og:url', canonicalUrl || window.location.href, true)
        updateMeta('og:site_name', 'AI 占卜', true)

        updateMeta('twitter:card', 'summary_large_image')
        updateMeta('twitter:title', fullTitle)
        updateMeta('twitter:description', description)
        updateMeta('twitter:image', ogImage.startsWith('http') ? ogImage : `${BASE_URL}${ogImage}`)

        if (noIndex) {
            updateMeta('robots', 'noindex, nofollow')
        } else {
            updateMeta('robots', 'index, follow')
        }

        let canonical = document.querySelector('link[rel="canonical"]') as HTMLLinkElement
        if (canonicalUrl) {
            if (!canonical) {
                canonical = document.createElement('link')
                canonical.rel = 'canonical'
                document.head.appendChild(canonical)
            }
            canonical.href = canonicalUrl
        } else if (canonical) {
            canonical.remove()
        }
    }, [fullTitle, description, keywords, ogImage, ogType, canonicalUrl, noIndex])

    return null
}

export const SEO_CONFIG = {
    home: {
        title: '首页',
        description: 'AI智能占卜平台，融合传统命理与人工智能，提供塔罗牌占卜、生辰八字、紫微斗数、周公解梦等专业服务',
        keywords: 'AI占卜,在线算命,塔罗牌,八字算命,紫微斗数,周公解梦,姓名测算'
    },
    tarot: {
        title: '塔罗牌占卜',
        description: 'AI智能塔罗牌占卜，深度解读爱情、事业、财运、健康等人生问题，提供专业塔罗牌分析',
        keywords: '塔罗牌,塔罗占卜,AI塔罗,在线塔罗,爱情占卜,事业占卜'
    },
    birthday: {
        title: '生辰八字',
        description: 'AI生辰八字分析，根据出生年月日时推算五行、十神、大运流年，解读命运格局',
        keywords: '生辰八字,八字算命,五行分析,命盘分析,大运流年'
    },
    ziwei: {
        title: '紫微斗数',
        description: 'AI紫微斗数排盘，十二宫位精准分析，大限小限流年流月全面解读命运走势',
        keywords: '紫微斗数,紫微排盘,命盘分析,大限流年,十二宫位'
    },
    dream: {
        title: '周公解梦',
        description: 'AI周公解梦，智能分析梦境含义，结合传统解梦典籍与现代心理学提供深度解读',
        keywords: '周公解梦,解梦,梦境分析,梦的含义,AI解梦'
    },
    name: {
        title: '姓名测算',
        description: 'AI姓名五格分析，测算姓名吉凶，解读名字对命运的影响',
        keywords: '姓名测算,五格数理,姓名吉凶,起名测名'
    },
    newName: {
        title: '起名取名',
        description: 'AI智能起名，根据生辰八字、五行喜用，为宝宝取一个吉祥好名',
        keywords: '起名,取名,宝宝起名,八字起名,AI起名'
    },
    liuyao: {
        title: '六爻占卜',
        description: 'AI六爻起卦，传统易经占卜方法，解读卦象吉凶，预测事物发展',
        keywords: '六爻,易经占卜,起卦,卦象分析,周易'
    },
    plumFlower: {
        title: '梅花易数',
        description: 'AI梅花易数占卜，心易相通的快速占卜术，即时解答疑惑',
        keywords: '梅花易数,心易,快速占卜,易数'
    },
    fate: {
        title: '姻缘配对',
        description: 'AI姻缘配对分析，根据双方八字测算缘分指数，解读感情发展趋势',
        keywords: '姻缘配对,合婚,缘分测试,八字合婚'
    },
    hehun: {
        title: '合婚配对',
        description: 'AI合婚分析，深度解读男女双方八字相合程度，提供婚姻建议',
        keywords: '合婚,八字合婚,婚姻配对,姻缘分析'
    },
    qimen: {
        title: '奇门遁甲',
        description: 'AI奇门遁甲排盘，古代帝王决策之术，预测吉凶、趋利避害',
        keywords: '奇门遁甲,奇门排盘,奇门预测,遁甲'
    },
    xiaoliu: {
        title: '小六壬',
        description: 'AI小六壬速断，简便快捷的占卜方法，即时解答日常疑问',
        keywords: '小六壬,速断,快速占卜,日常占卜'
    },
    chouqian: {
        title: '求签抽签',
        description: 'AI求签抽签，观音灵签、月老灵签等多种签文，虔诚求签解惑',
        keywords: '求签,抽签,观音灵签,月老灵签,灵签'
    },
    zhuge: {
        title: '诸葛神算',
        description: 'AI诸葛神算，传承诸葛亮智慧，384签全面解读人生疑问',
        keywords: '诸葛神算,诸葛亮,神算,384签'
    },
    laohuangli: {
        title: '老黄历',
        description: '每日老黄历查询，宜忌、吉时、冲煞等传统黄历信息一览无余',
        keywords: '老黄历,黄历查询,宜忌,吉时,冲煞'
    },
    daily: {
        title: '每日运势',
        description: '每日运势分析，根据生肖、星座解读今日运程，把握每一天',
        keywords: '每日运势,今日运势,运程分析'
    },
    zodiac: {
        title: '生肖运势',
        description: '十二生肖运势分析，年度运程、月度运势全面解读',
        keywords: '生肖运势,十二生肖,生肖运程'
    }
}
