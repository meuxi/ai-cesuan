/**
 * 紫微斗数 React Hook
 * 融合 iztro-hook 和 MingAI-master 的优点
 * 提供命盘计算和运限获取功能
 */

import { useState, useEffect, useMemo, useCallback } from 'react'
import { astro } from 'iztro'
import { logger } from '@/utils/logger'

// 使用 ReturnType 推断类型，避免直接导入内部类型
type FunctionalAstrolabe = ReturnType<typeof astro.bySolar>
type FunctionalHoroscope = ReturnType<FunctionalAstrolabe['horoscope']>

// 输入参数类型（参考iztro-hook的IztroInput）
export interface IztroInput {
    birthday: string           // 生日 YYYY-MM-DD 格式
    birthTime: number          // 时辰索引 0-12
    gender: '男' | '女'        // 性别
    birthdayType: 'lunar' | 'solar'  // 历法类型
    isLeapMonth?: boolean      // 是否闰月
    fixLeap?: boolean          // 是否修正闰月
    astroType?: 'heaven' | 'earth' | 'human'  // 天盘/地盘/人盘（iztro-hook特性）
    language?: string          // 语言 zh-CN | zh-TW | en-US | ja-JP
}

// 童限信息（1-6岁）
export interface ChildhoodInfo {
    age: number
    palaceIndex: number
    palaceName: string
    heavenlyStem: string
    earthlyBranch: string
    isCurrent: boolean
    ganzhi: string
}

// 大限信息
export interface DecadalInfo {
    index: number
    startAge: number
    endAge: number
    heavenlyStem: string
    earthlyBranch: string
    palaceName: string
    palaceIndex: number
    isChildhood?: boolean  // 是否为童限
    mutagen?: {
        lu: string
        quan: string
        ke: string
        ji: string
    }
}

// 流年/流月/流日信息
export interface FlowPeriodInfo {
    heavenlyStem: string
    earthlyBranch: string
    palaceIndex: number
    palaceName: string
    mutagen?: {
        lu: string
        quan: string
        ke: string
        ji: string
    }
}

// 完整运限信息
export interface HoroscopeData {
    decadal: DecadalInfo | null
    yearly: FlowPeriodInfo | null
    monthly: FlowPeriodInfo | null
    daily: FlowPeriodInfo | null
    hourly: FlowPeriodInfo | null
    isChildhood?: boolean  // 是否在童限期
    childhood?: ChildhoodInfo | null  // 当前童限信息
}

// 童限宫位映射表（参考iztro）
// 一命二财三疾厄，四岁夫妻五福德，六岁事业
export const CHILDHOOD_PALACE_NAMES = ['命宫', '财帛', '疾厄', '夫妻', '福德', '官禄']

// 将小时转换为时辰索引
export function hourToTimeIndex(hour: number): number {
    if (hour >= 23) return 12  // 晚子时
    if (hour >= 0 && hour < 1) return 0  // 早子时
    return Math.floor((hour + 1) / 2)
}

// 时辰索引转时辰名称
const TIME_NAMES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子']
export function timeIndexToName(index: number): string {
    return TIME_NAMES[index] || '子'
}

/**
 * useIztro Hook
 * 提供紫微斗数命盘和运限计算
 */
export function useIztro(input: IztroInput | null) {
    const [astrolabe, setAstrolabe] = useState<FunctionalAstrolabe | null>(null)
    const [horoscopeDate, setHoroscopeDate] = useState<Date>(new Date())
    const [horoscopeHour, setHoroscopeHour] = useState<number>(hourToTimeIndex(new Date().getHours()))
    const [horoscope, setHoroscope] = useState<FunctionalHoroscope | null>(null)
    const [error, setError] = useState<string | null>(null)

    // 计算命盘
    useEffect(() => {
        if (!input || !input.birthday) {
            setAstrolabe(null)
            return
        }

        try {
            const dateStr = input.birthday
            const date = new Date(dateStr)

            if (isNaN(date.getTime())) {
                setError('无效的日期格式')
                return
            }

            let result: FunctionalAstrolabe

            const lang = input.language || 'zh-CN'

            if (input.birthdayType === 'lunar') {
                result = astro.byLunar(
                    dateStr,
                    input.birthTime,
                    input.gender,
                    input.isLeapMonth ?? false,
                    input.fixLeap ?? true,
                    lang
                )
            } else {
                result = astro.bySolar(
                    dateStr,
                    input.birthTime,
                    input.gender,
                    input.fixLeap ?? true,
                    lang
                )
            }

            setAstrolabe(result)
            setError(null)
        } catch (err: unknown) {
            logger.error('命盘计算失败:', err)
            setError(err instanceof Error ? err.message : '命盘计算失败')
            setAstrolabe(null)
        }
    }, [input?.birthday, input?.birthTime, input?.gender, input?.birthdayType, input?.isLeapMonth, input?.fixLeap, input?.language])

    // 计算运限
    useEffect(() => {
        if (!astrolabe) {
            setHoroscope(null)
            return
        }

        try {
            const result = astrolabe.horoscope(horoscopeDate, horoscopeHour)
            setHoroscope(result)
        } catch (err) {
            logger.error('运限计算失败:', err)
            setHoroscope(null)
        }
    }, [astrolabe, horoscopeDate, horoscopeHour])

    // 设置运限日期
    const setHoroscopeDatetime = useCallback((date: Date | string, hour?: number) => {
        const newDate = typeof date === 'string' ? new Date(date) : date
        setHoroscopeDate(newDate)

        if (typeof hour === 'number') {
            setHoroscopeHour(hour)
        } else {
            setHoroscopeHour(hourToTimeIndex(newDate.getHours()))
        }
    }, [])

    // 解析运限数据
    const horoscopeData = useMemo<HoroscopeData | null>(() => {
        if (!horoscope) return null

        const parseFlowPeriod = (data: any): FlowPeriodInfo | null => {
            if (!data) return null
            return {
                heavenlyStem: data.heavenlyStem || '',
                earthlyBranch: data.earthlyBranch || '',
                palaceIndex: data.palaceIndex ?? 0,
                palaceName: data.name || '',
                mutagen: data.mutagen ? {
                    lu: data.mutagen[0] || '',
                    quan: data.mutagen[1] || '',
                    ke: data.mutagen[2] || '',
                    ji: data.mutagen[3] || ''
                } : undefined
            }
        }

        const decadalData = (horoscope as any).decadal
        const decadal: DecadalInfo | null = decadalData ? {
            index: decadalData.index ?? 0,
            startAge: decadalData.range?.[0] ?? 0,
            endAge: decadalData.range?.[1] ?? 0,
            heavenlyStem: decadalData.heavenlyStem || '',
            earthlyBranch: decadalData.earthlyBranch || '',
            palaceName: decadalData.name || '',
            palaceIndex: decadalData.palaceIndex ?? 0,
            mutagen: decadalData.mutagen ? {
                lu: decadalData.mutagen[0] || '',
                quan: decadalData.mutagen[1] || '',
                ke: decadalData.mutagen[2] || '',
                ji: decadalData.mutagen[3] || ''
            } : undefined
        } : null

        return {
            decadal,
            yearly: parseFlowPeriod((horoscope as any).yearly),
            monthly: parseFlowPeriod((horoscope as any).monthly),
            daily: parseFlowPeriod((horoscope as any).daily),
            hourly: parseFlowPeriod((horoscope as any).hourly)
        }
    }, [horoscope])

    // 获取童限列表（1-6岁）
    const childhoodList = useMemo<ChildhoodInfo[]>(() => {
        if (!astrolabe) return []

        const result: ChildhoodInfo[] = []
        const palaces = astrolabe.palaces as any[]
        
        // 建立宫位名称到宫位对象的映射
        const palaceMap: Record<string, any> = {}
        palaces.forEach((palace: any) => {
            palaceMap[palace.name] = palace
        })

        // 童限宫位：一命二财三疾厄，四岁夫妻五福德，六岁事业
        for (let age = 1; age <= 6; age++) {
            const palaceName = CHILDHOOD_PALACE_NAMES[age - 1]
            const palace = palaceMap[palaceName]
            
            if (palace) {
                const palaceIndex = palaces.findIndex((p: any) => p.name === palaceName)
                result.push({
                    age,
                    palaceIndex,
                    palaceName,
                    heavenlyStem: palace.heavenlyStem || '',
                    earthlyBranch: palace.earthlyBranch || '',
                    isCurrent: false, // 需要根据实际年龄判断
                    ganzhi: `${palace.heavenlyStem || ''}${palace.earthlyBranch || ''}`
                })
            }
        }

        return result
    }, [astrolabe])

    // 获取大限列表（含起运年龄计算）
    const decadalList = useMemo<DecadalInfo[]>(() => {
        if (!astrolabe) return []

        const fiveElement = astrolabe.fiveElementsClass || ''
        const fiveElementMap: Record<string, number> = {
            '二': 2, '三': 3, '四': 4, '五': 5, '六': 6
        }
        const match = fiveElement.match(/[二三四五六]/)
        const startAge = match ? (fiveElementMap[match[0]] || 2) : 2

        // 判断大限顺逆（阳男阴女顺行，阴男阳女逆行）
        const yearStem = astrolabe.chineseDate?.split('')?.[0] || ''
        const yangStems = ['甲', '丙', '戊', '庚', '壬']
        const isYangStem = yangStems.includes(yearStem)
        const isMale = astrolabe.gender === '男'
        const isClockwise = (isYangStem && isMale) || (!isYangStem && !isMale)

        const palaces = astrolabe.palaces as any[]
        const result: DecadalInfo[] = []

        for (let i = 0; i < 12; i++) {
            // 根据顺逆确定宫位索引
            const palaceIdx = isClockwise ? i : (12 - i) % 12
            const palace = palaces[palaceIdx]

            result.push({
                index: i,
                startAge: startAge + i * 10,
                endAge: startAge + (i + 1) * 10 - 1,
                heavenlyStem: palace?.heavenlyStem || '',
                earthlyBranch: palace?.earthlyBranch || '',
                palaceName: palace?.name || '',
                palaceIndex: palaceIdx
            })
        }

        return result
    }, [astrolabe])

    // 获取指定年份的流年信息
    const getYearlyHoroscope = useCallback((year: number): FlowPeriodInfo | null => {
        if (!astrolabe) return null
        try {
            const yearDate = new Date(year, 5, 15)  // 年中日期
            const yearHoroscope = astrolabe.horoscope(yearDate)
            const yearly = (yearHoroscope as any).yearly
            if (!yearly) return null
            return {
                heavenlyStem: yearly.heavenlyStem || '',
                earthlyBranch: yearly.earthlyBranch || '',
                palaceIndex: yearly.palaceIndex ?? 0,
                palaceName: yearly.name || '',
                mutagen: yearly.mutagen ? {
                    lu: yearly.mutagen[0] || '',
                    quan: yearly.mutagen[1] || '',
                    ke: yearly.mutagen[2] || '',
                    ji: yearly.mutagen[3] || ''
                } : undefined
            }
        } catch {
            return null
        }
    }, [astrolabe])

    // 获取指定月份的流月信息
    const getMonthlyHoroscope = useCallback((year: number, month: number): FlowPeriodInfo | null => {
        if (!astrolabe) return null
        try {
            const monthDate = new Date(year, month - 1, 15)
            const monthHoroscope = astrolabe.horoscope(monthDate)
            const monthly = (monthHoroscope as any).monthly
            if (!monthly) return null
            return {
                heavenlyStem: monthly.heavenlyStem || '',
                earthlyBranch: monthly.earthlyBranch || '',
                palaceIndex: monthly.palaceIndex ?? 0,
                palaceName: monthly.name || '',
                mutagen: monthly.mutagen ? {
                    lu: monthly.mutagen[0] || '',
                    quan: monthly.mutagen[1] || '',
                    ke: monthly.mutagen[2] || '',
                    ji: monthly.mutagen[3] || ''
                } : undefined
            }
        } catch {
            return null
        }
    }, [astrolabe])

    // 获取指定日期的流日信息
    const getDailyHoroscope = useCallback((date: Date): FlowPeriodInfo | null => {
        if (!astrolabe) return null
        try {
            const dayHoroscope = astrolabe.horoscope(date)
            const daily = (dayHoroscope as any).daily
            if (!daily) return null
            return {
                heavenlyStem: daily.heavenlyStem || '',
                earthlyBranch: daily.earthlyBranch || '',
                palaceIndex: daily.palaceIndex ?? 0,
                palaceName: daily.name || '',
                mutagen: daily.mutagen ? {
                    lu: daily.mutagen[0] || '',
                    quan: daily.mutagen[1] || '',
                    ke: daily.mutagen[2] || '',
                    ji: daily.mutagen[3] || ''
                } : undefined
            }
        } catch {
            return null
        }
    }, [astrolabe])

    // 获取指定时辰的流时信息
    const getHourlyHoroscope = useCallback((date: Date, timeIndex?: number): FlowPeriodInfo | null => {
        if (!astrolabe) return null
        try {
            const hourIdx = timeIndex ?? hourToTimeIndex(date.getHours())
            const hourHoroscope = astrolabe.horoscope(date, hourIdx)
            const hourly = (hourHoroscope as any).hourly
            if (!hourly) return null
            return {
                heavenlyStem: hourly.heavenlyStem || '',
                earthlyBranch: hourly.earthlyBranch || '',
                palaceIndex: hourly.palaceIndex ?? 0,
                palaceName: hourly.name || '',
                mutagen: hourly.mutagen ? {
                    lu: hourly.mutagen[0] || '',
                    quan: hourly.mutagen[1] || '',
                    ke: hourly.mutagen[2] || '',
                    ji: hourly.mutagen[3] || ''
                } : undefined
            }
        } catch {
            return null
        }
    }, [astrolabe])

    // 获取指定年龄对应的童限或大限信息
    const getDecadeByAge = useCallback((age: number): DecadalInfo | ChildhoodInfo | null => {
        // 1-6岁为童限
        if (age >= 1 && age <= 6) {
            return childhoodList[age - 1] || null
        }
        // 7岁以上查找大限
        const decade = decadalList.find(d => age >= d.startAge && age <= d.endAge)
        return decade || null
    }, [childhoodList, decadalList])

    // 生成命盘文字版本
    const generateChartText = useCallback((): string => {
        if (!astrolabe) return ''

        const lines: string[] = []
        lines.push('【紫微斗数命盘】')
        lines.push(`阳历：${astrolabe.solarDate}`)
        lines.push(`农历：${astrolabe.lunarDate}`)
        lines.push(`四柱：${astrolabe.chineseDate}`)
        lines.push(`命主：${astrolabe.soul}  身主：${astrolabe.body}`)
        lines.push(`五行局：${astrolabe.fiveElementsClass}`)
        lines.push(`属相：${astrolabe.zodiac}  星座：${astrolabe.sign}`)
        lines.push('')
        lines.push('【十二宫位】')

        astrolabe.palaces.forEach((palace: any) => {
            const bodyMark = palace.isBodyPalace ? '（身宫）' : ''
            const majorStars = palace.majorStars.map((s: any) => {
                let str = s.name
                if (s.brightness) str += s.brightness
                if (s.mutagen) str += `化${s.mutagen}`
                return str
            }).join('、') || '无主星'
            const minorStars = palace.minorStars.map((s: any) => s.name + (s.brightness || '')).join('、')
            lines.push(`${palace.name}${bodyMark}（${palace.heavenlyStem}${palace.earthlyBranch}）`)
            lines.push(`  主星：${majorStars}`)
            if (minorStars) lines.push(`  辅星：${minorStars}`)
        })

        // 添加运限信息
        if (horoscopeData) {
            lines.push('')
            lines.push('【当前运限】')
            if (horoscopeData.decadal) {
                lines.push(`大限：${horoscopeData.decadal.heavenlyStem}${horoscopeData.decadal.earthlyBranch} ${horoscopeData.decadal.palaceName} (${horoscopeData.decadal.startAge}-${horoscopeData.decadal.endAge}岁)`)
                if (horoscopeData.decadal.mutagen) {
                    lines.push(`  限四化：禄-${horoscopeData.decadal.mutagen.lu} 权-${horoscopeData.decadal.mutagen.quan} 科-${horoscopeData.decadal.mutagen.ke} 忌-${horoscopeData.decadal.mutagen.ji}`)
                }
            }
            if (horoscopeData.yearly) {
                lines.push(`流年：${horoscopeData.yearly.heavenlyStem}${horoscopeData.yearly.earthlyBranch} ${horoscopeData.yearly.palaceName}`)
                if (horoscopeData.yearly.mutagen) {
                    lines.push(`  年四化：禄-${horoscopeData.yearly.mutagen.lu} 权-${horoscopeData.yearly.mutagen.quan} 科-${horoscopeData.yearly.mutagen.ke} 忌-${horoscopeData.yearly.mutagen.ji}`)
                }
            }
        }

        return lines.join('\n')
    }, [astrolabe, horoscopeData])

    return {
        astrolabe,
        horoscope,
        horoscopeData,
        decadalList,
        childhoodList,      // 新增：童限列表
        error,
        setHoroscopeDatetime,
        getYearlyHoroscope,
        getMonthlyHoroscope,
        getDailyHoroscope,
        getHourlyHoroscope, // 新增：流时获取
        getDecadeByAge,     // 新增：按年龄获取运限
        generateChartText
    }
}

export default useIztro
