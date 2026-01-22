/**
 * 塔罗牌洗牌动画组件
 * 创造沉浸式的洗牌体验
 */

import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Sparkles, Shuffle } from 'lucide-react'
import { useTranslation } from 'react-i18next'

interface ShuffleAnimationProps {
    /** 是否正在洗牌 */
    isShuffling: boolean
    /** 洗牌完成回调 */
    onComplete?: () => void
    /** 洗牌持续时间（毫秒） */
    duration?: number
    /** 卡牌数量 */
    cardCount?: number
}

export function ShuffleAnimation({
    isShuffling,
    onComplete,
    duration = 3000,
    cardCount = 12
}: ShuffleAnimationProps) {
    const { i18n } = useTranslation()
    const [phase, setPhase] = useState<'idle' | 'gather' | 'shuffle' | 'spread' | 'done'>('idle')
    
    useEffect(() => {
        if (isShuffling) {
            setPhase('gather')
            
            const gatherTimer = setTimeout(() => setPhase('shuffle'), 400)
            const shuffleTimer = setTimeout(() => setPhase('spread'), duration - 600)
            const doneTimer = setTimeout(() => {
                setPhase('done')
                onComplete?.()
            }, duration)
            
            return () => {
                clearTimeout(gatherTimer)
                clearTimeout(shuffleTimer)
                clearTimeout(doneTimer)
            }
        } else {
            setPhase('idle')
        }
    }, [isShuffling, duration, onComplete])

    const shuffleText = i18n.language === 'en' ? 'Shuffling...' : '正在洗牌...'
    const focusText = i18n.language === 'en' ? 'Focus on your question' : '请专注于你的问题'

    return (
        <AnimatePresence>
            {isShuffling && (
                <motion.div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    {/* 神秘光晕背景 */}
                    <motion.div
                        className="absolute w-96 h-96 rounded-full"
                        style={{
                            background: 'radial-gradient(circle, rgba(147,51,234,0.3) 0%, transparent 70%)',
                        }}
                        animate={{
                            scale: [1, 1.2, 1],
                            opacity: [0.5, 0.8, 0.5],
                        }}
                        transition={{ duration: 2, repeat: Infinity }}
                    />
                    
                    {/* 卡牌动画容器 */}
                    <div className="relative w-80 h-52">
                        {[...Array(cardCount)].map((_, i) => (
                            <ShuffleCard
                                key={i}
                                index={i}
                                total={cardCount}
                                phase={phase}
                            />
                        ))}
                    </div>
                    
                    {/* 文字提示 */}
                    <motion.div
                        className="absolute bottom-32 flex flex-col items-center gap-3"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.5 }}
                    >
                        <div className="flex items-center gap-2 text-amber-400">
                            <Shuffle className="w-5 h-5 animate-spin" />
                            <span className="text-lg font-medium">{shuffleText}</span>
                        </div>
                        <p className="text-sm text-white/60">{focusText}</p>
                        
                        {/* 进度条 */}
                        <div className="w-48 h-1 bg-white/10 rounded-full overflow-hidden">
                            <motion.div
                                className="h-full bg-gradient-to-r from-purple-500 to-amber-500"
                                initial={{ width: '0%' }}
                                animate={{ width: '100%' }}
                                transition={{ duration: duration / 1000, ease: 'linear' }}
                            />
                        </div>
                    </motion.div>
                    
                    {/* 装饰粒子 */}
                    {[...Array(20)].map((_, i) => (
                        <motion.div
                            key={`particle-${i}`}
                            className="absolute w-1 h-1 bg-amber-400/60 rounded-full"
                            style={{
                                left: `${30 + Math.random() * 40}%`,
                                top: `${30 + Math.random() * 40}%`,
                            }}
                            animate={{
                                x: (Math.random() - 0.5) * 100,
                                y: (Math.random() - 0.5) * 100,
                                opacity: [0, 1, 0],
                                scale: [0, 1, 0],
                            }}
                            transition={{
                                duration: 2,
                                repeat: Infinity,
                                delay: Math.random() * 2,
                            }}
                        />
                    ))}
                </motion.div>
            )}
        </AnimatePresence>
    )
}

// 单张洗牌卡牌
function ShuffleCard({
    index,
    total,
    phase
}: {
    index: number
    total: number
    phase: string
}) {
    const getCardStyle = useCallback(() => {
        const centerOffset = (index - total / 2) * 3
        
        switch (phase) {
            case 'idle':
                return {
                    x: centerOffset * 8,
                    y: 0,
                    rotate: centerOffset,
                    scale: 1,
                }
            case 'gather':
                return {
                    x: 0,
                    y: 0,
                    rotate: 0,
                    scale: 0.95,
                }
            case 'shuffle':
                const shuffleX = (Math.random() - 0.5) * 120
                const shuffleY = (Math.random() - 0.5) * 80
                const shuffleRotate = (Math.random() - 0.5) * 30
                return {
                    x: shuffleX,
                    y: shuffleY,
                    rotate: shuffleRotate,
                    scale: 1,
                }
            case 'spread':
            case 'done':
                const spreadAngle = ((index / total) * 180 - 90) * (Math.PI / 180)
                const radius = 100
                return {
                    x: Math.cos(spreadAngle) * radius,
                    y: Math.sin(spreadAngle) * radius * 0.3 + 20,
                    rotate: (index / total) * 60 - 30,
                    scale: 1,
                }
            default:
                return { x: 0, y: 0, rotate: 0, scale: 1 }
        }
    }, [index, total, phase])

    const style = getCardStyle()

    return (
        <motion.div
            className="absolute left-1/2 top-1/2 w-16 h-24 -ml-8 -mt-12"
            animate={style}
            transition={{
                type: 'spring',
                stiffness: 100,
                damping: 15,
                delay: phase === 'shuffle' ? index * 0.02 : 0,
            }}
            style={{ zIndex: index }}
        >
            <div className="w-full h-full rounded-lg bg-gradient-to-br from-indigo-900 via-purple-900 to-violet-900 border border-amber-400/50 shadow-lg">
                <div className="absolute inset-1 border border-amber-400/20 rounded" />
                <div className="absolute inset-0 flex items-center justify-center">
                    <Sparkles className="w-4 h-4 text-amber-400/40" />
                </div>
            </div>
        </motion.div>
    )
}

// 洗牌按钮组件
interface ShuffleButtonProps {
    onClick: () => void
    disabled?: boolean
    isShuffling?: boolean
}

export function ShuffleButton({ onClick, disabled, isShuffling }: ShuffleButtonProps) {
    const { i18n } = useTranslation()
    const buttonText = i18n.language === 'en' ? 'Shuffle Cards' : '洗牌'
    const shufflingText = i18n.language === 'en' ? 'Shuffling...' : '洗牌中...'

    return (
        <motion.button
            onClick={onClick}
            disabled={disabled || isShuffling}
            className={`
                relative px-8 py-4 rounded-xl font-medium text-lg
                bg-gradient-to-r from-purple-600 to-indigo-600
                hover:from-purple-500 hover:to-indigo-500
                text-white shadow-lg
                disabled:opacity-50 disabled:cursor-not-allowed
                overflow-hidden
            `}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
        >
            {/* 发光效果 */}
            <motion.div
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
                animate={{
                    x: ['-100%', '100%'],
                }}
                transition={{
                    duration: 2,
                    repeat: Infinity,
                    repeatDelay: 1,
                }}
            />
            
            <span className="relative flex items-center gap-2">
                <motion.span
                    animate={isShuffling ? { rotate: 360 } : { rotate: 0 }}
                    transition={{ duration: 1, repeat: isShuffling ? Infinity : 0 }}
                >
                    <Shuffle className="w-5 h-5" />
                </motion.span>
                {isShuffling ? shufflingText : buttonText}
            </span>
        </motion.button>
    )
}
