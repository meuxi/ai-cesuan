/**
 * 紫微斗数专业类型定义
 * 参考mingpan项目的完整数据结构
 */

// ==================== 输入类型 ====================

export interface ZiweiInput {
    year: number;
    month: number;
    day: number;
    hour: number;
    minute?: number;
    gender: 'male' | 'female';
    language?: string;  // 'zh-CN' | 'zh-TW' | 'en-US' | 'ja-JP'
}

// ==================== 基础类型 ====================

export interface StemBranch {
    stem: string;      // 天干
    branch: string;    // 地支
}

export interface FourPillars {
    year: StemBranch;
    month: StemBranch;
    day: StemBranch;
    hour: StemBranch;
}

export interface BasicInfo {
    zodiac: string;           // 生肖
    constellation: string;    // 星座
    fourPillars: FourPillars; // 四柱
    fiveElement: string;      // 五行局
    soul: string;             // 命主
    body: string;             // 身主
}

// ==================== 星曜类型 ====================

export interface Star {
    name: string;             // 星曜名称
    brightness?: string;      // 亮度（庙旺得利平不陷）
    type: 'major' | 'minor' | 'auxiliary' | 'flower' | 'helper';  // 主星/辅星/杂曜/桃花星/解神
    scope?: string;           // 范围：origin(本命) / decadal(大限) / yearly(流年)
}

export interface StarWithMutagen extends Star {
    mutagen?: string[];       // 四化标记 ['本禄', '限权', '年科']
}

// 流曜类型
export interface HoroscopeStar {
    name: string;             // 流曜名称 (流昌、流曲、流魁、流钺等)
    type: 'soft' | 'tough' | 'flower' | 'helper';  // 吉星/凶星/桃花/解神
    scope: 'yearly' | 'decadal' | 'monthly' | 'daily' | 'hourly';  // 作用范围
}

// ==================== 宫位类型 ====================

export interface Palace {
    name: string;               // 宫位名称
    index: number;              // 宫位索引 (0-11)
    position: number;           // 命盘位置 (0-11)
    earthlyBranch: string;      // 地支
    heavenlyStem: string;       // 天干
    majorStars: StarWithMutagen[];    // 主星
    minorStars: StarWithMutagen[];    // 辅星
    adjStars?: StarWithMutagen[];     // 杂曜（参考MingAI）
    horoscopeStars?: HoroscopeStar[]; // 流曜
    isBodyPalace?: boolean;     // 是否为身宫
    extras?: {                  // 额外信息
        changsheng12?: string;    // 长生十二宫
        boshi12?: string;         // 博士十二宫
        jiangqian12?: string;     // 将前十二宫
        suiqian12?: string;       // 岁前十二宫
        ages?: number[];          // 小限年龄序列
    };
}

// ==================== 大限类型 ====================

export interface DecadeInfo {
    index: number;              // 大限索引 (0-11)
    palaceIndex: number;        // 对应的宫位索引
    startAge: number;           // 起始年龄（虚岁）
    endAge: number;             // 结束年龄（虚岁）
    heavenlyStem: string;       // 大限天干
    earthlyBranch: string;      // 大限地支
    palaceName: string;         // 大限宫位名称
    label: string;              // 显示标签
    isCurrent?: boolean;        // 是否为当前大限
    stars?: (string | HoroscopeStar)[][];  // 大限流曜 (12宫位数组)
}

// ==================== 流年类型 ====================

export interface YearlyInfo {
    year: number;               // 年份
    age: number;                // 虚岁
    heavenlyStem: string;       // 流年天干
    earthlyBranch: string;      // 流年地支
    palaceIndex: number;        // 流年命宫位置
    stars?: (string | HoroscopeStar)[][];  // 流年流曜 (12宫位数组)
}

// ==================== 童限类型 ====================

export interface ChildhoodLimitInfo {
    age: number;                // 年龄（1-6岁）
    palaceIndex: number;        // 对应宫位索引
    palaceName: string;         // 宫位名称
    heavenlyStem: string;       // 天干
    earthlyBranch: string;      // 地支
    label: string;              // 显示标签
    isCurrent: boolean;         // 是否为当前童限
    ganzhi: string;             // 干支组合
}

// ==================== 小限类型 ====================

export interface MinorLimitInfo {
    age: number;                // 虚岁
    year: number;               // 年份
    palaceIndex: number;        // 小限命宫位置
    heavenlyStem: string;       // 小限天干
    earthlyBranch: string;      // 小限地支
    palaceNames?: string[];     // 小限十二宫排列
    mutagen?: string[];         // 小限四化（化禄、化权、化科、化忌星曜）
}

// ==================== 四化类型 ====================

export interface MutagenInfo {
    lu?: string;                // 化禄星曜
    quan?: string;              // 化权星曜
    ke?: string;                // 化科星曜
    ji?: string;                // 化忌星曜
}

export interface CompleteMutagenInfo {
    natal: MutagenInfo;         // 本命四化
    decadal?: MutagenInfo;      // 大限四化
    minorLimit?: MutagenInfo;   // 小限四化
    yearly?: MutagenInfo;       // 流年四化
    monthly?: MutagenInfo;      // 流月四化
    daily?: MutagenInfo;        // 流日四化
    hourly?: MutagenInfo;       // 流时四化
    combined: Map<string, string[]>;  // 合并的四化信息
}

// ==================== 增强宫位类型（用于显示） ====================

export interface EnhancedPalace extends Palace {
    // 大限信息
    decadeInfo?: {
        startAge: number;
        endAge: number;
        isCurrent?: boolean;
    };

    // 动态宫位名称
    dynamicNames?: {
        decadal?: string;       // 大限时的名称（如"限财帛"）
        yearly?: string;        // 流年时的名称（如"年官禄"）
    };

    // 高亮状态
    isDecadeHighlight?: boolean;  // 是否为选中的大限宫位
    isYearlyHighlight?: boolean;  // 是否为选中的流年宫位

    // 小限年龄
    minorLimitAges?: number[];
}

// ==================== 最终结果类型 ====================

export interface ZiweiResult {
    // 基本信息
    basicInfo: BasicInfo;

    // 日期信息
    solarDate: string;          // 阳历日期
    lunarDate: {                // 农历日期
        year: number;
        month: number;
        day: number;
        isLeapMonth: boolean;
    };

    // 十二宫位
    palaces: EnhancedPalace[];

    // 童限信息（1-6岁）
    childhoodLimits?: ChildhoodLimitInfo[];
    currentChildhood?: ChildhoodLimitInfo;
    isInChildhood?: boolean;

    // 大限信息
    decades: DecadeInfo[];
    currentDecade?: DecadeInfo;

    // 流年信息（如果请求）
    yearlyInfo?: YearlyInfo;

    // 四化信息
    mutagenInfo?: CompleteMutagenInfo;

    // 其他信息
    gender: 'male' | 'female';
    birthYear: number;
    language: string;
}

// ==================== API响应类型 ====================

export interface ZiweiApiResponse {
    success: boolean;
    data: ZiweiResult;
    message?: string;
}

// ==================== 常量 ====================

export const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
export const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

// 宫位名称（按顺序 - 顺时针方向）
export const PALACE_NAMES = [
    '命宮', '父母', '福德', '田宅', '官祿', '交友',
    '遷移', '疾厄', '財帛', '子女', '夫妻', '兄弟'
];

// 英文宫位名称（顺时针方向）
export const PALACE_NAMES_EN = [
    'Life', 'Parents', 'Fortune', 'Property', 'Career', 'Friends',
    'Travel', 'Health', 'Wealth', 'Children', 'Marriage', 'Siblings'
];

// 地支位置映射
export const BRANCH_POSITIONS: Record<string, { row: number; col: number }> = {
    '巳': { row: 0, col: 0 }, '午': { row: 0, col: 1 }, '未': { row: 0, col: 2 }, '申': { row: 0, col: 3 },
    '酉': { row: 1, col: 3 }, '戌': { row: 2, col: 3 }, '亥': { row: 3, col: 3 }, '子': { row: 3, col: 2 },
    '丑': { row: 3, col: 1 }, '寅': { row: 3, col: 0 }, '卯': { row: 2, col: 0 }, '辰': { row: 1, col: 0 }
};

// 星曜亮度颜色映射
export const BRIGHTNESS_COLORS: Record<string, string> = {
    '庙': 'text-red-600 bg-red-50',
    '旺': 'text-orange-600 bg-orange-50',
    '得': 'text-yellow-600 bg-yellow-50',
    '利': 'text-green-600 bg-green-50',
    '平': 'text-blue-600 bg-blue-50',
    '不': 'text-gray-600 bg-gray-50',
    '陷': 'text-purple-600 bg-purple-50'
};

// 四化颜色映射
export const MUTAGEN_COLORS: Record<string, string> = {
    '禄': 'bg-green-100 text-green-700 border-green-300',
    '权': 'bg-red-100 text-red-700 border-red-300',
    '科': 'bg-blue-100 text-blue-700 border-blue-300',
    '忌': 'bg-purple-100 text-purple-700 border-purple-300'
};

// 星曜类型颜色映射
export const STAR_TYPE_COLORS: Record<string, string> = {
    'major': 'text-red-600 font-bold',
    'minor': 'text-blue-600',
    'auxiliary': 'text-gray-600',
    'flower': 'text-pink-600',
    'helper': 'text-green-600'
};
