import { useTranslation } from 'react-i18next'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { getDivinationOption } from '@/config/constants'
import { Sparkles, Eye, Loader2, Calendar } from 'lucide-react'
import * as LunarModule from 'lunar-javascript'
import { useState, useRef, useEffect } from 'react'
import { createPortal } from 'react-dom'
import './xiaoliu-ren.css'

// lunar-javascript 库的类型补充（库本身类型定义不完整）
interface LunarDate {
  getMonth(): number
  getDay(): number
}

const CONFIG = getDivinationOption('xiaoliu')!

// 小六壬基础数据
const sixGods = ['daan', 'liulian', 'suxi', 'chikou', 'xiaoji', 'kongwang']
const sixGodNames: Record<string, string> = {
  'daan': '大安',
  'liulian': '留连',
  'suxi': '速喜',
  'chikou': '赤口',
  'xiaoji': '小吉',
  'kongwang': '空亡'
}
const fiveElements = ['木', '木', '火', '金', '水', '土']

// 干支数据
const ganzhi: Record<string, string> = {
  'daan': '甲寅',
  'liulian': '乙卯',
  'suxi': '丙午',
  'chikou': '庚申',
  'xiaoji': '壬子',
  'kongwang': '戊己'
}

// 宫位到天干映射（参考站点）
const positionToGan: Record<string, string[]> = {
  'daan': ['甲', '乙'],
  'liulian': ['丙', '丁'],
  'suxi': ['戊', '己'],
  'chikou': ['庚', '辛'],
  'xiaoji': ['壬', '癸'],
  'kongwang': ['戊', '己']
}

// 农历月份名称
const lunarMonths = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月']

// 农历日期名称
const lunarDays = [
  '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
  '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
  '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'
]

// 时辰名称
const hourNames = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

// 时辰对照表
const hourTable = [
  { chinese: '子', range: '23:00-00:59', index: 1, earthlyBranch: '子', element: '水' },
  { chinese: '丑', range: '01:00-02:59', index: 2, earthlyBranch: '丑', element: '土' },
  { chinese: '寅', range: '03:00-04:59', index: 3, earthlyBranch: '寅', element: '木' },
  { chinese: '卯', range: '05:00-06:59', index: 4, earthlyBranch: '卯', element: '木' },
  { chinese: '辰', range: '07:00-08:59', index: 5, earthlyBranch: '辰', element: '土' },
  { chinese: '巳', range: '09:00-10:59', index: 6, earthlyBranch: '巳', element: '火' },
  { chinese: '午', range: '11:00-12:59', index: 7, earthlyBranch: '午', element: '火' },
  { chinese: '未', range: '13:00-14:59', index: 8, earthlyBranch: '未', element: '土' },
  { chinese: '申', range: '15:00-16:59', index: 9, earthlyBranch: '申', element: '金' },
  { chinese: '酉', range: '17:00-18:59', index: 10, earthlyBranch: '酉', element: '金' },
  { chinese: '戌', range: '19:00-20:59', index: 11, earthlyBranch: '戌', element: '土' },
  { chinese: '亥', range: '21:00-22:59', index: 12, earthlyBranch: '亥', element: '水' }
]

// 五星顺序
const fiveStars = ['木星', '火星', '土星', '金星', '水星', '天空']

// 卦象解读库（从源项目集成）
const interpretations: Record<string, { name: string; basic: string; combinations: Record<string, string> }> = {
  'daan': {
    name: '大安',
    basic: '大吉大利，百事顺遂。代表平安、顺利、吉祥。谋事可成，婚姻美满，出行平安，疾病不药而愈。',
    combinations: {
      'daan': '双重吉利，万事如意',
      'liulian': '先吉后阻，需耐心等待',
      'suxi': '速战速决，马到成功',
      'chikou': '吉中带凶，需谨慎行事',
      'xiaoji': '吉祥如意，小利可得',
      'kongwang': '吉处藏凶，事有阻碍'
    }
  },
  'liulian': {
    name: '留连',
    basic: '凶多吉少，办事迟缓。代表纠缠、拖延、阻碍。谋事难成，婚姻有阻，出行不利，疾病缠绵。',
    combinations: {
      'daan': '先阻后吉，终有好结果',
      'liulian': '双重阻碍，难以成功',
      'suxi': '虽有阻碍，终会成功',
      'chikou': '凶上加凶，灾祸临头',
      'xiaoji': '困境中有机遇',
      'kongwang': '完全受阻，宜守不宜进'
    }
  },
  'suxi': {
    name: '速喜',
    basic: '大吉之兆，百事顺遂。代表迅速、喜庆、成功。谋事速成，婚姻喜庆，出行顺利，疾病速愈。',
    combinations: {
      'daan': '大吉大利，万事如意',
      'liulian': '先吉后缓，不宜操之过急',
      'suxi': '双喜临门，运势亨通',
      'chikou': '先喜后忧，需防意外',
      'xiaoji': '喜庆连连，小利不断',
      'kongwang': '喜中有忧，事有变数'
    }
  },
  'chikou': {
    name: '赤口',
    basic: '大凶之兆，百事不利。代表口舌、是非、争斗。谋事不成，婚姻不顺，出行有灾，疾病加重。',
    combinations: {
      'daan': '凶中带吉，化险为夷',
      'liulian': '凶上加凶，大祸临头',
      'suxi': '先凶后吉，转危为安',
      'chikou': '双重凶险，灾难重重',
      'xiaoji': '凶中有机，小吉可求',
      'kongwang': '凶多吉少，宜守不宜进'
    }
  },
  'xiaoji': {
    name: '小吉',
    basic: '吉祥之兆，小利可得。代表小吉、顺利、进展。谋事小成，婚姻顺利，出行平安，疾病好转。',
    combinations: {
      'daan': '大吉小吉，万事如意',
      'liulian': '小有阻碍，终会成功',
      'suxi': '喜上加喜，运势亨通',
      'chikou': '小有不顺，需防口舌',
      'xiaoji': '双重小吉，步步顺利',
      'kongwang': '吉中带凶，事有变数'
    }
  },
  'kongwang': {
    name: '空亡',
    basic: '凶兆，百事无成。代表空虚、无望、失败。谋事不成，婚姻难成，出行不利，疾病难愈。',
    combinations: {
      'daan': '凶中带吉，终有转机',
      'liulian': '完全失败，不宜行动',
      'suxi': '先凶后吉，峰回路转',
      'chikou': '大凶之兆，灾祸临头',
      'xiaoji': '小吉化解，转危为安',
      'kongwang': '双重空亡，一事无成'
    }
  }
}

// 五行生克关系
const elementRelationships: Record<string, Record<string, string>> = {
  '木': { '生': '火', '克': '土', '被生': '水', '被克': '金' },
  '火': { '生': '土', '克': '金', '被生': '木', '被克': '水' },
  '土': { '生': '金', '克': '水', '被生': '火', '被克': '木' },
  '金': { '生': '水', '克': '木', '被生': '土', '被克': '火' },
  '水': { '生': '木', '克': '火', '被生': '金', '被克': '土' }
}



interface CalculatedResult {
  god: string
  godName: string
  element: string
  dayResult: number
  hourResult: number
  month: number
  day: number
  hour: number
  ganzhi: string
  gridData?: CellDetail[]
}

interface CellDetail {
  godName: string
  tianGan: string
  earthlyBranch: string
  branchElement: string
  liuqin: string
  fiveStar: string
  sixGodBeast: string
  validationInfo?: Record<string, any>
  god?: string
  ganzhi?: string
  isMonth?: boolean
  isDay?: boolean
  isFinal?: boolean
}

export default function XiaoLiuRenPage() {
  const { t } = useTranslation()
  const [prompt, setPrompt] = useLocalStorage('xiaoliu-prompt', '')
  const [method, setMethod] = useState<'date' | 'number'>('date')
  const [lastAIPrompt, setLastAIPrompt] = useState<string>('')
  const [showAlert, setShowAlert] = useState(false)
  const promptInputRef = useRef<HTMLTextAreaElement>(null)

  // 初始化时转换成农历月日 - 使用lunar-javascript库精确转换
  const solarToLunar = (solarDate: Date) => {
    const solar = LunarModule.Solar.fromYmdHms(
      solarDate.getFullYear(),
      solarDate.getMonth() + 1,
      solarDate.getDate(),
      solarDate.getHours(),
      solarDate.getMinutes(),
      solarDate.getSeconds()
    )
    const lunar = solar.getLunar()
    const year = solarDate.getFullYear()
    const month = (lunar as LunarDate).getMonth() // 农历月份 (1-12)
    const day = (lunar as LunarDate).getDay() // 农历日期 (1-30)

    return { year, month, day }
  }

  const getCurrentHourIndex = () => {
    const currentHour = new Date().getHours()
    if (currentHour >= 23 || currentHour < 1) return 1
    if (currentHour >= 1 && currentHour < 3) return 2
    if (currentHour >= 3 && currentHour < 5) return 3
    if (currentHour >= 5 && currentHour < 7) return 4
    if (currentHour >= 7 && currentHour < 9) return 5
    if (currentHour >= 9 && currentHour < 11) return 6
    if (currentHour >= 11 && currentHour < 13) return 7
    if (currentHour >= 13 && currentHour < 15) return 8
    if (currentHour >= 15 && currentHour < 17) return 9
    if (currentHour >= 17 && currentHour < 19) return 10
    if (currentHour >= 19 && currentHour < 21) return 11
    return 12
  }

  const now = new Date()
  const lunar = solarToLunar(now)
  const currentHourIdx = getCurrentHourIndex()

  const [month, setMonth] = useState(lunar.month)
  const [day, setDay] = useState(lunar.day)
  const [hour, setHour] = useState(currentHourIdx)
  const [calculatedResult, setCalculatedResult] = useState<CalculatedResult | null>(null)
  // refs to each palace cell DOM element (kept for future use)
  const cellRefs = useRef<Record<number, HTMLDivElement | null>>({})
  const [selectedCell, setSelectedCell] = useState<CellDetail | null>(null)

  // 神格映射（参考站保留）已内联于 cell validation 如需使用可重新启用

  // Previously we created portal-level time tags positioned on document.body.
  // That caused duplicates/conflicts with the in-card badges. Disable creation
  // and only ensure any existing portal tags are removed on update/unmount.
  useEffect(() => {
    const cleanup = () => {
      try {
        correctLayoutOrder.forEach((idx) => {
          const id = `portal-time-tag-${idx}`
          const t = document.getElementById(id)
          if (t) t.remove()
        })
      } catch (e) {
        // ignore
      }
    }
    // remove any leftover tags immediately
    cleanup()
    // also cleanup on unmount / dependency change
    return () => {
      cleanup()
    }
  }, [calculatedResult, month, day, hour])

  // 构建完整的六宫格数据（严格参考参考站 script.js 的逻辑）
  const buildGridData = (monthVal: number, dayVal: number, hourVal: number) => {
    const monthStart = 0
    const monthPosition = (monthStart + monthVal - 1) % 6
    const calcDayPosition = (monthStart + monthVal - 1 + dayVal - 1) % 6
    const calcHourPosition = (calcDayPosition + hourVal - 1) % 6

    const hourInfo = hourTable[hourVal - 1] || hourTable[0]
    const myEarthlyBranch = hourInfo.earthlyBranch
    const myElement = hourInfo.element

    const allEarthlyBranches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    const hourBranchIndex = allEarthlyBranches.indexOf(myEarthlyBranch)

    const gridData: CellDetail[] = []

    sixGods.forEach((god, index) => {
      // 月/日/时 标签
      const isMonth = index === monthPosition
      const isDay = index === calcDayPosition
      const isFinal = index === calcHourPosition

      // 计算地支（按参考：以时辰地支为基准，隔位排列）
      const positionDiff = (index - calcHourPosition + 6) % 6
      const branchOffset = positionDiff * 2
      const targetBranchIndex = (hourBranchIndex + branchOffset) % allEarthlyBranches.length
      const cellEarthlyBranch = allEarthlyBranches[targetBranchIndex]

      // 天干选择（positionToGan）按阴阳选择
      const gansForPosition = positionToGan[god] || ['甲', '乙']
      const isYangBranch = targetBranchIndex % 2 === 0
      const selectedGan = isYangBranch ? gansForPosition[0] : gansForPosition[1]
      const cellGanzhi = `${selectedGan}${cellEarthlyBranch}`

      // 六神兽计算
      const sixGodOrder = ['青龙', '朱雀', '勾陈', '白虎', '玄武', '螣蛇']
      let dragonStartPosition = 0
      switch (myEarthlyBranch) {
        case '子':
        case '午':
          dragonStartPosition = 0
          break
        case '丑':
        case '未':
          dragonStartPosition = 1
          break
        case '寅':
        case '申':
          dragonStartPosition = 2
          break
        case '卯':
        case '酉':
          dragonStartPosition = 3
          break
        case '辰':
        case '戌':
          dragonStartPosition = 4
          break
        case '巳':
        case '亥':
          dragonStartPosition = 5
          break
      }
      const sixOffset = (index - dragonStartPosition + 6) % 6
      const cellSixGod = sixGodOrder[sixOffset] || '未知'

      // 五星
      const fiveStarOffset = (index - calcDayPosition + 6) % 6
      const cellFiveStar = fiveStars[fiveStarOffset]

      // 地支五行
      const branchElement = hourTable.find(h => h.earthlyBranch === cellEarthlyBranch)?.element || fiveElements[index]

      // 六亲判断（生克逻辑）
      let cellLiuqin = ''
      if (index === calcHourPosition) {
        cellLiuqin = '自身'
      } else {
        if (elementRelationships[branchElement]['生'] === myElement) {
          cellLiuqin = '父母'
        } else if (elementRelationships[myElement]['生'] === branchElement) {
          cellLiuqin = '子孙'
        } else if (branchElement === myElement) {
          cellLiuqin = '兄弟'
        } else if (elementRelationships[myElement]['克'] === branchElement) {
          cellLiuqin = '妻财'
        } else if (elementRelationships[branchElement]['克'] === myElement) {
          cellLiuqin = '官鬼'
        }
      }

      const validationInfo = {
        position: index + 1,
        earthlyBranch: cellEarthlyBranch,
        element: branchElement,
        sixGod: cellSixGod,
        liuqin: cellLiuqin,
        fiveStar: cellFiveStar,
        isHourPosition: index === calcHourPosition,
        isDayPosition: index === calcDayPosition,
        isMonthPosition: index === monthPosition
      }

      const cellData: CellDetail = {
        god: god,
        godName: sixGodNames[god],
        tianGan: selectedGan,
        ganzhi: cellGanzhi,
        earthlyBranch: cellEarthlyBranch,
        branchElement,
        liuqin: cellLiuqin,
        fiveStar: cellFiveStar,
        sixGodBeast: cellSixGod,
        validationInfo,
        isMonth,
        isDay,
        isFinal
      }

      gridData.push(cellData)
    })

    return {
      gridData,
      monthPosition,
      calcDayPosition,
      calcHourPosition
    }
  }

  const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
    useDivination('xiaoliu')

  // 计算小六壬
  const calculateXiaoLiuRen = (): CalculatedResult => {
    const monthStart = 0
    const dayResult = (monthStart + month - 1 + day - 1) % 6
    const hourResult = (dayResult + hour - 1) % 6
    const finalResult = sixGods[hourResult]

    // build full grid data
    const { gridData } = buildGridData(month, day, hour)

    return {
      god: finalResult,
      godName: sixGodNames[finalResult],
      element: fiveElements[hourResult],
      dayResult,
      hourResult,
      month,
      day,
      hour,
      ganzhi: ganzhi[finalResult],
      gridData
    }
  }

  // 使用当前时间 - 获取当前公历时间转换成农历
  const useCurrentTime = () => {
    const now = new Date()
    const lunar = solarToLunar(now)  // 公历转农历
    const currentHourIdx = getCurrentHourIndex() // 获取当前时辰

    // 更新状态 - 自动更新上面的选择器（使用农历月日）
    setMonth(lunar.month)
    setDay(lunar.day)
    setHour(currentHourIdx)
    setMethod('date')
  }

  // 开始占卜（仅显示排盘结果）
  const handleSubmit = () => {
    if (!prompt || prompt.trim() === '') {
      promptInputRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' })
      promptInputRef.current?.focus()
      setTimeout(() => setShowAlert(true), 300)
      return
    }
    const xiaoliuResult = calculateXiaoLiuRen()
    setCalculatedResult(xiaoliuResult)
  }

  // AI解读（单独调用）
  const handleAIInterpret = () => {
    if (!calculatedResult) return
    const fullPrompt = `${prompt || '运势'}\n\n起卦：月${calculatedResult.month}日${calculatedResult.day}时${calculatedResult.hour}\n落宫：${calculatedResult.godName}\n五行：${calculatedResult.element}\n干支：${calculatedResult.ganzhi}`
    if (fullPrompt === lastAIPrompt && result) {
      setShowDrawer(true)
      return
    }
    setLastAIPrompt(fullPrompt)
    onSubmit({ prompt: fullPrompt })
    setShowDrawer(true)
  }

  // 六宫格布局顺序：留连、速喜、赤口 / 大安、空亡、小吉
  const correctLayoutOrder = [1, 2, 3, 0, 5, 4]

  return (
    <DivinationCardHeader
      title={t('xiaoliu.title')}
      description={t('xiaoliu.description')}
      icon={CONFIG.icon}
      divinationType="xiaoliu"
    >
      <div className="w-full max-w-5xl mx-auto space-y-8">
        {/* 问题输入 */}
        <div>
          <label className="text-sm font-medium mb-2 block text-foreground">
            {t('xiaoliu.questionLabel')}
          </label>
          <textarea
            ref={promptInputRef}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder={t('xiaoliu.questionPlaceholder')}
            maxLength={40}
            rows={3}
            className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground resize-none focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          />
          <p className="text-xs text-muted-foreground mt-2">
            {t('xiaoliu.questionTip')}
          </p>
        </div>

        {/* 起卦方式切换 */}
        <div className="flex justify-center gap-4">
          <button
            onClick={() => setMethod('date')}
            className={`px-6 py-3 text-sm font-medium transition-colors rounded-md ${method === 'date' ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
              }`}
          >
            时间起卦
          </button>
          <button
            onClick={() => setMethod('number')}
            className={`px-6 py-3 text-sm font-medium transition-colors rounded-md ${method === 'number' ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
              }`}
          >
            数字起卦
          </button>
        </div>

        {/* 输入区域 */}
        <div className="bg-card rounded-xl p-4 sm:p-6 border border-border">

          {method === 'date' ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2 text-foreground">
                    {t('xiaoliu.lunarMonth')}
                  </label>
                  <select
                    title={t('xiaoliu.lunarMonthLabel')}
                    aria-label={t('xiaoliu.lunarMonthLabel')}
                    value={month}
                    onChange={(e) => setMonth(parseInt(e.target.value))}
                    className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                  >
                    {lunarMonths.map((name, index) => (
                      <option key={index + 1} value={index + 1}>{name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-foreground">
                    {t('xiaoliu.lunarDay')}
                  </label>
                  <select
                    title={t('xiaoliu.lunarDayLabel')}
                    aria-label={t('xiaoliu.lunarDayLabel')}
                    value={day}
                    onChange={(e) => setDay(parseInt(e.target.value))}
                    className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                  >
                    {lunarDays.map((name, index) => (
                      <option key={index + 1} value={index + 1}>{name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-foreground">
                    {t('xiaoliu.hour')}
                  </label>
                  <select
                    title={t('xiaoliu.hourLabel')}
                    aria-label={t('xiaoliu.hourLabel')}
                    value={hour}
                    onChange={(e) => setHour(parseInt(e.target.value))}
                    className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                  >
                    {hourTable.map(h => (
                      <option key={h.index} value={h.index}>{h.chinese}时</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2 text-foreground">
                    {t('xiaoliu.monthNumber')}
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="12"
                    value={month}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setMonth(Math.min(12, Math.max(1, parseInt(e.target.value) || 1)))}
                    className="w-full px-3 py-2 text-sm text-center border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-foreground">
                    {t('xiaoliu.dayNumber')}
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="31"
                    value={day}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setDay(Math.min(31, Math.max(1, parseInt(e.target.value) || 1)))}
                    className="w-full px-3 py-2 text-sm text-center border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-foreground">
                    {t('xiaoliu.hourNumber')}
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="12"
                    value={hour}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setHour(Math.min(12, Math.max(1, parseInt(e.target.value) || 1)))}
                    className="w-full px-3 py-2 text-sm text-center border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                  />
                </div>
              </div>
            </div>
          )}

          {/* 按钮组 */}
          <div className="flex flex-col sm:flex-row gap-4 mt-6">
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="flex-1 inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium rounded-md bg-primary text-primary-foreground hover:bg-primary/90 transition-colors disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  {t('xiaoliu.divinating')}
                </>
              ) : (
                <>
                  <Sparkles className="h-4 w-4 mr-2" />
                  {t('xiaoliu.startDivination')}
                </>
              )}
            </button>
            {method === 'date' && (
              <button
                onClick={useCurrentTime}
                className="inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium rounded-md border border-input bg-background text-foreground hover:bg-secondary transition-colors"
                title={t('xiaoliu.useCurrentTime')}
              >
                <Calendar className="h-4 w-4 mr-2" />
                {t('xiaoliu.getCurrentTime')}
              </button>
            )}
          </div>
        </div>

        {/* 排盘结果 - 完整照抄目标网站 */}
        {calculatedResult && (
          <div className="space-y-4 sm:space-y-6">
            <div className="bg-card rounded-2xl p-4 sm:p-8 shadow-lg border border-border">
              <h3 className="text-xl sm:text-2xl font-bold mb-4 sm:mb-6 text-center text-foreground">
                {t('xiaoliu.paiPanResult')}
              </h3>

              {/* 六宫格 - 完全按照目标网站结构，保持3列布局 */}
              <div className="flex justify-center overflow-visible p-2 sm:p-5 w-full">
                <div
                  className="grid grid-cols-3 gap-1 sm:gap-3 border-[2px] sm:border-[3px] border-border rounded-lg sm:rounded-2xl shadow-2xl bg-card overflow-visible w-full max-w-[560px]"
                >
                  {correctLayoutOrder.map((index) => {
                    // Prefer authoritative gridData from calculation; fall back to building on the fly
                    const gridDataSource = calculatedResult?.gridData || (buildGridData(calculatedResult?.month || month, calculatedResult?.day || day, calculatedResult?.hour || hour).gridData)
                    const cell = gridDataSource?.[index]
                    const godName = cell?.godName || sixGodNames[sixGods[index]]
                    // Show only the TianGan (first character) in the center to match reference site
                    const ganzhiDisplay = cell?.tianGan || (cell?.ganzhi ? cell.ganzhi.charAt(0) : '')
                    const cellEarthlyBranch = cell?.earthlyBranch || ''
                    const branchElement = cell?.branchElement || fiveElements[index]
                    const liuqin = cell?.liuqin || ''
                    const sixGodBeast = cell?.sixGodBeast || ''
                    const fiveStar = cell?.fiveStar || ''
                    const isFinal = cell?.validationInfo?.isHourPosition || false
                    const isDay = cell?.validationInfo?.isDayPosition || false
                    const isMonth = cell?.validationInfo?.isMonthPosition || false
                    const tagLabels: string[] = []
                    if (isMonth) tagLabels.push('月')
                    if (isDay) tagLabels.push('日')
                    if (isFinal) tagLabels.push('时')

                    return (
                      <div
                        key={index}
                        ref={(el) => { cellRefs.current[index] = el }}
                        role="button"
                        tabIndex={0}
                        onClick={() => setSelectedCell(cell)}
                        data-month={isMonth ? '1' : ''}
                        data-day={isDay ? '1' : ''}
                        data-final={isFinal ? '1' : ''}
                        className={`relative transition-all hover:bg-muted/50 cursor-pointer ${isFinal ? 'bg-yellow-50 dark:bg-yellow-900/20 border-2 border-yellow-400 dark:border-yellow-500' : 'bg-card border border-border'} xiaoliu-card`}
                      >
                        {/* In-cell time badge: render month/day/hour tags inside the card's top-right corner.
                            Uses clamp() for responsive sizing so badge scales across viewports. */}
                        {tagLabels.length > 0 && (
                          <div className="xiaoliu-badge-container">
                            <div className={`xiaoliu-badge ${tagLabels.join('').length > 1 ? 'small' : ''}`}>{tagLabels.join('')}</div>
                          </div>
                        )}

                        {/* 点击显示详细信息：已绑定到宫格根节点（整个格子可点） */}

                        {/* 五行颜色条 - 底部 */}
                        <div
                          className={`xiaoliu-bottom-bar ${branchElement === '木' ? 'el-mu' :
                            branchElement === '火' ? 'el-huo' :
                              branchElement === '土' ? 'el-tu' :
                                branchElement === '金' ? 'el-jin' :
                                  branchElement === '水' ? 'el-shui' : 'el-default'
                            }`}
                        />

                        {/* 宫格内容 */}
                        <div className="xiaoliu-inner">
                          {/* 上部：六神名 + 六亲 */}
                          <div className="xiaoliu-top">
                            <div className={`xiaoliu-godname ${isFinal ? 'final' : ''}`}>
                              {godName}
                              {isFinal && <span className="xiaoliu-dot">●</span>}
                            </div>
                            <div className={`xiaoliu-liuqin ${isFinal ? 'final' : ''}`}>
                              {liuqin}
                            </div>
                          </div>

                          {/* 中部：天干、地支、五星、六神兽 */}
                          <div className="xiaoliu-mid">
                            <div className="xiaoliu-tianGan">
                              {ganzhiDisplay}
                            </div>

                            <div className="xiaoliu-branch">
                              <span className="branchName">{cellEarthlyBranch}</span>
                              <span className="branchElement">({branchElement})</span>
                            </div>

                            <div className="xiaoliu-fiveSix">
                              <span className="xiaoliu-fiveStar">{fiveStar}</span>
                              <span className="xiaoliu-sixGodBeast">{sixGodBeast}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>

              {/* 卦象解读 */}
              <div className="mt-6 sm:mt-8 p-4 sm:p-6 bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 rounded-xl border border-amber-200 dark:border-amber-700">
                <h4 className="font-bold text-foreground mb-4 text-base sm:text-lg flex items-center gap-2">
                  <span className="text-xl">📖</span> {t('xiaoliu.guaInterpret')}
                </h4>
                <div className="mb-4 p-4 bg-card rounded-lg shadow-sm">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`text-2xl font-bold ${calculatedResult.god === 'daan' || calculatedResult.god === 'suxi' || calculatedResult.god === 'xiaoji' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                      {calculatedResult.godName}
                    </span>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${calculatedResult.god === 'daan' || calculatedResult.god === 'suxi' ? 'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-300' : calculatedResult.god === 'xiaoji' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300' : 'bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-300'}`}>
                      {calculatedResult.god === 'daan' || calculatedResult.god === 'suxi' ? '大吉' : calculatedResult.god === 'xiaoji' ? '小吉' : '凶'}
                    </span>
                  </div>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    {interpretations[calculatedResult.god]?.basic}
                  </p>
                </div>
                <div className="p-4 bg-card rounded-lg shadow-sm">
                  <h5 className="font-medium text-foreground mb-3 text-sm">六神组合参考</h5>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                    {Object.entries(interpretations[calculatedResult.god]?.combinations || {}).map(([key, value]) => (
                      <div key={key} className={`p-2 rounded-lg text-xs ${key === calculatedResult.god ? 'bg-amber-100 dark:bg-amber-900/30 border border-amber-300 dark:border-amber-600' : 'bg-muted/50'}`}>
                        <span className="font-medium text-foreground">{calculatedResult.godName}+{sixGodNames[key]}：</span>
                        <span className="text-muted-foreground">{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* 起课步骤 - 完整8步 */}
              <div className="mt-6 sm:mt-8 p-4 sm:p-6 bg-muted/30 rounded-xl border border-border">
                <h4 className="font-bold text-foreground mb-4 text-base sm:text-lg">起课步骤</h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                  <div className="p-3 bg-card rounded-lg shadow-sm border-l-4 border-blue-400">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-5 h-5 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center font-bold shrink-0">1</span>
                      <span className="font-bold text-blue-600 dark:text-blue-400 text-xs">确定起卦方式</span>
                    </div>
                    <p className="text-muted-foreground text-xs">{method === 'date' ? '时间起卦' : '数字起卦'}</p>
                  </div>
                  <div className="p-3 bg-card rounded-lg shadow-sm border-l-4 border-cyan-400">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-5 h-5 rounded-full bg-cyan-500 text-white text-xs flex items-center justify-center font-bold shrink-0">2</span>
                      <span className="font-bold text-cyan-600 dark:text-cyan-400 text-xs">确定月日时参数</span>
                    </div>
                    <p className="text-muted-foreground text-xs">月={calculatedResult.month}, 日={calculatedResult.day}, 时={calculatedResult.hour}</p>
                  </div>
                  <div className="p-3 bg-card rounded-lg shadow-sm border-l-4 border-teal-400">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-5 h-5 rounded-full bg-teal-500 text-white text-xs flex items-center justify-center font-bold shrink-0">3</span>
                      <span className="font-bold text-teal-600 dark:text-teal-400 text-xs">月上起日计算</span>
                    </div>
                    <p className="text-muted-foreground text-xs">(0+{calculatedResult.month}-1+{calculatedResult.day}-1)%6={calculatedResult.dayResult}</p>
                  </div>
                  <div className="p-3 bg-card rounded-lg shadow-sm border-l-4 border-green-400">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-5 h-5 rounded-full bg-green-500 text-white text-xs flex items-center justify-center font-bold shrink-0">4</span>
                      <span className="font-bold text-green-600 dark:text-green-400 text-xs">确定日落地支</span>
                    </div>
                    <p className="text-muted-foreground text-xs">日落宫位 → <span className="font-medium text-foreground">{sixGodNames[sixGods[calculatedResult.dayResult]]}</span></p>
                  </div>
                  <div className="p-3 bg-card rounded-lg shadow-sm border-l-4 border-lime-400">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-5 h-5 rounded-full bg-lime-500 text-white text-xs flex items-center justify-center font-bold shrink-0">5</span>
                      <span className="font-bold text-lime-600 dark:text-lime-400 text-xs">日上起时计算</span>
                    </div>
                    <p className="text-muted-foreground text-xs">({calculatedResult.dayResult}+{calculatedResult.hour}-1)%6={calculatedResult.hourResult}</p>
                  </div>
                  <div className="p-3 bg-card rounded-lg shadow-sm border-l-4 border-amber-400">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-5 h-5 rounded-full bg-amber-500 text-white text-xs flex items-center justify-center font-bold shrink-0">6</span>
                      <span className="font-bold text-amber-600 dark:text-amber-400 text-xs">确定最终落宫</span>
                    </div>
                    <p className="text-muted-foreground text-xs">最终结果 → <span className="font-medium text-foreground">{calculatedResult.godName}</span></p>
                  </div>
                  <div className="p-3 bg-card rounded-lg shadow-sm border-l-4 border-orange-400">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-5 h-5 rounded-full bg-orange-500 text-white text-xs flex items-center justify-center font-bold shrink-0">7</span>
                      <span className="font-bold text-orange-600 dark:text-orange-400 text-xs">确定五行属性</span>
                    </div>
                    <p className="text-muted-foreground text-xs">五行属性 → <span className={`font-medium ${calculatedResult.element === '木' ? 'text-green-600' : calculatedResult.element === '火' ? 'text-red-600' : calculatedResult.element === '土' ? 'text-yellow-600' : calculatedResult.element === '金' ? 'text-gold-600' : 'text-blue-600'}`}>{calculatedResult.element}</span></p>
                  </div>
                  <div className="p-3 bg-card rounded-lg shadow-sm border-l-4 border-purple-400">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-5 h-5 rounded-full bg-purple-500 text-white text-xs flex items-center justify-center font-bold shrink-0">8</span>
                      <span className="font-bold text-purple-600 dark:text-purple-400 text-xs">确定干支属性</span>
                    </div>
                    <p className="text-muted-foreground text-xs">干支属性 → <span className="font-medium text-foreground">{calculatedResult.ganzhi}</span></p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 详细信息弹窗 - 使用Portal渲染到body确保始终居中 */}
        {selectedCell && createPortal(
          <div
            className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/60 backdrop-blur-sm"
            role="dialog"
            aria-modal="true"
            onClick={() => setSelectedCell(null)}
          >
            <div
              className="relative w-full max-w-[900px] mx-4 max-h-[85vh] overflow-y-auto bg-card rounded-2xl shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="sticky top-0 z-10 flex justify-end p-4 bg-gradient-to-b from-card via-card to-transparent">
                <button
                  className="w-10 h-10 rounded-full bg-muted hover:bg-muted/80 flex items-center justify-center text-muted-foreground text-xl font-bold transition-all hover:rotate-90"
                  onClick={() => setSelectedCell(null)}
                >
                  ×
                </button>
              </div>
              <div className="px-6 pb-6 -mt-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-200 dark:border-blue-800">
                    <h4 className="font-bold text-blue-700 dark:text-blue-300 mb-3 text-center border-b border-blue-200 dark:border-blue-700 pb-2">基本信息</h4>
                    <div className="space-y-2 text-sm">
                      <p className="flex justify-between py-2 border-b border-blue-100 dark:border-blue-800/50">
                        <strong className="text-muted-foreground">宫位</strong>
                        <span className="font-medium text-foreground">
                          {selectedCell.godName}
                          {selectedCell.validationInfo?.position ? ` (第${selectedCell.validationInfo.position}位)` : ''}
                        </span>
                      </p>
                      <p className="flex justify-between py-2 border-b border-blue-100 dark:border-blue-800/50">
                        <strong className="text-muted-foreground">干支</strong>
                        <span className="font-medium text-foreground">{selectedCell.ganzhi}</span>
                      </p>
                      <p className="flex justify-between py-2 border-b border-blue-100 dark:border-blue-800/50">
                        <strong className="text-muted-foreground">地支</strong>
                        <span className="font-medium text-foreground">{selectedCell.earthlyBranch}</span>
                      </p>
                      <p className="flex justify-between py-2 border-b border-blue-100 dark:border-blue-800/50">
                        <strong className="text-muted-foreground">五行属性</strong>
                        <span className="font-medium text-foreground">{selectedCell.branchElement}</span>
                      </p>
                      <p className="flex justify-between py-2 border-b border-blue-100 dark:border-blue-800/50">
                        <strong className="text-muted-foreground">六神</strong>
                        <span className="font-medium text-foreground">{selectedCell.sixGodBeast}</span>
                      </p>
                      <p className="flex justify-between py-2 border-b border-blue-100 dark:border-blue-800/50">
                        <strong className="text-muted-foreground">六亲</strong>
                        <span className="font-medium text-foreground">{selectedCell.liuqin}</span>
                      </p>
                      <p className="flex justify-between py-2">
                        <strong className="text-muted-foreground">五星</strong>
                        <span className="font-medium text-foreground">{selectedCell.fiveStar}</span>
                      </p>
                    </div>
                  </div>
                  <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-xl border border-purple-200 dark:border-purple-800">
                    <h4 className="font-bold text-purple-700 dark:text-purple-300 mb-3 text-center border-b border-purple-200 dark:border-purple-700 pb-2">校准验证信息</h4>
                    <div className="space-y-2 text-sm">
                      <p className="flex justify-between py-2 border-b border-purple-100 dark:border-purple-800/50">
                        <strong className="text-muted-foreground">时辰落宫</strong>
                        <span className={`font-medium ${selectedCell.validationInfo?.isHourPosition ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}>
                          {selectedCell.validationInfo?.isHourPosition ? '是' : '否'}
                        </span>
                      </p>
                      <p className="flex justify-between py-2 border-b border-purple-100 dark:border-purple-800/50">
                        <strong className="text-muted-foreground">日落宫位</strong>
                        <span className={`font-medium ${selectedCell.validationInfo?.isDayPosition ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}>
                          {selectedCell.validationInfo?.isDayPosition ? '是' : '否'}
                        </span>
                      </p>
                      <p className="flex justify-between py-2">
                        <strong className="text-muted-foreground">月落宫位</strong>
                        <span className={`font-medium ${selectedCell.validationInfo?.isMonthPosition ? 'text-green-600 dark:text-green-400' : 'text-muted-foreground'}`}>
                          {selectedCell.validationInfo?.isMonthPosition ? '是' : '否'}
                        </span>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>,
          document.body
        )}

        {/* 时辰对照表 */}
        <div className="bg-card rounded-2xl p-4 sm:p-8 shadow-lg border border-border">
          <h3 className="text-lg sm:text-xl font-bold mb-4 sm:mb-6 text-center text-foreground">
            时辰对照表
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2 sm:gap-4">
            {hourTable.map(h => (
              <div
                key={h.index}
                className="flex justify-between items-center p-2 sm:p-3 bg-secondary rounded-lg hover:bg-secondary/80 transition-colors"
              >
                <span className="font-medium text-foreground text-sm sm:text-base">
                  {h.chinese}时
                </span>
                <span className="text-xs sm:text-sm text-muted-foreground">
                  {h.range}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* AI解读按钮 - 排盘后显示 */}
        {calculatedResult && !result && !loading && (
          <div className="flex justify-center">
            <button
              onClick={handleAIInterpret}
              disabled={loading || resultLoading}
              className="inline-flex items-center justify-center gap-2 px-6 py-3 text-sm font-medium rounded-md bg-primary text-primary-foreground hover:bg-primary/90 transition-colors disabled:opacity-50"
            >
              <Sparkles className="h-5 w-5" />
              开始 AI 解读
            </button>
          </div>
        )}

        {/* AI分析结果内嵌展示 */}
        <InlineResult
          result={result}
          loading={resultLoading}
          streaming={streaming}
          title={CONFIG.title}
        />
      </div>

      {/* 自定义提示弹窗 - 居中显示 */}
      {showAlert && createPortal(
        <div
          className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/40 backdrop-blur-sm"
          onClick={() => setShowAlert(false)}
        >
          <div
            className="bg-gradient-to-br from-white to-amber-50/50 dark:from-gray-800 dark:to-amber-900/20 rounded-3xl shadow-2xl p-8 mx-4 max-w-[340px] w-full border border-amber-200/50 dark:border-amber-700/30"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="text-center">
              {/* 精致图标设计 */}
              <div className="relative w-20 h-20 mx-auto mb-5">
                <div className="absolute inset-0 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 opacity-20 blur-xl"></div>
                <div className="relative w-full h-full rounded-full bg-gradient-to-br from-amber-100 to-orange-100 dark:from-amber-900/40 dark:to-orange-900/40 border-2 border-amber-300/50 dark:border-amber-600/50 flex items-center justify-center shadow-lg">
                  <svg className="w-10 h-10 text-amber-600 dark:text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" />
                    <path d="M12 6v2" />
                    <path d="M12 16v2" />
                    <path d="M6 12h2" />
                    <path d="M16 12h2" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold bg-gradient-to-r from-amber-600 to-orange-600 dark:from-amber-400 dark:to-orange-400 bg-clip-text text-transparent mb-2">无事不起卦</h3>
              <p className="text-muted-foreground text-sm mb-6 leading-relaxed">请先输入您想要占卜的问题<br />方可开始起卦</p>
              <button
                onClick={() => {
                  setShowAlert(false)
                  promptInputRef.current?.focus()
                }}
                className="w-full py-2.5 text-sm font-medium rounded-md bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
              >
                去输入问题
              </button>
            </div>
          </div>
        </div>,
        document.body
      )}
    </DivinationCardHeader>
  )
}
