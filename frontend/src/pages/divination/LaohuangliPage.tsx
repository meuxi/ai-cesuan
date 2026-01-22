import { useState, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChevronLeft, ChevronRight, ChevronDown, CalendarDays, Grid3X3, List } from 'lucide-react'
import {
    Solar,
    weekList,
    getMonthDays,
    getHolidayWork,
    getDateInfo,
    getTimeGanZhiLuck,
    Lunar,
} from '@/utils/laohuangli'
import DatePickerModal from '@/components/laohuangli/DatePickerModal'
import { LunarCalendar } from '@/components/laohuangli'
import './laohuangli.css'

export default function LaohuangliPage() {
    const navigate = useNavigate()
    const today = Solar.fromDate(new Date())
    const todayLunar = today.getLunar()
    const nowTime = todayLunar.getTimeInGanZhi()

    // 固定年月日，用于判断当前时间
    const gdYear = new Date().getFullYear()
    const gdMonth = new Date().getMonth() + 1

    // 当前显示的年月（可随选择变化）
    const [nowYear, setNowYear] = useState(new Date().getFullYear())
    const [nowMonth, setNowMonth] = useState(new Date().getMonth() + 1)
    const nowDate = new Date().getDate()

    // 选中日期
    const [selectDate, setSelectDate] = useState(today)

    // 日期选择器显示状态
    const [showPicker, setShowPicker] = useState(false)
    
    // 视图模式：'detail' 详情视图 | 'calendar' 月历视图
    const [viewMode, setViewMode] = useState<'detail' | 'calendar'>('detail')

    // 获取日历数据
    const dateList = useMemo(() => getMonthDays(nowYear, nowMonth), [nowYear, nowMonth])

    // 获取选中日期的详细信息
    const dateInfo = useMemo(() => getDateInfo(selectDate), [selectDate])

    // 判断是否调休/休息
    const isWork = (solar: Solar): boolean | undefined => {
        return getHolidayWork(solar)
    }

    // 选择日期
    const handleSelectDay = (solar: Solar) => {
        setSelectDate(solar)
        setNowMonth(solar.getMonth())
        setNowYear(solar.getYear())
    }

    // 上一天/下一天
    const handleNextDay = (val: number) => {
        const newDate = selectDate.next(val)
        handleSelectDay(newDate)
    }

    // 确认选择日期（从日期选择器）
    const handleConfirm = (solar: Solar) => {
        handleSelectDay(solar)
        setShowPicker(false)
    }

    // 回到今天
    const handleBackToToday = () => {
        handleSelectDay(today)
    }

    // 跳转到吉日查询
    const handleToSelect = () => {
        navigate('/divination/laohuangli/select')
    }

    return (
        <div className="laohuangli-wrapper">
            {/* 导航栏 */}
            <div className="laohuangli-nav">
                <div className="laohuangli-nav-back"></div>
                <div className="laohuangli-nav-date" onClick={() => setShowPicker(true)}>
                    {nowYear}年{nowMonth}月
                    <ChevronDown className="w-4 h-4 ml-1 inline" />
                </div>
                <div className="laohuangli-nav-jin flex items-center gap-2">
                    {/* 视图切换按钮 */}
                    <button
                        className={`rounded-full w-8 h-8 p-0 border border-input transition-colors ${
                            viewMode === 'calendar' 
                                ? 'bg-primary text-primary-foreground' 
                                : 'text-muted-foreground hover:bg-primary hover:text-primary-foreground'
                        }`}
                        onClick={() => setViewMode(viewMode === 'detail' ? 'calendar' : 'detail')}
                        title={viewMode === 'detail' ? '切换月历视图' : '切换详情视图'}
                    >
                        {viewMode === 'detail' ? <Grid3X3 className="w-4 h-4" /> : <List className="w-4 h-4" />}
                    </button>
                    <button
                        className="rounded-full w-8 h-8 p-0 border border-input text-muted-foreground hover:bg-primary hover:text-primary-foreground transition-colors"
                        onClick={handleBackToToday}
                    >
                        今
                    </button>
                </div>
            </div>

            {/* 月历视图 - 新增 */}
            {viewMode === 'calendar' && (
                <div className="laohuangli-calendar p-4">
                    <LunarCalendar
                        initialDate={new Date(selectDate.getYear(), selectDate.getMonth() - 1, selectDate.getDay())}
                        onSelectDate={(date) => {
                            const solar = Solar.fromDate(date)
                            handleSelectDay(solar)
                        }}
                    />
                </div>
            )}
            
            {/* 日历主体 - 原详情视图 */}
            {viewMode === 'detail' && (
                <div className="laohuangli-calendar">
                    <div className="p-3">
                        {/* 星期头 */}
                        <div className="laohuangli-week-header">
                            {weekList.map((item: { label: string; value: number }) => (
                                <div key={item.value} className="laohuangli-week-item">
                                    {item.label}
                                </div>
                            ))}
                        </div>

                        {/* 日期网格 */}
                        <div className="laohuangli-date-grid">
                            {dateList.map((item: Solar, index: number) => {
                                const lunar = item.getLunar()
                                const isNotNowMonth = nowMonth !== item.getMonth()
                                const isToday =
                                    nowDate === item.getDay() &&
                                    gdMonth === item.getMonth() &&
                                    gdYear === item.getYear()
                                const isSelected =
                                    selectDate.getDay() === item.getDay() &&
                                    selectDate.getMonth() === item.getMonth() &&
                                    selectDate.getYear() === item.getYear()
                                const workStatus = isWork(item)

                                return (
                                    <div
                                        key={index}
                                        className={`laohuangli-date-item ${isNotNowMonth ? 'not-now-month' : ''} ${isToday ? 'today' : ''
                                            } ${isSelected ? 'selected' : ''} ${workStatus === false ? 'holiday' : ''
                                            } ${workStatus === true ? 'workday' : ''}`}
                                        onClick={() => handleSelectDay(item)}
                                    >
                                        <div className="date-solar">{item.getDay()}</div>
                                        {lunar.getJieQi() ? (
                                            <div className="date-jieqi">{lunar.getJieQi()}</div>
                                        ) : lunar.getFestivals()[0] ? (
                                            <div className="date-festival">{lunar.getFestivals()[0]}</div>
                                        ) : item.getFestivals()[0] ? (
                                            <div className="date-festival">{item.getFestivals()[0]}</div>
                                        ) : (
                                            <div className="date-lunar">{lunar.getDayInChinese()}</div>
                                        )}
                                        {workStatus === false && <span className="work-tag休">休</span>}
                                        {workStatus === true && <span className="work-tag班">班</span>}
                                    </div>
                                )
                            })}
                        </div>
                    </div>
                </div>
            )}

            {/* 日期信息 - 阴历显示 */}
            <div className="laohuangli-info-card">
                <div className="p-4">
                    <div className="laohuangli-yinli">
                        <ChevronLeft
                            className="w-8 h-8 cursor-pointer hover:text-muted-foreground transition-colors"
                            onClick={() => handleNextDay(-1)}
                        />
                        <div className="laohuangli-yinli-mid">
                            <div className="laohuangli-yinli-title">{dateInfo.yinli}</div>
                            <div className="laohuangli-yinli-info">
                                <span>{dateInfo.ganzhiyear}</span>
                                <span>{dateInfo.ganzhimonth}月</span>
                                <span>{dateInfo.ganzhiday}日</span>
                                <span>星期{dateInfo.xingqi}</span>
                            </div>
                        </div>
                        <ChevronRight
                            className="w-8 h-8 cursor-pointer hover:text-muted-foreground transition-colors"
                            onClick={() => handleNextDay(1)}
                        />
                    </div>
                </div>
            </div>

            {/* 宜忌信息 */}
            <div className="laohuangli-info-card">
                <div className="p-4">
                    <div className="laohuangli-yiji">
                        <div className="laohuangli-yiji-content">
                            <div className="yiji-row">
                                <div className="yiji-icon yi">
                                    <span>宜</span>
                                </div>
                                <div className="yiji-items">
                                    {dateInfo.dayyi.map((item: string, index: number) => (
                                        <span key={index}>{item}</span>
                                    ))}
                                </div>
                            </div>
                            <div className="yiji-row">
                                <div className="yiji-icon ji">
                                    <span>忌</span>
                                </div>
                                <div className="yiji-items">
                                    {dateInfo.dayji.map((item: string, index: number) => (
                                        <span key={index}>{item}</span>
                                    ))}
                                </div>
                            </div>
                        </div>
                        <div className="laohuangli-jiri-btn" onClick={handleToSelect}>
                            <div className="jiri-btn-inner">吉日查询</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* 五行冲煞等信息 */}
            <div className="laohuangli-info-card">
                <div className="p-0">
                    <div className="laohuangli-wxcs">
                        {/* 五行、冲煞、值神 */}
                        <div className="wxcs-row-top">
                            <div className="wxcs-item">
                                <div className="wxcs-label">五行</div>
                                <div className="wxcs-value">{dateInfo.wuxing}</div>
                            </div>
                            <div className="wxcs-item">
                                <div className="wxcs-label">冲煞</div>
                                <div className="wxcs-value">{dateInfo.chongsha}</div>
                            </div>
                            <div className="wxcs-item no-border">
                                <div className="wxcs-label">值神</div>
                                <div className="wxcs-value">{dateInfo.zhishen}</div>
                            </div>
                        </div>

                        {/* 时宜辰忌 */}
                        <div className="wxcs-time-row">
                            <div className="time-label">时宜辰忌</div>
                            <div className="time-values">
                                {dateInfo.times.map((item: { getGanZhi: () => string }, index: number) => (
                                    <div
                                        key={index}
                                        className={`time-item ${nowTime === item.getGanZhi() ? 'current' : ''}`}
                                    >
                                        {item.getGanZhi()}
                                        {getTimeGanZhiLuck(selectDate.getYear(), selectDate.getMonth(), selectDate.getDay(), index * 2)}
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* 财神、福神 */}
                        <div className="wxcs-shen-row">
                            <div className="shen-item">
                                <div className="shen-label">财神</div>
                                <div className="shen-value">{dateInfo.caishenpos}</div>
                            </div>
                            <div className="shen-item">
                                <div className="shen-label">福神</div>
                                <div className="shen-value">{dateInfo.fushenpos}</div>
                            </div>
                        </div>

                        {/* 喜神、阳贵 */}
                        <div className="wxcs-shen-row">
                            <div className="shen-item">
                                <div className="shen-label">喜神</div>
                                <div className="shen-value">{dateInfo.xishenpos}</div>
                            </div>
                            <div className="shen-item">
                                <div className="shen-label">阳贵</div>
                                <div className="shen-value">{dateInfo.yangguipos}</div>
                            </div>
                        </div>

                        {/* 彭祖百忌 */}
                        <div className="wxcs-pzbj">
                            <div className="pzbj-label">彭祖百忌</div>
                            <div className="pzbj-value">{dateInfo.pzbj}</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* 日期选择器弹窗 */}
            {showPicker && (
                <DatePickerModal
                    onConfirm={handleConfirm}
                    onClose={() => setShowPicker(false)}
                />
            )}
        </div>
    )
}
