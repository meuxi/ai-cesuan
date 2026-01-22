/**
 * 卡片翻转揭示动画组件
 * 用于塔罗牌、抽签等场景
 */
import { useState } from 'react'
import { motion } from 'framer-motion'

interface CardRevealProps {
  /** 卡片正面内容 */
  front: React.ReactNode
  /** 卡片背面内容 */
  back: React.ReactNode
  /** 是否已翻转显示正面 */
  isRevealed: boolean
  /** 翻转完成回调 */
  onReveal?: () => void
  /** 点击是否可翻转 */
  clickable?: boolean
  /** 卡片宽度 */
  width?: number
  /** 卡片高度 */
  height?: number
  /** 自定义类名 */
  className?: string
  /** 翻转动画时长(秒) */
  duration?: number
}

export function CardReveal({
  front,
  back,
  isRevealed,
  onReveal,
  clickable = true,
  width = 150,
  height = 220,
  className = '',
  duration = 0.6
}: CardRevealProps) {
  const [isFlipped, setIsFlipped] = useState(isRevealed)

  const handleClick = () => {
    if (clickable && !isFlipped) {
      setIsFlipped(true)
      setTimeout(() => {
        onReveal?.()
      }, duration * 1000)
    }
  }

  // 同步外部状态
  if (isRevealed !== isFlipped) {
    setIsFlipped(isRevealed)
  }

  return (
    <div
      className={`relative cursor-pointer perspective-1000 ${className}`}
      style={{ width, height }}
      onClick={handleClick}
    >
      <motion.div
        className="absolute inset-0 w-full h-full"
        initial={false}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration, ease: "easeInOut" }}
        style={{ transformStyle: 'preserve-3d' }}
      >
        {/* 背面 */}
        <div
          className="absolute inset-0 w-full h-full rounded-lg overflow-hidden"
          style={{ 
            backfaceVisibility: 'hidden',
            transform: 'rotateY(0deg)'
          }}
        >
          {back}
        </div>
        
        {/* 正面 */}
        <div
          className="absolute inset-0 w-full h-full rounded-lg overflow-hidden"
          style={{ 
            backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)'
          }}
        >
          {front}
        </div>
      </motion.div>
    </div>
  )
}

/**
 * 默认卡片背面样式
 */
export function DefaultCardBack({ 
  pattern = 'mystical',
  className = '' 
}: { 
  pattern?: 'mystical' | 'simple' | 'gradient'
  className?: string 
}) {
  const patterns = {
    mystical: (
      <div className={`w-full h-full bg-gradient-to-br from-purple-900 via-indigo-900 to-purple-800 flex items-center justify-center ${className}`}>
        <div className="absolute inset-2 border-2 border-amber-500/30 rounded" />
        <div className="text-4xl opacity-50">☯</div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,rgba(0,0,0,0.3)_100%)]" />
      </div>
    ),
    simple: (
      <div className={`w-full h-full bg-gradient-to-b from-slate-700 to-slate-900 flex items-center justify-center ${className}`}>
        <div className="text-2xl text-slate-500">?</div>
      </div>
    ),
    gradient: (
      <div className={`w-full h-full bg-gradient-to-br from-rose-600 via-purple-600 to-blue-600 ${className}`}>
        <div className="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_10px,rgba(255,255,255,0.05)_10px,rgba(255,255,255,0.05)_20px)]" />
      </div>
    )
  }
  
  return patterns[pattern]
}

/**
 * 卡片组揭示动画（依次翻转）
 */
interface CardGroupRevealProps {
  cards: Array<{
    front: React.ReactNode
    back: React.ReactNode
    revealed?: boolean
  }>
  /** 每张卡片翻转的延迟(毫秒) */
  staggerDelay?: number
  /** 卡片宽度 */
  cardWidth?: number
  /** 卡片高度 */
  cardHeight?: number
  /** 卡片间距 */
  gap?: number
  /** 自动依次翻转 */
  autoReveal?: boolean
  className?: string
}

export function CardGroupReveal({
  cards,
  staggerDelay = 300,
  cardWidth = 120,
  cardHeight = 180,
  gap = 16,
  autoReveal = false,
  className = ''
}: CardGroupRevealProps) {
  const [revealedIndices, setRevealedIndices] = useState<Set<number>>(new Set())

  const handleReveal = (index: number) => {
    setRevealedIndices(prev => new Set(prev).add(index))
    
    // 自动触发下一张
    if (autoReveal && index < cards.length - 1) {
      setTimeout(() => {
        handleReveal(index + 1)
      }, staggerDelay)
    }
  }

  return (
    <div 
      className={`flex items-center justify-center flex-wrap ${className}`}
      style={{ gap }}
    >
      {cards.map((card, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1, duration: 0.3 }}
        >
          <CardReveal
            front={card.front}
            back={card.back}
            isRevealed={card.revealed || revealedIndices.has(index)}
            onReveal={() => handleReveal(index)}
            width={cardWidth}
            height={cardHeight}
          />
        </motion.div>
      ))}
    </div>
  )
}
