/**
 * 塔罗牌阵组件
 * 支持多种经典牌阵布局
 */

import { memo, useCallback } from 'react'
import { motion } from 'framer-motion'
import { TarotCard } from '../TarotCard'
import { useTranslation } from 'react-i18next'

export type SpreadType = 'single' | 'three-card' | 'cross' | 'horseshoe' | 'celtic-cross'

export interface SpreadCard {
    cardCode?: string
    cardName?: string
    imageUrl?: string
    isReversed?: boolean
    position?: string
    meaning?: string
}

interface TarotSpreadProps {
    type: SpreadType
    cards: SpreadCard[]
    revealedIndices: number[]
    onRevealCard: (index: number) => void
    cardSize?: 'sm' | 'md' | 'lg'
}

// 牌阵位置名称（用于显示）
const SPREAD_POSITIONS: Record<SpreadType, string[]> = {
    'single': ['当前状况'],
    'three-card': ['过去', '现在', '未来'],
    'cross': ['现状', '障碍', '意识', '潜意识', '结果'],
    'horseshoe': ['过去', '现在', '隐藏影响', '障碍', '外部环境', '建议', '结果'],
    'celtic-cross': [
        '现状', '挑战', '基础', '过去', '可能', '近期未来',
        '自我态度', '环境影响', '希望恐惧', '最终结果'
    ]
}

// 英文位置名称
const SPREAD_POSITIONS_EN: Record<SpreadType, string[]> = {
    'single': ['Current Situation'],
    'three-card': ['Past', 'Present', 'Future'],
    'cross': ['Present', 'Challenge', 'Conscious', 'Subconscious', 'Outcome'],
    'horseshoe': ['Past', 'Present', 'Hidden Influence', 'Obstacle', 'Environment', 'Advice', 'Outcome'],
    'celtic-cross': [
        'Present', 'Challenge', 'Foundation', 'Past', 'Potential', 'Near Future',
        'Self', 'Environment', 'Hopes/Fears', 'Final Outcome'
    ]
}

export function TarotSpread({
    type,
    cards,
    revealedIndices,
    onRevealCard,
    cardSize = 'md'
}: TarotSpreadProps) {
    const { i18n } = useTranslation()
    const positions = i18n.language === 'en' ? SPREAD_POSITIONS_EN[type] : SPREAD_POSITIONS[type]
    
    // 根据牌阵类型返回不同的布局
    const renderSpread = () => {
        switch (type) {
            case 'single':
                return renderSingleCard()
            case 'three-card':
                return renderThreeCards()
            case 'cross':
                return renderCross()
            case 'horseshoe':
                return renderHorseshoe()
            case 'celtic-cross':
                return renderCelticCross()
            default:
                return renderThreeCards()
        }
    }

    // 单牌
    const renderSingleCard = () => (
        <div className="flex justify-center items-center py-8">
            {renderCardWithPosition(0)}
        </div>
    )

    // 三牌阵（过去-现在-未来）
    const renderThreeCards = () => (
        <div className="flex justify-center items-center gap-4 md:gap-8 py-6">
            {[0, 1, 2].map(i => renderCardWithPosition(i))}
        </div>
    )

    // 十字阵（5张）
    const renderCross = () => (
        <div className="relative py-8" style={{ minHeight: '380px' }}>
            <div className="flex flex-col items-center gap-2">
                {/* 顶部：意识 */}
                <div className="mb-2">
                    {renderCardWithPosition(2)}
                </div>
                {/* 中间行：过去-现状/障碍-未来 */}
                <div className="flex items-center gap-2 md:gap-4">
                    {renderCardWithPosition(3)}
                    <div className="relative">
                        {renderCardWithPosition(0)}
                        {/* 障碍牌（横置） */}
                        <motion.div 
                            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                            style={{ rotate: 90 }}
                        >
                            {cards[1] && (
                                <TarotCard
                                    cardCode={cards[1].cardCode}
                                    cardName={cards[1].cardName}
                                    imageUrl={cards[1].imageUrl}
                                    isRevealed={revealedIndices.includes(1)}
                                    isReversed={cards[1].isReversed}
                                    onReveal={() => onRevealCard(1)}
                                    delay={0.1}
                                    size="sm"
                                    enable3D={false}
                                />
                            )}
                        </motion.div>
                    </div>
                    {renderCardWithPosition(4)}
                </div>
                {/* 底部：潜意识 */}
                <div className="mt-2">
                    {renderCardWithPosition(3)}
                </div>
            </div>
        </div>
    )

    // 马蹄阵（7张）
    const renderHorseshoe = () => (
        <div className="py-6">
            {/* 顶部弧形排列 */}
            <div className="flex justify-center gap-2 md:gap-4 mb-4">
                {[5, 6].map(i => (
                    <motion.div 
                        key={i} 
                        initial={{ y: -10 }}
                        animate={{ y: 0 }}
                        transition={{ delay: i * 0.1 }}
                    >
                        {renderCardWithPosition(i)}
                    </motion.div>
                ))}
            </div>
            {/* 中间行 */}
            <div className="flex justify-center gap-3 md:gap-6 mb-4">
                {[3, 4].map(i => renderCardWithPosition(i))}
            </div>
            {/* 底部行 */}
            <div className="flex justify-center gap-2 md:gap-4">
                {[0, 1, 2].map(i => renderCardWithPosition(i))}
            </div>
        </div>
    )

    // 凯尔特十字阵（10张）
    const renderCelticCross = () => (
        <div className="py-6 px-2">
            <div className="flex flex-col lg:flex-row items-center justify-center gap-6">
                {/* 左侧：主十字 */}
                <div className="relative" style={{ width: '280px', height: '360px' }}>
                    {/* 基础（底部） */}
                    <div className="absolute bottom-0 left-1/2 -translate-x-1/2">
                        {renderCardWithPosition(2, 'sm')}
                    </div>
                    {/* 中心十字 */}
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
                        {renderCardWithPosition(0, 'sm')}
                        <motion.div 
                            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                            style={{ rotate: 90 }}
                        >
                            {cards[1] && (
                                <TarotCard
                                    cardCode={cards[1].cardCode}
                                    cardName={cards[1].cardName}
                                    imageUrl={cards[1].imageUrl}
                                    isRevealed={revealedIndices.includes(1)}
                                    isReversed={cards[1].isReversed}
                                    onReveal={() => onRevealCard(1)}
                                    delay={0.1}
                                    size="sm"
                                    enable3D={false}
                                />
                            )}
                        </motion.div>
                    </div>
                    {/* 过去（左） */}
                    <div className="absolute top-1/2 left-0 -translate-y-1/2">
                        {renderCardWithPosition(3, 'sm')}
                    </div>
                    {/* 可能（顶） */}
                    <div className="absolute top-0 left-1/2 -translate-x-1/2">
                        {renderCardWithPosition(4, 'sm')}
                    </div>
                    {/* 近期未来（右） */}
                    <div className="absolute top-1/2 right-0 -translate-y-1/2">
                        {renderCardWithPosition(5, 'sm')}
                    </div>
                </div>
                
                {/* 右侧：权杖（4张垂直排列） */}
                <div className="flex flex-col gap-2">
                    {[9, 8, 7, 6].map(i => (
                        <div key={i} className="relative">
                            {renderCardWithPosition(i, 'sm')}
                            <span className="absolute -left-4 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                                {10 - (9 - i)}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )

    // 渲染带位置标签的卡牌
    const renderCardWithPosition = (index: number, size?: 'sm' | 'md' | 'lg') => {
        const card = cards[index]
        if (!card) return null
        
        return (
            <div className="flex flex-col items-center gap-2">
                <TarotCard
                    cardCode={card.cardCode}
                    cardName={card.cardName}
                    imageUrl={card.imageUrl}
                    isRevealed={revealedIndices.includes(index)}
                    isReversed={card.isReversed}
                    onReveal={() => onRevealCard(index)}
                    delay={index * 0.15}
                    size={size || cardSize}
                />
                <motion.span 
                    className="text-xs text-muted-foreground text-center max-w-[80px] line-clamp-1"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                >
                    {card.position || positions[index]}
                </motion.span>
            </div>
        )
    }

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="w-full"
        >
            {renderSpread()}
        </motion.div>
    )
}

// 牌阵配置数据
const SPREADS: { type: SpreadType; name: string; nameEn: string; cards: number; icon: string }[] = [
    { type: 'single', name: '单牌', nameEn: 'Single', cards: 1, icon: '🎴' },
    { type: 'three-card', name: '三牌阵', nameEn: 'Three Card', cards: 3, icon: '🃏' },
    { type: 'cross', name: '十字阵', nameEn: 'Cross', cards: 5, icon: '✚' },
    { type: 'horseshoe', name: '马蹄阵', nameEn: 'Horseshoe', cards: 7, icon: '🔮' },
    { type: 'celtic-cross', name: '凯尔特十字', nameEn: 'Celtic Cross', cards: 10, icon: '⚜️' },
]

// 牌阵按钮组件（使用 memo 优化）
interface SpreadButtonProps {
    spread: typeof SPREADS[number]
    isSelected: boolean
    isEnglish: boolean
    onClick: (type: SpreadType) => void
}

const SpreadButton = memo(function SpreadButton({ 
    spread, 
    isSelected, 
    isEnglish, 
    onClick 
}: SpreadButtonProps) {
    const handleClick = useCallback(() => {
        onClick(spread.type)
    }, [spread.type, onClick])

    return (
        <motion.button
            onClick={handleClick}
            className={`
                px-3 py-2 rounded-lg text-sm font-medium transition-all
                flex items-center gap-2
                ${isSelected 
                    ? 'bg-primary text-primary-foreground shadow-lg' 
                    : 'bg-card border border-border hover:bg-accent hover:text-accent-foreground'
                }
            `}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
        >
            <span>{spread.icon}</span>
            <span>{isEnglish ? spread.nameEn : spread.name}</span>
            <span className="text-xs opacity-60">({spread.cards})</span>
        </motion.button>
    )
})

// 牌阵选择器组件
interface SpreadSelectorProps {
    value: SpreadType
    onChange: (type: SpreadType) => void
}

export function SpreadSelector({ value, onChange }: SpreadSelectorProps) {
    const { i18n } = useTranslation()
    const isEnglish = i18n.language === 'en'

    return (
        <div className="flex flex-wrap justify-center gap-2 md:gap-3">
            {SPREADS.map(spread => (
                <SpreadButton
                    key={spread.type}
                    spread={spread}
                    isSelected={value === spread.type}
                    isEnglish={isEnglish}
                    onClick={onChange}
                />
            ))}
        </div>
    )
}
