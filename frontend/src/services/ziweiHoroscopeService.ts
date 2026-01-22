/**
 * 紫微斗数运限服务
 * 使用 iztro 前端库计算精确的运限信息
 * 包括大限四化、流年四化、流曜等
 */

import { astro } from 'iztro'
import { logger } from '@/utils/logger'

// 运限类型
type Astrolabe = ReturnType<typeof astro.bySolar>
type Horoscope = ReturnType<Astrolabe['horoscope']>

// 四化信息
export interface MutagenInfo {
    lu: string      // 化禄
    quan: string    // 化权
    ke: string      // 化科
    ji: string      // 化忌
}

// 流曜信息
export interface FlowStar {
    name: string
    type: 'soft' | 'tough' | 'flower' | 'helper'  // 吉/凶/桃花/解神
}

// 大限详细信息
export interface DecadalDetail {
    index: number
    startAge: number
    endAge: number
    heavenlyStem: string
    earthlyBranch: string
    palaceName: string
    palaceIndex: number
    mutagen?: MutagenInfo
    stars?: FlowStar[][]  // 12宫的流曜
    palaceNames?: string[]  // 运限重排宫名
}

// 流年详细信息
export interface YearlyDetail {
    year: number
    heavenlyStem: string
    earthlyBranch: string
    palaceIndex: number
    palaceName: string
    mutagen?: MutagenInfo
    stars?: FlowStar[][]  // 12宫的流曜
    palaceNames?: string[]  // 运限重排宫名
}

// 流月详细信息
export interface MonthlyDetail {
    month: number
    heavenlyStem: string
    earthlyBranch: string
    palaceIndex: number
    palaceName: string
    mutagen?: MutagenInfo
    palaceNames?: string[]  // 运限重排宫名
}

// 流日详细信息
export interface DailyDetail {
    day: number
    heavenlyStem: string
    earthlyBranch: string
    palaceIndex: number
    palaceName: string
    mutagen?: MutagenInfo
    palaceNames?: string[]  // 运限重排宫名
}

// 流时详细信息
export interface HourlyDetail {
    hour: number           // 时辰索引 0-11
    hourName: string       // 时辰名称（子丑寅卯...）
    heavenlyStem: string
    earthlyBranch: string
    palaceIndex: number
    palaceName: string
    mutagen?: MutagenInfo
    palaceNames?: string[]  // 运限重排宫名
}

// 服务类
export class ZiweiHoroscopeService {
    private astrolabe: Astrolabe | null = null
    private birthYear: number = 0

    /**
     * 初始化命盘
     */
    initialize(params: {
        solarDate: string      // YYYY-MM-DD 格式
        timeIndex: number      // 时辰索引 0-12
        gender: '男' | '女'
    }): boolean {
        try {
            this.astrolabe = astro.bySolar(
                params.solarDate,
                params.timeIndex,
                params.gender,
                true,  // fixLeap
                'zh-CN'
            )
            this.birthYear = parseInt(params.solarDate.split('-')[0])
            return true
        } catch (error) {
            logger.error('初始化命盘失败:', error)
            return false
        }
    }

    /**
     * 获取大限列表（带四化信息）
     */
    getDecadalList(): DecadalDetail[] {
        if (!this.astrolabe) return []

        const fiveElement = this.astrolabe.fiveElementsClass || ''
        const fiveElementMap: Record<string, number> = {
            '二': 2, '三': 3, '四': 4, '五': 5, '六': 6
        }
        const match = fiveElement.match(/[二三四五六]/)
        const startAge = match ? (fiveElementMap[match[0]] || 2) : 2

        return this.astrolabe.palaces.map((palace: any, index: number) => {
            const decadeStartAge = startAge + index * 10
            const decadeEndAge = decadeStartAge + 9

            // 获取大限四化（通过大限天干）
            const mutagen = this.getMutagenByStem(palace.heavenlyStem)

            // 获取大限重排宫名：通过该大限年龄计算 horoscope
            let palaceNames: string[] | undefined
            try {
                const decadeYear = this.birthYear + decadeStartAge
                const horoscope = this.astrolabe?.horoscope(new Date(decadeYear, 5, 15)) as any
                if (horoscope?.decadal?.palaceNames) {
                    palaceNames = horoscope.decadal.palaceNames
                }
            } catch {
                // ignore
            }

            return {
                index,
                startAge: decadeStartAge,
                endAge: decadeEndAge,
                heavenlyStem: palace.heavenlyStem || '',
                earthlyBranch: palace.earthlyBranch || '',
                palaceName: palace.name || '',
                palaceIndex: index,
                mutagen,
                palaceNames
            }
        })
    }

    /**
     * 获取指定年份的流年信息（带四化）
     */
    getYearlyDetail(year: number): YearlyDetail | null {
        if (!this.astrolabe) return null

        try {
            const yearDate = new Date(year, 5, 15)
            const horoscope = this.astrolabe.horoscope(yearDate) as any

            if (!horoscope?.yearly) return null

            const yearly = horoscope.yearly
            const mutagen = this.parseMutagen(yearly.mutagen)

            return {
                year,
                heavenlyStem: yearly.heavenlyStem || '',
                earthlyBranch: yearly.earthlyBranch || '',
                palaceIndex: yearly.index ?? yearly.palaceIndex ?? 0,
                palaceName: yearly.name || '',
                mutagen,
                palaceNames: yearly.palaceNames || undefined
            }
        } catch {
            return null
        }
    }

    /**
     * 获取大限内的流年列表
     */
    getYearlyListInDecade(decadeStartAge: number, decadeEndAge: number): YearlyDetail[] {
        const years: YearlyDetail[] = []
        const startYear = this.birthYear + decadeStartAge - 1
        const endYear = this.birthYear + decadeEndAge - 1

        for (let year = startYear; year <= endYear; year++) {
            const detail = this.getYearlyDetail(year)
            if (detail) {
                years.push(detail)
            }
        }

        return years
    }

    /**
     * 获取指定年月的流月信息
     */
    getMonthlyDetail(year: number, month: number): MonthlyDetail | null {
        if (!this.astrolabe) return null

        try {
            const monthDate = new Date(year, month - 1, 15)
            const horoscope = this.astrolabe.horoscope(monthDate) as any

            if (!horoscope?.monthly) return null

            const monthly = horoscope.monthly
            const mutagen = this.parseMutagen(monthly.mutagen)

            return {
                month,
                heavenlyStem: monthly.heavenlyStem || '',
                earthlyBranch: monthly.earthlyBranch || '',
                palaceIndex: monthly.index ?? monthly.palaceIndex ?? 0,
                palaceName: monthly.name || '',
                mutagen,
                palaceNames: monthly.palaceNames || undefined
            }
        } catch {
            return null
        }
    }

    /**
     * 获取12个月的流月列表
     */
    getMonthlyList(year: number): MonthlyDetail[] {
        const months: MonthlyDetail[] = []
        for (let m = 1; m <= 12; m++) {
            const detail = this.getMonthlyDetail(year, m)
            if (detail) {
                months.push(detail)
            }
        }
        return months
    }

    /**
     * 获取指定日期的流日信息
     */
    getDailyDetail(year: number, month: number, day: number): DailyDetail | null {
        if (!this.astrolabe) return null

        try {
            const dayDate = new Date(year, month - 1, day)
            const horoscope = this.astrolabe.horoscope(dayDate) as any

            if (!horoscope?.daily) return null

            const daily = horoscope.daily
            const mutagen = this.parseMutagen(daily.mutagen)

            return {
                day,
                heavenlyStem: daily.heavenlyStem || '',
                earthlyBranch: daily.earthlyBranch || '',
                palaceIndex: daily.index ?? daily.palaceIndex ?? 0,
                palaceName: daily.name || '',
                mutagen,
                palaceNames: daily.palaceNames || undefined
            }
        } catch {
            return null
        }
    }

    /**
     * 获取某月所有日的流日列表
     */
    getDailyList(year: number, month: number): DailyDetail[] {
        const daysInMonth = new Date(year, month, 0).getDate()
        const days: DailyDetail[] = []

        for (let d = 1; d <= daysInMonth; d++) {
            const detail = this.getDailyDetail(year, month, d)
            if (detail) {
                days.push(detail)
            }
        }

        return days
    }

    /**
     * 获取指定时辰的流时信息
     */
    getHourlyDetail(year: number, month: number, day: number, hour: number): HourlyDetail | null {
        if (!this.astrolabe) return null

        const hourNames = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

        try {
            const hourDate = new Date(year, month - 1, day, hour * 2 + 1)
            const horoscope = this.astrolabe.horoscope(hourDate, hour) as any

            if (!horoscope?.hourly) return null

            const hourly = horoscope.hourly
            const mutagen = this.parseMutagen(hourly.mutagen)

            return {
                hour,
                hourName: hourNames[hour] || '',
                heavenlyStem: hourly.heavenlyStem || '',
                earthlyBranch: hourly.earthlyBranch || '',
                palaceIndex: hourly.index ?? hourly.palaceIndex ?? 0,
                palaceName: hourly.name || '',
                mutagen,
                palaceNames: hourly.palaceNames || undefined
            }
        } catch {
            return null
        }
    }

    /**
     * 获取12个时辰的流时列表
     */
    getHourlyList(year: number, month: number, day: number): HourlyDetail[] {
        const hours: HourlyDetail[] = []
        for (let h = 0; h < 12; h++) {
            const detail = this.getHourlyDetail(year, month, day, h)
            if (detail) {
                hours.push(detail)
            }
        }
        return hours
    }

    /**
     * 根据天干获取四化
     */
    private getMutagenByStem(stem: string): MutagenInfo | undefined {
        // 四化表：甲廉破武阳、乙机梁紫阴...
        const mutagenTable: Record<string, string[]> = {
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

        const stars = mutagenTable[stem]
        if (!stars) return undefined

        return {
            lu: stars[0],
            quan: stars[1],
            ke: stars[2],
            ji: stars[3]
        }
    }

    /**
     * 解析四化数组
     */
    private parseMutagen(mutagenArray: any): MutagenInfo | undefined {
        if (!mutagenArray || !Array.isArray(mutagenArray) || mutagenArray.length < 4) {
            return undefined
        }

        return {
            lu: mutagenArray[0] || '',
            quan: mutagenArray[1] || '',
            ke: mutagenArray[2] || '',
            ji: mutagenArray[3] || ''
        }
    }

    /**
     * 根据当前年龄获取当前大限
     */
    getCurrentDecade(currentYear: number): DecadalDetail | null {
        const age = currentYear - this.birthYear + 1
        const decadalList = this.getDecadalList()
        return decadalList.find(d => d.startAge <= age && age <= d.endAge) || null
    }
}

// 导出单例
export const ziweiHoroscopeService = new ZiweiHoroscopeService()
