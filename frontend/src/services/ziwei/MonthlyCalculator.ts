/**
 * 流月计算器
 * 参考 mingpan 的 MonthlyCalculator 实现
 * 紫微斗数流月使用农历月，从正月到腊月
 */

import { Solar, Lunar } from 'lunar-javascript'

export interface MonthlyInfo {
    year: number
    month: number           // 农历月份 1-12
    isLeapMonth: boolean    // 是否闰月
    heavenlyStem: string    // 天干
    earthlyBranch: string   // 地支
    palaceIndex: number     // 流月命宫索引
    palaceName?: string     // 宫位名称
    mutagen?: {             // 流月四化
        lu: string
        quan: string
        ke: string
        ji: string
    }
    startDate?: Date        // 月份起始日期
    endDate?: Date          // 月份结束日期
    lunarMonthName?: string // 农历月份名称（如"正月"、"闰四月"）
}

// 天干
const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

// 地支
const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

// 农历月份名称
const LUNAR_MONTH_NAMES = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月']

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

export class MonthlyCalculator {
    /**
     * 计算流月天干地支
     * 流月干支规则：以流年天干起正月
     * 甲己之年丙作首，乙庚之岁戊为头，
     * 丙辛之岁寻庚上，丁壬壬位顺行流，
     * 更有戊癸何处起，甲寅之上好追求。
     */
    static getMonthStemBranch(yearStem: string, lunarMonth: number): { stem: string; branch: string } {
        // 年干起月干的规则
        const monthStartMap: Record<string, number> = {
            '甲': 2, '己': 2,  // 丙寅
            '乙': 4, '庚': 4,  // 戊寅
            '丙': 6, '辛': 6,  // 庚寅
            '丁': 8, '壬': 8,  // 壬寅
            '戊': 0, '癸': 0   // 甲寅
        }

        const startStemIndex = monthStartMap[yearStem] ?? 0
        // 正月地支固定为寅(索引2)，逐月顺推
        const stemIndex = (startStemIndex + lunarMonth - 1) % 10
        const branchIndex = (2 + lunarMonth - 1) % 12  // 从寅开始

        return {
            stem: HEAVENLY_STEMS[stemIndex],
            branch: EARTHLY_BRANCHES[branchIndex]
        }
    }

    /**
     * 计算流月命宫索引
     * 流月命宫：以流月地支所在宫位为流月命宫
     */
    static getMonthlyPalaceIndex(monthBranch: string, palaces: Array<{ earthlyBranch: string }>): number {
        const index = palaces.findIndex(p => p.earthlyBranch === monthBranch)
        return index !== -1 ? index : 0
    }

    /**
     * 获取指定农历年的闰月
     * 简化实现：根据已知的闰月规律返回
     * @returns 闰月月份(1-12)，如果没有闰月返回0
     */
    static getLeapMonth(year: number): number {
        // 已知闰月表（2020-2030）
        const leapMonthTable: Record<number, number> = {
            2020: 4,  // 闰四月
            2023: 2,  // 闰二月
            2025: 6,  // 闰六月
            2028: 5,  // 闰五月
        }
        return leapMonthTable[year] || 0
    }

    /**
     * 计算指定年月的流月信息
     */
    static calculate(
        yearStem: string,
        year: number,
        lunarMonth: number,
        isLeapMonth: boolean,
        palaces: Array<{ earthlyBranch: string; name: string }>
    ): MonthlyInfo {
        const { stem, branch } = this.getMonthStemBranch(yearStem, lunarMonth)
        const palaceIndex = this.getMonthlyPalaceIndex(branch, palaces)
        const mutagen = MUTAGEN_MAP[stem]

        // 日期信息（简化处理，不计算精确起止日期）
        // 精确日期需要后端农历库支持
        const startDate: Date | undefined = undefined
        const endDate: Date | undefined = undefined

        const monthName = isLeapMonth ? `闰${LUNAR_MONTH_NAMES[lunarMonth - 1]}` : LUNAR_MONTH_NAMES[lunarMonth - 1]

        return {
            year,
            month: lunarMonth,
            isLeapMonth,
            heavenlyStem: stem,
            earthlyBranch: branch,
            palaceIndex,
            palaceName: palaces[palaceIndex]?.name || '',
            mutagen,
            startDate,
            endDate,
            lunarMonthName: monthName
        }
    }

    /**
     * 批量计算一年的流月信息（农历月，包含闰月）
     */
    static calculateYear(
        yearStem: string,
        year: number,
        palaces: Array<{ earthlyBranch: string; name: string }>
    ): MonthlyInfo[] {
        const months: MonthlyInfo[] = []
        const leapMonth = this.getLeapMonth(year)

        for (let lunarMonth = 1; lunarMonth <= 12; lunarMonth++) {
            // 正常月份
            months.push(this.calculate(yearStem, year, lunarMonth, false, palaces))

            // 闰月
            if (leapMonth === lunarMonth) {
                months.push(this.calculate(yearStem, year, lunarMonth, true, palaces))
            }
        }

        return months
    }

    /**
     * 获取当前农历月份
     */
    static getCurrentLunarMonth(): { year: number; month: number; isLeapMonth: boolean } {
        const now = new Date()
        try {
            const solar = Solar.fromDate(now)
            const lunar = solar.getLunar()
            return {
                year: lunar.getYear(),
                month: Math.abs(lunar.getMonth()),
                isLeapMonth: lunar.getMonth() < 0
            }
        } catch {
            return { year: now.getFullYear(), month: now.getMonth() + 1, isLeapMonth: false }
        }
    }
}

export default MonthlyCalculator
