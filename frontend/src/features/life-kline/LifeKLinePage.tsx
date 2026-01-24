/**
 * 人生K线图页面
 */

import React, { useState, useMemo } from 'react';
import BaziInputForm from './BaziInputForm';
import LifeKLineChart from './LifeKLineChart';
import AnalysisResult from './AnalysisResult';
import YearlyDetailTable from './YearlyDetailTable';
import ImportDataMode from './ImportDataMode';
import { LifeKLineInput, LifeKLineResult } from './types';
import { exportToJson, exportLifeKLineHtmlReport, printPage } from '../../utils/exportUtils';
import { Upload } from 'lucide-react';

type ViewMode = 'chart' | 'table';
type InputMode = 'api' | 'manual';

const API_BASE = import.meta.env.VITE_API_BASE || '';

const LifeKLinePage: React.FC = () => {
    const [result, setResult] = useState<LifeKLineResult | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [viewMode, setViewMode] = useState<ViewMode>('chart');
    const [inputMode, setInputMode] = useState<InputMode>('api');

    // 手动导入数据处理
    const handleDataImport = (data: LifeKLineResult) => {
        setResult(data);
        setError(null);
    };

    // 重新排盘
    const handleReset = () => {
        setResult(null);
        setError(null);
    };

    // JSON文件导入
    const handleJsonFileImport = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const content = e.target?.result as string;
                let jsonContent = content.trim();

                // 提取 JSON
                const jsonMatch = jsonContent.match(/```(?:json)?\s*([\s\S]*?)```/);
                if (jsonMatch) {
                    jsonContent = jsonMatch[1].trim();
                } else {
                    const startIdx = jsonContent.indexOf('{');
                    const endIdx = jsonContent.lastIndexOf('}');
                    if (startIdx !== -1 && endIdx !== -1) {
                        jsonContent = jsonContent.substring(startIdx, endIdx + 1);
                    }
                }

                const data = JSON.parse(jsonContent);

                if (!data.chartPoints && !data.chartData) {
                    throw new Error('无效的数据格式：缺少 chartPoints 或 chartData');
                }

                const importedResult: LifeKLineResult = {
                    chartData: data.chartPoints || data.chartData,
                    analysis: {
                        bazi: data.bazi || data.analysis?.bazi || [],
                        summary: data.summary || data.analysis?.summary || '',
                        summaryScore: data.summaryScore || data.analysis?.summaryScore || 5,
                        personality: data.personality || data.analysis?.personality || '',
                        personalityScore: data.personalityScore || data.analysis?.personalityScore || 5,
                        industry: data.industry || data.analysis?.industry || '',
                        industryScore: data.industryScore || data.analysis?.industryScore || 5,
                        fengShui: data.fengShui || data.analysis?.fengShui || '',
                        fengShuiScore: data.fengShuiScore || data.analysis?.fengShuiScore || 5,
                        wealth: data.wealth || data.analysis?.wealth || '',
                        wealthScore: data.wealthScore || data.analysis?.wealthScore || 5,
                        marriage: data.marriage || data.analysis?.marriage || '',
                        marriageScore: data.marriageScore || data.analysis?.marriageScore || 5,
                        health: data.health || data.analysis?.health || '',
                        healthScore: data.healthScore || data.analysis?.healthScore || 5,
                        family: data.family || data.analysis?.family || '',
                        familyScore: data.familyScore || data.analysis?.familyScore || 5,
                    },
                };

                setResult(importedResult);
                setError(null);
            } catch (err: unknown) {
                const message = err instanceof Error ? err.message : '未知错误'
                setError(`文件解析失败：${message}`);
            }
        };
        reader.readAsText(file);
        event.target.value = '';
    };

    // 计算巅峰和低谷年份
    const peakYear = useMemo(() => {
        if (!result?.chartData?.length) return null;
        const validData = result.chartData.filter(point => point && typeof point.score === 'number');
        if (!validData.length) return null;
        return validData.reduce((max, curr) => curr.score > max.score ? curr : max, validData[0]);
    }, [result]);

    const valleyYear = useMemo(() => {
        if (!result?.chartData?.length) return null;
        const validData = result.chartData.filter(point => point && typeof point.score === 'number');
        if (!validData.length) return null;
        return validData.reduce((min, curr) => curr.score < min.score ? curr : min, validData[0]);
    }, [result]);

    // 导出处理
    const handleExportJson = () => {
        if (!result) return;
        exportToJson(result, `人生K线_${new Date().toISOString().slice(0, 10)}`);
    };

    const handleExportHtml = () => {
        if (!result) return;
        exportLifeKLineHtmlReport({
            chartData: result.chartData,
            analysis: result.analysis as Record<string, unknown> | undefined,
        });
    };

    const handleSubmit = async (data: LifeKLineInput) => {
        setIsLoading(true);
        setError(null);

        try {
            // 总是使用AI接口，后端会根据配置自动选择AI或回退算法
            const endpoint = `${API_BASE}/api/life-kline/generate`;

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: data.name,
                    gender: data.gender,
                    birth_year: data.birthYear,
                    year_pillar: data.yearPillar,
                    month_pillar: data.monthPillar,
                    day_pillar: data.dayPillar,
                    hour_pillar: data.hourPillar,
                    start_age: data.startAge,
                    first_dayun: data.firstDaYun,
                    is_forward: data.isForward,
                    use_ai: data.useAi,
                    api_key: data.apiKey,
                    api_base_url: data.apiBaseUrl,
                    model_name: data.modelName,
                }),
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.detail || '请求失败');
            }

            const resultData = await response.json();
            setResult(resultData);
        } catch (err) {
            setError(err instanceof Error ? err.message : '生成失败，请重试');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background py-8 px-4">
            <div className="max-w-7xl mx-auto">
                {/* 标题 */}
                <div className="text-center mb-8">
                    <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
                        人生K线图
                    </h1>
                    <p className="text-muted-foreground">
                        基于八字命理，生成1-100岁的人生运势可视化图表
                    </p>
                </div>

                {/* JSON文件快速导入 */}
                {!result && (
                    <div className="flex justify-center mb-4">
                        <label className="flex items-center gap-3 px-6 py-3 bg-card border-2 border-dashed border-primary/30 rounded-xl cursor-pointer hover:border-primary hover:bg-accent transition-all group">
                            <Upload className="w-5 h-5 text-primary group-hover:text-primary" />
                            <span className="text-sm font-medium text-muted-foreground group-hover:text-foreground">已有 JSON 文件？点击直接导入</span>
                            <input
                                type="file"
                                accept=".json"
                                onChange={handleJsonFileImport}
                                className="hidden"
                            />
                        </label>
                    </div>
                )}

                {/* 输入模式切换 */}
                {!result && (
                    <div className="flex justify-center mb-6">
                        <div className="inline-flex rounded-lg border border-border bg-card p-1 shadow-sm">
                            <button
                                onClick={() => setInputMode('api')}
                                className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${inputMode === 'api'
                                    ? 'bg-primary text-primary-foreground shadow'
                                    : 'text-muted-foreground hover:bg-accent'
                                    }`}
                            >
                                🚀 API模式
                            </button>
                            <button
                                onClick={() => setInputMode('manual')}
                                className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${inputMode === 'manual'
                                    ? 'bg-primary text-primary-foreground shadow'
                                    : 'text-muted-foreground hover:bg-accent'
                                    }`}
                            >
                                ✍️ 手动导入
                            </button>
                        </div>
                    </div>
                )}

                {/* 输入表单 */}
                {!result && (
                    <div className="mb-8 flex justify-center">
                        {inputMode === 'api' ? (
                            <BaziInputForm onSubmit={handleSubmit} isLoading={isLoading} />
                        ) : (
                            <ImportDataMode onDataImport={handleDataImport} />
                        )}
                    </div>
                )}

                {/* 错误提示 */}
                {error && (
                    <div className="mb-8 bg-destructive/10 border border-destructive/20 rounded-lg p-4 text-destructive">
                        <div className="flex items-center gap-2">
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                            <span>{error}</span>
                        </div>
                    </div>
                )}

                {/* 结果展示 */}
                {result && (
                    <div className="space-y-8">
                        {/* 巅峰/低谷年份显示 */}
                        {peakYear && valleyYear && (
                            <div className="flex flex-wrap justify-center gap-4">
                                <div className="flex items-center gap-2 px-4 py-2 bg-chart-2/10 border border-chart-2/30 rounded-lg">
                                    <span className="text-lg">🏔️</span>
                                    <span className="text-chart-2 font-bold">
                                        人生巅峰：{peakYear.year}年({peakYear.age}岁) {peakYear.score}分
                                    </span>
                                </div>
                                <div className="flex items-center gap-2 px-4 py-2 bg-destructive/10 border border-destructive/30 rounded-lg">
                                    <span className="text-lg">🌊</span>
                                    <span className="text-destructive font-bold">
                                        人生低谷：{valleyYear.year}年({valleyYear.age}岁) {valleyYear.score}分
                                    </span>
                                </div>
                            </div>
                        )}

                        {/* 视图切换和导出按钮 */}
                        <div className="flex flex-wrap justify-center gap-2">
                            <button
                                onClick={() => setViewMode('chart')}
                                className={`px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${viewMode === 'chart'
                                    ? 'bg-primary text-primary-foreground shadow-lg'
                                    : 'bg-card text-muted-foreground hover:bg-accent border'
                                    }`}
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                                </svg>
                                K线图
                            </button>
                            <button
                                onClick={() => setViewMode('table')}
                                className={`px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${viewMode === 'table'
                                    ? 'bg-primary text-primary-foreground shadow-lg'
                                    : 'bg-card text-muted-foreground hover:bg-accent border'
                                    }`}
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                </svg>
                                详批表格
                            </button>

                            {/* 重新排盘按钮 */}
                            <button
                                onClick={handleReset}
                                className="px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 bg-secondary text-secondary-foreground hover:bg-secondary/80"
                            >
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                </svg>
                                重新排盘
                            </button>

                            {/* 分隔线 */}
                            <div className="w-px h-8 bg-border mx-2" />

                            {/* 导出按钮组 */}
                            <button
                                onClick={handleExportJson}
                                className="px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 bg-chart-2 text-white hover:bg-chart-2/90"
                            >
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                </svg>
                                JSON
                            </button>
                            <button
                                onClick={handleExportHtml}
                                className="px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 bg-primary text-primary-foreground hover:bg-primary/90"
                            >
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                报告
                            </button>
                            <button
                                onClick={printPage}
                                className="px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 bg-card text-muted-foreground hover:bg-accent border"
                            >
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                                </svg>
                                打印
                            </button>
                        </div>

                        {/* 根据视图模式显示内容 */}
                        {viewMode === 'chart' ? (
                            <LifeKLineChart data={result.chartData} />
                        ) : (
                            <YearlyDetailTable data={result.chartData} />
                        )}

                        {/* 分析结果 */}
                        <AnalysisResult analysis={result.analysis} />
                    </div>
                )}

                {/* 空状态 */}
                {!result && !isLoading && !error && (
                    <div className="text-center py-16 text-muted-foreground">
                        <div className="text-6xl mb-4">📈</div>
                        <p>填写八字信息，生成你的人生K线图</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default LifeKLinePage;
