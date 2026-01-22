import React from 'react';
import { motion } from 'framer-motion';

interface ScoreBarProps {
    score: number;
    max?: number;
    label?: string;
    showLabel?: boolean;
    size?: 'sm' | 'md' | 'lg';
    animated?: boolean;
}

const getColorClass = (score: number, max: number): string => {
    const percentage = (score / max) * 100;
    if (percentage >= 80) return 'bg-gradient-to-r from-green-500 to-emerald-400';
    if (percentage >= 60) return 'bg-gradient-to-r from-indigo-500 to-blue-400';
    if (percentage >= 40) return 'bg-gradient-to-r from-yellow-500 to-amber-400';
    if (percentage >= 20) return 'bg-gradient-to-r from-orange-500 to-red-400';
    return 'bg-gradient-to-r from-red-600 to-rose-500';
};

const getTextColorClass = (score: number, max: number): string => {
    const percentage = (score / max) * 100;
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 60) return 'text-indigo-600';
    if (percentage >= 40) return 'text-yellow-600';
    if (percentage >= 20) return 'text-orange-600';
    return 'text-red-600';
};

const SIZE_CONFIG = {
    sm: { height: 'h-1.5', text: 'text-xs', gap: 'gap-2' },
    md: { height: 'h-2', text: 'text-sm', gap: 'gap-3' },
    lg: { height: 'h-3', text: 'text-base', gap: 'gap-4' },
};

const ScoreBar: React.FC<ScoreBarProps> = ({
    score,
    max = 10,
    label,
    showLabel = true,
    size = 'md',
    animated = true,
}) => {
    // 评分自适应：如果 score > max，认为是百分制，自动转换
    const normalizedScore = score > max ? Math.round(score / (100 / max)) : score;
    const displayScore = Math.min(max, Math.max(0, normalizedScore));
    const percentage = Math.min(100, Math.max(0, (displayScore / max) * 100));
    const colorClass = getColorClass(displayScore, max);
    const textColorClass = getTextColorClass(displayScore, max);
    const sizeConfig = SIZE_CONFIG[size];

    const barContent = (
        <div
            className={`${colorClass} ${sizeConfig.height} rounded-full`}
            style={{ width: `${percentage}%` }}
        />
    );

    return (
        <div className={`flex items-center ${sizeConfig.gap}`}>
            {label && showLabel && (
                <span className={`${sizeConfig.text} text-muted-foreground min-w-[60px]`}>{label}</span>
            )}
            <div className={`flex-1 ${sizeConfig.height} bg-muted rounded-full overflow-hidden`}>
                {animated ? (
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${percentage}%` }}
                        transition={{ duration: 1, ease: 'easeOut' }}
                        className={`${colorClass} ${sizeConfig.height} rounded-full`}
                    />
                ) : (
                    barContent
                )}
            </div>
            <span className={`${sizeConfig.text} font-bold ${textColorClass} min-w-[40px] text-right`}>
                {displayScore}/{max}
            </span>
        </div>
    );
};

export default ScoreBar;
