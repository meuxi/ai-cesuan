/**
 * 流年详批表格组件
 * 以表格形式展示逐年运势详批
 */

import React, { useMemo, useState } from 'react';
import { KLinePoint } from './types';

interface YearlyDetailTableProps {
    data: KLinePoint[];
}

const YearlyDetailTable: React.FC<YearlyDetailTableProps> = ({ data }) => {
    const [sortBy, setSortBy] = useState<'age' | 'score'>('age');
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
    const [filterDaYun, setFilterDaYun] = useState<string>('all');

    // 获取所有大运
    const allDaYun = useMemo(() => {
        const dayunSet = new Set(data.map(d => d.daYun));
        return Array.from(dayunSet);
    }, [data]);

    // 找出巅峰年份
    const peakYear = useMemo(() => {
        if (!data.length) return null;
        const validData = data.filter(point => point && typeof point.score === 'number');
        if (!validData.length) return null;
        return validData.reduce((max, curr) => curr.score > max.score ? curr : max, validData[0]);
    }, [data]);

    // 找出低谷年份
    const valleyYear = useMemo(() => {
        if (!data.length) return null;
        const validData = data.filter(point => point && typeof point.score === 'number');
        if (!validData.length) return null;
        return validData.reduce((min, curr) => curr.score < min.score ? curr : min, validData[0]);
    }, [data]);

    // 排序和过滤后的数据
    const sortedData = useMemo(() => {
        let filtered = filterDaYun === 'all'
            ? [...data]
            : data.filter(d => d.daYun === filterDaYun);

        return filtered.sort((a, b) => {
            const aVal = sortBy === 'age' ? a.age : (a.score || 0);
            const bVal = sortBy === 'age' ? b.age : (b.score || 0);
            return sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
        });
    }, [data, sortBy, sortOrder, filterDaYun]);

    // 评分对应的颜色
    const getScoreColor = (score: number) => {
        if (score >= 80) return 'text-green-600 bg-green-50';
        if (score >= 60) return 'text-blue-600 bg-blue-50';
        if (score >= 40) return 'text-yellow-600 bg-yellow-50';
        return 'text-red-600 bg-red-50';
    };

    // 评分等级
    const getScoreLevel = (score: number) => {
        if (score >= 90) return '大吉';
        if (score >= 75) return '中吉';
        if (score >= 60) return '小吉';
        if (score >= 40) return '平';
        if (score >= 25) return '小凶';
        return '凶';
    };

    const handleSort = (field: 'age' | 'score') => {
        if (sortBy === field) {
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
        } else {
            setSortBy(field);
            setSortOrder('asc');
        }
    };

    return (
        <div className="bg-card rounded-xl shadow-lg overflow-hidden">
            {/* 表头和控制栏 */}
            <div className="p-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white">
                <h3 className="text-lg font-bold mb-3">📋 流年详批表格</h3>
                <div className="flex flex-wrap gap-4 items-center text-sm">
                    {/* 大运筛选 */}
                    <div className="flex items-center gap-2">
                        <span>大运筛选:</span>
                        <select
                            value={filterDaYun}
                            onChange={(e) => setFilterDaYun(e.target.value)}
                            className="bg-white/20 rounded px-2 py-1 text-white border border-white/30"
                        >
                            <option value="all" className="text-foreground">全部</option>
                            {allDaYun.map(dy => (
                                <option key={dy} value={dy} className="text-foreground">{dy}</option>
                            ))}
                        </select>
                    </div>

                    {/* 统计信息 */}
                    {peakYear && (
                        <div className="flex items-center gap-4">
                            <span className="bg-green-400/30 px-2 py-1 rounded">
                                🏔️ 巅峰: {peakYear.year}年({peakYear.age}岁) {peakYear.score}分
                            </span>
                            {valleyYear && (
                                <span className="bg-red-400/30 px-2 py-1 rounded">
                                    🌊 低谷: {valleyYear.year}年({valleyYear.age}岁) {valleyYear.score}分
                                </span>
                            )}
                        </div>
                    )}
                </div>
            </div>

            {/* 表格 */}
            <div className="overflow-x-auto max-h-[600px] overflow-y-auto">
                <table className="w-full text-sm">
                    <thead className="bg-secondary sticky top-0">
                        <tr>
                            <th
                                className="px-4 py-3 text-left cursor-pointer hover:bg-accent"
                                onClick={() => handleSort('age')}
                            >
                                年龄 {sortBy === 'age' && (sortOrder === 'asc' ? '↑' : '↓')}
                            </th>
                            <th className="px-4 py-3 text-left">年份</th>
                            <th className="px-4 py-3 text-left">流年干支</th>
                            <th className="px-4 py-3 text-left">大运</th>
                            <th
                                className="px-4 py-3 text-left cursor-pointer hover:bg-accent"
                                onClick={() => handleSort('score')}
                            >
                                评分 {sortBy === 'score' && (sortOrder === 'asc' ? '↑' : '↓')}
                            </th>
                            <th className="px-4 py-3 text-left">等级</th>
                            <th className="px-4 py-3 text-left">K线区间</th>
                            <th className="px-4 py-3 text-left min-w-[300px]">流年详批</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sortedData.map((point, idx) => {
                            const isPeak = peakYear && point.age === peakYear.age;
                            const isValley = valleyYear && point.age === valleyYear.age;

                            return (
                                <tr
                                    key={point.age}
                                    className={`
                                        border-b hover:bg-accent transition-colors
                                        ${isPeak ? 'bg-green-50 border-l-4 border-l-green-500' : ''}
                                        ${isValley ? 'bg-red-50 border-l-4 border-l-red-500' : ''}
                                        ${idx % 2 === 0 && !isPeak && !isValley ? 'bg-card' : ''}
                                    `}
                                >
                                    <td className="px-4 py-3 font-medium">
                                        {point.age}岁
                                        {isPeak && <span className="ml-1 text-green-600">🏔️</span>}
                                        {isValley && <span className="ml-1 text-red-600">🌊</span>}
                                    </td>
                                    <td className="px-4 py-3">{point.year}年</td>
                                    <td className="px-4 py-3 font-medium text-indigo-600">{point.ganZhi}</td>
                                    <td className="px-4 py-3 text-purple-600">{point.daYun}</td>
                                    <td className="px-4 py-3">
                                        <span className={`px-2 py-1 rounded font-bold ${getScoreColor(point.score || 0)}`}>
                                            {point.score || 0}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3">
                                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${getScoreColor(point.score || 0)}`}>
                                            {getScoreLevel(point.score || 0)}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3 text-muted-foreground text-xs">
                                        L:{point.low} O:{point.open} C:{point.close} H:{point.high}
                                    </td>
                                    <td className="px-4 py-3 text-foreground">{point.reason}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>

            {/* 底部统计 */}
            <div className="p-4 bg-secondary border-t text-sm text-muted-foreground flex justify-between items-center">
                <span>共 {sortedData.length} 条记录</span>
                <span>
                    平均分: {(sortedData.reduce((sum, d) => sum + (d.score || 0), 0) / sortedData.length).toFixed(1)}
                </span>
            </div>
        </div>
    );
};

export default YearlyDetailTable;
