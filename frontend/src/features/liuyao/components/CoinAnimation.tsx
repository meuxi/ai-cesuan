/**
 * 铜钱动画组件
 * 移植自源项目 F:\备份\六爻起卦工具源码\components\Coin.tsx
 */

import React from 'react';
import { motion } from 'framer-motion';

interface CoinProps {
    isHeads: boolean; // 正面 = 字 (有文字), 反面 = 背 (花纹)
    isSpinning: boolean;
    delay?: number;
}

const Coin: React.FC<CoinProps> = ({ isHeads, isSpinning, delay = 0 }) => {
    return (
        <div className="relative w-24 h-24" style={{ perspective: '1000px' }}>
            <motion.div
                className="w-full h-full relative"
                animate={{
                    rotateX: isSpinning ? 1080 + (isHeads ? 0 : 180) : (isHeads ? 0 : 180),
                    rotateY: isSpinning ? 720 : 0,
                    y: isSpinning ? [0, -150, 0] : 0,
                    scale: isSpinning ? [1, 1.2, 1] : 1
                }}
                transition={{
                    duration: isSpinning ? 1.5 : 0.5,
                    ease: "easeInOut",
                    delay: delay
                }}
                style={{ transformStyle: 'preserve-3d' }}
            >
                {/* 正面 (字面) */}
                <div
                    className="absolute inset-0 w-full h-full rounded-full bg-gradient-to-br from-yellow-300 via-yellow-500 to-yellow-700 shadow-xl flex items-center justify-center border-4 border-yellow-600"
                    style={{ backfaceVisibility: 'hidden' }}
                >
                    {/* 方孔 */}
                    <div className="w-8 h-8 bg-stone-900 border border-yellow-800 flex items-center justify-center"></div>
                    {/* 文字 */}
                    <div className="absolute top-1 left-1/2 -translate-x-1/2 text-xs font-serif text-yellow-900 font-bold">乾</div>
                    <div className="absolute bottom-1 left-1/2 -translate-x-1/2 text-xs font-serif text-yellow-900 font-bold">隆</div>
                    <div className="absolute left-1 top-1/2 -translate-y-1/2 text-xs font-serif text-yellow-900 font-bold">宝</div>
                    <div className="absolute right-1 top-1/2 -translate-y-1/2 text-xs font-serif text-yellow-900 font-bold">通</div>
                </div>

                {/* 反面 (背面/花纹) */}
                <div
                    className="absolute inset-0 w-full h-full rounded-full bg-gradient-to-br from-yellow-300 via-yellow-500 to-yellow-700 shadow-xl flex items-center justify-center border-4 border-yellow-600"
                    style={{
                        backfaceVisibility: 'hidden',
                        transform: 'rotateX(180deg)'
                    }}
                >
                    {/* 方孔 */}
                    <div className="w-8 h-8 bg-stone-900 border border-yellow-800"></div>
                    {/* 花纹 */}
                    <div className="absolute w-16 h-16 border-2 border-dotted border-yellow-900 rounded-full opacity-50"></div>
                    <div className="absolute w-12 h-12 border border-dashed border-yellow-900 rounded-full opacity-40"></div>
                </div>
            </motion.div>
        </div>
    );
};

// 三枚铜钱组件
interface ThreeCoinsProps {
    results: boolean[]; // 三枚铜钱的正反面结果
    isSpinning: boolean;
    onAnimationComplete?: () => void;
}

export const ThreeCoins: React.FC<ThreeCoinsProps> = ({ results, isSpinning, onAnimationComplete }) => {
    return (
        <div className="flex gap-4 justify-center items-center py-8">
            {results.map((isHeads, index) => (
                <motion.div
                    key={index}
                    onAnimationComplete={index === 2 ? onAnimationComplete : undefined}
                >
                    <Coin
                        isHeads={isHeads}
                        isSpinning={isSpinning}
                        delay={index * 0.1}
                    />
                </motion.div>
            ))}
        </div>
    );
};

// 摇卦结果显示
interface CoinResultProps {
    backs: number; // 背面数量 0-3
    lineName: string; // 爻名
}

export const CoinResult: React.FC<CoinResultProps> = ({ backs, lineName }) => {
    const getResultText = (backs: number): string => {
        switch (backs) {
            case 0: return '三字 (老阴)';
            case 1: return '一背 (少阳)';
            case 2: return '二背 (少阴)';
            case 3: return '三背 (老阳)';
            default: return '';
        }
    };

    return (
        <div className="flex items-center gap-2 text-sm">
            <span className="text-muted-foreground">{getResultText(backs)}</span>
            <span className="text-primary font-medium">→ {lineName}</span>
        </div>
    );
};

export default Coin;
