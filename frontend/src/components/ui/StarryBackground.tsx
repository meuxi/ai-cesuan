import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

interface StarryBackgroundProps {
    children?: React.ReactNode;
    intensity?: 'low' | 'medium' | 'high';
    animated?: boolean;
    className?: string;
}

/**
 * 星空主题背景组件
 * 移植自 Diviner 项目
 */
const StarryBackground: React.FC<StarryBackgroundProps> = ({
    children,
    intensity = 'medium',
    animated = true,
    className = ''
}) => {
    const starConfig = {
        low: { count: 50, twinkle: 30 },
        medium: { count: 100, twinkle: 50 },
        high: { count: 150, twinkle: 80 },
    };

    const config = starConfig[intensity];

    return (
        <div className={`relative min-h-screen overflow-hidden ${className}`}>
            {/* 渐变背景 */}
            <div
                className="fixed inset-0 -z-20"
                style={{
                    background: 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)'
                }}
            />

            {/* 星星层 */}
            <div
                className="fixed inset-0 -z-10 pointer-events-none"
                style={{
                    backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Ccircle fill='%23fff' cx='25' cy='25' r='1'/%3E%3Ccircle fill='%23fff' cx='75' cy='75' r='0.5'/%3E%3Ccircle fill='%23fff' cx='125' cy='45' r='1.2'/%3E%3Ccircle fill='%23fff' cx='175' cy='125' r='0.8'/%3E%3Ccircle fill='%23fff' cx='50' cy='150' r='1'/%3E%3Ccircle fill='%23fff' cx='150' cy='175' r='0.6'/%3E%3Ccircle fill='%23fff' cx='100' cy='100' r='1.5'/%3E%3Ccircle fill='%23fff' cx='25' cy='175' r='0.7'/%3E%3Ccircle fill='%23fff' cx='175' cy='25' r='1.1'/%3E%3C/svg%3E")`,
                    backgroundSize: '200px 200px',
                    animation: animated ? 'moveStars 100s linear infinite' : 'none',
                }}
            />

            {/* 闪烁星星层 */}
            <div
                className="fixed inset-0 -z-10 pointer-events-none opacity-50"
                style={{
                    backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 300'%3E%3Ccircle fill='%23ffffff88' cx='50' cy='50' r='1'/%3E%3Ccircle fill='%23ffffff66' cx='150' cy='100' r='0.8'/%3E%3Ccircle fill='%23ffffffaa' cx='250' cy='200' r='1.2'/%3E%3Ccircle fill='%23ffffff55' cx='100' cy='250' r='0.6'/%3E%3C/svg%3E")`,
                    backgroundSize: '300px 300px',
                    animation: animated ? 'moveTwinkling 50s linear infinite' : 'none',
                }}
            />

            {/* 内容 */}
            <div className="relative z-10">
                {children}
            </div>

            {/* 动画样式 */}
            <style>{`
                @keyframes moveStars {
                    from { transform: translateY(0); }
                    to { transform: translateY(-200px); }
                }
                @keyframes moveTwinkling {
                    from { transform: translateX(0); }
                    to { transform: translateX(-300px); }
                }
            `}</style>
        </div>
    );
};

/**
 * 神秘光晕效果
 */
export const MysticalGlow: React.FC<{ className?: string }> = ({ className = '' }) => (
    <motion.div
        className={`absolute rounded-full blur-3xl opacity-30 ${className}`}
        animate={{
            scale: [1, 1.2, 1],
            opacity: [0.2, 0.4, 0.2],
        }}
        transition={{
            duration: 4,
            repeat: Infinity,
            ease: 'easeInOut',
        }}
        style={{
            background: 'radial-gradient(circle, #8E2DE2 0%, #4A00E0 50%, transparent 70%)',
        }}
    />
);

/**
 * 浮动粒子效果
 */
export const FloatingParticles: React.FC<{ count?: number }> = ({ count = 20 }) => {
    const particles = Array.from({ length: count }, (_, i) => ({
        id: i,
        size: Math.random() * 4 + 2,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 10 + 10,
        delay: Math.random() * 5,
    }));

    return (
        <div className="fixed inset-0 pointer-events-none overflow-hidden -z-5">
            {particles.map((p) => (
                <motion.div
                    key={p.id}
                    className="absolute rounded-full bg-purple-400/30"
                    style={{
                        width: p.size,
                        height: p.size,
                        left: `${p.x}%`,
                        top: `${p.y}%`,
                    }}
                    animate={{
                        y: [0, -100, 0],
                        opacity: [0, 0.8, 0],
                    }}
                    transition={{
                        duration: p.duration,
                        repeat: Infinity,
                        delay: p.delay,
                        ease: 'easeInOut',
                    }}
                />
            ))}
        </div>
    );
};

/**
 * 神秘边框卡片
 */
export const MysticalCard: React.FC<{
    children: React.ReactNode;
    className?: string;
    glowing?: boolean;
}> = ({ children, className = '', glowing = false }) => (
    <div
        className={`
            relative rounded-2xl p-6
            bg-gradient-to-br from-slate-900/90 via-purple-950/80 to-slate-900/90
            backdrop-blur-xl
            border border-purple-500/30
            ${glowing ? 'shadow-lg shadow-purple-500/20' : ''}
            ${className}
        `}
    >
        {glowing && (
            <div
                className="absolute inset-0 rounded-2xl -z-10"
                style={{
                    background: 'linear-gradient(45deg, #8E2DE2, #4A00E0, #8E2DE2)',
                    backgroundSize: '200% 200%',
                    animation: 'gradientShift 3s ease infinite',
                    opacity: 0.3,
                    filter: 'blur(20px)',
                }}
            />
        )}
        {children}
        <style>{`
            @keyframes gradientShift {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }
        `}</style>
    </div>
);

/**
 * 神秘文字样式
 */
export const MysticalText: React.FC<{
    children: React.ReactNode;
    variant?: 'gold' | 'silver' | 'purple';
    className?: string;
}> = ({ children, variant = 'gold', className = '' }) => {
    const gradients = {
        gold: 'from-amber-400 via-yellow-200 to-amber-400',
        silver: 'from-gray-300 via-white to-gray-300',
        purple: 'from-purple-400 via-indigo-300 to-purple-400',
    };

    return (
        <span
            className={`
                bg-gradient-to-r ${gradients[variant]}
                bg-clip-text text-transparent
                font-bold
                ${className}
            `}
        >
            {children}
        </span>
    );
};

export default StarryBackground;
