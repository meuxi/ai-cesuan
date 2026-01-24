/**
 * 六爻高级分析Hook
 * 提供空亡、旺衰、神系等专业分析功能
 */

import { useState, useCallback } from 'react';
import { 
    HexagramInfo, 
    AdvancedAnalysisResult, 
    KongWangState, 
    TimeRecommendation, 
    ExtendedYaoInfo,
    YaoAction,
    WangShuai,
    SpecialStatus,
    HuaType,
    ChangShengStage
} from '../types';

const API_BASE = '/api/liuyao';

// 地支列表
const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

// 天干列表
const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];

// 后端响应类型定义（snake_case）
interface BackendKongWang {
    xun: string;
    kong_dizhi: [string, string];
}

interface BackendInfluence {
    month_action?: string;
    day_action?: string;
    description?: string;
}

interface BackendStrength {
    wang_shuai?: string;
    score?: number;
    factors?: string[];
    is_strong?: boolean;
    special_status?: string;
}

interface BackendChangeAnalysis {
    hua_type: string;
    original_zhi: string;
    changed_zhi: string;
    description: string;
}

interface BackendChangSheng {
    stage: string;
    strength: string;
    description: string;
}

interface BackendExtendedYao {
    index: number;
    branch: string;
    element: string;
    liu_qin: string;
    is_moving: boolean;
    kong_wang_state: string;
    influence?: BackendInfluence;
    strength?: BackendStrength;
    change_analysis?: BackendChangeAnalysis;
    chang_sheng?: BackendChangSheng;
}

interface BackendShenInfo {
    liu_qin: string;
    wu_xing: string;
    positions: number[];
}

interface BackendShenSystem {
    yuan_shen?: BackendShenInfo;
    ji_shen?: BackendShenInfo;
    chou_shen?: BackendShenInfo;
}

interface BackendTimeRecommendation {
    type: string;
    timeframe: string;
    earthly_branch: string;
    description: string;
}

interface BackendAnalysisResult {
    kong_wang?: BackendKongWang;
    extended_yaos?: BackendExtendedYao[];
    san_he_analysis?: {
        has_full_san_he: boolean;
        full_san_he?: unknown;
        has_ban_he: boolean;
        ban_he?: unknown[];
    };
    liu_chong_gua?: {
        is_liu_chong_gua: boolean;
        description?: string;
    };
    shen_system?: BackendShenSystem;
    time_recommendations?: BackendTimeRecommendation[];
}

/**
 * 根据公历日期计算干支
 * 简化算法，实际应用中建议使用更精确的农历库
 */
function calculateGanZhi(date: Date): { monthZhi: string; dayGan: string; dayZhi: string } {
    // 基准日期：1900年1月1日 甲戌日
    const baseDate = new Date(1900, 0, 1);
    const diffDays = Math.floor((date.getTime() - baseDate.getTime()) / (1000 * 60 * 60 * 24));

    // 日干支
    const dayGanIndex = (diffDays + 10) % 10; // 甲=0
    const dayZhiIndex = (diffDays + 10) % 12; // 戌=10 -> 调整为子=0

    // 月支（简化：按公历月份近似）
    // 实际应该使用节气判断
    const month = date.getMonth(); // 0-11
    // 寅月为正月，对应公历约2月
    const monthZhiIndex = (month + 2) % 12;

    return {
        monthZhi: DI_ZHI[monthZhiIndex],
        dayGan: TIAN_GAN[dayGanIndex],
        dayZhi: DI_ZHI[dayZhiIndex]
    };
}

// 转换后端snake_case为前端camelCase
const transformAnalysisResult = (data: BackendAnalysisResult): AdvancedAnalysisResult => {
    return {
        kongWang: {
            xun: data.kong_wang?.xun || '',
            kongDizhi: data.kong_wang?.kong_dizhi || ['', '']
        },
        extendedYaos: (data.extended_yaos || []).map((yao): ExtendedYaoInfo => ({
            index: yao.index,
            branch: yao.branch,
            element: yao.element,
            liuQin: yao.liu_qin,
            isMoving: yao.is_moving,
            kongWangState: yao.kong_wang_state as KongWangState,
            influence: {
                monthAction: (yao.influence?.month_action || '无') as YaoAction,
                dayAction: (yao.influence?.day_action || '无') as YaoAction,
                description: yao.influence?.description || ''
            },
            strength: {
                wangShuai: (yao.strength?.wang_shuai || '休') as WangShuai,
                score: yao.strength?.score ?? 0,
                factors: yao.strength?.factors || [],
                isStrong: yao.strength?.is_strong ?? false,
                specialStatus: (yao.strength?.special_status || '无') as SpecialStatus
            },
            changeAnalysis: yao.change_analysis ? {
                huaType: yao.change_analysis.hua_type as HuaType,
                originalZhi: yao.change_analysis.original_zhi,
                changedZhi: yao.change_analysis.changed_zhi,
                description: yao.change_analysis.description
            } : undefined,
            changSheng: yao.chang_sheng ? {
                stage: yao.chang_sheng.stage as ChangShengStage,
                strength: yao.chang_sheng.strength,
                description: yao.chang_sheng.description
            } : undefined
        })),
        sanHeAnalysis: {
            hasFullSanHe: data.san_he_analysis?.has_full_san_he || false,
            fullSanHe: data.san_he_analysis?.full_san_he as { name: string; result: string; positions: number[] } | undefined,
            hasBanHe: data.san_he_analysis?.has_ban_he || false,
            banHe: (data.san_he_analysis?.ban_he || []) as Array<{ branches: [string, string]; result: string; type: 'sheng' | 'mu'; positions: number[] }>
        },
        liuChongGua: {
            isLiuChongGua: data.liu_chong_gua?.is_liu_chong_gua || false,
            description: data.liu_chong_gua?.description
        },
        shenSystem: data.shen_system ? {
            yuanShen: data.shen_system.yuan_shen ? {
                liuQin: data.shen_system.yuan_shen.liu_qin,
                wuXing: data.shen_system.yuan_shen.wu_xing,
                positions: data.shen_system.yuan_shen.positions
            } : undefined,
            jiShen: data.shen_system.ji_shen ? {
                liuQin: data.shen_system.ji_shen.liu_qin,
                wuXing: data.shen_system.ji_shen.wu_xing,
                positions: data.shen_system.ji_shen.positions
            } : undefined,
            chouShen: data.shen_system.chou_shen ? {
                liuQin: data.shen_system.chou_shen.liu_qin,
                wuXing: data.shen_system.chou_shen.wu_xing,
                positions: data.shen_system.chou_shen.positions
            } : undefined
        } : undefined,
        timeRecommendations: (data.time_recommendations || []).map((rec): TimeRecommendation => ({
            type: rec.type as 'favorable' | 'unfavorable' | 'critical',
            timeframe: rec.timeframe,
            earthlyBranch: rec.earthly_branch,
            description: rec.description
        }))
    };
};

interface UseAdvancedAnalysisReturn {
    analysis: AdvancedAnalysisResult | null;
    loading: boolean;
    error: string | null;
    analyze: (
        hexagram: HexagramInfo,
        options?: {
            monthZhi?: string;
            dayGan?: string;
            dayZhi?: string;
            yongShenElement?: string;
        }
    ) => Promise<void>;
    reset: () => void;
}

export const useAdvancedAnalysis = (): UseAdvancedAnalysisReturn => {
    const [analysis, setAnalysis] = useState<AdvancedAnalysisResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const reset = useCallback(() => {
        setAnalysis(null);
        setError(null);
    }, []);

    const analyze = useCallback(async (
        hexagram: HexagramInfo,
        options?: {
            monthZhi?: string;
            dayGan?: string;
            dayZhi?: string;
            yongShenElement?: string;
        }
    ) => {
        setLoading(true);
        setError(null);

        try {
            // 如果没有提供干支，自动计算当前日期的干支
            let monthZhi = options?.monthZhi;
            let dayGan = options?.dayGan;
            let dayZhi = options?.dayZhi;

            if (!monthZhi || !dayGan || !dayZhi) {
                const ganZhi = calculateGanZhi(new Date());
                monthZhi = monthZhi || ganZhi.monthZhi;
                dayGan = dayGan || ganZhi.dayGan;
                dayZhi = dayZhi || ganZhi.dayZhi;
            }

            // 构建请求体
            const hexagramData = {
                name: hexagram.name,
                palace_name: hexagram.palaceName,
                palace_element: hexagram.palaceElement,
                transformed_name: hexagram.transformedName,
                lines: hexagram.lines.map(line => ({
                    index: line.index,
                    type: line.type,
                    branch: line.branch,
                    element: line.element,
                    six_relation: line.sixRelation,
                    is_moving: line.isMoving,
                    changed_branch: line.changedBranch
                }))
            };

            const response = await fetch(`${API_BASE}/advanced-analysis`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    hexagram_data: hexagramData,
                    month_zhi: monthZhi,
                    day_gan: dayGan,
                    day_zhi: dayZhi,
                    yong_shen_element: options?.yongShenElement
                })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || '高级分析失败');
            }

            const data = await response.json();
            setAnalysis(transformAnalysisResult(data.analysis));
        } catch (e) {
            setError(e instanceof Error ? e.message : '未知错误');
        } finally {
            setLoading(false);
        }
    }, []);

    return {
        analysis,
        loading,
        error,
        analyze,
        reset
    };
};

export default useAdvancedAnalysis;
