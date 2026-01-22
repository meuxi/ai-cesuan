/**
 * 四化核心计算模块
 * 参考mingpan实现的完整四化对照表
 */

import { MutagenInfo, CompleteMutagenInfo } from '@/types/ziwei'

// 四化对照表 - 十天干对应的四化星曜
const MUTAGEN_MAP: Record<string, [string, string, string, string]> = {
    '甲': ['廉贞', '破军', '武曲', '太阳'],
    '乙': ['天机', '天梁', '紫微', '太阴'],
    '丙': ['天同', '天机', '文昌', '廉贞'],
    '丁': ['太阴', '天同', '天机', '巨门'],
    '戊': ['贪狼', '太阴', '右弼', '天机'],
    '己': ['武曲', '贪狼', '天梁', '文曲'],
    '庚': ['太阳', '武曲', '太阴', '天同'],
    '辛': ['巨门', '太阳', '文曲', '文昌'],
    '壬': ['天梁', '紫微', '左辅', '武曲'],
    '癸': ['破军', '巨门', '太阴', '贪狼']
}

// 繁简转换映射
const STAR_NAME_MAP: Record<string, string> = {
    '廉貞': '廉贞', '破軍': '破军', '武曲': '武曲', '太陽': '太阳',
    '天機': '天机', '天梁': '天梁', '紫微': '紫微', '太陰': '太阴',
    '天同': '天同', '文昌': '文昌', '貪狼': '贪狼', '右弼': '右弼',
    '文曲': '文曲', '左輔': '左辅', '巨門': '巨门', '七殺': '七杀'
}

export class MutagenCore {
    /**
     * 根据天干获取四化
     */
    static getMutagen(stem: string): MutagenInfo {
        const mutagen = MUTAGEN_MAP[stem]
        if (!mutagen) {
            return { lu: '', quan: '', ke: '', ji: '' }
        }
        return {
            lu: mutagen[0],
            quan: mutagen[1],
            ke: mutagen[2],
            ji: mutagen[3]
        }
    }

    /**
     * 标准化星曜名称（繁体转简体）
     */
    static normalizeStarName(name: string): string {
        return STAR_NAME_MAP[name] || name
    }

    /**
     * 计算完整四化信息
     */
    static getCompleteMutagenInfo(
        natalStem: string,
        decadalStem?: string,
        yearlyStem?: string
    ): { natal: MutagenInfo; decade?: MutagenInfo; yearly?: MutagenInfo } {
        return {
            natal: this.getMutagen(natalStem),
            decade: decadalStem ? this.getMutagen(decadalStem) : undefined,
            yearly: yearlyStem ? this.getMutagen(yearlyStem) : undefined
        }
    }

    /**
     * 获取四化前缀（多语言支持）
     */
    static getMutagenPrefixes(language: string = 'zh-CN'): Record<string, string> {
        if (language === 'zh-CN' || language === 'zh-TW') {
            return { natal: '本', decade: '限', yearly: '年' }
        }
        return { natal: 'N-', decade: 'D-', yearly: 'Y-' }
    }

    /**
     * 获取四化类型名称（多语言支持）
     */
    static getMutagenTypeNames(language: string = 'zh-CN'): Record<string, string> {
        if (language === 'zh-CN' || language === 'zh-TW') {
            return { lu: '禄', quan: '权', ke: '科', ji: '忌' }
        }
        return { lu: 'Lu', quan: 'Quan', ke: 'Ke', ji: 'Ji' }
    }

    /**
     * 合并多层四化到Map
     */
    static combineMutagens(
        natal: MutagenInfo,
        decade?: MutagenInfo,
        yearly?: MutagenInfo,
        monthly?: MutagenInfo,
        daily?: MutagenInfo,
        language: string = 'zh-CN'
    ): Map<string, string[]> {
        const combined = new Map<string, string[]>()
        const prefixes = this.getAllMutagenPrefixes(language)
        const typeNames = this.getMutagenTypeNames(language)

        const addMutagen = (info: MutagenInfo, prefix: string) => {
            if (info.lu) {
                const existing = combined.get(info.lu) || []
                combined.set(info.lu, [...existing, `${prefix}${typeNames.lu}`])
            }
            if (info.quan) {
                const existing = combined.get(info.quan) || []
                combined.set(info.quan, [...existing, `${prefix}${typeNames.quan}`])
            }
            if (info.ke) {
                const existing = combined.get(info.ke) || []
                combined.set(info.ke, [...existing, `${prefix}${typeNames.ke}`])
            }
            if (info.ji) {
                const existing = combined.get(info.ji) || []
                combined.set(info.ji, [...existing, `${prefix}${typeNames.ji}`])
            }
        }

        addMutagen(natal, prefixes.natal)
        if (decade) addMutagen(decade, prefixes.decade)
        if (yearly) addMutagen(yearly, prefixes.yearly)
        if (monthly) addMutagen(monthly, prefixes.monthly)
        if (daily) addMutagen(daily, prefixes.daily)

        return combined
    }

    /**
     * 获取所有四化前缀（含流月流日）
     */
    static getAllMutagenPrefixes(language: string = 'zh-CN'): Record<string, string> {
        if (language === 'zh-CN' || language === 'zh-TW') {
            return { natal: '本', decade: '限', yearly: '年', monthly: '月', daily: '日' }
        }
        return { natal: 'N-', decade: 'D-', yearly: 'Y-', monthly: 'M-', daily: 'Da-' }
    }

    /**
     * 应用四化到宫位星曜
     * 返回星曜名称到四化标签的映射
     */
    static applyMutagenToPalaces(
        palaces: Array<{ majorStars: Array<{ name: string; mutagen?: string[] }>; minorStars: Array<{ name: string; mutagen?: string[] }> }>,
        mutagenMap: Map<string, string[]>
    ): void {
        palaces.forEach(palace => {
            // 应用到主星
            palace.majorStars.forEach(star => {
                const normalizedName = this.normalizeStarName(star.name)
                const mutagens = mutagenMap.get(normalizedName) || mutagenMap.get(star.name)
                if (mutagens && mutagens.length > 0) {
                    star.mutagen = [...(star.mutagen || []), ...mutagens]
                }
            })
            // 应用到辅星（部分辅星也可能有四化，如文昌文曲左辅右弼）
            palace.minorStars.forEach(star => {
                const normalizedName = this.normalizeStarName(star.name)
                const mutagens = mutagenMap.get(normalizedName) || mutagenMap.get(star.name)
                if (mutagens && mutagens.length > 0) {
                    star.mutagen = [...(star.mutagen || []), ...mutagens]
                }
            })
        })
    }

    /**
     * 获取四化颜色样式
     */
    static getMutagenColor(mutagenLabel: string): string {
        if (mutagenLabel.includes('禄')) return 'text-green-500'
        if (mutagenLabel.includes('权')) return 'text-red-500'
        if (mutagenLabel.includes('科')) return 'text-blue-500'
        if (mutagenLabel.includes('忌')) return 'text-purple-500'
        return 'text-foreground'
    }

    /**
     * 获取四化背景颜色样式
     */
    static getMutagenBgColor(mutagenLabel: string): string {
        if (mutagenLabel.includes('禄')) return 'bg-green-500/10'
        if (mutagenLabel.includes('权')) return 'bg-red-500/10'
        if (mutagenLabel.includes('科')) return 'bg-blue-500/10'
        if (mutagenLabel.includes('忌')) return 'bg-purple-500/10'
        return 'bg-muted'
    }

    /**
     * 格式化四化标签用于显示
     */
    static formatMutagenLabels(mutagens: string[]): string {
        return mutagens.join(' ')
    }

    /**
     * 检查是否有重叠四化（如本禄+年禄）
     */
    static hasOverlappingMutagen(mutagens: string[]): boolean {
        const types = mutagens.map(m => {
            if (m.includes('禄')) return '禄'
            if (m.includes('权')) return '权'
            if (m.includes('科')) return '科'
            if (m.includes('忌')) return '忌'
            return ''
        })
        return new Set(types).size < types.length
    }

    /**
     * 获取完整四化信息（含流月流日）
     */
    static getFullMutagenInfo(
        natalStem: string,
        decadalStem?: string,
        yearlyStem?: string,
        monthlyStem?: string,
        dailyStem?: string
    ): {
        natal: MutagenInfo
        decade?: MutagenInfo
        yearly?: MutagenInfo
        monthly?: MutagenInfo
        daily?: MutagenInfo
    } {
        return {
            natal: this.getMutagen(natalStem),
            decade: decadalStem ? this.getMutagen(decadalStem) : undefined,
            yearly: yearlyStem ? this.getMutagen(yearlyStem) : undefined,
            monthly: monthlyStem ? this.getMutagen(monthlyStem) : undefined,
            daily: dailyStem ? this.getMutagen(dailyStem) : undefined
        }
    }
}
