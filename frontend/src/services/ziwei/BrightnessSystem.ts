/**
 * 星曜亮度计算系统
 * 参考mingpan实现
 */

export type BrightnessLevel = '庙' | '旺' | '得' | '利' | '平' | '不' | '陷'

// 主星亮度表 - 星曜在不同地支宫位的亮度
const MAJOR_STAR_BRIGHTNESS: Record<string, Record<string, BrightnessLevel>> = {
    '紫微': { '子': '旺', '丑': '庙', '寅': '庙', '卯': '旺', '辰': '庙', '巳': '旺', '午': '旺', '未': '庙', '申': '旺', '酉': '平', '戌': '庙', '亥': '旺' },
    '天机': { '子': '庙', '丑': '陷', '寅': '庙', '卯': '旺', '辰': '旺', '巳': '平', '午': '陷', '未': '旺', '申': '庙', '酉': '旺', '戌': '旺', '亥': '平' },
    '太阳': { '子': '陷', '丑': '陷', '寅': '旺', '卯': '庙', '辰': '旺', '巳': '庙', '午': '旺', '未': '得', '申': '平', '酉': '陷', '戌': '陷', '亥': '陷' },
    '武曲': { '子': '旺', '丑': '庙', '寅': '利', '卯': '平', '辰': '庙', '巳': '利', '午': '旺', '未': '庙', '申': '利', '酉': '平', '戌': '庙', '亥': '利' },
    '天同': { '子': '旺', '丑': '得', '寅': '平', '卯': '陷', '辰': '平', '巳': '庙', '午': '陷', '未': '得', '申': '平', '酉': '庙', '戌': '平', '亥': '旺' },
    '廉贞': { '子': '平', '丑': '庙', '寅': '旺', '卯': '得', '辰': '庙', '巳': '利', '午': '平', '未': '庙', '申': '旺', '酉': '得', '戌': '庙', '亥': '利' },
    '天府': { '子': '庙', '丑': '庙', '寅': '得', '卯': '庙', '辰': '庙', '巳': '旺', '午': '庙', '未': '庙', '申': '得', '酉': '庙', '戌': '庙', '亥': '旺' },
    '太阴': { '子': '庙', '丑': '旺', '寅': '得', '卯': '平', '辰': '陷', '巳': '陷', '午': '陷', '未': '陷', '申': '平', '酉': '旺', '戌': '庙', '亥': '庙' },
    '贪狼': { '子': '旺', '丑': '平', '寅': '庙', '卯': '陷', '辰': '旺', '巳': '平', '午': '庙', '未': '陷', '申': '旺', '酉': '平', '戌': '庙', '亥': '陷' },
    '巨门': { '子': '旺', '丑': '陷', '寅': '庙', '卯': '旺', '辰': '陷', '巳': '平', '午': '庙', '未': '陷', '申': '庙', '酉': '旺', '戌': '陷', '亥': '平' },
    '天相': { '子': '庙', '丑': '庙', '寅': '庙', '卯': '陷', '辰': '得', '巳': '庙', '午': '庙', '未': '庙', '申': '庙', '酉': '陷', '戌': '得', '亥': '庙' },
    '天梁': { '子': '庙', '丑': '庙', '寅': '庙', '卯': '旺', '辰': '陷', '巳': '庙', '午': '旺', '未': '庙', '申': '庙', '酉': '旺', '戌': '陷', '亥': '庙' },
    '七杀': { '子': '旺', '丑': '庙', '寅': '庙', '卯': '旺', '辰': '庙', '巳': '平', '午': '旺', '未': '庙', '申': '庙', '酉': '旺', '戌': '庙', '亥': '平' },
    '破军': { '子': '旺', '丑': '庙', '寅': '平', '卯': '陷', '辰': '庙', '巳': '得', '午': '旺', '未': '庙', '申': '平', '酉': '陷', '戌': '庙', '亥': '得' }
}

// 亮度分数映射
const BRIGHTNESS_SCORES: Record<BrightnessLevel, number> = {
    '庙': 100,
    '旺': 90,
    '得': 70,
    '利': 60,
    '平': 50,
    '不': 30,
    '陷': 20
}

export class BrightnessSystem {
    /**
     * 计算星曜在指定宫位的亮度
     */
    static calculateBrightness(starName: string, earthlyBranch: string): BrightnessLevel {
        const starBrightness = MAJOR_STAR_BRIGHTNESS[starName]
        if (starBrightness && starBrightness[earthlyBranch]) {
            return starBrightness[earthlyBranch]
        }
        return '平' // 默认亮度
    }

    /**
     * 获取亮度分数
     */
    static getBrightnessScore(level: BrightnessLevel): number {
        return BRIGHTNESS_SCORES[level] || 50
    }

    /**
     * 获取亮度描述
     */
    static getBrightnessDescription(level: BrightnessLevel, language: string = 'zh-CN'): string {
        const descriptions: Record<string, Record<BrightnessLevel, string>> = {
            'zh-CN': {
                '庙': '庙旺 - 星曜能量最强',
                '旺': '旺盛 - 星曜能量充沛',
                '得': '得地 - 星曜表现良好',
                '利': '利位 - 星曜发挥正常',
                '平': '平和 - 星曜能量一般',
                '不': '不得 - 星曜能量偏弱',
                '陷': '落陷 - 星曜能量受限'
            },
            'en': {
                '庙': 'Temple - Strongest energy',
                '旺': 'Prosperous - Abundant energy',
                '得': 'Favorable - Good performance',
                '利': 'Beneficial - Normal function',
                '平': 'Neutral - Average energy',
                '不': 'Unfavorable - Weak energy',
                '陷': 'Fallen - Limited energy'
            }
        }
        return descriptions[language]?.[level] || descriptions['zh-CN'][level]
    }

    /**
     * 获取亮度颜色
     */
    static getBrightnessColor(level: BrightnessLevel): string {
        const colors: Record<BrightnessLevel, string> = {
            '庙': '#ef4444', // red
            '旺': '#f97316', // orange
            '得': '#eab308', // yellow
            '利': '#22c55e', // green
            '平': '#6b7280', // gray
            '不': '#3b82f6', // blue
            '陷': '#8b5cf6'  // purple
        }
        return colors[level] || '#6b7280'
    }
}
