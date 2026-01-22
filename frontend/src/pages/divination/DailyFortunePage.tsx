/**
 * 每日运势页面
 * 移植自 MingAI-master/src/app/daily/page.tsx
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
    Compass,
    Sparkles,
    RefreshCw
} from 'lucide-react';

const API_BASE = '/api/fortune';

interface FortuneScores {
    overall: number;
    career: number;
    love: number;
    wealth: number;
    health: number;
    social: number;
}

interface DailyFortune extends FortuneScores {
    date: string;
    day_stem?: string;
    day_branch?: string;
    ten_god?: string;
    advice: string[];
    lucky_color?: string;
    lucky_direction?: string;
    personalized: boolean;
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
    { value: '', label: '通用运势' },
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

export default function DailyFortunePage() {
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [dayMaster, setDayMaster] = useState('');
    const [fortune, setFortune] = useState<DailyFortune | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const formatDate = (date: Date) => {
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long',
        });
    };

    const formatDateForApi = (date: Date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    const changeDate = (days: number) => {
        const newDate = new Date(selectedDate);
        newDate.setDate(newDate.getDate() + days);
        setSelectedDate(newDate);
    };

    const goToToday = () => {
        setSelectedDate(new Date());
    };

    const isToday = selectedDate.toDateString() === new Date().toDateString();

    const fetchFortune = async () => {
        setLoading(true);
        setError(null);
        try {
            const params = new URLSearchParams();
            if (dayMaster) {
                params.append('day_master', dayMaster);
            }
            params.append('date', formatDateForApi(selectedDate));

            const response = await fetch(`${API_BASE}/daily?${params.toString()}`);
            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || '获取运势失败');
            }

            const data = await response.json();
            setFortune({
                ...data,
                ...data.scores,
            });
        } catch (e) {
            setError(e instanceof Error ? e.message : '未知错误');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFortune();
    }, [selectedDate, dayMaster]);

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
                        每日运势
                    </h1>
                    <p className="text-muted-foreground">
                        基于八字命理的个性化运势分析
                    </p>
                </div>

                {/* 日期选择器 */}
                <div className="flex items-center justify-between mb-6 p-4 bg-card rounded-lg border border-border">
                    <button
                        onClick={() => changeDate(-1)}
                        className="p-2 rounded-md hover:bg-secondary transition-colors"
                    >
                        <ChevronLeft className="w-5 h-5 text-muted-foreground" />
                    </button>

                    <div className="text-center">
                        <div className="flex items-center justify-center gap-2 mb-1">
                            <Calendar className="w-5 h-5 text-muted-foreground" />
                            <span className="font-semibold text-foreground">{formatDate(selectedDate)}</span>
                        </div>
                        {isToday ? (
                            <span className="text-sm text-muted-foreground">今日运势</span>
                        ) : (
                            <button
                                onClick={goToToday}
                                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                            >
                                回到今天
                            </button>
                        )}
                    </div>

                    <button
                        onClick={() => changeDate(1)}
                        className="p-2 rounded-md hover:bg-secondary transition-colors"
                    >
                        <ChevronRight className="w-5 h-5 text-muted-foreground" />
                    </button>
                </div>

                {/* 日主选择 */}
                <div className="mb-6 p-4 bg-card rounded-lg border border-border">
                    <label className="block text-sm font-medium text-foreground mb-2">
                        选择日主天干（可选）
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
                    <p className="mt-2 text-xs text-muted-foreground">
                        日主天干可在八字排盘结果中查看，选择后获取个性化运势分析
                    </p>
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
                    <div className="bg-card rounded-xl border border-border p-6">
                        {/* 个性化标识 */}
                        {fortune.personalized ? (
                            <div className="flex items-center justify-center gap-2 mb-4 text-foreground">
                                <Sparkles className="w-4 h-4" />
                                <span className="text-sm">个性化运势 · {dayMaster}日主</span>
                            </div>
                        ) : (
                            <div className="flex items-center justify-center gap-2 mb-4 text-muted-foreground">
                                <User className="w-4 h-4" />
                                <span className="text-sm">通用运势</span>
                            </div>
                        )}

                        {/* 流日信息 */}
                        {fortune.personalized && fortune.day_stem && (
                            <div className="flex items-center justify-center gap-4 mb-4 text-sm text-muted-foreground">
                                <span>流日：{fortune.day_stem}{fortune.day_branch}</span>
                                <span>•</span>
                                <span>十神：{fortune.ten_god}</span>
                            </div>
                        )}

                        {/* 运势评分 */}
                        <div className="space-y-4 mb-6">
                            {scoreItems.map((item) => {
                                const score = fortune[item.key as keyof FortuneScores] as number;
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

                        {/* 幸运信息 */}
                        {fortune.personalized && fortune.lucky_color && (
                            <div className="grid grid-cols-2 gap-4 py-4 border-t border-border">
                                <div>
                                    <div className="flex items-center gap-2 text-muted-foreground mb-1">
                                        <div className="w-4 h-4 rounded-full bg-gradient-to-r from-red-500 via-yellow-500 to-blue-500" />
                                        <span className="text-sm">幸运色</span>
                                    </div>
                                    <span className="font-medium text-foreground">{fortune.lucky_color}</span>
                                </div>
                                <div>
                                    <div className="flex items-center gap-2 text-muted-foreground mb-1">
                                        <Compass className="w-4 h-4" />
                                        <span className="text-sm">吉方位</span>
                                    </div>
                                    <span className="font-medium text-foreground">{fortune.lucky_direction}</span>
                                </div>
                            </div>
                        )}

                        {/* 今日建议 */}
                        <div className="pt-4 border-t border-border">
                            <h3 className="font-semibold flex items-center gap-2 mb-3 text-foreground">
                                <Star className="w-5 h-5 text-muted-foreground" />
                                {isToday ? '今日' : formatDate(selectedDate).split(' ')[0]}建议
                            </h3>
                            <ul className="space-y-2">
                                {fortune.advice.map((advice, index) => (
                                    <li key={index} className="flex items-start gap-3">
                                        <span className="w-5 h-5 rounded-full bg-secondary flex items-center justify-center flex-shrink-0 text-muted-foreground text-xs">
                                            {index + 1}
                                        </span>
                                        <span className="text-muted-foreground text-sm">{advice}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}

                {/* 底部提示 */}
                {!fortune?.personalized && !loading && (
                    <p className="text-center text-sm text-muted-foreground mt-6">
                        选择日主天干获取更精准的个性化运势分析
                    </p>
                )}
            </div>
        </div>
    );
}
