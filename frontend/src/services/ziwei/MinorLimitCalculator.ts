/**
 * 小限计算器
 * 参考mingpan实现
 * 
 * 小限规则：
 * - 以出生年支确定起始宫位
 * - 男顺女逆运行
 * - 每年一宫，12年一轮回
 */

import { EnhancedPalace } from '@/types/ziwei'

export interface MinorLimitInfo {
    age: number
    year: number
    palaceIndex: number
    heavenlyStem: string
    earthlyBranch: string
}

// 小限起始宫位对照表（根据出生年支）
const MINOR_LIMIT_START: Record<string, string> = {
    '寅': '辰', '午': '辰', '戌': '辰',  // 寅午戌年生人从辰宫起
    '申': '戌', '子': '戌', '辰': '戌',  // 申子辰年生人从戌宫起
    '巳': '未', '酉': '未', '丑': '未',  // 巳酉丑年生人从未宫起
    '亥': '丑', '卯': '丑', '未': '丑'   // 亥卯未年生人从丑宫起
}

// 地支顺序
const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

// 天干顺序
const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

export class MinorLimitCalculator {
    /**
     * 获取小限起始地支
     */
    static getStartBranch(yearBranch: string): string {
        return MINOR_LIMIT_START[yearBranch] || '辰'
    }

    /**
     * 计算指定年龄的小限宫位索引
     */
    static getMinorLimitPalaceIndex(
        yearBranch: string,
        gender: 'male' | 'female',
        age: number,
        palaces: EnhancedPalace[]
    ): number {
        const startBranch = this.getStartBranch(yearBranch)
        const startIndex = EARTHLY_BRANCHES.indexOf(startBranch)

        if (startIndex === -1) return 0

        const offset = (age - 1) % 12
        let targetBranchIndex: number

        if (gender === 'male') {
            // 男命顺行
            targetBranchIndex = (startIndex + offset) % 12
        } else {
            // 女命逆行
            targetBranchIndex = (startIndex - offset + 12) % 12
        }

        const targetBranch = EARTHLY_BRANCHES[targetBranchIndex]
        const palaceIndex = palaces.findIndex(p => p.earthlyBranch === targetBranch)

        return palaceIndex !== -1 ? palaceIndex : 0
    }

    /**
     * 计算指定年份的小限信息
     */
    static calculate(
        birthYear: number,
        targetYear: number,
        yearBranch: string,
        gender: 'male' | 'female',
        palaces: EnhancedPalace[]
    ): MinorLimitInfo {
        const age = targetYear - birthYear + 1  // 虚岁
        const palaceIndex = this.getMinorLimitPalaceIndex(yearBranch, gender, age, palaces)

        // 计算小限天干地支
        const { stem, branch } = this.getYearStemBranch(targetYear)

        return {
            age,
            year: targetYear,
            palaceIndex,
            heavenlyStem: stem,
            earthlyBranch: branch
        }
    }

    /**
     * 计算年份范围内的小限
     */
    static calculateRange(
        birthYear: number,
        startYear: number,
        endYear: number,
        yearBranch: string,
        gender: 'male' | 'female',
        palaces: EnhancedPalace[]
    ): MinorLimitInfo[] {
        const results: MinorLimitInfo[] = []

        for (let year = startYear; year <= endYear; year++) {
            results.push(this.calculate(birthYear, year, yearBranch, gender, palaces))
        }

        return results
    }

    /**
     * 计算宫位的小限年龄序列
     */
    static calculatePalaceAges(
        palaceIndex: number,
        yearBranch: string,
        gender: 'male' | 'female',
        palaces: EnhancedPalace[],
        maxAge: number = 96
    ): number[] {
        const ages: number[] = []
        const palaceBranch = palaces[palaceIndex]?.earthlyBranch
        if (!palaceBranch) return ages

        for (let age = 1; age <= maxAge; age++) {
            const idx = this.getMinorLimitPalaceIndex(yearBranch, gender, age, palaces)
            if (idx === palaceIndex) {
                ages.push(age)
            }
        }

        return ages
    }

    /**
     * 获取年份的天干地支
     */
    private static getYearStemBranch(year: number): { stem: string; branch: string } {
        const offset = year - 4  // 公元4年为甲子年
        const stemIndex = ((offset % 10) + 10) % 10
        const branchIndex = ((offset % 12) + 12) % 12

        return {
            stem: HEAVENLY_STEMS[stemIndex],
            branch: EARTHLY_BRANCHES[branchIndex]
        }
    }
}
