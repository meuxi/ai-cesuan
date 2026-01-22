/**
 * 淡入动画组件
 * 支持多种方向和时序
 */
import { motion, Variants } from 'framer-motion'
import { ReactNode } from 'react'

type Direction = 'up' | 'down' | 'left' | 'right' | 'none'

interface FadeInProps {
  children: ReactNode
  /** 动画方向 */
  direction?: Direction
  /** 延迟时间(秒) */
  delay?: number
  /** 动画时长(秒) */
  duration?: number
  /** 移动距离(px) */
  distance?: number
  /** 是否只在首次进入视口时动画 */
  once?: boolean
  /** 自定义类名 */
  className?: string
}

const getDirectionOffset = (direction: Direction, distance: number) => {
  switch (direction) {
    case 'up': return { y: distance }
    case 'down': return { y: -distance }
    case 'left': return { x: distance }
    case 'right': return { x: -distance }
    case 'none': return {}
  }
}

export function FadeIn({
  children,
  direction = 'up',
  delay = 0,
  duration = 0.5,
  distance = 20,
  once = true,
  className = ''
}: FadeInProps) {
  const variants: Variants = {
    hidden: {
      opacity: 0,
      ...getDirectionOffset(direction, distance)
    },
    visible: {
      opacity: 1,
      x: 0,
      y: 0,
      transition: {
        duration,
        delay,
        ease: [0.25, 0.1, 0.25, 1] // cubic-bezier
      }
    }
  }

  return (
    <motion.div
      className={className}
      initial="hidden"
      whileInView="visible"
      viewport={{ once, amount: 0.1 }}
      variants={variants}
    >
      {children}
    </motion.div>
  )
}

/**
 * 依次淡入的容器
 */
interface StaggerFadeInProps {
  children: ReactNode[]
  /** 每个子元素的延迟间隔(秒) */
  staggerDelay?: number
  /** 动画方向 */
  direction?: Direction
  /** 基础延迟时间(秒) */
  baseDelay?: number
  /** 动画时长(秒) */
  duration?: number
  /** 自定义类名 */
  className?: string
  /** 子元素类名 */
  itemClassName?: string
}

export function StaggerFadeIn({
  children,
  staggerDelay = 0.1,
  direction = 'up',
  baseDelay = 0,
  duration = 0.4,
  className = '',
  itemClassName = ''
}: StaggerFadeInProps) {
  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        delayChildren: baseDelay,
        staggerChildren: staggerDelay
      }
    }
  }

  const itemVariants: Variants = {
    hidden: {
      opacity: 0,
      ...getDirectionOffset(direction, 20)
    },
    visible: {
      opacity: 1,
      x: 0,
      y: 0,
      transition: { duration, ease: "easeOut" }
    }
  }

  return (
    <motion.div
      className={className}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.1 }}
      variants={containerVariants}
    >
      {children.map((child, index) => (
        <motion.div key={index} className={itemClassName} variants={itemVariants}>
          {child}
        </motion.div>
      ))}
    </motion.div>
  )
}

/**
 * 页面加载动画包装器
 */
export function PageTransition({ 
  children, 
  className = '' 
}: { 
  children: ReactNode
  className?: string 
}) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  )
}
