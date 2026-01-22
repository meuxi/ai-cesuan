import React from 'react';
import { LifeKLineAnalysis } from './types';
import { ScrollText, Briefcase, Coins, Heart, Activity, Users, Star, Info, Brain, Bitcoin, Compass, LucideIcon } from 'lucide-react';

interface AnalysisResultProps {
    analysis: LifeKLineAnalysis;
}

interface CardProps {
    title: string;
    icon: LucideIcon;
    content: string | React.ReactNode | string[];
    score: number;
    colorClass: string;
    extraBadges?: React.ReactNode;
}

const ScoreBar = ({ score }: { score: number }) => {
    // 自动检测评分制度：如果 score > 10，认为是百分制，需要转换为十分制
    const normalizedScore = score > 10 ? Math.round(score / 10) : score;

    // Color based on normalized score (0-10)
    let colorClass = "bg-muted";
    if (normalizedScore >= 9) colorClass = "bg-chart-2";
    else if (normalizedScore >= 7) colorClass = "bg-primary";
    else if (normalizedScore >= 5) colorClass = "bg-chart-4";
    else if (normalizedScore >= 3) colorClass = "bg-chart-5";
    else colorClass = "bg-destructive";

    return (
        <div className="flex items-center gap-3 mt-3">
            <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                <div
                    className={`h-full ${colorClass} transition-all duration-1000 ease-out`}
                    style={{ width: `${normalizedScore * 10}%` }}
                />
            </div>
            <span className="text-sm font-bold text-foreground min-w-[2.5rem] text-right">
                {normalizedScore} / 10
            </span>
        </div>
    );
};


const Card = ({ title, icon: Icon, content, score, colorClass, extraBadges }: CardProps) => {
    let displayContent: React.ReactNode;

    if (React.isValidElement(content)) {
        displayContent = content;
    } else {
        // Clean content: remove markdown bold symbols (**) to ensure uniform plain text look
        // Ensure content is a string before calling replace to avoid "content.replace is not a function" error
        let safeContent = '';

        if (typeof content === 'string') {
            safeContent = content;
        } else if (content === null || content === undefined) {
            safeContent = '';
        } else if (typeof content === 'object') {
            // If AI returns an object or array (unexpected but possible), stringify it readable
            try {
                // If it's a simple array of strings, join them
                if (Array.isArray(content)) {
                    safeContent = content.map((c: unknown) => String(c)).join('\n');
                } else {
                    // Fallback for object
                    safeContent = JSON.stringify(content);
                }
            } catch {
                safeContent = String(content);
            }
        } else {
            safeContent = String(content);
        }

        displayContent = safeContent.replace(/\*\*/g, '');
    }

    return (
        <div className="bg-card p-6 rounded-xl shadow-sm border border-border hover:shadow-md transition-shadow flex flex-col h-full relative overflow-hidden">
            <div className={`flex items-center justify-between mb-3 ${colorClass}`}>
                <div className="flex items-center gap-2">
                    <Icon className="w-5 h-5" />
                    <h3 className="font-serif-sc font-bold text-lg">{title}</h3>
                </div>
                <Star className="w-4 h-4 opacity-50" />
            </div>

            {/* Extra Badges for Crypto */}
            {extraBadges && (
                <div className="flex flex-wrap gap-2 mb-3">
                    {extraBadges}
                </div>
            )}

            <div className="text-muted-foreground text-sm leading-relaxed whitespace-pre-wrap flex-grow">
                {displayContent}
            </div>
            {typeof score === 'number' && (
                <div className="pt-4 mt-2 border-t border-border">
                    <div className="text-xs text-muted-foreground font-medium mb-1 uppercase tracking-wider">Rating</div>
                    <ScoreBar score={score} />
                </div>
            )}
        </div>
    );
};

const AnalysisResult: React.FC<AnalysisResultProps> = ({ analysis }) => {
    return (
        <div className="w-full space-y-8 animate-fade-in-up">
            {/* Bazi Pillars */}
            <div className="flex justify-center gap-2 md:gap-8 bg-foreground text-background p-6 rounded-xl shadow-lg overflow-x-auto">
                {analysis.bazi.map((pillar, index) => {
                    const labels = ['年柱', '月柱', '日柱', '时柱'];
                    return (
                        <div key={index} className="text-center min-w-[60px]">
                            <div className="text-xs text-muted mb-1">{labels[index]}</div>
                            <div className="text-xl md:text-3xl font-serif-sc font-bold tracking-widest">{pillar}</div>
                        </div>
                    );
                })}
            </div>

            {/* Summary with Score */}
            <div className="bg-gradient-to-br from-primary/10 to-card p-6 rounded-xl border border-primary/20 shadow-sm">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                    <h3 className="flex items-center gap-2 font-serif-sc font-bold text-xl text-primary">
                        <ScrollText className="w-5 h-5" />
                        命理总评
                    </h3>
                    <div className="w-full md:w-1/3">
                        <ScoreBar score={analysis.summaryScore} />
                    </div>
                </div>
                <p className="text-foreground leading-relaxed whitespace-pre-wrap font-medium">{analysis.summary}</p>
            </div>

            {/* Grid for categorical analysis with Scores */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                <Card
                    title="性格分析"
                    icon={Brain}
                    content={analysis.personality}
                    score={analysis.personalityScore}
                    colorClass="text-teal-600"
                />
                <Card
                    title="事业行业"
                    icon={Briefcase}
                    content={analysis.industry}
                    score={analysis.industryScore}
                    colorClass="text-blue-600"
                />

                {/* Feng Shui Analysis */}
                <Card
                    title="发展风水"
                    icon={Compass}
                    content={analysis.fengShui}
                    score={analysis.fengShuiScore}
                    colorClass="text-cyan-700"
                />

                <Card
                    title="财富层级"
                    icon={Coins}
                    content={analysis.wealth}
                    score={analysis.wealthScore}
                    colorClass="text-amber-600"
                />
                <Card
                    title="婚姻情感"
                    icon={Heart}
                    content={analysis.marriage}
                    score={analysis.marriageScore}
                    colorClass="text-pink-600"
                />
                <Card
                    title="身体健康"
                    icon={Activity}
                    content={analysis.health}
                    score={analysis.healthScore}
                    colorClass="text-emerald-600"
                />
                <Card
                    title="六亲关系"
                    icon={Users}
                    content={analysis.family}
                    score={analysis.familyScore}
                    colorClass="text-purple-600"
                />

                {/* Static Score Explanation Card */}
                <Card
                    title="评分讲解"
                    icon={Info}
                    colorClass="text-muted-foreground"
                    content={
                        <div className="space-y-4">
                            <ul className="space-y-1.5 font-mono text-xs md:text-sm">
                                <li className="flex justify-between items-center border-b border-border pb-1">
                                    <span>0-2分</span>
                                    <span className="text-xs px-2 py-0.5 bg-destructive/20 text-destructive rounded font-bold">极差</span>
                                </li>
                                <li className="flex justify-between items-center border-b border-border pb-1">
                                    <span>3-4分</span>
                                    <span className="text-xs px-2 py-0.5 bg-chart-5/20 text-chart-5 rounded font-bold">差</span>
                                </li>
                                <li className="flex justify-between items-center border-b border-border pb-1">
                                    <span>5-6分</span>
                                    <span className="text-xs px-2 py-0.5 bg-chart-4/20 text-chart-4 rounded font-bold">一般</span>
                                </li>
                                <li className="flex justify-between items-center border-b border-border pb-1">
                                    <span>7-8分</span>
                                    <span className="text-xs px-2 py-0.5 bg-primary/20 text-primary rounded font-bold">好</span>
                                </li>
                                <li className="flex justify-between items-center">
                                    <span>9-10分</span>
                                    <span className="text-xs px-2 py-0.5 bg-chart-2/20 text-chart-2 rounded font-bold">极好</span>
                                </li>
                            </ul>
                            <p className="text-xs text-foreground leading-relaxed border-t border-border pt-2 text-justify">
                                注：命运还受环境和个人选择影响，八字趋势不能完全代表真实人生，命理学不是玄学，而是帮助我们在人生列车上做出更好选择的哲学工具。一命二运三风水 四积阴德五读书 六名七相八敬神 九遇贵人十养生。
                            </p>
                        </div>
                    }
                />
            </div>
        </div>
    );
};

export default AnalysisResult;
