import { Solar, SolarMonth, HolidayUtil, Lunar, LunarTime } from 'lunar-javascript'

export const weekList = [
    { label: '日', value: 0 },
    { label: '一', value: 1 },
    { label: '二', value: 2 },
    { label: '三', value: 3 },
    { label: '四', value: 4 },
    { label: '五', value: 5 },
    { label: '六', value: 6 },
]

export const yijiList = [
    {
        type: '热门',
        childrens: '嫁娶 开市 置产 入宅 出行 盖屋 会亲友 订盟 祈福',
    },
    {
        type: '婚姻',
        childrens: '嫁娶 安床 纳采 问名 纳婿 合帐',
    },
    {
        type: '生活',
        childrens: '会亲友 扫舍 入学 伐木 探病 出行 理发 栽种 针灸 习艺 求医 移徙',
    },
    {
        type: '工商',
        childrens: '开市 赴任 立券 开仓 订盟 交易 出货财 纳财 置产',
    },
    {
        type: '建筑',
        childrens: '入宅 动士 开渠 作梁 盖屋 作灶 上梁 造仓 掘井',
    },
    {
        type: '祭祀',
        childrens: '祭祀 祈福 安香 求嗣 入殓 修坟 开光 安葬 行丧',
    },
]

export const todesMap: Record<string, string> = {
    '嫁娶': '男娶女嫁,举行大典的吉日',
    '安床': '指安置睡床卧铺之意',
    '纳采': '古代汉族婚姻风俗',
    '问名': '中国婚姻礼仪之一。西周六礼中第二礼',
    '纳婿': '男方入赘于女方为婿',
    '合帐': '是单位管理人员分类建立的账目、原始资料或记录',
    '会亲友': '与亲戚朋友联络交往',
    '扫舍': '扫去房顶灰尘和家中死角的尘土',
    '入学': '学童初次进入学校读书',
    '伐木': '采伐林木',
    '探病': '探望病人',
    '出行': '出发去异地旅游、考察、公差等',
    '理发': '初生婴儿第一次剃胎发或出家之落',
    '栽种': '栽种植物',
    '针灸': '使用针灸的方法治疗身体',
    '习艺': '学习技艺',
    '求医': '去看医生',
    '移徙': '搬动住处;迁移',
    '开市': '开门营业,开始贸易',
    '赴任': '到某地担任职务',
    '立券': '订立各种契约互相买卖之事',
    '开仓': '买卖',
    '订盟': '婚姻说合,送订婚礼金',
    '交易': '投资,买卖等交易之事',
    '出货财': '发货、销货和促销',
    '纳财': '黄道日历里购屋产业、进货、收帐、收租等',
    '置产': '购置物件',
    '入宅': '旧家搬到新家去',
    '动士': '建筑房屋时,按所择日时,用锄头在吉方锄下第一锄土的时间',
    '开渠': '开通河道或水沟',
    '作梁': '乔迁新居的时候,就可以选择吉日来庆祝乔迁的日子',
    '盖屋': '装盖房屋的屋顶等工作',
    '作灶': '安修厨灶、厨炉移位',
    '上梁': '装上建筑物屋顶的梁木,同架马',
    '造仓': '建造仓库或修理仓库',
    '掘井': '开凿水井',
    '祭祀': '一种信仰活动,源于天地和谐共生的信仰理念',
    '祈福': '祈求神明降福还愿的仪式',
    '安香': '安土地公或祖先之神位',
    '求嗣': '指向神明祈求后嗣(子孙)之意',
    '入殓': '将尸体放入棺材之意',
    '修坟': '旧墓修理及添葬之日',
    '开光': '世俗中的挂牌仪式,或揭牌仪式',
    '安葬': '葬礼举行埋葬仪式',
    '行丧': '举办丧事',
}

export const addZero = (num: number): string => {
    return num > 9 ? String(num) : '0' + num
}

export function getYearWeek(year: number, month: number, date: number): number {
    const dateNow = new Date(year, month - 1, date)
    const dateFirst = new Date(year, 0, 1)
    const dataNumber = Math.round((dateNow.valueOf() - dateFirst.valueOf()) / 86400000)
    return Math.ceil((dataNumber + (dateFirst.getDay() + 1 - 1)) / 7)
}

export const getMonthDays = (year: number, month: number): Solar[] => {
    const d = SolarMonth.fromYm(year, month)
    const days = d.getDays()
    const firstweek = days[0].getWeek()

    const prevMonth = d.next(-1)
    const prevDays = prevMonth.getDays()
    const prefixdate = prevDays.slice(prevDays.length - firstweek, prevDays.length)

    const lastweek = days[days.length - 1].getWeek()
    const nextMonth = d.next(1)
    const nextDays = nextMonth.getDays()
    const enddate = nextDays.slice(0, 6 - lastweek)

    return [...prefixdate, ...days, ...enddate]
}

export const getHolidayWork = (solar: Solar): boolean | undefined => {
    const d = HolidayUtil.getHoliday(solar.getYear(), solar.getMonth(), solar.getDay())
    return d?.isWork()
}

export interface DateInfo {
    yinli: string
    ganzhiyear: string
    ganzhimonth: string
    ganzhiday: string
    weeks: number
    dayyi: string[]
    dayji: string[]
    wuxing: string
    chongsha: string
    zhishen: string
    xishenpos: string
    yangguipos: string
    fushenpos: string
    caishenpos: string
    times: LunarTime[]
    xingqi: string
    pzbj: string
}

export const getDateInfo = (solar: Solar): DateInfo => {
    const lunar = solar.getLunar()
    const times = [...lunar.getTimes()]
    times.pop()

    return {
        yinli: lunar.getMonthInChinese() + '月' + lunar.getDayInChinese(),
        ganzhiyear: lunar.getYearInGanZhi() + lunar.getYearShengXiao() + '年',
        ganzhimonth: lunar.getMonthInGanZhi(),
        ganzhiday: lunar.getDayInGanZhi(),
        weeks: getYearWeek(solar.getYear(), solar.getMonth(), solar.getDay()),
        dayyi: lunar.getDayYi(),
        dayji: lunar.getDayJi(),
        wuxing: lunar.getDayNaYin(),
        xingqi: solar.getWeekInChinese(),
        pzbj: lunar.getPengZuGan() + ' ' + lunar.getPengZuZhi(),
        chongsha: lunar.getDayShengXiao() + '日冲' + lunar.getDayChongShengXiao(),
        zhishen: lunar.getDayTianShen(),
        caishenpos: lunar.getDayPositionCaiDesc(),
        xishenpos: lunar.getDayPositionXiDesc(),
        yangguipos: lunar.getDayPositionYangGuiDesc(),
        fushenpos: lunar.getDayPositionFuDesc(),
        times,
    }
}

export const getJiRiList = (
    type: '1' | '2',
    name: string,
    starttime: number,
    endtime: number
): Solar[] => {
    const solarList: Solar[] = []
    for (let i = starttime; i < endtime + 100; i = i + 86400000) {
        const solar = Solar.fromDate(new Date(i))
        const lunar = solar.getLunar()
        if (type === '1' && lunar.getDayYi().indexOf(name) !== -1) {
            solarList.push(solar)
        }
        if (type === '2' && lunar.getDayJi().indexOf(name) !== -1) {
            solarList.push(solar)
        }
    }
    return solarList
}

export const getTimeGanZhiLuck = (year: number, month: number, day: number, hour: number): string => {
    const lunar = Lunar.fromDate(new Date(year, month - 1, day, hour, 0, 0))
    return lunar.getTimeTianShenLuck()
}

export { Solar, SolarMonth, Lunar, HolidayUtil }
export type { LunarTime }
