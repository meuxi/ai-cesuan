/**
 * 流时计算器
 * 参考 mingpan 的 HourlyCalculator 实现
 * 紫微斗数流时使用时辰（地支）
 */

export interface HourlyInfo {
    hour: number              // 小时 0-23
    timeIndex: number         // 时辰索引 0-11
    heavenlyStem: string      // 时干
    earthlyBranch: string     // 时支
    palaceIndex: number       // 流时命宫索引
    palaceName?: string       // 宫位名称
    mutagen?: {               // 流时四化
        lu: string
        quan: string
        ke: string
        ji: string
    }
    timeName: string          // 时辰名称（如"子时"）
    timeRange: string         // 时间范围（如"23:00-01:00"）
}

// 天干
const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

// 地支
const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

// 时辰名称
const TIME_NAMES = ['子时', '丑时', '寅时', '卯时', '辰时', '巳时', '午时', '未时', '申时', '酉时', '戌时', '亥时']

// 时辰时间范围
const TIME_RANGES = [
    '23:00-01:00', '01:00-03:00', '03:00-05:00', '05:00-07:00',
    '07:00-09:00', '09:00-11:00', '11:00-13:00', '13:00-15:00',
    '15:00-17:00', '17:00-19:00', '19:00-21:00', '21:00-23:00'
]

// 四化对照表
const MUTAGEN_MAP: Record<string, { lu: string; quan: string; ke: string; ji: string }> = {
    '甲': { lu: '廉贞', quan: '破军', ke: '武曲', ji: '太阳' },
    '乙': { lu: '天机', quan: '天梁', ke: '紫微', ji: '太阴' },
    '丙': { lu: '天同', quan: '天机', ke: '文昌', ji: '廉贞' },
    '丁': { lu: '太阴', quan: '天同', ke: '天机', ji: '巨门' },
    '戊': { lu: '贪狼', quan: '太阴', ke: '右弼', ji: '天机' },
    '己': { lu: '武曲', quan: '贪狼', ke: '天梁', ji: '文曲' },
    '庚': { lu: '太阳', quan: '武曲', ke: '太阴', ji: '天同' },
    '辛': { lu: '巨门', quan: '太阳', ke: '文曲', ji: '文昌' },
    '壬': { lu: '天梁', quan: '紫微', ke: '左辅', ji: '武曲' },
    '癸': { lu: '破军', quan: '巨门', ke: '太阴', ji: '贪狼' }
}

export class HourlyCalculator {
    /**
     * 将小时转换为时辰索引
     * 子时(23-1), 丑时(1-3), 寅时(3-5)...
     */
    static hourToTimeIndex(hour: number): number {
        if (hour >= 23 || hour < 1) return 0   // 子时
        return Math.floor((hour + 1) / 2)
    }

    /**
     * 计算时干支
     * 日上起时规则：
     * 甲己还加甲，乙庚丙作初，
     * 丙辛从戊起，丁壬庚子居，
     * 戊癸何方发，壬子是真途。
     */
    static getHourStemBranch(dayStem: string, timeIndex: number): { stem: string; branch: string } {
        // 日干起时干的规则
        const hourStartMap: Record<string, number> = {
            '甲': 0, '己': 0,  // 甲子时
            '乙': 2, '庚': 2,  // 丙子时
            '丙': 4, '辛': 4,  // 戊子时
            '丁': 6, '壬': 6,  // 庚子时
            '戊': 8, '癸': 8   // 壬子时
        }

        const startStemIndex = hourStartMap[dayStem] ?? 0
        const stemIndex = (startStemIndex + timeIndex) % 10
        const branchIndex = timeIndex % 12

        return {
            stem: HEAVENLY_STEMS[stemIndex],
            branch: EARTHLY_BRANCHES[branchIndex]
        }
    }

    /**
     * 计算流时命宫索引
     * 流时命宫：以流时地支所在宫位为流时命宫
     */
    static getHourlyPalaceIndex(hourBranch: string, palaces: Array<{ earthlyBranch: string }>): number {
        const index = palaces.findIndex(p => p.earthlyBranch === hourBranch)
        return index !== -1 ? index : 0
    }

    /**
     * 计算指定时辰的流时信息
     */
    static calculate(
        dayStem: string,
        hour: number,
        palaces: Array<{ earthlyBranch: string; name: string }>
    ): HourlyInfo {
        const timeIndex = this.hourToTimeIndex(hour)
        const { stem, branch } = this.getHourStemBranch(dayStem, timeIndex)
        const palaceIndex = this.getHourlyPalaceIndex(branch, palaces)
        const mutagen = MUTAGEN_MAP[stem]

        return {
            hour,
            timeIndex,
            heavenlyStem: stem,
            earthlyBranch: branch,
            palaceIndex,
            palaceName: palaces[palaceIndex]?.name || '',
            mutagen,
            timeName: TIME_NAMES[timeIndex],
            timeRange: TIME_RANGES[timeIndex]
        }
    }

    /**
     * 批量计算一天的12个时辰
     */
    static calculateDay(
        dayStem: string,
        palaces: Array<{ earthlyBranch: string; name: string }>
    ): HourlyInfo[] {
        const hours: HourlyInfo[] = []

        // 12个时辰对应的代表小时
        const representativeHours = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]

        for (const hour of representativeHours) {
            hours.push(this.calculate(dayStem, hour, palaces))
        }

        return hours
    }

    /**
     * 获取当前时辰的流时信息
     */
    static getCurrentHour(
        dayStem: string,
        palaces: Array<{ earthlyBranch: string; name: string }>
    ): HourlyInfo {
        const now = new Date()
        return this.calculate(dayStem, now.getHours(), palaces)
    }

    /**
     * 获取时辰名称
     */
    static getTimeName(timeIndex: number): string {
        return TIME_NAMES[timeIndex] || '子时'
    }

    /**
     * 获取时辰时间范围
     */
    static getTimeRange(timeIndex: number): string {
        return TIME_RANGES[timeIndex] || '23:00-01:00'
    }
}

export default HourlyCalculator
