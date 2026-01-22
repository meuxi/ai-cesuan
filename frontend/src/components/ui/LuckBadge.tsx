import React from 'react';
import { motion } from 'framer-motion';

type LuckLevel = '大吉' | '中吉' | '小吉' | '平' | '小凶' | '中凶' | '大凶';

interface LuckBadgeProps {
    level: LuckLevel | string;
    size?: 'sm' | 'md' | 'lg';
    animated?: boolean;
}

const LUCK_STYLES: Record<string, { bg: string; text: string; border: string; glow?: string }> = {
    '大吉': {
        bg: 'bg-gradient-to-r from-amber-100 to-yellow-100',
        text: 'text-amber-700',
        border: 'border-amber-300',
        glow: 'shadow-amber-200'
    },
    '中吉': {
        bg: 'bg-gradient-to-r from-green-100 to-emerald-100',
        text: 'text-green-700',
        border: 'border-green-300',
        glow: 'shadow-green-200'
    },
    '小吉': {
        bg: 'bg-gradient-to-r from-lime-100 to-green-100',
        text: 'text-lime-700',
        border: 'border-lime-300',
    },
    '平': {
        bg: 'bg-gradient-to-r from-gray-100 to-slate-100',
        text: 'text-gray-600',
        border: 'border-gray-300',
    },
    '小凶': {
        bg: 'bg-gradient-to-r from-orange-100 to-amber-100',
        text: 'text-orange-700',
        border: 'border-orange-300',
    },
    '中凶': {
        bg: 'bg-gradient-to-r from-red-100 to-orange-100',
        text: 'text-red-600',
        border: 'border-red-300',
    },
    '大凶': {
        bg: 'bg-gradient-to-r from-red-200 to-rose-200',
        text: 'text-red-800',
        border: 'border-red-400',
        glow: 'shadow-red-200'
    },
};

const SIZE_CLASSES = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-1.5 text-base',
};

const LuckBadge: React.FC<LuckBadgeProps> = ({ level, size = 'md', animated = false }) => {
    const style = LUCK_STYLES[level] || LUCK_STYLES['平'];
    const sizeClass = SIZE_CLASSES[size];

    const badge = (
        <span
            className={`
                inline-flex items-center justify-center
                font-bold rounded-full border
                ${style.bg} ${style.text} ${style.border}
                ${style.glow ? `shadow-md ${style.glow}` : ''}
                ${sizeClass}
            `}
        >
            {level}
        </span>
    );

    if (animated) {
        return (
            <motion.span
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            >
                {badge}
            </motion.span>
        );
    }

    return badge;
};

export default LuckBadge;
