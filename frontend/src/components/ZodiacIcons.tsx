import { FC } from 'react'

interface ZodiacIconProps {
  className?: string
  size?: number
}

// 白羊座 - 火红色渐变
export const AriesIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="aries-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#FF6B6B" />
        <stop offset="100%" stopColor="#EE5A5A" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#aries-grad)" opacity="0.15" />
    <path
      d="M20 44c0-12 6-20 12-20s12 8 12 20M32 24V14M20 24c-4 0-6-4-6-8s2-6 6-6 6 3 6 6M44 24c4 0 6-4 6-8s-2-6-6-6-6 3-6 6"
      fill="none"
      stroke="url(#aries-grad)"
      strokeWidth="3"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
)

// 金牛座 - 大地棕色渐变
export const TaurusIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="taurus-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#8B7355" />
        <stop offset="100%" stopColor="#A0826D" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#taurus-grad)" opacity="0.15" />
    <circle cx="32" cy="38" r="14" fill="none" stroke="url(#taurus-grad)" strokeWidth="3" />
    <path
      d="M18 22c0-6 4-10 8-10 3 0 5 2 6 5 1-3 3-5 6-5 4 0 8 4 8 10"
      fill="none"
      stroke="url(#taurus-grad)"
      strokeWidth="3"
      strokeLinecap="round"
    />
  </svg>
)

// 双子座 - 天蓝色渐变
export const GeminiIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="gemini-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#4ECDC4" />
        <stop offset="100%" stopColor="#44A08D" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#gemini-grad)" opacity="0.15" />
    <path
      d="M16 12h32M16 52h32M24 12v40M40 12v40"
      fill="none"
      stroke="url(#gemini-grad)"
      strokeWidth="3"
      strokeLinecap="round"
    />
  </svg>
)

// 巨蟹座 - 月光银蓝
export const CancerIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="cancer-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#667eea" />
        <stop offset="100%" stopColor="#764ba2" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#cancer-grad)" opacity="0.15" />
    <circle cx="22" cy="26" r="8" fill="none" stroke="url(#cancer-grad)" strokeWidth="3" />
    <circle cx="42" cy="38" r="8" fill="none" stroke="url(#cancer-grad)" strokeWidth="3" />
    <path
      d="M30 26c8 0 14-4 18-8M34 38c-8 0-14 4-18 8"
      fill="none"
      stroke="url(#cancer-grad)"
      strokeWidth="3"
      strokeLinecap="round"
    />
  </svg>
)

// 狮子座 - 金黄色渐变
export const LeoIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="leo-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#F7971E" />
        <stop offset="100%" stopColor="#FFD200" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#leo-grad)" opacity="0.15" />
    <circle cx="26" cy="24" r="10" fill="none" stroke="url(#leo-grad)" strokeWidth="3" />
    <path
      d="M36 24c0 12-4 20-4 26 0 4 6 6 10 2"
      fill="none"
      stroke="url(#leo-grad)"
      strokeWidth="3"
      strokeLinecap="round"
    />
  </svg>
)

// 处女座 - 淡紫色渐变
export const VirgoIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="virgo-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#a18cd1" />
        <stop offset="100%" stopColor="#fbc2eb" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#virgo-grad)" opacity="0.15" />
    <path
      d="M16 14v28c0 6 4 10 8 10M26 14v28c0 6 4 10 8 10M36 14v28M46 26c-4-8-10-12-10-12v24c0 6 6 10 12 6"
      fill="none"
      stroke="url(#virgo-grad)"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
)

// 天秤座 - 粉蓝渐变
export const LibraIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="libra-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#89f7fe" />
        <stop offset="100%" stopColor="#66a6ff" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#libra-grad)" opacity="0.15" />
    <path
      d="M12 48h40M12 36h40M32 36V18M20 18a12 12 0 0 1 24 0"
      fill="none"
      stroke="url(#libra-grad)"
      strokeWidth="3"
      strokeLinecap="round"
    />
  </svg>
)

// 天蝎座 - 深红渐变
export const ScorpioIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="scorpio-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#b91d73" />
        <stop offset="100%" stopColor="#f953c6" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#scorpio-grad)" opacity="0.15" />
    <path
      d="M14 14v24c0 8 5 12 10 12s10-4 10-12V14M34 14v24c0 8 5 12 10 12 3 0 6-2 6-2l4 6"
      fill="none"
      stroke="url(#scorpio-grad)"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
)

// 射手座 - 紫红渐变
export const SagittariusIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="sagittarius-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#8E2DE2" />
        <stop offset="100%" stopColor="#4A00E0" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#sagittarius-grad)" opacity="0.15" />
    <path
      d="M16 48L48 16M48 16H32M48 16v16M36 28L20 44"
      fill="none"
      stroke="url(#sagittarius-grad)"
      strokeWidth="3"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
)

// 摩羯座 - 深绿渐变
export const CapricornIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="capricorn-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#134E5E" />
        <stop offset="100%" stopColor="#71B280" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#capricorn-grad)" opacity="0.15" />
    <path
      d="M18 14v20c0 8 6 14 14 14h6c4 0 8-4 8-10s-4-10-10-10c-4 0-6 2-6 6s2 6 6 6"
      fill="none"
      stroke="url(#capricorn-grad)"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <circle cx="46" cy="48" r="6" fill="none" stroke="url(#capricorn-grad)" strokeWidth="2.5" />
  </svg>
)

// 水瓶座 - 天蓝渐变
export const AquariusIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="aquarius-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#00c6ff" />
        <stop offset="100%" stopColor="#0072ff" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#aquarius-grad)" opacity="0.15" />
    <path
      d="M10 24c4-4 8-4 12 0s8 4 12 0 8-4 12 0 8 4 8 0M10 40c4-4 8-4 12 0s8 4 12 0 8-4 12 0 8 4 8 0"
      fill="none"
      stroke="url(#aquarius-grad)"
      strokeWidth="3"
      strokeLinecap="round"
    />
  </svg>
)

// 双鱼座 - 海蓝渐变
export const PiscesIcon: FC<ZodiacIconProps> = ({ className = '', size = 32 }) => (
  <svg viewBox="0 0 64 64" width={size} height={size} className={className}>
    <defs>
      <linearGradient id="pisces-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#2193b0" />
        <stop offset="100%" stopColor="#6dd5ed" />
      </linearGradient>
    </defs>
    <circle cx="32" cy="32" r="30" fill="url(#pisces-grad)" opacity="0.15" />
    <path
      d="M12 32h40M20 14c-8 6-8 18 0 24M44 14c8 6 8 18 0 24"
      fill="none"
      stroke="url(#pisces-grad)"
      strokeWidth="3"
      strokeLinecap="round"
    />
  </svg>
)

// 星座图标映射
export const ZodiacIconMap: Record<string, FC<ZodiacIconProps>> = {
  '白羊座': AriesIcon,
  '金牛座': TaurusIcon,
  '双子座': GeminiIcon,
  '巨蟹座': CancerIcon,
  '狮子座': LeoIcon,
  '处女座': VirgoIcon,
  '天秤座': LibraIcon,
  '天蝎座': ScorpioIcon,
  '射手座': SagittariusIcon,
  '摩羯座': CapricornIcon,
  '水瓶座': AquariusIcon,
  '双鱼座': PiscesIcon,
}

// 通用星座图标组件
interface ZodiacIconComponentProps extends ZodiacIconProps {
  zodiac: string
}

export const ZodiacIcon: FC<ZodiacIconComponentProps> = ({ zodiac, ...props }) => {
  const IconComponent = ZodiacIconMap[zodiac]
  if (IconComponent) {
    return <IconComponent {...props} />
  }
  return null
}

export default ZodiacIcon
