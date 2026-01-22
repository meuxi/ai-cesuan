/**
 * 老黄历月历视图组件
 * 显示农历月历，支持选择日期查看黄历信息
 */

import { useState, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronLeft, ChevronRight, Calendar, Sun, Moon } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useTranslation } from 'react-i18next'

// 使用 lunar-javascript 库（如果可用）或手动计算
interface LunarDayInfo {
  day: number
  month: number
  year: number
  lunarDay: string
  lunarMonth: string
  isToday: boolean
  isCurrentMonth: boolean
  yi: string[]
  ji: string[]
  jieqi?: string
  festival?: string
}

interface LunarCalendarProps {
  initialDate?: Date
  onSelectDate?: (date: Date, lunarInfo: LunarDayInfo) => void
  className?: string
}

// 农历月份名称
const LUNAR_MONTHS = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']
// 农历日期名称
const LUNAR_DAYS = [
  '', '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
  '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
  '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'
]
// 节气
const JIEQI = [
  '小寒', '大寒', '立春', '雨水', '惊蛰', '春分',
  '清明', '谷雨', '立夏', '小满', '芒种', '夏至',
  '小暑', '大暑', '立秋', '处暑', '白露', '秋分',
  '寒露', '霜降', '立冬', '小雪', '大雪', '冬至'
]

// 星期名称
const WEEKDAYS = ['日', '一', '二', '三', '四', '五', '六']
const WEEKDAYS_EN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

export function LunarCalendar({ initialDate, onSelectDate, className }: LunarCalendarProps) {
  const { i18n } = useTranslation()
  const today = new Date()
  const [currentDate, setCurrentDate] = useState(initialDate || today)
  const [selectedDate, setSelectedDate] = useState<Date | null>(null)
  const [viewMode, setViewMode] = useState<'month' | 'year'>('month')

  const currentYear = currentDate.getFullYear()
  const currentMonth = currentDate.getMonth()

  // 生成月历数据
  const calendarDays = useMemo(() => {
    const days: (LunarDayInfo | null)[] = []
    
    // 获取当月第一天和最后一天
    const firstDay = new Date(currentYear, currentMonth, 1)
    const lastDay = new Date(currentYear, currentMonth + 1, 0)
    const daysInMonth = lastDay.getDate()
    const startWeekday = firstDay.getDay()
    
    // 上月填充
    const prevMonthLastDay = new Date(currentYear, currentMonth, 0).getDate()
    for (let i = startWeekday - 1; i >= 0; i--) {
      const day = prevMonthLastDay - i
      days.push(createDayInfo(new Date(currentYear, currentMonth - 1, day), false))
    }
    
    // 当月日期
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(createDayInfo(new Date(currentYear, currentMonth, day), true))
    }
    
    // 下月填充
    const remainingDays = 42 - days.length // 6行 x 7天
    for (let day = 1; day <= remainingDays; day++) {
      days.push(createDayInfo(new Date(currentYear, currentMonth + 1, day), false))
    }
    
    return days
  }, [currentYear, currentMonth])

  // 创建日期信息（简化版，实际应使用 lunar-javascript）
  function createDayInfo(date: Date, isCurrentMonth: boolean): LunarDayInfo {
    const isToday = date.toDateString() === today.toDateString()
    
    // 简化的农历计算（实际应使用完整的农历库）
    const lunarDay = ((date.getDate() - 1) % 30) + 1
    const lunarMonth = (date.getMonth() + 11) % 12
    
    // 简化的宜忌（实际应从后端获取）
    const yi = getSimpleYi(date)
    const ji = getSimpleJi(date)
    
    // 检查节气
    const jieqi = checkJieqi(date)
    
    return {
      day: date.getDate(),
      month: date.getMonth(),
      year: date.getFullYear(),
      lunarDay: LUNAR_DAYS[lunarDay] || `${lunarDay}`,
      lunarMonth: LUNAR_MONTHS[lunarMonth] + '月',
      isToday,
      isCurrentMonth,
      yi,
      ji,
      jieqi
    }
  }

  // 简化的宜事计算
  function getSimpleYi(date: Date): string[] {
    const dayOfWeek = date.getDay()
    const dayNum = date.getDate()
    const options = ['祭祀', '祈福', '求嗣', '开光', '出行', '解除', '嫁娶', '纳采', '移徙', '入宅', '修造', '动土']
    const selected: string[] = []
    for (let i = 0; i < 4; i++) {
      selected.push(options[(dayNum + dayOfWeek + i) % options.length])
    }
    return selected
  }

  // 简化的忌事计算
  function getSimpleJi(date: Date): string[] {
    const dayOfWeek = date.getDay()
    const dayNum = date.getDate()
    const options = ['作灶', '安床', '开市', '破土', '安葬', '出货财', '启攒', '入殓', '移柩']
    const selected: string[] = []
    for (let i = 0; i < 3; i++) {
      selected.push(options[(dayNum + dayOfWeek + i + 3) % options.length])
    }
    return selected
  }

  // 检查节气
  function checkJieqi(date: Date): string | undefined {
    // 简化版：根据固定日期判断（实际需要精确计算）
    const month = date.getMonth()
    const day = date.getDate()
    const jieqiDates: Record<number, number[]> = {
      0: [6, 20], 1: [4, 19], 2: [6, 21], 3: [5, 20],
      4: [6, 21], 5: [6, 21], 6: [7, 23], 7: [8, 23],
      8: [8, 23], 9: [8, 24], 10: [8, 22], 11: [7, 22]
    }
    const days = jieqiDates[month]
    if (days) {
      if (day === days[0]) return JIEQI[month * 2]
      if (day === days[1]) return JIEQI[month * 2 + 1]
    }
    return undefined
  }

  // 月份导航
  const goToPrevMonth = () => {
    setCurrentDate(new Date(currentYear, currentMonth - 1, 1))
  }

  const goToNextMonth = () => {
    setCurrentDate(new Date(currentYear, currentMonth + 1, 1))
  }

  const goToToday = () => {
    setCurrentDate(new Date())
    setSelectedDate(null)
  }

  // 选择日期
  const handleSelectDate = (dayInfo: LunarDayInfo | null) => {
    if (!dayInfo) return
    const date = new Date(dayInfo.year, dayInfo.month, dayInfo.day)
    setSelectedDate(date)
    onSelectDate?.(date, dayInfo)
  }

  const weekdays = i18n.language === 'en' ? WEEKDAYS_EN : WEEKDAYS

  return (
    <div className={cn('w-full max-w-md mx-auto', className)}>
      {/* 月份导航 */}
      <div className="flex items-center justify-between mb-4 px-2">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={goToPrevMonth}
          className="p-2 rounded-full hover:bg-secondary transition-colors"
        >
          <ChevronLeft className="w-5 h-5 text-foreground" />
        </motion.button>
        
        <div className="text-center">
          <h2 className="text-xl font-bold text-foreground">
            {currentYear}年 {currentMonth + 1}月
          </h2>
          <p className="text-sm text-muted-foreground">
            {LUNAR_MONTHS[(currentMonth + 11) % 12]}月
          </p>
        </div>
        
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={goToNextMonth}
          className="p-2 rounded-full hover:bg-secondary transition-colors"
        >
          <ChevronRight className="w-5 h-5 text-foreground" />
        </motion.button>
      </div>

      {/* 返回今天按钮 */}
      <div className="flex justify-center mb-4">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={goToToday}
          className="px-4 py-1.5 text-sm bg-primary/10 text-primary rounded-full hover:bg-primary/20 transition-colors flex items-center gap-1"
        >
          <Calendar className="w-4 h-4" />
          今天
        </motion.button>
      </div>

      {/* 星期标题 */}
      <div className="grid grid-cols-7 mb-2">
        {weekdays.map((day, i) => (
          <div
            key={day}
            className={cn(
              'text-center text-sm font-medium py-2',
              i === 0 || i === 6 ? 'text-red-500' : 'text-muted-foreground'
            )}
          >
            {day}
          </div>
        ))}
      </div>

      {/* 日历网格 */}
      <div className="grid grid-cols-7 gap-1">
        {calendarDays.map((dayInfo, index) => {
          if (!dayInfo) return <div key={index} className="aspect-square" />
          
          const isSelected = selectedDate?.toDateString() === new Date(dayInfo.year, dayInfo.month, dayInfo.day).toDateString()
          const isWeekend = index % 7 === 0 || index % 7 === 6
          
          return (
            <motion.button
              key={index}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleSelectDate(dayInfo)}
              className={cn(
                'aspect-square rounded-lg p-1 flex flex-col items-center justify-center transition-all',
                'hover:bg-accent border border-transparent',
                !dayInfo.isCurrentMonth && 'opacity-40',
                dayInfo.isToday && 'border-primary bg-primary/10',
                isSelected && 'bg-primary text-primary-foreground border-primary',
                isWeekend && !isSelected && dayInfo.isCurrentMonth && 'text-red-500'
              )}
            >
              <span className={cn(
                'text-sm font-medium',
                isSelected && 'text-primary-foreground'
              )}>
                {dayInfo.day}
              </span>
              <span className={cn(
                'text-[10px]',
                dayInfo.jieqi ? 'text-green-500 font-medium' : 'text-muted-foreground',
                isSelected && 'text-primary-foreground'
              )}>
                {dayInfo.jieqi || dayInfo.lunarDay}
              </span>
            </motion.button>
          )
        })}
      </div>

      {/* 选中日期详情 */}
      <AnimatePresence>
        {selectedDate && calendarDays.find(d => 
          d && d.day === selectedDate.getDate() && d.month === selectedDate.getMonth()
        ) && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 overflow-hidden"
          >
            <DayDetailCard dayInfo={calendarDays.find(d => 
              d && d.day === selectedDate.getDate() && d.month === selectedDate.getMonth()
            )!} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

// 日期详情卡片
function DayDetailCard({ dayInfo }: { dayInfo: LunarDayInfo }) {
  return (
    <div className="p-4 rounded-xl bg-card border border-border">
      {/* 日期标题 */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-2xl font-bold text-foreground">
            {dayInfo.month + 1}月{dayInfo.day}日
          </h3>
          <p className="text-sm text-muted-foreground">
            农历 {dayInfo.lunarMonth}{dayInfo.lunarDay}
          </p>
        </div>
        {dayInfo.jieqi && (
          <div className="px-3 py-1 bg-green-500/20 text-green-600 dark:text-green-400 rounded-full text-sm font-medium">
            {dayInfo.jieqi}
          </div>
        )}
      </div>
      
      {/* 宜忌 */}
      <div className="grid grid-cols-2 gap-4">
        {/* 宜 */}
        <div className="p-3 rounded-lg bg-[hsl(var(--jiri-yi-bg))] border border-[hsl(var(--jiri-yi-border))]">
          <div className="flex items-center gap-2 mb-2">
            <Sun className="w-4 h-4 text-[hsl(var(--jiri-yi-primary))]" />
            <span className="font-medium text-[hsl(var(--jiri-yi-primary))]">宜</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {dayInfo.yi.map((item, i) => (
              <span 
                key={i}
                className="px-2 py-0.5 text-xs rounded bg-[hsl(var(--jiri-yi-primary))]/20 text-[hsl(var(--jiri-yi-primary))]"
              >
                {item}
              </span>
            ))}
          </div>
        </div>
        
        {/* 忌 */}
        <div className="p-3 rounded-lg bg-[hsl(var(--jiri-ji-bg))] border border-[hsl(var(--jiri-ji-border))]">
          <div className="flex items-center gap-2 mb-2">
            <Moon className="w-4 h-4 text-[hsl(var(--jiri-ji-primary))]" />
            <span className="font-medium text-[hsl(var(--jiri-ji-primary))]">忌</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {dayInfo.ji.map((item, i) => (
              <span 
                key={i}
                className="px-2 py-0.5 text-xs rounded bg-[hsl(var(--jiri-ji-primary))]/20 text-[hsl(var(--jiri-ji-primary))]"
              >
                {item}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
