/**
 * 大限计算器
 * 参考mingpan实现
 */

import { DecadeInfo, FourPillars, EnhancedPalace } from '@/types/ziwei'

export class DecadeCalculator {
    /**
     * 根据五行局获取起运年龄
     */
    static getStartAge(fiveElement: string): number {
        if (fiveElement.includes('水二')) return 2
        if (fiveElement.includes('木三')) return 3
        if (fiveElement.includes('金四')) return 4
        if (fiveElement.includes('土五')) return 5
        if (fiveElement.includes('火六')) return 6
        return 3 // 默认
    }

    /**
     * 判断大限是否顺行
     * 阳男阴女顺行，阴男阳女逆行
     */
    static isClockwise(yearStem: string, gender: 'male' | 'female'): boolean {
        const yangStems = ['甲', '丙', '戊', '庚', '壬']
        const isYangYear = yangStems.includes(yearStem)
        const isMale = gender === 'male'
        return (isYangYear && isMale) || (!isYangYear && !isMale)
    }

    /**
     * 计算大限信息
     */
    static calculate(
        palaces: EnhancedPalace[],
        fiveElement: string,
        fourPillars: FourPillars,
        gender: 'male' | 'female',
        birthYear: number
    ): DecadeInfo[] {
        const decades: DecadeInfo[] = []

        // 找到命宫索引
        let mingGongIndex = palaces.findIndex(p =>
            p.name === '命宮' || p.name === '命宫' || p.name.includes('命')
        )
        if (mingGongIndex === -1) mingGongIndex = 0

        // 获取起运年龄
        const startAge = this.getStartAge(fiveElement)

        // 判断顺逆行
        const isClockwise = this.isClockwise(fourPillars.year.stem, gender)

        // 如果起运年龄大于1，添加童限
        if (startAge > 1) {
            decades.push({
                index: -1,
                palaceIndex: mingGongIndex,
                startAge: 1,
                endAge: startAge - 1,
                heavenlyStem: palaces[mingGongIndex]?.heavenlyStem || '',
                earthlyBranch: palaces[mingGongIndex]?.earthlyBranch || '',
                palaceName: '童限',
                label: `童限 1-${startAge - 1}岁`,
                isCurrent: this.isCurrentDecade(1, startAge - 1, birthYear)
            })
        }

        // 生成12个大限
        let currentStartAge = startAge
        for (let i = 0; i < 12; i++) {
            const palaceIndex = isClockwise
                ? (mingGongIndex + i) % 12
                : (mingGongIndex - i + 12) % 12

            const palace = palaces[palaceIndex]
            const endAge = currentStartAge + 9

            decades.push({
                index: i,
                palaceIndex,
                startAge: currentStartAge,
                endAge,
                heavenlyStem: palace?.heavenlyStem || '',
                earthlyBranch: palace?.earthlyBranch || '',
                palaceName: palace?.name || '',
                label: `${palace?.name || ''} ${currentStartAge}-${endAge}岁`,
                isCurrent: this.isCurrentDecade(currentStartAge, endAge, birthYear)
            })

            currentStartAge = endAge + 1
        }

        return decades
    }

    /**
     * 判断是否为当前大限
     */
    static isCurrentDecade(startAge: number, endAge: number, birthYear: number): boolean {
        const currentAge = new Date().getFullYear() - birthYear + 1
        return currentAge >= startAge && currentAge <= endAge
    }

    /**
     * 获取当前大限
     */
    static getCurrentDecade(decades: DecadeInfo[], birthYear: number): DecadeInfo | undefined {
        const currentAge = new Date().getFullYear() - birthYear + 1
        return decades.find(d => currentAge >= d.startAge && currentAge <= d.endAge)
    }

    /**
     * 计算当前年龄（虚岁）
     */
    static getCurrentAge(birthYear: number, targetYear?: number): number {
        const actualTargetYear = targetYear || new Date().getFullYear()
        return actualTargetYear - birthYear + 1
    }
}
