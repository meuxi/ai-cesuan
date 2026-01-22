import { useState, useRef, useEffect } from 'react'
import { Solar } from '@/utils/laohuangli'
import { X } from 'lucide-react'

interface DatePickerModalProps {
    title?: string
    onConfirm: (solar: Solar) => void
    onClose: () => void
}

export default function DatePickerModal({ title = '选择日期', onConfirm, onClose }: DatePickerModalProps) {
    const now = Solar.fromDate(new Date())
    const [selectedDate, setSelectedDate] = useState(now)

    // 年月日选择状态
    const [year, setYear] = useState(now.getYear())
    const [month, setMonth] = useState(now.getMonth())
    const [day, setDay] = useState(now.getDay())

    // 生成年份列表 (1900-2200)
    const years = Array.from({ length: 301 }, (_, i) => 1900 + i)
    // 生成月份列表 (1-12)
    const months = Array.from({ length: 12 }, (_, i) => i + 1)
    // 生成日期列表 (根据年月动态计算)
    const getDaysInMonth = (y: number, m: number) => {
        return new Date(y, m, 0).getDate()
    }
    const days = Array.from({ length: getDaysInMonth(year, month) }, (_, i) => i + 1)

    // 滚动容器引用
    const yearRef = useRef<HTMLDivElement>(null)
    const monthRef = useRef<HTMLDivElement>(null)
    const dayRef = useRef<HTMLDivElement>(null)

    // 更新选中日期
    useEffect(() => {
        const maxDay = getDaysInMonth(year, month)
        const validDay = day > maxDay ? maxDay : day
        if (validDay !== day) {
            setDay(validDay)
        }
        const solar = Solar.fromYmd(year, month, validDay)
        setSelectedDate(solar)
    }, [year, month, day])

    // 滚动到当前选中项
    useEffect(() => {
        const scrollToCenter = (ref: React.RefObject<HTMLDivElement>, index: number) => {
            if (ref.current) {
                const itemHeight = 36
                ref.current.scrollTop = index * itemHeight
            }
        }
        scrollToCenter(yearRef, years.indexOf(year))
        scrollToCenter(monthRef, month - 1)
        scrollToCenter(dayRef, day - 1)
    }, [])

    const handleConfirm = () => {
        onConfirm(selectedDate)
    }

    const handleBackToToday = () => {
        onConfirm(now)
    }

    const lunar = selectedDate.getLunar()

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" onClick={onClose}>
            <div
                className="bg-card rounded-xl w-[85%] max-w-md p-4 shadow-2xl border border-border"
                onClick={(e) => e.stopPropagation()}
            >
                {/* 标题 */}
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium text-foreground">{title}</h3>
                    <button onClick={onClose} className="p-2 hover:bg-accent rounded-lg transition-colors">
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* 日期选择器 */}
                <div className="flex gap-2 h-[180px] overflow-hidden">
                    {/* 年 */}
                    <div className="flex-1 relative">
                        <div
                            ref={yearRef}
                            className="h-full overflow-y-auto scrollbar-hide snap-y snap-mandatory"
                            onScroll={(e) => {
                                const target = e.target as HTMLDivElement
                                const index = Math.round(target.scrollTop / 36)
                                if (years[index] && years[index] !== year) {
                                    setYear(years[index])
                                }
                            }}
                        >
                            <div className="h-[72px]"></div>
                            {years.map((y) => (
                                <div
                                    key={y}
                                    className={`h-9 flex items-center justify-center snap-center cursor-pointer transition-all ${y === year ? 'text-foreground font-bold text-lg' : 'text-muted-foreground'
                                        }`}
                                    onClick={() => setYear(y)}
                                >
                                    {y}年
                                </div>
                            ))}
                            <div className="h-[72px]"></div>
                        </div>
                        <div className="absolute inset-x-0 top-[72px] h-9 border-y border-border pointer-events-none"></div>
                    </div>

                    {/* 月 */}
                    <div className="flex-1 relative">
                        <div
                            ref={monthRef}
                            className="h-full overflow-y-auto scrollbar-hide snap-y snap-mandatory"
                            onScroll={(e) => {
                                const target = e.target as HTMLDivElement
                                const index = Math.round(target.scrollTop / 36)
                                if (months[index] && months[index] !== month) {
                                    setMonth(months[index])
                                }
                            }}
                        >
                            <div className="h-[72px]"></div>
                            {months.map((m) => (
                                <div
                                    key={m}
                                    className={`h-9 flex items-center justify-center snap-center cursor-pointer transition-all ${m === month ? 'text-foreground font-bold text-lg' : 'text-muted-foreground'
                                        }`}
                                    onClick={() => setMonth(m)}
                                >
                                    {m}月
                                </div>
                            ))}
                            <div className="h-[72px]"></div>
                        </div>
                        <div className="absolute inset-x-0 top-[72px] h-9 border-y border-border pointer-events-none"></div>
                    </div>

                    {/* 日 */}
                    <div className="flex-1 relative">
                        <div
                            ref={dayRef}
                            className="h-full overflow-y-auto scrollbar-hide snap-y snap-mandatory"
                            onScroll={(e) => {
                                const target = e.target as HTMLDivElement
                                const index = Math.round(target.scrollTop / 36)
                                if (days[index] && days[index] !== day) {
                                    setDay(days[index])
                                }
                            }}
                        >
                            <div className="h-[72px]"></div>
                            {days.map((d) => (
                                <div
                                    key={d}
                                    className={`h-9 flex items-center justify-center snap-center cursor-pointer transition-all ${d === day ? 'text-foreground font-bold text-lg' : 'text-muted-foreground'
                                        }`}
                                    onClick={() => setDay(d)}
                                >
                                    {d}日
                                </div>
                            ))}
                            <div className="h-[72px]"></div>
                        </div>
                        <div className="absolute inset-x-0 top-[72px] h-9 border-y border-border pointer-events-none"></div>
                    </div>
                </div>

                {/* 农历信息 */}
                <div className="text-center text-muted-foreground py-3 border-t border-border mt-3">
                    {lunar.toString()} 周{selectedDate.getWeekInChinese()}
                </div>

                {/* 按钮 */}
                <div className="flex gap-3 pt-2">
                    <button
                        className="flex-1 py-2.5 text-sm font-medium rounded-md border border-input bg-background text-foreground hover:bg-accent transition-colors"
                        onClick={handleBackToToday}
                    >
                        回到今天
                    </button>
                    <button
                        className="flex-1 py-2.5 text-sm font-medium rounded-md bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
                        onClick={handleConfirm}
                    >
                        确定
                    </button>
                </div>
            </div>
        </div>
    )
}
