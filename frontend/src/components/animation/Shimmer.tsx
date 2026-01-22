/**
 * 闪烁/骨架屏动画组件
 * 用于加载状态、占位符等场景
 */
import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface ShimmerProps {
  /** 宽度 */
  width?: string | number
  /** 高度 */
  height?: string | number
  /** 圆角 */
  borderRadius?: string | number
  /** 基础颜色 */
  baseColor?: string
  /** 高亮颜色 */
  highlightColor?: string
  /** 动画时长(秒) */
  duration?: number
  /** 自定义类名 */
  className?: string
}

export function Shimmer({
  width = '100%',
  height = 20,
  borderRadius = 4,
  baseColor = 'hsl(var(--muted))',
  highlightColor = 'hsl(var(--muted-foreground) / 0.1)',
  duration = 1.5,
  className = ''
}: ShimmerProps) {
  return (
    <div
      className={`relative overflow-hidden ${className}`}
      style={{
        width,
        height,
        borderRadius,
        backgroundColor: baseColor
      }}
    >
      <motion.div
        className="absolute inset-0"
        style={{
          background: `linear-gradient(90deg, transparent 0%, ${highlightColor} 50%, transparent 100%)`,
        }}
        animate={{
          x: ['-100%', '100%']
        }}
        transition={{
          duration,
          repeat: Infinity,
          ease: "linear"
        }}
      />
    </div>
  )
}

/**
 * 骨架屏组件
 */
interface SkeletonProps {
  /** 变体类型 */
  variant?: 'text' | 'circular' | 'rectangular'
  /** 宽度 */
  width?: string | number
  /** 高度 */
  height?: string | number
  /** 圆角 */
  borderRadius?: string | number
  /** 行数（仅 text 变体） */
  lines?: number
  /** 是否带动画 */
  animation?: boolean
  className?: string
}

export function Skeleton({
  variant = 'text',
  width,
  height,
  borderRadius,
  lines = 1,
  animation = true,
  className = ''
}: SkeletonProps) {
  const baseClass = 'bg-muted'

  if (variant === 'text') {
    return (
      <div className={`space-y-2 ${className}`} style={{ width }}>
        {Array.from({ length: lines }).map((_, i) => (
          <Shimmer
            key={i}
            width={i === lines - 1 && lines > 1 ? '80%' : '100%'}
            height={height || 16}
            borderRadius={4}
          />
        ))}
      </div>
    )
  }

  if (variant === 'circular') {
    const size = width || height || 40
    return (
      <Shimmer
        width={size}
        height={size}
        borderRadius="50%"
        className={className}
      />
    )
  }

  // rectangular
  return (
    <Shimmer
      width={width || '100%'}
      height={height || 100}
      borderRadius={borderRadius ?? 8}
      className={className}
    />
  )
}

/**
 * 预置骨架屏模板
 */

// 卡片骨架
export function CardSkeleton({ className = '' }: { className?: string }) {
  return (
    <div className={`p-4 rounded-lg border border-border ${className}`}>
      <Skeleton variant="rectangular" height={120} />
      <div className="mt-4 space-y-2">
        <Skeleton variant="text" width="70%" />
        <Skeleton variant="text" lines={2} />
      </div>
    </div>
  )
}

// 列表项骨架
export function ListItemSkeleton({ className = '' }: { className?: string }) {
  return (
    <div className={`flex items-center gap-3 p-3 ${className}`}>
      <Skeleton variant="circular" width={40} height={40} />
      <div className="flex-1">
        <Skeleton variant="text" width="60%" />
        <Skeleton variant="text" width="40%" height={12} />
      </div>
    </div>
  )
}

// 头像+文本骨架
export function AvatarTextSkeleton({ className = '' }: { className?: string }) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <Skeleton variant="circular" width={32} height={32} />
      <Skeleton variant="text" width={100} />
    </div>
  )
}

// 占卜结果骨架
export function DivinationResultSkeleton({ className = '' }: { className?: string }) {
  return (
    <div className={`space-y-4 ${className}`}>
      <div className="flex items-center justify-center">
        <Skeleton variant="rectangular" width={200} height={200} borderRadius={12} />
      </div>
      <div className="space-y-3">
        <Skeleton variant="text" width="40%" height={24} />
        <Skeleton variant="text" lines={4} />
      </div>
    </div>
  )
}

/**
 * 发光边框效果
 */
interface GlowBorderProps {
  children: ReactNode
  /** 是否激活 */
  active?: boolean
  /** 发光颜色 */
  color?: string
  /** 边框圆角 */
  borderRadius?: number
  className?: string
}

export function GlowBorder({
  children,
  active = true,
  color = 'rgba(139, 92, 246, 0.5)',
  borderRadius = 8,
  className = ''
}: GlowBorderProps) {
  return (
    <motion.div
      className={`relative ${className}`}
      animate={active ? {
        boxShadow: [
          `0 0 0 1px ${color}`,
          `0 0 20px 2px ${color}`,
          `0 0 0 1px ${color}`
        ]
      } : {}}
      transition={{
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }}
      style={{ borderRadius }}
    >
      {children}
    </motion.div>
  )
}
