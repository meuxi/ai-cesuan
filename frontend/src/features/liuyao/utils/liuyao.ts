/**
 * 六爻算法工具
 * 移植自源项目 F:\备份\六爻起卦工具源码\utils\iching.ts
 *
 * @deprecated 此文件仅用于历史记录的离线fallback计算
 * 主要卦象计算应使用后端API（useLiuYao hook）
 * 后端算法在 src/liuyao.py 中实现
 */

import { LineType, Trigram, HexagramInfo, LineDetails, FuShenInfo } from '../types';

// ========== 常量定义 ==========

// 八卦定义
export const TRIGRAMS: Record<number, Trigram> = {
    1: { name: 'Heaven', chineseName: '乾', nature: 'Sky', number: 1, element: '金', binary: '111' },
    2: { name: 'Lake', chineseName: '兑', nature: 'Marsh', number: 2, element: '金', binary: '011' },
    3: { name: 'Fire', chineseName: '离', nature: 'Fire', number: 3, element: '火', binary: '101' },
    4: { name: 'Thunder', chineseName: '震', nature: 'Thunder', number: 4, element: '木', binary: '001' },
    5: { name: 'Wind', chineseName: '巽', nature: 'Wind', number: 5, element: '木', binary: '110' },
    6: { name: 'Water', chineseName: '坎', nature: 'Water', number: 6, element: '水', binary: '010' },
    7: { name: 'Mountain', chineseName: '艮', nature: 'Mountain', number: 7, element: '土', binary: '100' },
    8: { name: 'Earth', chineseName: '坤', nature: 'Earth', number: 8, element: '土', binary: '000' },
};

// 天干
const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];

// 六神
const SIX_BEASTS = ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武'];

// 五亲
const ALL_RELATIONS = ['父母', '兄弟', '官鬼', '妻财', '子孙'];

// 地支五行映射
const BRANCH_ELEMENTS: Record<string, string> = {
    '子': '水', '亥': '水',
    '寅': '木', '卯': '木',
    '巳': '火', '午': '火',
    '申': '金', '酉': '金',
    '辰': '土', '戌': '土', '丑': '土', '未': '土'
};

// 纳甲法规则
const NA_JIA_RULES: Record<number, { inner: string[], outer: string[], innerStem: string, outerStem: string }> = {
    1: { inner: ['子', '寅', '辰'], outer: ['午', '申', '戌'], innerStem: '甲', outerStem: '壬' },
    2: { inner: ['巳', '卯', '丑'], outer: ['亥', '酉', '未'], innerStem: '丁', outerStem: '丁' },
    3: { inner: ['卯', '丑', '亥'], outer: ['酉', '未', '巳'], innerStem: '己', outerStem: '己' },
    4: { inner: ['子', '寅', '辰'], outer: ['午', '申', '戌'], innerStem: '庚', outerStem: '庚' },
    5: { inner: ['丑', '亥', '酉'], outer: ['未', '巳', '卯'], innerStem: '辛', outerStem: '辛' },
    6: { inner: ['寅', '辰', '午'], outer: ['申', '戌', '子'], innerStem: '戊', outerStem: '戊' },
    7: { inner: ['辰', '午', '申'], outer: ['戌', '子', '寅'], innerStem: '丙', outerStem: '丙' },
    8: { inner: ['未', '巳', '卯'], outer: ['丑', '亥', '酉'], innerStem: '乙', outerStem: '癸' },
};

// 64卦名
const HEXAGRAM_NAMES: Record<number, Record<number, string>> = {
    1: { 1: '乾为天', 2: '天泽履', 3: '天火同人', 4: '天雷无妄', 5: '天风姤', 6: '天水讼', 7: '天山遁', 8: '天地否' },
    2: { 1: '泽天夬', 2: '兑为泽', 3: '泽火革', 4: '泽雷随', 5: '泽风大过', 6: '泽水困', 7: '泽山咸', 8: '泽地萃' },
    3: { 1: '火天大有', 2: '火泽睽', 3: '离为火', 4: '火雷噬嗑', 5: '火风鼎', 6: '火水未济', 7: '火山旅', 8: '火地晋' },
    4: { 1: '雷天大壮', 2: '雷泽归妹', 3: '雷火丰', 4: '震为雷', 5: '雷风恒', 6: '雷水解', 7: '雷山小过', 8: '雷地豫' },
    5: { 1: '风天小畜', 2: '风泽中孚', 3: '风火家人', 4: '风雷益', 5: '巽为风', 6: '风水涣', 7: '风山渐', 8: '风地观' },
    6: { 1: '水天需', 2: '水泽节', 3: '水火既济', 4: '水雷屯', 5: '水风井', 6: '坎为水', 7: '水山蹇', 8: '水地比' },
    7: { 1: '山天大畜', 2: '山泽损', 3: '山火贲', 4: '山雷颐', 5: '山风蛊', 6: '山水蒙', 7: '艮为山', 8: '山地剥' },
    8: { 1: '地天泰', 2: '地泽临', 3: '地火明夷', 4: '地雷复', 5: '地风升', 6: '地水师', 7: '地山谦', 8: '坤为地' },
};

// ========== 辅助函数 ==========

export const getTrigramNumber = (num: number): number => {
    const rem = num % 8;
    return rem === 0 ? 8 : rem;
};

export const getMovingLinePosition = (num: number): number => {
    const rem = num % 6;
    return rem === 0 ? 6 : rem;
};

export const determineLine = (backs: number): LineType => {
    if (backs === 1) return 0;
    if (backs === 2) return 1;
    if (backs === 3) return 2;
    return 3;
};

export const getLineName = (type: LineType): string => {
    switch (type) {
        case 0: return '少阳';
        case 1: return '少阴';
        case 2: return '老阳';
        case 3: return '老阴';
        default: return '未知';
    }
};

const toBinary = (lines: LineType[]): boolean[] => {
    return lines.map(l => (l === 0 || l === 2));
};

const getTrigramIndex = (l1: boolean, l2: boolean, l3: boolean): number => {
    if (l1 && l2 && l3) return 1;
    if (l1 && l2 && !l3) return 2;
    if (l1 && !l2 && l3) return 3;
    if (l1 && !l2 && !l3) return 4;
    if (!l1 && l2 && l3) return 5;
    if (!l1 && l2 && !l3) return 6;
    if (!l1 && !l2 && l3) return 7;
    if (!l1 && !l2 && !l3) return 8;
    return 1;
};

const getPalaceAndShiYing = (lines: boolean[]) => {
    const target = [...lines];
    const isPure = (l: boolean[]) => {
        const lower = getTrigramIndex(l[0], l[1], l[2]);
        const upper = getTrigramIndex(l[3], l[4], l[5]);
        return lower === upper;
    };

    if (isPure(target)) return { palaceTrigram: getTrigramIndex(target[0], target[1], target[2]), shi: 5, ying: 2 };

    target[0] = !target[0]; if (isPure(target)) return { palaceTrigram: getTrigramIndex(target[0], target[1], target[2]), shi: 0, ying: 3 };
    target[1] = !target[1]; if (isPure(target)) return { palaceTrigram: getTrigramIndex(target[0], target[1], target[2]), shi: 1, ying: 4 };
    target[2] = !target[2]; if (isPure(target)) return { palaceTrigram: getTrigramIndex(target[0], target[1], target[2]), shi: 2, ying: 5 };
    target[3] = !target[3]; if (isPure(target)) return { palaceTrigram: getTrigramIndex(target[0], target[1], target[2]), shi: 3, ying: 0 };
    target[4] = !target[4]; if (isPure(target)) return { palaceTrigram: getTrigramIndex(target[0], target[1], target[2]), shi: 4, ying: 1 };

    // 游魂
    target[3] = !target[3]; if (isPure(target)) return { palaceTrigram: getTrigramIndex(target[0], target[1], target[2]), shi: 3, ying: 0 };

    // 归魂
    target[0] = !target[0]; target[1] = !target[1]; target[2] = !target[2];
    if (isPure(target)) return { palaceTrigram: getTrigramIndex(target[0], target[1], target[2]), shi: 2, ying: 5 };

    return { palaceTrigram: 1, shi: 0, ying: 0 };
};

const getRelation = (palaceEl: string, lineEl: string): string => {
    const map: Record<string, Record<string, string>> = {
        '金': { '金': '兄弟', '木': '妻财', '水': '子孙', '火': '官鬼', '土': '父母' },
        '木': { '金': '官鬼', '木': '兄弟', '水': '父母', '火': '子孙', '土': '妻财' },
        '水': { '金': '父母', '木': '子孙', '水': '兄弟', '火': '妻财', '土': '官鬼' },
        '火': { '金': '妻财', '木': '父母', '水': '官鬼', '火': '兄弟', '土': '子孙' },
        '土': { '金': '子孙', '木': '官鬼', '水': '妻财', '火': '父母', '土': '兄弟' },
    };
    return map[palaceEl]?.[lineEl] || '兄弟';
};

const getDayStem = (): string => {
    const idx = new Date().getDate() % 10;
    return HEAVENLY_STEMS[idx];
};

const getSixBeastsStart = (dayStem: string): number => {
    if (['甲', '乙'].includes(dayStem)) return 0;
    if (['丙', '丁'].includes(dayStem)) return 1;
    if (dayStem === '戊') return 2;
    if (dayStem === '己') return 3;
    if (['庚', '辛'].includes(dayStem)) return 4;
    return 5;
};

const getHexagramBasicInfo = (upperIdx: number, lowerIdx: number, palaceElement: string) => {
    const lowerRule = NA_JIA_RULES[lowerIdx];
    const upperRule = NA_JIA_RULES[upperIdx];

    const allBranches = [...lowerRule.inner, ...upperRule.outer];
    const allStems = [...Array(3).fill(lowerRule.innerStem), ...Array(3).fill(upperRule.outerStem)];

    return allBranches.map((branch, i) => {
        const stem = allStems[i];
        const element = BRANCH_ELEMENTS[branch];
        const relation = getRelation(palaceElement, element);
        return { branch, stem, element, relation };
    });
};

// ========== 核心计算函数 ==========

export const calculateHexagram = (lines: LineType[]): HexagramInfo => {
    const binary = toBinary(lines);
    const lowerIdx = getTrigramIndex(binary[0], binary[1], binary[2]);
    const upperIdx = getTrigramIndex(binary[3], binary[4], binary[5]);

    const name = HEXAGRAM_NAMES[upperIdx][lowerIdx];
    const { palaceTrigram, shi, ying } = getPalaceAndShiYing(binary);
    const palaceElement = TRIGRAMS[palaceTrigram].element;
    const palaceName = TRIGRAMS[palaceTrigram].chineseName + '宫';

    // 1. 计算本卦详情
    const mainHexInfo = getHexagramBasicInfo(upperIdx, lowerIdx, palaceElement);

    // 2. 计算六神
    const startBeast = getSixBeastsStart(getDayStem());

    // 3. 计算变卦
    const hasMoving = lines.some(l => l === 2 || l === 3);
    let transformedDetails: ReturnType<typeof getHexagramBasicInfo> = [];
    let transformedName: string | undefined = undefined;

    if (hasMoving) {
        const transformedBinary = lines.map(l => {
            if (l === 2) return false;
            if (l === 3) return true;
            if (l === 0) return true;
            return false;
        });

        const tLower = getTrigramIndex(transformedBinary[0], transformedBinary[1], transformedBinary[2]);
        const tUpper = getTrigramIndex(transformedBinary[3], transformedBinary[4], transformedBinary[5]);

        transformedDetails = getHexagramBasicInfo(tUpper, tLower, palaceElement);
        transformedName = HEXAGRAM_NAMES[tUpper][tLower];
    }

    // 4. 计算伏神
    const presentRelations = new Set(mainHexInfo.map(i => i.relation));
    const missingRelations = ALL_RELATIONS.filter(r => !presentRelations.has(r));
    const fuShenMap: Record<number, FuShenInfo> = {};

    if (missingRelations.length > 0) {
        const palaceHexInfo = getHexagramBasicInfo(palaceTrigram, palaceTrigram, palaceElement);

        missingRelations.forEach(missing => {
            const idx = palaceHexInfo.findIndex(info => info.relation === missing);
            if (idx !== -1) {
                const info = palaceHexInfo[idx];
                fuShenMap[idx] = {
                    stem: info.stem,
                    branch: info.branch,
                    relation: info.relation,
                    element: info.element
                };
            }
        });
    }

    // 5. 构建爻详情
    const lineDetails: LineDetails[] = lines.map((l, i) => {
        const info = mainHexInfo[i];

        let changedType: LineType | undefined;
        let changedBranch: string | undefined;
        let changedStem: string | undefined;
        let changedRelation: string | undefined;

        if (hasMoving && transformedDetails.length > 0) {
            const tInfo = transformedDetails[i];
            changedType = (l === 0 || l === 3) ? 0 : 1;
            changedBranch = tInfo.branch;
            changedStem = tInfo.stem;
            changedRelation = tInfo.relation;
        }

        return {
            index: i,
            type: l,
            typeName: getLineName(l),
            isMoving: l === 2 || l === 3,
            branch: info.branch,
            stem: info.stem,
            element: info.element,
            sixRelation: info.relation,
            sixBeast: SIX_BEASTS[(startBeast + i) % 6],
            isShi: i === shi,
            isYing: i === ying,
            fuShen: fuShenMap[i],
            changedType,
            changedBranch,
            changedStem,
            changedRelation
        };
    });

    return {
        name,
        palaceName,
        palaceElement,
        lines: lineDetails,
        transformedName
    };
};

export const buildHexagramFromTrigrams = (upper: number, lower: number, movingLinePos: number): LineType[] => {
    const getLines = (tNum: number): boolean[] => {
        const map: Record<number, boolean[]> = {
            1: [true, true, true],
            2: [true, true, false],
            3: [true, false, true],
            4: [true, false, false],
            5: [false, true, true],
            6: [false, true, false],
            7: [false, false, true],
            8: [false, false, false],
        };
        return map[tNum];
    };

    const lowerLines = getLines(lower);
    const upperLines = getLines(upper);
    const allStaticLines = [...lowerLines, ...upperLines];

    return allStaticLines.map((isYang, index) => {
        const linePos = index + 1;
        const isMoving = linePos === movingLinePos;
        if (isMoving) return isYang ? 2 : 3;
        return isYang ? 0 : 1;
    });
};

// ========== 起卦方法 ==========

/**
 * 模拟摇一次铜钱（三枚）
 * 真实概率分布：
 * - 0背(三字/老阴): 1/8 = 12.5%
 * - 1背(少阳): 3/8 = 37.5%
 * - 2背(少阴): 3/8 = 37.5%
 * - 3背(老阳): 1/8 = 12.5%
 */
export const coinCastSingle = (): { lineType: LineType; backs: number } => {
    // 模拟三枚铜钱，true=正面(字), false=反面(背)
    const coin1 = Math.random() > 0.5;
    const coin2 = Math.random() > 0.5;
    const coin3 = Math.random() > 0.5;
    // 计算反面(背)的数量
    const backs = [coin1, coin2, coin3].filter(c => !c).length;
    return { lineType: determineLine(backs), backs };
};

export const coinCastFull = (): Array<{ lineType: LineType; backs: number }> => {
    return Array.from({ length: 6 }, () => coinCastSingle());
};

export const numberMethod = (upperNum: number, lowerNum: number, movingNum: number): LineType[] => {
    const upper = getTrigramNumber(upperNum);
    const lower = getTrigramNumber(lowerNum);
    const moving = getMovingLinePosition(movingNum);
    return buildHexagramFromTrigrams(upper, lower, moving);
};

/**
 * 时空起卦法
 * 上卦 = 时 + 分
 * 下卦 = 日 + 月
 * 动爻 = 上卦数 + 下卦数
 */
export const timeMethod = (): LineType[] => {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const day = now.getDate();
    const month = now.getMonth() + 1;

    const upper = getTrigramNumber(hours + minutes);
    const lower = getTrigramNumber(day + month);
    const moving = getMovingLinePosition(upper + lower);

    return buildHexagramFromTrigrams(upper, lower, moving);
};
