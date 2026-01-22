/**
 * 六爻铜钱动画组件
 * 模拟三枚铜钱的抛掷动画
 */

import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { cn } from '@/lib/utils'

// 铜钱面值：0=背（阴面，一道线），1=字（阳面，两道线）
type CoinFace = 0 | 1

// 一次投掷结果：三个铜钱的正反面
type TossResult = [CoinFace, CoinFace, CoinFace]

// 爻的类型
type YaoType = 'laoyin' | 'shaoyang' | 'shaoyin' | 'laoyang'

interface CoinTossProps {
  /** 当前爻的索引（0-5） */
  yaoIndex: number
  /** 投掷完成回调 */
  onComplete: (result: TossResult, yaoType: YaoType) => void
  /** 是否自动投掷 */
  autoToss?: boolean
  /** 投掷延迟 */
  delay?: number
}

// 铜钱组件
function Coin({ 
  face, 
  index, 
  isSpinning,
  delay = 0 
}: { 
  face: CoinFace
  index: number
  isSpinning: boolean
  delay?: number
}) {
  return (
    <motion.div
      className="relative w-16 h-16 md:w-20 md:h-20"
      style={{ perspective: '500px' }}
      initial={{ y: -100, opacity: 0 }}
      animate={{ 
        y: isSpinning ? [0, -50, 0] : 0,
        opacity: 1,
        rotateY: isSpinning ? [0, 1080, 1800] : (face === 1 ? 0 : 180),
      }}
      transition={{
        y: { 
          duration: 1.5,
          times: [0, 0.5, 1],
          ease: "easeOut",
          delay: delay
        },
        rotateY: {
          duration: 1.5,
          ease: "easeOut",
          delay: delay
        },
        opacity: {
          duration: 0.3,
          delay: delay
        }
      }}
    >
      <div 
        className="w-full h-full"
        style={{ transformStyle: 'preserve-3d' }}
      >
        {/* 正面（字） - 阳 */}
        <div 
          className={cn(
            "absolute inset-0 rounded-full flex items-center justify-center",
            "bg-gradient-to-br from-amber-400 via-yellow-500 to-amber-600",
            "border-4 border-amber-700/50 shadow-lg"
          )}
          style={{ backfaceVisibility: 'hidden' }}
        >
          <div className="w-4 h-4 rounded-full bg-amber-900/30" />
          <div className="absolute inset-3 border-2 border-amber-700/30 rounded-full" />
          {/* 两道纹 - 阳 */}
          <div className="absolute bottom-2 left-1/2 -translate-x-1/2 flex flex-col gap-0.5">
            <div className="w-6 h-0.5 bg-amber-800/60 rounded" />
            <div className="w-6 h-0.5 bg-amber-800/60 rounded" />
          </div>
        </div>
        
        {/* 背面（背） - 阴 */}
        <div 
          className={cn(
            "absolute inset-0 rounded-full flex items-center justify-center",
            "bg-gradient-to-br from-amber-500 via-yellow-600 to-amber-700",
            "border-4 border-amber-800/50 shadow-lg"
          )}
          style={{ 
            backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)'
          }}
        >
          <div className="w-4 h-4 rounded-full bg-amber-900/40" />
          <div className="absolute inset-3 border-2 border-amber-800/30 rounded-full" />
          {/* 一道纹 - 阴 */}
          <div className="absolute bottom-2 left-1/2 -translate-x-1/2">
            <div className="w-6 h-0.5 bg-amber-900/60 rounded" />
          </div>
        </div>
      </div>
    </motion.div>
  )
}

// 计算爻的类型
function getYaoType(result: TossResult): YaoType {
  const sum = result.reduce((a, b) => a + b, 0)
  switch (sum) {
    case 0: return 'laoyin'    // 三背 - 老阴（变爻）
    case 1: return 'shaoyang'  // 一字二背 - 少阳
    case 2: return 'shaoyin'   // 二字一背 - 少阴
    case 3: return 'laoyang'   // 三字 - 老阳（变爻）
    default: return 'shaoyang'
  }
}

// 爻的显示名称
const YAO_NAMES: Record<YaoType, { zh: string; en: string; symbol: string }> = {
  'laoyin': { zh: '老阴', en: 'Old Yin', symbol: '⚋×' },
  'shaoyang': { zh: '少阳', en: 'Young Yang', symbol: '⚊' },
  'shaoyin': { zh: '少阴', en: 'Young Yin', symbol: '⚋' },
  'laoyang': { zh: '老阳', en: 'Old Yang', symbol: '⚊○' },
}

export function CoinToss({ yaoIndex, onComplete, autoToss = false, delay = 0 }: CoinTossProps) {
  const { i18n } = useTranslation()
  const [isSpinning, setIsSpinning] = useState(false)
  const [result, setResult] = useState<TossResult | null>(null)
  const [hasCompleted, setHasCompleted] = useState(false)

  // 投掷铜钱
  const toss = useCallback(() => {
    if (isSpinning || hasCompleted) return
    
    setIsSpinning(true)
    setResult(null)
    
    // 生成随机结果
    const newResult: TossResult = [
      Math.random() > 0.5 ? 1 : 0,
      Math.random() > 0.5 ? 1 : 0,
      Math.random() > 0.5 ? 1 : 0,
    ]
    
    // 动画结束后显示结果
    setTimeout(() => {
      setResult(newResult)
      setIsSpinning(false)
      setHasCompleted(true)
      
      const yaoType = getYaoType(newResult)
      onComplete(newResult, yaoType)
    }, 2000)
  }, [isSpinning, hasCompleted, onComplete])

  // 自动投掷
  useEffect(() => {
    if (autoToss && !hasCompleted) {
      const timer = setTimeout(toss, delay)
      return () => clearTimeout(timer)
    }
  }, [autoToss, delay, hasCompleted, toss])

  const yaoType = result ? getYaoType(result) : null
  const yaoInfo = yaoType ? YAO_NAMES[yaoType] : null
  const yaoLabel = yaoInfo ? (i18n.language === 'en' ? yaoInfo.en : yaoInfo.zh) : ''

  return (
    <div className="flex flex-col items-center gap-4">
      {/* 爻位标题 */}
      <div className="text-center">
        <span className="text-sm text-muted-foreground">
          {i18n.language === 'en' ? `Line ${yaoIndex + 1}` : `第${['初', '二', '三', '四', '五', '上'][yaoIndex]}爻`}
        </span>
      </div>
      
      {/* 铜钱 */}
      <div className="flex items-center justify-center gap-3">
        {[0, 1, 2].map((i) => (
          <Coin
            key={i}
            face={result ? result[i] : 1}
            index={i}
            isSpinning={isSpinning}
            delay={i * 0.1}
          />
        ))}
      </div>
      
      {/* 结果显示 */}
      <AnimatePresence>
        {result && yaoInfo && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="text-center"
          >
            <div className="flex items-center justify-center gap-2">
              <span className="text-2xl">{yaoInfo.symbol}</span>
              <span className={cn(
                "font-bold",
                yaoType === 'laoyang' || yaoType === 'shaoyang' 
                  ? 'text-amber-600 dark:text-amber-400' 
                  : 'text-slate-600 dark:text-slate-400'
              )}>
                {yaoLabel}
              </span>
              {(yaoType === 'laoyin' || yaoType === 'laoyang') && (
                <span className="text-xs px-1.5 py-0.5 bg-red-500/20 text-red-500 rounded">
                  {i18n.language === 'en' ? 'Changing' : '变爻'}
                </span>
              )}
            </div>
            <div className="text-xs text-muted-foreground mt-1">
              {result.map((f, i) => f === 1 ? '字' : '背').join(' ')}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* 投掷按钮 */}
      {!autoToss && !hasCompleted && (
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={toss}
          disabled={isSpinning}
          className={cn(
            "px-6 py-2 rounded-lg font-medium transition-all",
            "bg-gradient-to-r from-amber-500 to-yellow-500",
            "hover:from-amber-400 hover:to-yellow-400",
            "text-white shadow-lg",
            "disabled:opacity-50 disabled:cursor-not-allowed"
          )}
        >
          {isSpinning 
            ? (i18n.language === 'en' ? 'Tossing...' : '投掷中...') 
            : (i18n.language === 'en' ? 'Toss Coins' : '投掷铜钱')
          }
        </motion.button>
      )}
    </div>
  )
}

// 六爻完整投掷组件
interface SixCoinTossProps {
  onComplete: (results: Array<{ result: TossResult; yaoType: YaoType }>) => void
  autoToss?: boolean
}

export function SixCoinToss({ onComplete, autoToss = false }: SixCoinTossProps) {
  const { i18n } = useTranslation()
  const [currentYao, setCurrentYao] = useState(0)
  const [results, setResults] = useState<Array<{ result: TossResult; yaoType: YaoType }>>([])
  const [isComplete, setIsComplete] = useState(false)

  const handleYaoComplete = useCallback((result: TossResult, yaoType: YaoType) => {
    const newResults = [...results, { result, yaoType }]
    setResults(newResults)
    
    if (currentYao < 5) {
      setTimeout(() => setCurrentYao(prev => prev + 1), 500)
    } else {
      setIsComplete(true)
      onComplete(newResults)
    }
  }, [currentYao, results, onComplete])

  const handleReset = () => {
    setCurrentYao(0)
    setResults([])
    setIsComplete(false)
  }

  return (
    <div className="space-y-6">
      {/* 已完成的爻 */}
      <div className="flex flex-wrap justify-center gap-4">
        {results.map((r, i) => {
          const info = YAO_NAMES[r.yaoType]
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              className={cn(
                "px-4 py-2 rounded-lg text-center",
                r.yaoType === 'laoyang' || r.yaoType === 'shaoyang'
                  ? 'bg-amber-500/20 border border-amber-500/50'
                  : 'bg-slate-500/20 border border-slate-500/50'
              )}
            >
              <div className="text-lg">{info.symbol}</div>
              <div className="text-xs text-muted-foreground">
                {i18n.language === 'en' ? `Line ${i + 1}` : `第${['初', '二', '三', '四', '五', '上'][i]}爻`}
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* 当前投掷 */}
      {!isComplete && (
        <div className="p-6 rounded-xl bg-card/50 border border-border">
          <CoinToss
            key={currentYao}
            yaoIndex={currentYao}
            onComplete={handleYaoComplete}
            autoToss={autoToss}
            delay={300}
          />
        </div>
      )}

      {/* 完成状态 */}
      {isComplete && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center space-y-4"
        >
          <p className="text-lg font-medium text-foreground">
            {i18n.language === 'en' ? 'Hexagram Complete!' : '六爻齐备！'}
          </p>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleReset}
            className="px-6 py-2 rounded-lg bg-secondary text-secondary-foreground hover:bg-accent transition-colors"
          >
            {i18n.language === 'en' ? 'Start Over' : '重新起卦'}
          </motion.button>
        </motion.div>
      )}
    </div>
  )
}
