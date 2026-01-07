import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Input } from '@/components/ui/input'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { ResultDrawer } from '@/components/ResultDrawer'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { getDivinationOption } from '@/config/constants'
import { Sparkles, Eye, Loader2, Calendar } from 'lucide-react'
import * as LunarModule from 'lunar-javascript'
import { useState, useRef, useEffect } from 'react'
import './xiaoliu-ren.css'

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
  const [prompt, setPrompt] = useLocalStorage('xiaoliu-prompt', '')
  const [method, setMethod] = useState<'date' | 'number'>('date')

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
    const month = (lunar as any).getMonth() // 农历月份 (1-12)
    const day = (lunar as any).getDay() // 农历日期 (1-30)
    
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

    const allEarthlyBranches = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']
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
      const gansForPosition = positionToGan[god] || ['甲','乙']
      const isYangBranch = targetBranchIndex % 2 === 0
      const selectedGan = isYangBranch ? gansForPosition[0] : gansForPosition[1]
      const cellGanzhi = `${selectedGan}${cellEarthlyBranch}`

      // 六神兽计算
      const sixGodOrder = ['青龙','朱雀','勾陈','白虎','玄武','螣蛇']
      let dragonStartPosition = 0
      switch(myEarthlyBranch) {
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

  // 开始占卜
  const handleSubmit = () => {
    const xiaoliuResult = calculateXiaoLiuRen()
    setCalculatedResult(xiaoliuResult)
    
    const fullPrompt = `${prompt || '运势'}

起卦：月${month}日${day}时${hour}
落宫：${xiaoliuResult.godName}
五行：${xiaoliuResult.element}
干支：${xiaoliuResult.ganzhi}`
    
    onSubmit({ prompt: fullPrompt })
  }

  // 六宫格布局顺序：留连、速喜、赤口 / 大安、空亡、小吉
  const correctLayoutOrder = [1, 2, 3, 0, 5, 4]

  return (
    <DivinationCardHeader
      title={CONFIG.title}
      description={CONFIG.description}
      icon={CONFIG.icon}
      divinationType="xiaoliu"
    >
      <div className="w-full max-w-5xl mx-auto space-y-8">
        {/* 问题输入 */}
        <div>
          <label className="text-sm font-medium mb-2 block text-gray-700 dark:text-gray-300">
            占卜问题
          </label>
          <Textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="请输入您想要占卜的问题..."
            maxLength={40}
            rows={3}
            className="resize-none w-full"
          />
          <p className="text-xs text-muted-foreground mt-2">
            请输入您想要占卜的问题（最多40字）
          </p>
        </div>

        {/* 起卦方式切换 */}
        <div className="flex justify-center gap-4">
          <Button
            onClick={() => setMethod('date')}
            variant={method === 'date' ? 'default' : 'outline'}
            className={`px-8 py-6 text-base font-medium transition-all ${
              method === 'date' 
                ? 'bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 text-white shadow-lg' 
                : ''
            }`}
          >
            时间起卦
          </Button>
          <Button
            onClick={() => setMethod('number')}
            variant={method === 'number' ? 'default' : 'outline'}
            className={`px-8 py-6 text-base font-medium transition-all ${
              method === 'number' 
                ? 'bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 text-white shadow-lg' 
                : ''
            }`}
          >
            数字起卦
          </Button>
        </div>

        {/* 输入区域 */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-500 via-red-500 to-blue-500" />
          
          {method === 'date' ? (
            <div className="space-y-6">
              <div className="grid grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                    农历月份
                  </label>
                  <select
                    title="农历月份"
                    aria-label="农历月份"
                    value={month}
                    onChange={(e) => setMonth(parseInt(e.target.value))}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                  >
                    {lunarMonths.map((name, index) => (
                      <option key={index + 1} value={index + 1}>{name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                    农历日期
                  </label>
                  <select
                    title="农历日期"
                    aria-label="农历日期"
                    value={day}
                    onChange={(e) => setDay(parseInt(e.target.value))}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                  >
                    {lunarDays.map((name, index) => (
                      <option key={index + 1} value={index + 1}>{name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                    时辰
                  </label>
                  <select
                    title="时辰"
                    aria-label="时辰"
                    value={hour}
                    onChange={(e) => setHour(parseInt(e.target.value))}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                  >
                    {hourTable.map(h => (
                      <option key={h.index} value={h.index}>{h.chinese}时</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="grid grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                    月数 (1-12)
                  </label>
                  <Input
                    type="number"
                    min="1"
                    max="12"
                    value={month}
                    onChange={(e) => setMonth(Math.min(12, Math.max(1, parseInt(e.target.value) || 1)))}
                    className="text-center text-lg py-6"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                    日数 (1-31)
                  </label>
                  <Input
                    type="number"
                    min="1"
                    max="31"
                    value={day}
                    onChange={(e) => setDay(Math.min(31, Math.max(1, parseInt(e.target.value) || 1)))}
                    className="text-center text-lg py-6"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                    时数 (1-12)
                  </label>
                  <Input
                    type="number"
                    min="1"
                    max="12"
                    value={hour}
                    onChange={(e) => setHour(Math.min(12, Math.max(1, parseInt(e.target.value) || 1)))}
                    className="text-center text-lg py-6"
                  />
                </div>
              </div>
            </div>
          )}

          {/* 按钮组 */}
          <div className="flex gap-4 mt-8">
            <Button
              onClick={handleSubmit}
              disabled={loading}
              className="flex-1 py-6 text-lg font-medium bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 shadow-lg hover:shadow-xl transition-all"
            >
              {loading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin mr-2" />
                  占卜中...
                </>
              ) : (
                <>
                  <Sparkles className="h-5 w-5 mr-2" />
                  开始占卜
                </>
              )}
            </Button>
            {method === 'date' && (
              <Button
                onClick={useCurrentTime}
                className="px-6 py-6 font-medium bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 shadow-lg hover:shadow-xl transition-all"
                title="使用当前时间"
              >
                <Calendar className="h-5 w-5 mr-2" />
                获取当前时间
              </Button>
            )}
          </div>
        </div>

        {/* 排盘结果 - 完整照抄目标网站 */}
        {calculatedResult && (
          <div className="space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700">
              <h3 className="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-gray-100">
                排盘结果
              </h3>
              
              {/* 六宫格 - 完全按照目标网站结构 */}
              <div className="flex justify-center overflow-visible p-5">
                <div 
                  className="grid grid-cols-3 border-[3px] border-gray-300 dark:border-gray-600 rounded-2xl shadow-2xl bg-white dark:bg-gray-800 overflow-visible"
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
                        className={`relative transition-all hover:bg-gray-50 dark:hover:bg-gray-750 cursor-pointer ${isFinal ? 'bg-yellow-50 dark:bg-yellow-900/20 border-2 border-yellow-400 dark:border-yellow-500' : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700'} xiaoliu-card`}
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
                          className={`xiaoliu-bottom-bar ${
                            branchElement === '木' ? 'el-mu' :
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

              {/* 计算过程 */}
              <div className="mt-8 p-6 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700">
                <h4 className="font-bold text-gray-900 dark:text-gray-100 mb-4 text-lg">起课步骤</h4>
                <div className="space-y-3 text-sm">
                  <div className="p-4 bg-white dark:bg-gray-800 rounded-lg border-l-4 border-blue-500">
                    <span className="font-bold text-blue-600 dark:text-blue-400">① 月上起日：</span>
                    <span className="text-gray-700 dark:text-gray-300 ml-2">
                      从大安起，数到{lunarMonths[calculatedResult.month - 1]}，再数到{lunarDays[calculatedResult.day - 1]}，
                      落在 <span className="font-bold text-gray-900 dark:text-gray-100">{sixGodNames[sixGods[calculatedResult.dayResult]]}</span>
                    </span>
                  </div>
                  <div className="p-4 bg-white dark:bg-gray-800 rounded-lg border-l-4 border-green-500">
                    <span className="font-bold text-green-600 dark:text-green-400">② 日上起时：</span>
                    <span className="text-gray-700 dark:text-gray-300 ml-2">
                      从 {sixGodNames[sixGods[calculatedResult.dayResult]]} 起，数到{hourNames[calculatedResult.hour - 1]}时，
                      最终落在 <span className="font-bold text-gray-900 dark:text-gray-100">{calculatedResult.godName}</span>
                    </span>
                  </div>
                  <div className="p-4 bg-white dark:bg-gray-800 rounded-lg border-l-4 border-purple-500">
                    <span className="font-bold text-purple-600 dark:text-purple-400">③ 五行属性：</span>
                    <span className="text-gray-700 dark:text-gray-300 ml-2">
                      {calculatedResult.godName} 对应五行为 
                      <span className={`font-bold ml-1 element-color ${
                        calculatedResult.element === '木' ? 'el-color-mu' :
                        calculatedResult.element === '火' ? 'el-color-huo' :
                        calculatedResult.element === '土' ? 'el-color-tu' :
                        calculatedResult.element === '金' ? 'el-color-jin' :
                        calculatedResult.element === '水' ? 'el-color-shui' : ''
                      }`}>
                        {calculatedResult.element}
                      </span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 详细信息弹窗 - 完全照抄参考站样式 */}
        {selectedCell && (
          <div className="info-dialog-reference" role="dialog" aria-modal="true">
            <div className="dialog-content">
              <div className="dialog-header">
                <button className="close-btn" onClick={() => setSelectedCell(null)}>×</button>
              </div>
              <div className="content-wrapper">
                <div className="basic-info">
                  <p>
                    <strong>宫位：</strong>
                    <span className="value">
                      {selectedCell.godName}
                      {selectedCell.validationInfo?.position ? ` (第${selectedCell.validationInfo.position}位)` : ''}
                    </span>
                  </p>
                  <p><strong>干支：</strong><span className="value">{selectedCell.ganzhi}</span></p>
                  <p><strong>地支：</strong><span className="value">{selectedCell.earthlyBranch}</span></p>
                  <p><strong>五行属性：</strong><span className="value">{selectedCell.branchElement}</span></p>
                  <p><strong>六神：</strong><span className="value">{selectedCell.sixGodBeast}</span></p>
                  <p><strong>六亲：</strong><span className="value">{selectedCell.liuqin}</span></p>
                  <p><strong>五星：</strong><span className="value">{selectedCell.fiveStar}</span></p>
                </div>
                <div className="validation-section">
                  <h4>校准验证信息</h4>
                  <p><strong>时辰落宫：</strong><span className="value">{selectedCell.validationInfo?.isHourPosition ? '是' : '否'}</span></p>
                  <p><strong>日落宫位：</strong><span className="value">{selectedCell.validationInfo?.isDayPosition ? '是' : '否'}</span></p>
                  <p><strong>月落宫位：</strong><span className="value">{selectedCell.validationInfo?.isMonthPosition ? '是' : '否'}</span></p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 时辰对照表 */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700">
          <h3 className="text-xl font-bold mb-6 text-center text-gray-900 dark:text-gray-100">
            时辰对照表
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {hourTable.map(h => (
              <div 
                key={h.index} 
                className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-900 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <span className="font-medium text-primary">
                  {h.chinese}时
                </span>
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {h.range}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* 查看AI解读按钮 */}
        {result && (
          <div className="flex justify-center">
            <Button
              onClick={() => setShowDrawer(true)}
              variant="outline"
              size="lg"
              className="gap-2 px-8 py-6 text-lg"
            >
              <Eye className="h-5 w-5" />
              查看AI解读
            </Button>
          </div>
        )}
      </div>

      <ResultDrawer
        show={showDrawer}
        onClose={() => setShowDrawer(false)}
        result={result}
        loading={resultLoading}
        streaming={streaming}
        title={CONFIG.title}
      />
    </DivinationCardHeader>
  )
}
