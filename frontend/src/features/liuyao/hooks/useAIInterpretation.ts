/**
 * AI解卦Hook - 支持流式输出
 */

import { useState, useCallback, useRef } from 'react';
import { HexagramInfo, AIStyle } from '../types';
import { useGlobalState } from '@/store';

const API_BASE = '/api/liuyao';

interface UseAIInterpretationReturn {
    interpretation: string | null;
    provider: string | null;
    loading: boolean;
    streaming: boolean;
    error: string | null;
    interpret: (hexagram: HexagramInfo, question?: string, style?: AIStyle) => Promise<void>;
    reset: () => void;
}

export const useAIInterpretation = (): UseAIInterpretationReturn => {
    const { customOpenAISettings } = useGlobalState();
    const [interpretation, setInterpretation] = useState<string | null>(null);
    const [provider, setProvider] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [streaming, setStreaming] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const abortControllerRef = useRef<AbortController | null>(null);

    const reset = useCallback(() => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }
        setInterpretation(null);
        setProvider(null);
        setError(null);
        setStreaming(false);
    }, []);

    const interpret = useCallback(async (
        hexagram: HexagramInfo,
        question?: string,
        style: AIStyle = 'detailed'
    ) => {
        // 取消之前的请求
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }
        abortControllerRef.current = new AbortController();

        setLoading(true);
        setStreaming(true);
        setError(null);
        setInterpretation('');

        try {
            // 构建卦象数据
            const hexagramData = {
                name: hexagram.name,
                palace_name: hexagram.palaceName,
                palace_element: hexagram.palaceElement,
                transformed_name: hexagram.transformedName,
                lines: hexagram.lines.map(line => ({
                    index: line.index,
                    type: line.type,
                    type_name: line.typeName,
                    is_moving: line.isMoving,
                    stem: line.stem,
                    branch: line.branch,
                    element: line.element,
                    six_relation: line.sixRelation,
                    six_beast: line.sixBeast,
                    is_shi: line.isShi,
                    is_ying: line.isYing,
                    fu_shen: line.fuShen ? {
                        stem: line.fuShen.stem,
                        branch: line.fuShen.branch,
                        relation: line.fuShen.relation,
                        element: line.fuShen.element
                    } : null,
                    changed_type: line.changedType,
                    changed_branch: line.changedBranch,
                    changed_stem: line.changedStem,
                    changed_relation: line.changedRelation
                }))
            };

            // 构建headers
            const headers: Record<string, string> = {
                'Content-Type': 'application/json'
            };

            if (customOpenAISettings.enable) {
                headers['x-api-key'] = customOpenAISettings.apiKey;
                headers['x-api-url'] = customOpenAISettings.baseUrl;
                headers['x-api-model'] = customOpenAISettings.model;
            }

            // 使用流式端点
            const response = await fetch(`${API_BASE}/interpret/stream`, {
                method: 'POST',
                headers,
                body: JSON.stringify({
                    hexagram_data: hexagramData,
                    question: question || '',
                    style
                }),
                signal: abortControllerRef.current.signal
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'AI解卦失败');
            }

            // 处理流式响应
            const reader = response.body?.getReader();
            if (!reader) {
                throw new Error('无法读取响应流');
            }

            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            if (typeof data === 'string') {
                                setInterpretation(prev => (prev || '') + data);
                            } else if (data.error) {
                                throw new Error(data.error);
                            }
                        } catch {
                            // 忽略解析错误
                        }
                    }
                }
            }

            setProvider('AI故障转移系统');
        } catch (e) {
            if (e instanceof Error && e.name === 'AbortError') {
                return; // 请求被取消，不设置错误
            }
            setError(e instanceof Error ? e.message : '未知错误');
        } finally {
            setLoading(false);
            setStreaming(false);
        }
    }, [customOpenAISettings]);

    return {
        interpretation,
        provider,
        loading,
        streaming,
        error,
        interpret,
        reset
    };
};

export default useAIInterpretation;
