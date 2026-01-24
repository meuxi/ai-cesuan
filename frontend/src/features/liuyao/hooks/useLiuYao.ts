/**
 * 六爻起卦Hook
 */

import { useState, useCallback } from 'react';
import { HexagramInfo, LineDetails, FuShenInfo, CoinCastResult, LineType } from '../types';

const API_BASE = '/api/liuyao';

// 后端响应类型定义（snake_case）
interface BackendFuShen {
    stem: string;
    branch: string;
    relation: string;
    element: string;
}

interface BackendLine {
    index: number;
    type: string;
    type_name: string;
    is_moving: boolean;
    stem: string;
    branch: string;
    element: string;
    six_relation: string;
    six_beast: string;
    is_shi: boolean;
    is_ying: boolean;
    fu_shen?: BackendFuShen;
    changed_type?: string;
    changed_branch?: string;
    changed_stem?: string;
    changed_relation?: string;
}

interface BackendHexagram {
    name: string;
    palace_name: string;
    palace_element: string;
    transformed_name?: string;
    lines: BackendLine[];
}

// 将后端snake_case转换为前端camelCase
const transformHexagram = (data: BackendHexagram): HexagramInfo => {
    return {
        name: data.name,
        palaceName: data.palace_name,
        palaceElement: data.palace_element,
        transformedName: data.transformed_name,
        lines: data.lines.map((line): LineDetails => ({
            index: line.index,
            type: Number(line.type) as LineType,
            typeName: line.type_name,
            isMoving: line.is_moving,
            stem: line.stem,
            branch: line.branch,
            element: line.element,
            sixRelation: line.six_relation,
            sixBeast: line.six_beast,
            isShi: line.is_shi,
            isYing: line.is_ying,
            fuShen: line.fu_shen ? {
                stem: line.fu_shen.stem,
                branch: line.fu_shen.branch,
                relation: line.fu_shen.relation,
                element: line.fu_shen.element
            } as FuShenInfo : undefined,
            changedType: line.changed_type !== undefined ? Number(line.changed_type) as LineType : undefined,
            changedBranch: line.changed_branch,
            changedStem: line.changed_stem,
            changedRelation: line.changed_relation
        }))
    };
};

interface UseLiuYaoReturn {
    hexagram: HexagramInfo | null;
    castResults: CoinCastResult[] | null;
    loading: boolean;
    error: string | null;
    coinCast: (question?: string) => Promise<void>;
    numberCast: (upper: number, lower: number, moving: number, question?: string) => Promise<void>;
    timeCast: (question?: string) => Promise<void>;
    manualCast: (lines: number[], question?: string) => Promise<void>;
    reset: () => void;
}

export const useLiuYao = (): UseLiuYaoReturn => {
    const [hexagram, setHexagram] = useState<HexagramInfo | null>(null);
    const [castResults, setCastResults] = useState<CoinCastResult[] | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const reset = useCallback(() => {
        setHexagram(null);
        setCastResults(null);
        setError(null);
    }, []);

    // 摇钱卦
    const coinCast = useCallback(async (question?: string) => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE}/coin`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question || '' })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || '摇钱卦失败');
            }

            const data = await response.json();
            setHexagram(transformHexagram(data.hexagram));
            setCastResults(data.cast_results || null);
        } catch (e) {
            setError(e instanceof Error ? e.message : '未知错误');
        } finally {
            setLoading(false);
        }
    }, []);

    // 数理卦
    const numberCast = useCallback(async (upper: number, lower: number, moving: number, question?: string) => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE}/number`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    upper_num: upper,
                    lower_num: lower,
                    moving_num: moving,
                    question: question || ''
                })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || '数理卦失败');
            }

            const data = await response.json();
            setHexagram(transformHexagram(data.hexagram));
            setCastResults(null);
        } catch (e) {
            setError(e instanceof Error ? e.message : '未知错误');
        } finally {
            setLoading(false);
        }
    }, []);

    // 时空卦
    const timeCast = useCallback(async (question?: string) => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE}/time`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question || '' })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || '时空卦失败');
            }

            const data = await response.json();
            setHexagram(transformHexagram(data.hexagram));
            setCastResults(null);
        } catch (e) {
            setError(e instanceof Error ? e.message : '未知错误');
        } finally {
            setLoading(false);
        }
    }, []);

    // 手动输入
    const manualCast = useCallback(async (lines: number[], question?: string) => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE}/manual`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lines, question: question || '' })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || '手动输入失败');
            }

            const data = await response.json();
            setHexagram(transformHexagram(data.hexagram));
            setCastResults(null);
        } catch (e) {
            setError(e instanceof Error ? e.message : '未知错误');
        } finally {
            setLoading(false);
        }
    }, []);

    return {
        hexagram,
        castResults,
        loading,
        error,
        coinCast,
        numberCast,
        timeCast,
        manualCast,
        reset
    };
};

export default useLiuYao;
