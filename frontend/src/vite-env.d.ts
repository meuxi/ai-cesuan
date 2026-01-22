/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE?: string
  readonly VITE_IS_TAURI?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare module 'virtual:pwa-register' {
  export interface RegisterSWOptions {
    immediate?: boolean
    onNeedRefresh?: () => void
    onOfflineReady?: () => void
    onRegistered?: (registration: ServiceWorkerRegistration | undefined) => void
    onRegisterError?: (error: any) => void
  }

  export function registerSW(options?: RegisterSWOptions): (reloadPage?: boolean) => Promise<void>
}

declare module 'lunar-javascript' {
  export class Solar {
    static fromYmdHms(
      year: number,
      month: number,
      day: number,
      hour: number,
      minute: number,
      second: number
    ): Solar
    static fromDate(date: Date): Solar
    static fromYmd(year: number, month: number, day: number): Solar
    getLunar(): Lunar
    getYear(): number
    getMonth(): number
    getDay(): number
    getWeek(): number
    getWeekInChinese(): string
    next(days: number): Solar
    subtract(solar: Solar): number
    getFestivals(): string[]
    getOtherFestivals(): string[]
  }

  export class SolarMonth {
    static fromYm(year: number, month: number): SolarMonth
    getDays(): Solar[]
    next(months: number): SolarMonth
  }

  export class Lunar {
    static fromDate(date: Date): Lunar
    toFullString(): string
    getYear(): number
    getMonth(): number
    getDay(): number
    getMonthInChinese(): string
    getDayInChinese(): string
    getYearInGanZhi(): string
    getYearShengXiao(): string
    getMonthInGanZhi(): string
    getDayInGanZhi(): string
    getTimeInGanZhi(): string
    getDayYi(): string[]
    getDayJi(): string[]
    getDayNaYin(): string
    getDayShengXiao(): string
    getDayChongShengXiao(): string
    getDayTianShen(): string
    getDayTianShenLuck(): string
    getTimeTianShenLuck(): string
    getDayPositionCaiDesc(): string
    getDayPositionXiDesc(): string
    getDayPositionYangGuiDesc(): string
    getDayPositionFuDesc(): string
    getPengZuGan(): string
    getPengZuZhi(): string
    getTimes(): LunarTime[]
    getJieQi(): string
    getFestivals(): string[]
    getZhiXing(): string
    getXiu(): string
    getZheng(): string
    getAnimal(): string
    toString(): string
  }

  export class LunarTime {
    getGanZhi(): string
  }

  export class HolidayUtil {
    static getHoliday(year: number, month: number, day: number): Holiday | null
  }

  export interface Holiday {
    isWork(): boolean
    getName(): string
  }
}
