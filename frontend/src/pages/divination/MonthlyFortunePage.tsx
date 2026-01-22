/**
 * 每月运势页面
 * 移植自 MingAI-master/src/app/monthly/page.tsx
 */

import { useState, useEffect } from 'react';
import {
    Calendar,
    ChevronLeft,
    ChevronRight,
    Briefcase,
    Heart,
    Wallet,
    Activity,
    Star,
    User,
    Sparkles,
    RefreshCw,
    AlertCircle,
    TrendingUp,
    Zap
} from 'lucide-react';

const API_BASE = '/api/fortune';

interface KeyDate {
    date: number;
    desc: string;
    type: 'lucky' | 'warning' | 'turning';
}

interface MonthlyFortune {
    year: number;
    month: number;
    month_stem: string;
    month_branch: string;
    ten_god: string;
    scores: {
        overall: number;
        career: number;
        love: number;
        wealth: number;
        health: number;
        social: number;
    };
    summary: string;
    key_dates: KeyDate[];
}

const scoreItems = [
    { key: 'overall', label: '综合运势', icon: Star, color: 'text-amber-500' },
    { key: 'career', label: '事业运', icon: Briefcase, color: 'text-blue-500' },
    { key: 'love', label: '感情运', icon: Heart, color: 'text-pink-500' },
    { key: 'wealth', label: '财运', icon: Wallet, color: 'text-green-500' },
    { key: 'health', label: '健康运', icon: Activity, color: 'text-red-500' },
    { key: 'social', label: '人际运', icon: User, color: 'text-purple-500' },
];

const dayMasterOptions = [
    { value: '甲', label: '甲木' },
    { value: '乙', label: '乙木' },
    { value: '丙', label: '丙火' },
    { value: '丁', label: '丁火' },
    { value: '戊', label: '戊土' },
    { value: '己', label: '己土' },
    { value: '庚', label: '庚金' },
    { value: '辛', label: '辛金' },
    { value: '壬', label: '壬水' },
    { value: '癸', label: '癸水' },
];

const keyDateIcons: Record<string, any> = {
    lucky: Star,
    warning: AlertCircle,
    turning: TrendingUp,
};

const keyDateColors: Record<string, string> = {
    lucky: 'bg-chart-2/20 text-chart-2',
    warning: 'bg-destructive/20 text-destructive',
    turning: 'bg-primary/20 text-primary',
};

export default function MonthlyFortunePage() {
    const [year, setYear] = useState(new Date().getFullYear());
    const [month, setMonth] = useState(new Date().getMonth() + 1);
    const [dayMaster, setDayMaster] = useState('甲');
    const [fortune, setFortune] = useState<MonthlyFortune | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const changeMonth = (delta: number) => {
        let newMonth = month + delta;
        let newYear = year;

        if (newMonth > 12) {
            newMonth = 1;
            newYear += 1;
        } else if (newMonth < 1) {
            newMonth = 12;
            newYear -= 1;
        }

        setMonth(newMonth);
        setYear(newYear);
    };

    const goToCurrentMonth = () => {
        const now = new Date();
        setYear(now.getFullYear());
        setMonth(now.getMonth() + 1);
    };

    const isCurrentMonth = year === new Date().getFullYear() && month === new Date().getMonth() + 1;

    const fetchFortune = async () => {
        setLoading(true);
        setError(null);
        try {
            const params = new URLSearchParams({
                day_master: dayMaster,
                year: year.toString(),
                month: month.toString(),
            });

            const response = await fetch(`${API_BASE}/monthly?${params.toString()}`);
            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || '获取运势失败');
            }

            const data = await response.json();
            setFortune(data);
        } catch (e) {
            setError(e instanceof Error ? e.message : '未知错误');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFortune();
    }, [year, month, dayMaster]);

    const getScoreColor = (score: number) => {
        if (score >= 80) return 'bg-green-500';
        if (score >= 60) return 'bg-amber-500';
        return 'bg-red-500';
    };

    return (
        <div className="space-y-6">
            <div className="max-w-2xl mx-auto">
                {/* 标题 */}
                <div className="text-center mb-8">
                    <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
                        每月运势
                    </h1>
                    <p className="text-muted-foreground">
                        基于八字命理的月度运势预测
                    </p>
                </div>

                {/* 月份选择器 */}
                <div className="flex items-center justify-between mb-6 p-4 bg-card rounded-lg border border-border">
                    <button
                        onClick={() => changeMonth(-1)}
                        className="p-2 rounded-md hover:bg-secondary transition-colors"
                    >
                        <ChevronLeft className="w-5 h-5 text-muted-foreground" />
                    </button>

                    <div className="text-center">
                        <div className="flex items-center justify-center gap-2 mb-1">
                            <Calendar className="w-5 h-5 text-muted-foreground" />
                            <span className="font-semibold text-foreground">{year}年{month}月</span>
                        </div>
                        {isCurrentMonth ? (
                            <span className="text-sm text-muted-foreground">本月运势</span>
                        ) : (
                            <button
                                onClick={goToCurrentMonth}
                                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                            >
                                回到本月
                            </button>
                        )}
                    </div>

                    <button
                        onClick={() => changeMonth(1)}
                        className="p-2 rounded-md hover:bg-secondary transition-colors"
                    >
                        <ChevronRight className="w-5 h-5 text-muted-foreground" />
                    </button>
                </div>

                {/* 日主选择 */}
                <div className="mb-6 p-4 bg-card rounded-lg border border-border">
                    <label className="block text-sm font-medium text-foreground mb-2">
                        选择日主天干
                    </label>
                    <select
                        value={dayMaster}
                        onChange={(e) => setDayMaster(e.target.value)}
                        className="w-full px-3 py-2 bg-background border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring text-foreground"
                    >
                        {dayMasterOptions.map((opt) => (
                            <option key={opt.value} value={opt.value}>
                                {opt.label}
                            </option>
                        ))}
                    </select>
                </div>

                {/* 加载状态 */}
                {loading && (
                    <div className="text-center py-12">
                        <div className="animate-spin w-8 h-8 border-2 border-muted border-t-foreground rounded-full mx-auto" />
                        <p className="mt-4 text-muted-foreground">加载中...</p>
                    </div>
                )}

                {/* 错误状态 */}
                {error && (
                    <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-center">
                        <p className="text-destructive">{error}</p>
                        <button
                            onClick={fetchFortune}
                            className="mt-2 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                        >
                            重试
                        </button>
                    </div>
                )}

                {/* 运势卡片 */}
                {fortune && !loading && (
                    <div className="space-y-6">
                        {/* 月度概览 */}
                        <div className="bg-card rounded-xl border border-border p-6">
                            <div className="flex items-center justify-center gap-2 mb-4 text-foreground">
                                <Sparkles className="w-4 h-4" />
                                <span className="text-sm">
                                    流月：{fortune.month_stem}{fortune.month_branch} · 十神：{fortune.ten_god}
                                </span>
                            </div>

                            {/* 月度总结 */}
                            <div className="p-4 bg-secondary rounded-lg mb-6">
                                <p className="text-foreground text-center">
                                    {fortune.summary}
                                </p>
                            </div>

                            {/* 运势评分 */}
                            <div className="space-y-4">
                                {scoreItems.map((item) => {
                                    const score = fortune.scores[item.key as keyof typeof fortune.scores];
                                    const Icon = item.icon;

                                    return (
                                        <div key={item.key}>
                                            <div className="flex items-center justify-between mb-2">
                                                <div className="flex items-center gap-3">
                                                    <Icon className={`w-5 h-5 ${item.color}`} />
                                                    <span className="font-medium text-foreground">{item.label}</span>
                                                </div>
                                                <span className="text-lg font-bold text-foreground">{score}</span>
                                            </div>
                                            <div className="h-2 bg-secondary rounded-full overflow-hidden">
                                                <div
                                                    style={{ width: `${score}%` }}
                                                    className={`h-full rounded-full transition-all duration-500 ${getScoreColor(score)}`}
                                                />
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        {/* 重要日期 */}
                        {fortune.key_dates.length > 0 && (
                            <div className="bg-card rounded-xl border border-border p-6">
                                <h3 className="font-semibold flex items-center gap-2 mb-4 text-foreground">
                                    <Calendar className="w-5 h-5 text-muted-foreground" />
                                    重要日期
                                </h3>
                                <div className="grid grid-cols-2 gap-3">
                                    {fortune.key_dates.map((kd, index) => {
                                        const Icon = keyDateIcons[kd.type] || Star;
                                        const colorClass = keyDateColors[kd.type] || keyDateColors.lucky;

                                        return (
                                            <div
                                                key={index}
                                                className={`p-3 rounded-lg ${colorClass}`}
                                            >
                                                <div className="flex items-center gap-2">
                                                    <Icon className="w-4 h-4" />
                                                    <span className="font-bold">{kd.date}日</span>
                                                </div>
                                                <p className="text-sm mt-1">{kd.desc}</p>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
