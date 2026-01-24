/**
 * 塔罗牌动画组件
 * 提供仪式感的3D翻牌动画效果，支持图片显示
 */

import { useState, useEffect } from 'react'
import { motion, AnimatePresence, useMotionValue, useTransform } from 'framer-motion'
import { Sparkles, Star, Moon } from 'lucide-react'
import { getCardImageUrl } from '@/services/tarotApi'
import { useTranslation } from 'react-i18next'

interface TarotCardProps {
    cardCode?: string
    cardName?: string
    imageUrl?: string
    isRevealed: boolean
    isReversed?: boolean
    onReveal?: () => void
    delay?: number
    size?: 'sm' | 'md' | 'lg' | 'xl'
    /** 3D视差效果 */
    enable3D?: boolean
    /** 发光效果 */
    enableGlow?: boolean
}

export function TarotCard({
    cardCode,
    cardName,
    imageUrl,
    isRevealed,
    isReversed = false,
    onReveal,
    delay = 0,
    size = 'md',
    enable3D = true,
    enableGlow = true
}: TarotCardProps) {
    const { t, i18n } = useTranslation()
    const [isFlipping, setIsFlipping] = useState(false)
    const [imageError, setImageError] = useState(false)
    const [isHovered, setIsHovered] = useState(false)

    // 3D 视差效果
    const x = useMotionValue(0)
    const y = useMotionValue(0)
    const rotateX = useTransform(y, [-100, 100], [10, -10])
    const rotateYParallax = useTransform(x, [-100, 100], [170, 190])

    const sizeClasses = {
        sm: 'w-16 h-24 sm:w-20 sm:h-32',
        md: 'w-20 h-32 sm:w-28 sm:h-44',
        lg: 'w-24 h-36 sm:w-32 sm:h-48 md:w-36 md:h-56',
        xl: 'w-32 h-48 sm:w-40 sm:h-60 md:w-44 md:h-68'
    }

    const handleClick = () => {
        if (!isRevealed && onReveal) {
            setIsFlipping(true)
            setTimeout(() => {
                onReveal()
                setIsFlipping(false)
            }, 800)
        }
    }

    const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
        if (!enable3D || !isRevealed) return
        const rect = e.currentTarget.getBoundingClientRect()
        const centerX = rect.left + rect.width / 2
        const centerY = rect.top + rect.height / 2
        x.set(e.clientX - centerX)
        y.set(e.clientY - centerY)
    }

    const handleMouseLeave = () => {
        x.set(0)
        y.set(0)
        setIsHovered(false)
    }

    const finalImageUrl = imageUrl || (cardCode ? getCardImageUrl(cardCode) : '')
    const clickText = i18n.language === 'en' ? 'Click to reveal' : '点击翻牌'
    const reversedText = i18n.language === 'en' ? '(Reversed)' : '(逆位)'

    return (
        <motion.div
            className={`${sizeClasses[size]} relative cursor-pointer`}
            style={{
                perspective: '1200px',
                transformStyle: 'preserve-3d'
            }}
            initial={{ opacity: 0, y: 30, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay, duration: 0.6, ease: [0.23, 1, 0.32, 1] }}
            onClick={handleClick}
            onMouseMove={handleMouseMove}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={handleMouseLeave}
        >
            <motion.div
                className="w-full h-full relative"
                animate={{
                    rotateY: isRevealed || isFlipping ? 180 : 0,
                }}
                transition={{
                    duration: 0.8,
                    ease: [0.23, 1, 0.32, 1]
                }}
                style={{
                    transformStyle: 'preserve-3d',
                    rotateX: enable3D && isRevealed ? rotateX : 0,
                    rotateY: enable3D && isRevealed ? rotateYParallax : (isRevealed || isFlipping ? 180 : 0),
                }}
            >
                {/* 牌背 - 神秘星空设计 */}
                <div
                    className="absolute inset-0 rounded-xl overflow-hidden shadow-2xl"
                    style={{ backfaceVisibility: 'hidden' }}
                >
                    {/* 背景渐变 */}
                    <div className="absolute inset-0 bg-gradient-to-br from-indigo-950 via-purple-900 to-violet-950" />

                    {/* 星空纹理 */}
                    <div className="absolute inset-0 opacity-30">
                        {[...Array(20)].map((_, i) => (
                            <motion.div
                                key={i}
                                className="absolute w-1 h-1 bg-white rounded-full"
                                style={{
                                    left: `${Math.random() * 100}%`,
                                    top: `${Math.random() * 100}%`,
                                }}
                                animate={{
                                    opacity: [0.3, 1, 0.3],
                                    scale: [1, 1.2, 1],
                                }}
                                transition={{
                                    duration: 2 + Math.random() * 2,
                                    repeat: Infinity,
                                    delay: Math.random() * 2,
                                }}
                            />
                        ))}
                    </div>

                    {/* 装饰边框 */}
                    <div className="absolute inset-1.5 border border-amber-400/40 rounded-lg" />
                    <div className="absolute inset-3 border border-amber-400/20 rounded" />

                    {/* 中心图案 */}
                    <div className="absolute inset-0 flex items-center justify-center">
                        <motion.div
                            className="relative"
                            animate={{ rotate: 360 }}
                            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                        >
                            <Moon className="w-16 h-16 text-amber-400/40" />
                        </motion.div>
                        <motion.div
                            className="absolute"
                            animate={{
                                scale: [1, 1.1, 1],
                                opacity: [0.5, 0.8, 0.5]
                            }}
                            transition={{ duration: 2, repeat: Infinity }}
                        >
                            <Star className="w-10 h-10 text-amber-400/60" />
                        </motion.div>
                    </div>

                    {/* 角落装饰 */}
                    <Sparkles className="absolute top-2 left-2 w-4 h-4 text-amber-400/50" />
                    <Sparkles className="absolute top-2 right-2 w-4 h-4 text-amber-400/50" />
                    <Sparkles className="absolute bottom-2 left-2 w-4 h-4 text-amber-400/50" />
                    <Sparkles className="absolute bottom-2 right-2 w-4 h-4 text-amber-400/50" />

                    {/* 悬停提示 */}
                    {!isRevealed && (
                        <motion.div
                            className="absolute inset-0 flex items-center justify-center bg-black/0 hover:bg-black/30 transition-all duration-300"
                            whileHover={{ scale: 1.02 }}
                        >
                            <motion.span
                                className="text-xs text-amber-200/80 opacity-0 hover:opacity-100 transition-opacity px-2 py-1 bg-black/40 rounded"
                                initial={{ y: 10 }}
                                whileHover={{ y: 0 }}
                            >
                                {clickText}
                            </motion.span>
                        </motion.div>
                    )}

                    {/* 外发光边框 */}
                    <div className="absolute inset-0 rounded-xl border-2 border-amber-400/50 shadow-[0_0_20px_rgba(251,191,36,0.3)]" />
                </div>

                {/* 牌面 - 显示图片 */}
                <div
                    className="absolute inset-0 rounded-xl shadow-2xl overflow-hidden"
                    style={{
                        backfaceVisibility: 'hidden',
                        transform: `rotateY(180deg) ${isReversed ? 'rotate(180deg)' : ''}`
                    }}
                >
                    {finalImageUrl && !imageError ? (
                        <>
                            <img
                                src={finalImageUrl}
                                alt={cardName || 'Tarot Card'}
                                className="w-full h-full object-cover"
                                loading="lazy"
                                decoding="async"
                                onError={() => setImageError(true)}
                            />
                            {/* 图片光泽效果 */}
                            {enableGlow && isHovered && (
                                <motion.div
                                    className="absolute inset-0 pointer-events-none"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 0.3 }}
                                    style={{
                                        background: 'linear-gradient(135deg, transparent 40%, rgba(255,255,255,0.4) 50%, transparent 60%)',
                                    }}
                                />
                            )}
                        </>
                    ) : (
                        <div className="w-full h-full bg-gradient-to-br from-amber-50 to-orange-100 dark:from-amber-900/50 dark:to-orange-900/50 flex flex-col items-center justify-center p-3">
                            <Sparkles className="w-10 h-10 mx-auto text-amber-600 dark:text-amber-400 mb-3" />
                            <p className="text-sm font-medium text-amber-800 dark:text-amber-200 line-clamp-2 text-center">
                                {cardName || 'Tarot'}
                            </p>
                        </div>
                    )}

                    {/* 卡牌名称底栏 */}
                    {finalImageUrl && !imageError && cardName && (
                        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 via-black/50 to-transparent p-2 pt-6">
                            <p className="text-xs text-white text-center font-medium truncate">
                                {cardName}{isReversed ? ` ${reversedText}` : ''}
                            </p>
                        </div>
                    )}

                    {/* 牌面边框 */}
                    <div className="absolute inset-0 rounded-xl border-2 border-amber-500/70" />
                </div>
            </motion.div>

            {/* 翻牌光芒效果 */}
            <AnimatePresence>
                {isFlipping && (
                    <>
                        <motion.div
                            className="absolute inset-0 rounded-xl pointer-events-none"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: [0, 1, 0] }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.8 }}
                        >
                            <div className="absolute inset-0 bg-gradient-radial from-amber-400/60 via-amber-400/20 to-transparent rounded-xl" />
                        </motion.div>
                        {/* 粒子效果 */}
                        {[...Array(8)].map((_, i) => (
                            <motion.div
                                key={i}
                                className="absolute w-2 h-2 bg-amber-400 rounded-full"
                                style={{
                                    left: '50%',
                                    top: '50%',
                                }}
                                initial={{ opacity: 1, scale: 0 }}
                                animate={{
                                    opacity: [1, 0],
                                    scale: [0, 1],
                                    x: Math.cos((i / 8) * Math.PI * 2) * 60,
                                    y: Math.sin((i / 8) * Math.PI * 2) * 80,
                                }}
                                transition={{ duration: 0.6, ease: "easeOut" }}
                            />
                        ))}
                    </>
                )}
            </AnimatePresence>

            {/* 悬停发光效果 */}
            {enableGlow && isHovered && isRevealed && (
                <motion.div
                    className="absolute -inset-2 rounded-2xl pointer-events-none"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    style={{
                        background: 'radial-gradient(ellipse at center, rgba(251,191,36,0.15) 0%, transparent 70%)',
                        filter: 'blur(8px)',
                    }}
                />
            )}
        </motion.div>
    )
}

// 三牌阵布局
interface ThreeCardSpreadProps {
    cards: { name: string; revealed: boolean }[]
    onRevealCard: (index: number) => void
}

export function ThreeCardSpread({ cards, onRevealCard }: ThreeCardSpreadProps) {
    const positions = ['过去', '现在', '未来']

    return (
        <div className="flex flex-col items-center gap-4">
            <div className="flex gap-4 justify-center">
                {cards.map((card, index) => (
                    <div key={index} className="flex flex-col items-center gap-2">
                        <TarotCard
                            cardName={card.name}
                            isRevealed={card.revealed}
                            onReveal={() => onRevealCard(index)}
                            delay={index * 0.2}
                        />
                        <span className="text-xs text-muted-foreground">
                            {positions[index]}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    )
}

// 洗牌动画
interface ShuffleAnimationProps {
    isShuffling: boolean
    onComplete?: () => void
}

export function ShuffleAnimation({ isShuffling, onComplete }: ShuffleAnimationProps) {
    return (
        <AnimatePresence>
            {isShuffling && (
                <motion.div
                    className="flex justify-center items-center py-8"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onAnimationComplete={onComplete}
                >
                    <div className="relative">
                        {[...Array(5)].map((_, i) => (
                            <motion.div
                                key={i}
                                className="absolute w-20 h-32 rounded-lg bg-gradient-to-br from-indigo-900 to-purple-900 border border-amber-400/50"
                                initial={{ x: 0, y: 0, rotate: 0 }}
                                animate={{
                                    x: [0, (i - 2) * 30, 0],
                                    y: [0, -20, 0],
                                    rotate: [0, (i - 2) * 10, 0],
                                }}
                                transition={{
                                    duration: 0.5,
                                    repeat: 3,
                                    repeatType: 'reverse',
                                    delay: i * 0.05,
                                }}
                                style={{ zIndex: 5 - i }}
                            />
                        ))}
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    )
}

export default TarotCard
