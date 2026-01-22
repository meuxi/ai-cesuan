/**
 * 脉冲/呼吸动画组件
 * 用于强调、加载指示等场景
 */
import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface PulseProps {
  children: ReactNode
  /** 是否激活动画 */
  active?: boolean
  /** 缩放范围 [最小, 最大] */
  scale?: [number, number]
  /** 透明度范围 [最小, 最大] */
  opacity?: [number, number]
  /** 动画周期(秒) */
  duration?: number
  /** 自定义类名 */
  className?: string
}

export function Pulse({
  children,
  active = true,
  scale = [1, 1.05],
  opacity = [1, 0.8],
  duration = 1.5,
  className = ''
}: PulseProps) {
  return (
    <motion.div
      className={className}
      animate={active ? {
        scale: [scale[0], scale[1], scale[0]],
        opacity: [opacity[0], opacity[1], opacity[0]]
      } : {}}
      transition={{
        duration,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    >
      {children}
    </motion.div>
  )
}

/**
 * 发光脉冲效果
 */
interface GlowPulseProps {
  /** 发光颜色 */
  color?: string
  /** 发光半径 */
  radius?: number
  /** 是否激活 */
  active?: boolean
  /** 尺寸 */
  size?: number
  className?: string
}

export function GlowPulse({
  color = 'rgba(139, 92, 246, 0.5)',
  radius = 20,
  active = true,
  size = 20,
  className = ''
}: GlowPulseProps) {
  return (
    <motion.div
      className={`rounded-full ${className}`}
      style={{
        width: size,
        height: size,
        backgroundColor: color,
      }}
      animate={active ? {
        boxShadow: [
          `0 0 0 0 ${color}`,
          `0 0 ${radius}px ${radius / 2}px ${color}`,
          `0 0 0 0 ${color}`
        ]
      } : {}}
      transition={{
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    />
  )
}

/**
 * 心跳动画
 */
interface HeartbeatProps {
  children: ReactNode
  /** 是否激活 */
  active?: boolean
  /** 动画强度 */
  intensity?: 'subtle' | 'normal' | 'strong'
  className?: string
}

export function Heartbeat({
  children,
  active = true,
  intensity = 'normal',
  className = ''
}: HeartbeatProps) {
  const scales = {
    subtle: [1, 1.02, 1],
    normal: [1, 1.05, 1],
    strong: [1, 1.1, 0.95, 1]
  }

  return (
    <motion.div
      className={className}
      animate={active ? { scale: scales[intensity] } : {}}
      transition={{
        duration: intensity === 'strong' ? 0.8 : 0.6,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    >
      {children}
    </motion.div>
  )
}

/**
 * 加载点动画
 */
export function LoadingDots({
  size = 8,
  gap = 4,
  color = 'currentColor',
  className = ''
}: {
  size?: number
  gap?: number
  color?: string
  className?: string
}) {
  return (
    <div className={`flex items-center ${className}`} style={{ gap }}>
      {[0, 1, 2].map(i => (
        <motion.div
          key={i}
          className="rounded-full"
          style={{
            width: size,
            height: size,
            backgroundColor: color
          }}
          animate={{
            y: [0, -size, 0],
            opacity: [0.5, 1, 0.5]
          }}
          transition={{
            duration: 0.6,
            repeat: Infinity,
            delay: i * 0.15,
            ease: "easeInOut"
          }}
        />
      ))}
    </div>
  )
}
