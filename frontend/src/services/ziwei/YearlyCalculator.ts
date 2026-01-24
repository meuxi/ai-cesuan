/**
 * 流年计算器
 * 参考mingpan实现
 */

import { YearlyInfo, EnhancedPalace } from '@/types/ziwei'

// iztro 流年数据接口
interface HoroscopeYearlyData {
    heavenlyStem?: string
    earthlyBranch?: string
    index?: number
    palaceIndex?: number
    name?: string
    mutagen?: string[]
    palaceNames?: string[]
    _fixed?: boolean
}

// 天干顺序
const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

// 地支顺序
const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

// 已知年份对照表（用于验证）
const KNOWN_YEARS: Record<number, { stem: string; branch: string }> = {
    2020: { stem: '庚', branch: '子' },
    2021: { stem: '辛', branch: '丑' },
    2022: { stem: '壬', branch: '寅' },
    2023: { stem: '癸', branch: '卯' },
    2024: { stem: '甲', branch: '辰' },
    2025: { stem: '乙', branch: '巳' },
    2026: { stem: '丙', branch: '午' },
    2027: { stem: '丁', branch: '未' },
    2028: { stem: '戊', branch: '申' },
    2029: { stem: '己', branch: '酉' },
    2030: { stem: '庚', branch: '戌' }
}

export class YearlyCalculator {
    /**
     * 获取指定年份的天干地支
     */
    static getYearStemBranch(year: number): { stem: string; branch: string } {
        // 如果有已知的对照表，直接返回
        if (KNOWN_YEARS[year]) {
            return KNOWN_YEARS[year]
        }

        // 使用公元4年为甲子年的基准进行计算
        const offset = year - 4
        const stemIndex = ((offset % 10) + 10) % 10
        const branchIndex = ((offset % 12) + 12) % 12

        return {
            stem: HEAVENLY_STEMS[stemIndex],
            branch: EARTHLY_BRANCHES[branchIndex]
        }
    }

    /**
     * 计算指定年份的流年信息
     */
    static calculate(
        year: number,
        birthYear: number,
        palaces: EnhancedPalace[]
    ): YearlyInfo {
        // 计算虚岁
        const age = year - birthYear + 1

        // 获取流年天干地支
        const { stem, branch } = this.getYearStemBranch(year)

        // 找到流年地支对应的宫位（流年命宫）
        const palaceIndex = palaces.findIndex(p => p.earthlyBranch === branch)

        return {
            year,
            age,
            heavenlyStem: stem,
            earthlyBranch: branch,
            palaceIndex: palaceIndex !== -1 ? palaceIndex : 0
        }
    }

    /**
     * 计算年份范围的流年
     */
    static calculateRange(
        startYear: number,
        endYear: number,
        birthYear: number,
        palaces: EnhancedPalace[]
    ): YearlyInfo[] {
        const results: YearlyInfo[] = []

        for (let year = startYear; year <= endYear; year++) {
            results.push(this.calculate(year, birthYear, palaces))
        }

        return results
    }

    /**
     * 获取流年宫位名称映射
     */
    static getYearlyPalaceNames(yearlyBranch: string, palaces: EnhancedPalace[]): Map<number, string> {
        const mapping = new Map<number, string>()

        // 找到流年地支对应的宫位作为流年命宫
        const yearlyMingIndex = palaces.findIndex(p => p.earthlyBranch === yearlyBranch)
        if (yearlyMingIndex === -1) return mapping

        // 十二宫位名称
        const palaceNames = [
            '命宮', '兄弟', '夫妻', '子女', '財帛', '疾厄',
            '遷移', '交友', '官祿', '田宅', '福德', '父母'
        ]

        // 根据流年命宫重新排列
        for (let i = 0; i < 12; i++) {
            const currentIndex = (yearlyMingIndex + i) % 12
            mapping.set(currentIndex, `年${palaceNames[i]}`)
        }

        return mapping
    }

    /**
     * 修正流年信息（如果iztro返回错误）
     */
    static fixYearlyInfo(horoscopeYearly: HoroscopeYearlyData | null, targetYear: number): HoroscopeYearlyData | null {
        if (!horoscopeYearly) return null

        const correct = this.getYearStemBranch(targetYear)

        // 检查是否需要修正
        if (horoscopeYearly.earthlyBranch !== correct.branch) {
            return {
                ...horoscopeYearly,
                heavenlyStem: correct.stem,
                earthlyBranch: correct.branch,
                _fixed: true
            }
        }

        return horoscopeYearly
    }
}
