/**
 * 占卜问题输入组件
 * 统一的问题输入界面，支持多种交互模式
 */

import { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Sparkles, Lightbulb, RefreshCw } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useTranslation } from 'react-i18next'

interface QuestionInputProps {
  /** 占卜类型 */
  divinationType: string
  /** 提交回调 */
  onSubmit: (question: string) => void
  /** 是否加载中 */
  loading?: boolean
  /** 最大字符数 */
  maxLength?: number
  /** 占位符文本 */
  placeholder?: string
  /** 示例问题 */
  exampleQuestions?: string[]
  /** 是否显示示例 */
  showExamples?: boolean
  /** 自定义类名 */
  className?: string
}

// 各类型占卜的默认示例问题
const DEFAULT_EXAMPLES: Record<string, { zh: string[]; en: string[] }> = {
  tarot: {
    zh: ['我的爱情会有什么发展？', '我的事业前景如何？', '最近有什么需要注意的事情？'],
    en: ['What will happen in my love life?', 'How is my career outlook?', 'What should I pay attention to recently?']
  },
  liuyao: {
    zh: ['这件事情能否成功？', '出行是否顺利？', '这个决定是否正确？'],
    en: ['Will this matter succeed?', 'Will my trip go smoothly?', 'Is this decision correct?']
  },
  bazi: {
    zh: ['我的命运如何？', '今年运势怎么样？', '适合从事什么行业？'],
    en: ['What is my destiny?', 'How is my fortune this year?', 'What industry suits me?']
  },
  ziwei: {
    zh: ['我的事业运如何？', '我的婚姻状况怎样？', '今年有什么机遇？'],
    en: ['How is my career luck?', 'What is my marriage situation?', 'What opportunities await me this year?']
  },
  dream: {
    zh: ['梦到蛇代表什么？', '梦到飞翔是什么意思？', '梦到水有什么寓意？'],
    en: ['What does dreaming of snakes mean?', 'What does flying in dreams signify?', 'What is the meaning of water in dreams?']
  },
  default: {
    zh: ['请帮我解答这个问题', '我想知道未来会如何', '给我一些指引'],
    en: ['Please help me answer this question', 'I want to know what the future holds', 'Give me some guidance']
  }
}

export function QuestionInput({
  divinationType,
  onSubmit,
  loading = false,
  maxLength = 200,
  placeholder,
  exampleQuestions,
  showExamples = true,
  className
}: QuestionInputProps) {
  const { t, i18n } = useTranslation()
  const [question, setQuestion] = useState('')
  const [isFocused, setIsFocused] = useState(false)

  // 获取示例问题
  const examples = exampleQuestions || 
    (DEFAULT_EXAMPLES[divinationType] || DEFAULT_EXAMPLES.default)[i18n.language === 'en' ? 'en' : 'zh']

  // 默认占位符
  const defaultPlaceholder = i18n.language === 'en' 
    ? 'Please enter your question...' 
    : '请输入您的问题...'

  // 提交问题
  const handleSubmit = useCallback(() => {
    if (question.trim() && !loading) {
      onSubmit(question.trim())
    }
  }, [question, loading, onSubmit])

  // 使用示例问题
  const useExample = useCallback((example: string) => {
    setQuestion(example)
  }, [])

  // 随机示例
  const randomExample = useCallback(() => {
    const randomIndex = Math.floor(Math.random() * examples.length)
    setQuestion(examples[randomIndex])
  }, [examples])

  // 键盘提交
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className={cn('space-y-4', className)}>
      {/* 输入框区域 */}
      <div className={cn(
        'relative rounded-xl transition-all duration-300',
        'bg-card border',
        isFocused ? 'border-primary shadow-lg shadow-primary/10' : 'border-border'
      )}>
        {/* 顶部装饰 */}
        <div className="absolute -top-px left-1/2 -translate-x-1/2 w-24 h-1 bg-gradient-to-r from-transparent via-primary/50 to-transparent rounded-full" />
        
        {/* 文本输入 */}
        <div className="p-4">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value.slice(0, maxLength))}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder || defaultPlaceholder}
            disabled={loading}
            rows={3}
            className={cn(
              'w-full resize-none bg-transparent',
              'text-foreground placeholder:text-muted-foreground',
              'focus:outline-none',
              'disabled:opacity-50 disabled:cursor-not-allowed'
            )}
          />
        </div>
        
        {/* 底部工具栏 */}
        <div className="flex items-center justify-between px-4 py-2 border-t border-border bg-muted/30 rounded-b-xl">
          {/* 字数统计 */}
          <span className={cn(
            'text-xs',
            question.length > maxLength * 0.9 ? 'text-amber-500' : 'text-muted-foreground'
          )}>
            {question.length}/{maxLength}
          </span>
          
          {/* 按钮组 */}
          <div className="flex items-center gap-2">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={randomExample}
              disabled={loading}
              className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors disabled:opacity-50"
              title={i18n.language === 'en' ? 'Random Example' : '随机示例'}
            >
              <RefreshCw className="w-4 h-4" />
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleSubmit}
              disabled={!question.trim() || loading}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all',
                'bg-primary text-primary-foreground',
                'hover:bg-primary/90',
                'disabled:opacity-50 disabled:cursor-not-allowed'
              )}
            >
              {loading ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                  >
                    <Sparkles className="w-4 h-4" />
                  </motion.div>
                  <span>{i18n.language === 'en' ? 'Divining...' : '占卜中...'}</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>{i18n.language === 'en' ? 'Ask' : '提问'}</span>
                </>
              )}
            </motion.button>
          </div>
        </div>
      </div>

      {/* 示例问题 */}
      <AnimatePresence>
        {showExamples && !question && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-2"
          >
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Lightbulb className="w-4 h-4" />
              <span>{i18n.language === 'en' ? 'Example questions:' : '示例问题：'}</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {examples.map((example, i) => (
                <motion.button
                  key={i}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => useExample(example)}
                  className={cn(
                    'px-3 py-1.5 text-sm rounded-lg transition-colors',
                    'bg-secondary/50 text-secondary-foreground',
                    'hover:bg-secondary border border-transparent hover:border-border'
                  )}
                >
                  {example}
                </motion.button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
