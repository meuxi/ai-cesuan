import { useState, useMemo } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Switch } from '@/components/ui/switch'
import { ChevronLeft, ChevronDown } from 'lucide-react'
import { Solar, getJiRiList, addZero, todesMap } from '@/utils/laohuangli'
import DatePickerModal from '@/components/laohuangli/DatePickerModal'

export default function JiriDetailPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  const name = searchParams.get('name') || ''
  const type = (searchParams.get('type') || '1') as '1' | '2'
  const yijiName = (type === '1' ? '宜' : '忌') + name

  const today = Solar.fromDate(new Date())

  // 日期范围
  const [startTime, setStartTime] = useState(new Date().getTime())
  const [endTime, setEndTime] = useState(new Date().getTime() + 86400000 * 185) // 约6个月

  // 只看周末
  const [isWeekShow, setIsWeekShow] = useState(false)

  // 日期选择器
  const [showStartPicker, setShowStartPicker] = useState(false)
  const [showEndPicker, setShowEndPicker] = useState(false)

  // 获取吉日列表
  const dayList = useMemo(() => {
    return getJiRiList(type, name, startTime, endTime)
  }, [type, name, startTime, endTime])

  // 计算显示的天数
  const displayDays = useMemo(() => {
    if (!isWeekShow) return dayList
    return dayList.filter((item) => item.getWeek() === 0 || item.getWeek() === 6)
  }, [dayList, isWeekShow])

  const dayNum = displayDays.length

  const handleBack = () => {
    navigate('/divination/laohuangli/select')
  }

  const handleConfirmStart = (solar: Solar) => {
    setStartTime(new Date(solar.getYear(), solar.getMonth() - 1, solar.getDay()).getTime())
    setShowStartPicker(false)
  }

  const handleConfirmEnd = (solar: Solar) => {
    setEndTime(new Date(solar.getYear(), solar.getMonth() - 1, solar.getDay()).getTime())
    setShowEndPicker(false)
  }

  const formatDate = (timestamp: number) => {
    const date = new Date(timestamp)
    const solar = Solar.fromDate(date)
    const lunar = solar.getLunar()
    return {
      solar: `${date.getFullYear()}.${addZero(date.getMonth() + 1)}.${addZero(date.getDate())}`,
      lunar: `${lunar.getMonthInChinese()}月${lunar.getDayInChinese()}`
    }
  }

  const startDateInfo = formatDate(startTime)
  const endDateInfo = formatDate(endTime)

  return (
    <div className="jiri-detail-wrapper">
      {/* 导航栏 */}
      <div className="jiri-detail-nav">
        <div className="jiri-nav-back" onClick={handleBack}>
          <ChevronLeft className="w-6 h-6" />
        </div>
        <div className={`jiri-nav-title ${type === '2' ? 'ji-color' : ''}`}>
          {yijiName}
        </div>
        <div className="jiri-nav-right"></div>
      </div>

      {/* 顶部信息 */}
      <div className="jiri-detail-top">
        <div className="p-4">
          {/* 日期选择 */}
          <div className="jiri-date-select">
            <div className="date-select-left">
              <div className="date-row" onClick={() => setShowStartPicker(true)}>
                <span className="date-label">开始</span>
                <span className="date-value">{startDateInfo.solar} {startDateInfo.lunar}</span>
                <ChevronDown className="w-4 h-4" />
              </div>
              <div className="date-row" onClick={() => setShowEndPicker(true)}>
                <span className="date-label">结束</span>
                <span className="date-value">{endDateInfo.solar} {endDateInfo.lunar}</span>
                <ChevronDown className="w-4 h-4" />
              </div>
            </div>
            <div className="date-select-right">
              <Switch
                checked={isWeekShow}
                onCheckedChange={setIsWeekShow}
                className="data-[state=checked]:bg-destructive"
              />
              <span className="weekend-label">只看周末</span>
            </div>
          </div>

          {/* 宜忌说明 */}
          <div className={`jiri-info-box ${type === '2' ? 'ji-bg' : ''}`}>
            <div className="info-name-badge">
              <div className="info-name-inner">{yijiName}</div>
            </div>
            <div className="info-count">区间内{yijiName}的日子有{dayNum}天</div>
            <div className="info-desc">
              {name}是指{todesMap[name] || '相关活动'}
            </div>
          </div>
        </div>
      </div>

      {/* 吉日列表 */}
      <div className="jiri-day-list">
        {displayDays.map((solar, index) => {
          const lunar = solar.getLunar()
          const daysLater = solar.subtract(today)

          return (
            <div key={index} className="jiri-item-card">
              <div className="p-3">
                <div className="jiri-item-content">
                  {/* 天数标签 */}
                  <div className="days-later">
                    {daysLater > 0 ? `${daysLater}天后` : daysLater === 0 ? '今天' : `${Math.abs(daysLater)}天前`}
                  </div>

                  {/* 日期卡片 */}
                  <div className="date-card">
                    <div className="date-ym">
                      {solar.getYear()}.{addZero(solar.getMonth())}
                    </div>
                    <div className="date-d">{addZero(solar.getDay())}</div>
                    <div className="date-w">周{daysLater > 0 ? '未知' : solar.getWeekInChinese()}</div>
                  </div>

                  {/* 详细信息 */}
                  <div className="date-info">
                    <div className="info-lunar">
                      {lunar.getMonthInChinese()}月{lunar.getDayInChinese()}
                    </div>
                    <div className="info-ganzhi">
                      {lunar.getYearInGanZhi()}年 {lunar.getMonthInGanZhi()}月 {lunar.getDayInGanZhi()}日
                    </div>
                    <div className="info-shen">
                      值神: {lunar.getDayTianShen()} &nbsp;&nbsp; 十二神: {lunar.getZhiXing()}日
                    </div>
                    <div className="info-shen">
                      星宿: {lunar.getXiu()}{lunar.getZheng()}{lunar.getAnimal()}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )
        })}

        {displayDays.length === 0 && (
          <div className="empty-list">
            <p>该时间范围内没有符合条件的日期</p>
          </div>
        )}
      </div>

      {/* 日期选择器弹窗 */}
      {showStartPicker && (
        <DatePickerModal
          title="选择开始日期"
          onConfirm={handleConfirmStart}
          onClose={() => setShowStartPicker(false)}
        />
      )}
      {showEndPicker && (
        <DatePickerModal
          title="选择结束日期"
          onConfirm={handleConfirmEnd}
          onClose={() => setShowEndPicker(false)}
        />
      )}

      <style>{`
        .jiri-detail-wrapper {
          min-height: calc(100vh - 120px);
          padding-bottom: 20px;
        }

        .jiri-detail-nav {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 12px 16px;
          background: hsl(var(--card));
          border-radius: 12px;
          margin-bottom: 16px;
          position: sticky;
          top: 0;
          z-index: 50;
        }

        .jiri-nav-back {
          cursor: pointer;
          padding: 4px;
          border-radius: 8px;
          transition: background 0.2s;
        }

        .jiri-nav-back:hover {
          background: hsl(var(--accent));
        }

        .jiri-nav-title {
          color: hsl(var(--jiri-yi));
          font-size: 16px;
          font-weight: 500;
        }

        .jiri-nav-title.ji-color {
          color: hsl(var(--jiri-ji));
        }

        .jiri-nav-right {
          width: 32px;
        }

        .jiri-detail-top {
          margin-bottom: 16px;
        }

        .jiri-date-select {
          display: flex;
          gap: 16px;
          margin-bottom: 16px;
        }

        .date-select-left {
          flex: 1;
        }

        .date-row {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 8px;
          cursor: pointer;
          padding: 4px 0;
        }

        .date-label {
          color: hsl(var(--jiri-text));
          font-size: 14px;
        }

        .date-value {
          font-weight: bold;
          font-size: 14px;
        }

        .date-select-right {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 6px;
          width: 80px;
        }

        .weekend-label {
          color: hsl(var(--jiri-text));
          font-size: 12px;
        }

        .jiri-info-box {
          border: 1px solid hsl(var(--jiri-border));
          background: hsl(var(--jiri-yi-light));
          border-radius: 10px;
          padding: 16px;
          text-align: center;
        }

        .jiri-info-box.ji-bg {
          background: hsl(var(--jiri-ji-light));
        }

        .info-name-badge {
          display: inline-block;
          border: 1px solid hsl(var(--jiri-border));
          padding: 3px;
          border-radius: 6px;
          margin-bottom: 10px;
        }

        .info-name-inner {
          border: 1px solid hsl(var(--jiri-border));
          border-radius: 4px;
          padding: 4px 16px;
          font-size: 15px;
        }

        .info-count {
          font-weight: bold;
          margin-bottom: 6px;
        }

        .info-desc {
          color: hsl(var(--muted-foreground));
          font-size: 14px;
        }

        .jiri-list {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .jiri-item-card {
          overflow: visible;
        }

        .jiri-item-content {
          display: flex;
          gap: 12px;
          position: relative;
        }

        .days-later {
          position: absolute;
          top: 0;
          right: 0;
          color: hsl(var(--jiri-text));
          font-size: 12px;
        }

        .date-card {
          width: 72px;
          border: 1px solid hsl(var(--jiri-ji));
          color: hsl(var(--jiri-ji));
          padding: 10px 8px;
          text-align: center;
          border-radius: 10px;
          flex-shrink: 0;
        }

        .date-ym {
          font-size: 12px;
          margin-bottom: 4px;
        }

        .date-d {
          font-size: 24px;
          font-weight: bold;
          margin-bottom: 4px;
        }

        .date-w {
          font-size: 12px;
        }

        .date-info {
          flex: 1;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          padding-right: 50px;
        }

        .info-lunar {
          font-weight: bold;
          font-size: 16px;
        }

        .info-ganzhi {
          font-size: 13px;
          font-weight: 500;
        }

        .info-shen {
          color: hsl(var(--muted-foreground));
          font-size: 13px;
        }

        .empty-list {
          text-align: center;
          padding: 40px;
          color: hsl(var(--muted-foreground));
        }
      `}</style>
    </div>
  )
}
