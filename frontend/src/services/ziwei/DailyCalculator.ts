/**
 * 流日计算器
 * 参考 mingpan 的 DailyCalculator 实现
 * 紫微斗数流日使用农历日
 */

import { Solar } from 'lunar-javascript'
import { logger } from '@/utils/logger'

export interface DailyInfo {
    year: number
    month: number
    day: number
    solarDate: Date           // 阳历日期
    heavenlyStem: string      // 日干
    earthlyBranch: string     // 日支
    palaceIndex: number       // 流日命宫索引
    palaceName?: string       // 宫位名称
    mutagen?: {               // 流日四化
        lu: string
        quan: string
        ke: string
        ji: string
    }
    lunarDateStr?: string     // 农历日期字符串
}

// 天干
const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

// 地支
const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

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

export class DailyCalculator {
    /**
     * 计算指定日期的日干支
     * 使用lunar-javascript库获取日干支
     */
    static getDayStemBranch(date: Date): { stem: string; branch: string } {
        try {
            const solar = Solar.fromDate(date)
            const lunar = solar.getLunar()
            const ganZhi = lunar.getDayInGanZhi()

            if (ganZhi && ganZhi.length >= 2) {
                return {
                    stem: ganZhi[0],
                    branch: ganZhi[1]
                }
            }
        } catch (e) {
            logger.error('获取日干支失败:', e)
        }

        // 回退：使用公式计算
        return this.calculateDayStemBranch(date)
    }

    /**
     * 使用公式计算日干支（备用方法）
     * 以1900年1月1日为甲戌日基准
     */
    static calculateDayStemBranch(date: Date): { stem: string; branch: string } {
        // 1900年1月1日是甲戌日（干索引0，支索引10）
        const baseDate = new Date(1900, 0, 1)
        const diffDays = Math.floor((date.getTime() - baseDate.getTime()) / (1000 * 60 * 60 * 24))

        const stemIndex = (diffDays % 10 + 10) % 10
        const branchIndex = ((diffDays + 10) % 12 + 12) % 12  // 甲戌日支索引为10

        return {
            stem: HEAVENLY_STEMS[stemIndex],
            branch: EARTHLY_BRANCHES[branchIndex]
        }
    }

    /**
     * 计算流日命宫索引
     * 流日命宫：以流日地支所在宫位为流日命宫
     */
    static getDailyPalaceIndex(dayBranch: string, palaces: Array<{ earthlyBranch: string }>): number {
        const index = palaces.findIndex(p => p.earthlyBranch === dayBranch)
        return index !== -1 ? index : 0
    }

    /**
     * 计算指定日期的流日信息
     */
    static calculate(
        date: Date,
        palaces: Array<{ earthlyBranch: string; name: string }>
    ): DailyInfo {
        const { stem, branch } = this.getDayStemBranch(date)
        const palaceIndex = this.getDailyPalaceIndex(branch, palaces)
        const mutagen = MUTAGEN_MAP[stem]

        // 获取农历日期字符串
        let lunarDateStr = ''
        try {
            const solar = Solar.fromDate(date)
            const lunar = solar.getLunar()
            lunarDateStr = `${lunar.getMonthInChinese()}月${lunar.getDayInChinese()}`
        } catch {
            // 忽略错误
        }

        return {
            year: date.getFullYear(),
            month: date.getMonth() + 1,
            day: date.getDate(),
            solarDate: date,
            heavenlyStem: stem,
            earthlyBranch: branch,
            palaceIndex,
            palaceName: palaces[palaceIndex]?.name || '',
            mutagen,
            lunarDateStr
        }
    }

    /**
     * 批量计算一个月的流日信息
     */
    static calculateMonth(
        year: number,
        month: number,
        palaces: Array<{ earthlyBranch: string; name: string }>
    ): DailyInfo[] {
        const days: DailyInfo[] = []
        const daysInMonth = new Date(year, month, 0).getDate()

        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month - 1, day)
            days.push(this.calculate(date, palaces))
        }

        return days
    }

    /**
     * 计算日期范围的流日信息
     */
    static calculateRange(
        startDate: Date,
        endDate: Date,
        palaces: Array<{ earthlyBranch: string; name: string }>
    ): DailyInfo[] {
        const days: DailyInfo[] = []
        const current = new Date(startDate)

        while (current <= endDate) {
            days.push(this.calculate(new Date(current), palaces))
            current.setDate(current.getDate() + 1)
        }

        return days
    }

    /**
     * 获取今天的流日信息
     */
    static getToday(palaces: Array<{ earthlyBranch: string; name: string }>): DailyInfo {
        return this.calculate(new Date(), palaces)
    }
}

export default DailyCalculator
