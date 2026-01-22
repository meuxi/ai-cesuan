/**
 * 铜钱翻转动画组件
 * 用于六爻摇卦等场景
 */
import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface CoinFlipProps {
  /** 是否正在翻转 */
  isFlipping: boolean
  /** 翻转结果：true=正面(阳)，false=反面(阴) */
  result?: boolean
  /** 翻转完成回调 */
  onComplete?: (result: boolean) => void
  /** 铜钱大小 */
  size?: number
  /** 翻转次数 */
  flipCount?: number
  /** 自定义类名 */
  className?: string
}

export function CoinFlip({
  isFlipping,
  result,
  onComplete,
  size = 60,
  flipCount = 5,
  className = ''
}: CoinFlipProps) {
  const [currentSide, setCurrentSide] = useState<boolean>(true)
  const [isAnimating, setIsAnimating] = useState(false)

  useEffect(() => {
    if (isFlipping && !isAnimating) {
      setIsAnimating(true)
      
      // 模拟翻转过程
      let count = 0
      const interval = setInterval(() => {
        setCurrentSide(prev => !prev)
        count++
        
        if (count >= flipCount * 2) {
          clearInterval(interval)
          // 设置最终结果
          if (result !== undefined) {
            setCurrentSide(result)
          }
          setIsAnimating(false)
          onComplete?.(result ?? Math.random() > 0.5)
        }
      }, 100)
      
      return () => clearInterval(interval)
    }
  }, [isFlipping, result, onComplete, flipCount, isAnimating])

  return (
    <motion.div
      className={`relative inline-flex items-center justify-center ${className}`}
      style={{ width: size, height: size }}
      animate={isAnimating ? {
        rotateY: [0, 180, 360],
        scale: [1, 1.1, 1],
      } : {}}
      transition={{
        duration: 0.2,
        repeat: isAnimating ? Infinity : 0,
        ease: "linear"
      }}
    >
      {/* 铜钱正面 - 阳 */}
      <AnimatePresence mode="wait">
        {currentSide ? (
          <motion.div
            key="yang"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            className="absolute inset-0 rounded-full flex items-center justify-center"
            style={{
              background: 'linear-gradient(145deg, #d4af37, #b8860b)',
              boxShadow: 'inset 0 2px 4px rgba(255,255,255,0.3), 0 4px 8px rgba(0,0,0,0.3)',
            }}
          >
            {/* 方孔 */}
            <div 
              className="bg-amber-900"
              style={{
                width: size * 0.2,
                height: size * 0.2,
              }}
            />
            <span className="absolute text-amber-900 font-bold text-xs">阳</span>
          </motion.div>
        ) : (
          <motion.div
            key="yin"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            className="absolute inset-0 rounded-full flex items-center justify-center"
            style={{
              background: 'linear-gradient(145deg, #8b7355, #6b5344)',
              boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.3), 0 4px 8px rgba(0,0,0,0.3)',
            }}
          >
            {/* 方孔 */}
            <div 
              className="bg-amber-950"
              style={{
                width: size * 0.2,
                height: size * 0.2,
              }}
            />
            <span className="absolute text-amber-200 font-bold text-xs">阴</span>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

/**
 * 三枚铜钱组合
 */
interface ThreeCoinsProps {
  isFlipping: boolean
  results?: boolean[]
  onComplete?: (results: boolean[]) => void
  className?: string
}

export function ThreeCoins({
  isFlipping,
  results,
  onComplete,
  className = ''
}: ThreeCoinsProps) {
  const [coinResults, setCoinResults] = useState<boolean[]>([true, true, true])
  const [completed, setCompleted] = useState(0)

  const handleCoinComplete = (index: number, result: boolean) => {
    setCoinResults(prev => {
      const next = [...prev]
      next[index] = result
      return next
    })
    setCompleted(prev => prev + 1)
  }

  useEffect(() => {
    if (completed === 3 && !isFlipping) {
      onComplete?.(coinResults)
      setCompleted(0)
    }
  }, [completed, isFlipping, coinResults, onComplete])

  return (
    <div className={`flex items-center justify-center gap-4 ${className}`}>
      {[0, 1, 2].map(index => (
        <CoinFlip
          key={index}
          isFlipping={isFlipping}
          result={results?.[index]}
          onComplete={(result) => handleCoinComplete(index, result)}
          flipCount={5 + index} // 错开翻转节奏
        />
      ))}
    </div>
  )
}
