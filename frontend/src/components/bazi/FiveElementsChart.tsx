/**
 * 五行分析图表组件
 * 
 * 显示五行力量的可视化图表（柱状图+分析）
 */
import { useMemo } from 'react'
import { useTranslation } from 'react-i18next'

// 五行类型
type FiveElement = '木' | '火' | '土' | '金' | '水'

// 五行颜色映射
const ELEMENT_COLORS: Record<FiveElement, string> = {
  '木': '#22c55e',  // green-500
  '火': '#ef4444',  // red-500
  '土': '#eab308',  // yellow-500
  '金': '#f59e0b',  // amber-500 (金色)
  '水': '#3b82f6',  // blue-500
}

// 五行图标
const ELEMENT_ICONS: Record<FiveElement, string> = {
  '木': '🌳',
  '火': '🔥',
  '土': '⛰️',
  '金': '⚜️',
  '水': '💧',
}

// 五行顺序（相生顺序）
const ELEMENT_ORDER: FiveElement[] = ['木', '火', '土', '金', '水']

// 五行英文名称
const ELEMENT_NAMES: Record<FiveElement, string> = {
  '木': 'Wood',
  '火': 'Fire',
  '土': 'Earth',
  '金': 'Metal',
  '水': 'Water',
}

interface FiveElementsChartProps {
  elements: Record<FiveElement, number>
  showAnalysis?: boolean
  className?: string
}

export function FiveElementsChart({ 
  elements, 
  showAnalysis = true,
  className = ''
}: FiveElementsChartProps) {
  const { t, i18n } = useTranslation()
  const isEnglish = i18n.language === 'en'
  
  const maxValue = Math.max(...Object.values(elements), 1)
  const total = Object.values(elements).reduce((a, b) => a + b, 0)

  // 五行分析
  const analysis = useMemo(() => {
    const sorted = ELEMENT_ORDER
      .map(el => ({ element: el, count: elements[el] || 0 }))
      .sort((a, b) => b.count - a.count)

    const strongest = sorted.filter(s => s.count === sorted[0].count && s.count > 0)
    const weakest = sorted.filter(s => s.count === sorted[sorted.length - 1].count && s.count > 0)
    const missing = sorted.filter(s => s.count === 0)

    return { strongest, weakest, missing }
  }, [elements])

  const getElementName = (el: FiveElement) => {
    return isEnglish ? ELEMENT_NAMES[el] : el
  }

  return (
    <div className={`space-y-3 ${className}`}>
      {/* 柱状图 */}
      <div className="grid grid-cols-5 gap-2">
        {ELEMENT_ORDER.map((element) => {
          const value = elements[element] || 0
          const percentage = total > 0 ? Math.round((value / total) * 100) : 0
          const barHeight = maxValue > 0 ? (value / maxValue) * 100 : 0
          const color = ELEMENT_COLORS[element]

          return (
            <div key={element} className="text-center">
              {/* 柱状图 */}
              <div className="relative w-10 h-16 bg-muted rounded mx-auto mb-1 overflow-hidden">
                <div
                  className="absolute bottom-0 left-0 right-0 transition-all duration-500 rounded-t"
                  style={{ 
                    height: `${barHeight}%`, 
                    backgroundColor: color,
                    boxShadow: `0 0 8px ${color}40`
                  }}
                />
              </div>
              {/* 图标 */}
              <div className="text-lg leading-none">{ELEMENT_ICONS[element]}</div>
              {/* 名称徽章 */}
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold mx-auto mt-1 text-sm"
                style={{ backgroundColor: color }}
              >
                {isEnglish ? element : element}
              </div>
              {/* 数量和百分比 */}
              <div className="text-xs text-muted-foreground mt-1">
                {value}{isEnglish ? '' : '个'} ({percentage}%)
              </div>
            </div>
          )
        })}
      </div>

      {/* 五行分析 */}
      {showAnalysis && (
        <div className="text-xs space-y-1.5 pt-2 border-t border-border">
          {/* 最旺 */}
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-muted-foreground">
              {isEnglish ? 'Strongest:' : '五行最旺：'}
            </span>
            {analysis.strongest.map(s => (
              <span
                key={s.element}
                className="px-1.5 py-0.5 rounded text-white font-medium"
                style={{ backgroundColor: ELEMENT_COLORS[s.element] }}
              >
                {getElementName(s.element)}({s.count})
              </span>
            ))}
          </div>
          
          {/* 最弱 */}
          {analysis.weakest.length > 0 && analysis.weakest[0].count < analysis.strongest[0].count && (
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-muted-foreground">
                {isEnglish ? 'Weakest:' : '五行最弱：'}
              </span>
              {analysis.weakest.map(s => (
                <span
                  key={s.element}
                  className="px-1.5 py-0.5 rounded font-medium"
                  style={{ 
                    backgroundColor: `${ELEMENT_COLORS[s.element]}20`,
                    color: ELEMENT_COLORS[s.element]
                  }}
                >
                  {getElementName(s.element)}({s.count})
                </span>
              ))}
            </div>
          )}
          
          {/* 缺失 */}
          {analysis.missing.length > 0 && (
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-muted-foreground">
                {isEnglish ? 'Missing:' : '五行缺失：'}
              </span>
              {analysis.missing.map(s => (
                <span 
                  key={s.element} 
                  className="px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-500 font-medium"
                >
                  {isEnglish ? `No ${ELEMENT_NAMES[s.element]}` : `缺${s.element}`}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

/**
 * 圆环饼图版本
 */
interface FiveElementsPieProps {
  elements: Record<FiveElement, number>
  size?: number
  className?: string
}

export function FiveElementsPie({ 
  elements, 
  size = 120,
  className = ''
}: FiveElementsPieProps) {
  const total = Object.values(elements).reduce((a, b) => a + b, 0)
  if (total === 0) return null

  // 计算每个五行的角度
  let currentAngle = -90 // 从顶部开始
  const segments = ELEMENT_ORDER.map(element => {
    const value = elements[element] || 0
    const angle = (value / total) * 360
    const segment = {
      element,
      value,
      startAngle: currentAngle,
      endAngle: currentAngle + angle,
      color: ELEMENT_COLORS[element]
    }
    currentAngle += angle
    return segment
  }).filter(s => s.value > 0)

  // SVG路径计算
  const createArcPath = (startAngle: number, endAngle: number, radius: number, innerRadius: number) => {
    const startRad = (startAngle * Math.PI) / 180
    const endRad = (endAngle * Math.PI) / 180
    const cx = size / 2
    const cy = size / 2
    
    const x1 = cx + radius * Math.cos(startRad)
    const y1 = cy + radius * Math.sin(startRad)
    const x2 = cx + radius * Math.cos(endRad)
    const y2 = cy + radius * Math.sin(endRad)
    const x3 = cx + innerRadius * Math.cos(endRad)
    const y3 = cy + innerRadius * Math.sin(endRad)
    const x4 = cx + innerRadius * Math.cos(startRad)
    const y4 = cy + innerRadius * Math.sin(startRad)
    
    const largeArc = endAngle - startAngle > 180 ? 1 : 0
    
    return `M ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2} L ${x3} ${y3} A ${innerRadius} ${innerRadius} 0 ${largeArc} 0 ${x4} ${y4} Z`
  }

  const radius = size / 2 - 4
  const innerRadius = radius * 0.6

  return (
    <div className={`relative inline-block ${className}`}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {segments.map((segment, i) => (
          <path
            key={segment.element}
            d={createArcPath(segment.startAngle, segment.endAngle, radius, innerRadius)}
            fill={segment.color}
            className="transition-all duration-300 hover:opacity-80"
          >
            <title>{segment.element}: {segment.value}</title>
          </path>
        ))}
      </svg>
      {/* 中心文字 */}
      <div 
        className="absolute inset-0 flex items-center justify-center text-center"
        style={{ 
          top: innerRadius * 0.3, 
          left: innerRadius * 0.3,
          right: innerRadius * 0.3,
          bottom: innerRadius * 0.3
        }}
      >
        <div>
          <div className="text-xs text-muted-foreground">五行</div>
          <div className="text-lg font-bold">{total}</div>
        </div>
      </div>
    </div>
  )
}
