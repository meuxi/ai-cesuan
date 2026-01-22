/**
 * 人生K线图类型定义
 * 参考 lifekline3 项目
 */

export interface KLinePoint {
    age: number;        // 虚岁
    year: number;       // 年份
    ganZhi: string;     // 流年干支
    daYun: string;      // 大运干支
    open: number;       // 开盘值
    close: number;      // 收盘值
    high: number;       // 最高值
    low: number;        // 最低值
    score: number;      // 综合评分
    reason: string;     // 流年详批
}

export interface LifeKLineAnalysis {
    bazi: string[];
    summary: string;
    summaryScore: number;
    personality: string;
    personalityScore: number;
    industry: string;
    industryScore: number;
    fengShui: string;
    fengShuiScore: number;
    wealth: string;
    wealthScore: number;
    marriage: string;
    marriageScore: number;
    health: string;
    healthScore: number;
    family: string;
    familyScore: number;
}

export interface LifeKLineResult {
    chartData: KLinePoint[];
    analysis: LifeKLineAnalysis;
}

export enum Gender {
    MALE = 'male',
    FEMALE = 'female',
}

export interface LifeKLineInput {
    name: string;
    gender: Gender;
    birthYear: number;
    yearPillar: string;
    monthPillar: string;
    dayPillar: string;
    hourPillar: string;
    startAge: number;
    firstDaYun: string;
    isForward?: boolean;
    useAi?: boolean;
    apiKey?: string;
    apiBaseUrl?: string;
    modelName?: string;
}
