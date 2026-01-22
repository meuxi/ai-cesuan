/**
 * 奇门遁甲九宫格组件
 * 美观的九宫布局展示
 */

import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

export interface GongData {
  position: number
  gong_name: string
  ba_men: string
  jiu_xing: string
  ba_shen: string
  tian_pan_gan: string
  di_pan_gan: string
}

interface QimenGridProps {
  jiugong: GongData[]
  className?: string
}

// 八门颜色映射
const BAMEN_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  '开门': { bg: 'bg-emerald-500/20', text: 'text-emerald-600 dark:text-emerald-400', border: 'border-emerald-500/50' },
  '休门': { bg: 'bg-blue-500/20', text: 'text-blue-600 dark:text-blue-400', border: 'border-blue-500/50' },
  '生门': { bg: 'bg-green-500/20', text: 'text-green-600 dark:text-green-400', border: 'border-green-500/50' },
  '伤门': { bg: 'bg-orange-500/20', text: 'text-orange-600 dark:text-orange-400', border: 'border-orange-500/50' },
  '杜门': { bg: 'bg-purple-500/20', text: 'text-purple-600 dark:text-purple-400', border: 'border-purple-500/50' },
  '景门': { bg: 'bg-red-500/20', text: 'text-red-600 dark:text-red-400', border: 'border-red-500/50' },
  '死门': { bg: 'bg-gray-500/20', text: 'text-gray-600 dark:text-gray-400', border: 'border-gray-500/50' },
  '惊门': { bg: 'bg-yellow-500/20', text: 'text-yellow-600 dark:text-yellow-400', border: 'border-yellow-500/50' },
}

// 九星颜色映射
const JIUXING_COLORS: Record<string, string> = {
  '天蓬': 'text-blue-500',
  '天任': 'text-yellow-600 dark:text-yellow-400',
  '天冲': 'text-green-500',
  '天辅': 'text-emerald-500',
  '天英': 'text-red-500',
  '天芮': 'text-orange-500',
  '天柱': 'text-gray-500',
  '天心': 'text-purple-500',
  '天禽': 'text-amber-600 dark:text-amber-400',
}

// 八神颜色映射
const BASHEN_COLORS: Record<string, string> = {
  '值符': 'text-amber-500',
  '腾蛇': 'text-red-400',
  '太阴': 'text-indigo-400',
  '六合': 'text-green-400',
  '白虎': 'text-gray-300 dark:text-gray-500',
  '玄武': 'text-slate-600 dark:text-slate-400',
  '九地': 'text-yellow-700 dark:text-yellow-500',
  '九天': 'text-cyan-500',
}

// 宫位名称映射
const GONG_NAMES: Record<string, { icon: string; direction: string }> = {
  '巽四宫': { icon: '☴', direction: '东南' },
  '离九宫': { icon: '☲', direction: '南' },
  '坤二宫': { icon: '☷', direction: '西南' },
  '震三宫': { icon: '☳', direction: '东' },
  '中五宫': { icon: '☯', direction: '中' },
  '兑七宫': { icon: '☱', direction: '西' },
  '艮八宫': { icon: '☶', direction: '东北' },
  '坎一宫': { icon: '☵', direction: '北' },
  '乾六宫': { icon: '☰', direction: '西北' },
}

// 九宫排列顺序（后天八卦）
const GRID_ORDER = [3, 8, 1, 2, 4, 6, 7, 0, 5] // 巽4 离9 坤2 / 震3 中5 兑7 / 艮8 坎1 乾6

export function QimenGrid({ jiugong, className }: QimenGridProps) {
  return (
    <div className={cn('w-full max-w-lg mx-auto', className)}>
      {/* 九宫背景装饰 */}
      <div className="relative">
        {/* 太极图装饰（中宫背景） */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-5">
          <div className="w-32 h-32 rounded-full border-4 border-current" />
        </div>
        
        {/* 九宫格 */}
        <div className="grid grid-cols-3 gap-2 p-2 bg-card/50 rounded-2xl border border-border backdrop-blur-sm">
          {GRID_ORDER.map((idx, gridIdx) => {
            const gong = jiugong[idx]
            if (!gong) {
              return (
                <div 
                  key={gridIdx}
                  className="aspect-square rounded-xl bg-muted/50 border border-border"
                />
              )
            }
            
            const bamenStyle = BAMEN_COLORS[gong.ba_men] || BAMEN_COLORS['开门']
            const jiuxingColor = JIUXING_COLORS[gong.jiu_xing] || 'text-foreground'
            const bashenColor = BASHEN_COLORS[gong.ba_shen] || 'text-muted-foreground'
            const gongInfo = GONG_NAMES[gong.gong_name] || { icon: '☯', direction: '' }
            const isCenter = gong.position === 5
            
            return (
              <motion.div
                key={gridIdx}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: gridIdx * 0.05, duration: 0.3 }}
                className={cn(
                  'aspect-square rounded-xl p-2 flex flex-col border-2 transition-all duration-300',
                  'hover:scale-[1.02] hover:shadow-lg cursor-default',
                  bamenStyle.bg,
                  bamenStyle.border,
                  isCenter && 'ring-2 ring-primary/50'
                )}
              >
                {/* 顶部：宫位名称 + 方向 */}
                <div className="flex items-center justify-between text-[10px]">
                  <span className="text-lg">{gongInfo.icon}</span>
                  <span className="text-muted-foreground font-medium">{gongInfo.direction}</span>
                </div>
                
                {/* 中部：八门（主要信息） */}
                <div className="flex-1 flex flex-col items-center justify-center">
                  <span className={cn('text-lg font-bold', bamenStyle.text)}>
                    {gong.ba_men}
                  </span>
                  <span className={cn('text-xs font-medium', jiuxingColor)}>
                    {gong.jiu_xing}
                  </span>
                </div>
                
                {/* 底部：八神 + 天地盘 */}
                <div className="space-y-0.5">
                  <div className={cn('text-[10px] text-center font-medium', bashenColor)}>
                    {gong.ba_shen}
                  </div>
                  <div className="flex justify-center gap-1 text-[9px] text-muted-foreground border-t border-border/50 pt-0.5">
                    <span className="text-amber-500" title="天盘">天{gong.tian_pan_gan}</span>
                    <span>/</span>
                    <span className="text-emerald-500" title="地盘">地{gong.di_pan_gan}</span>
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
      
      {/* 图例 */}
      <div className="mt-4 p-3 bg-secondary/50 rounded-lg">
        <p className="text-xs text-center text-muted-foreground mb-2">八门吉凶</p>
        <div className="flex flex-wrap justify-center gap-2">
          {[
            { name: '开', type: '吉', color: 'bg-emerald-500' },
            { name: '休', type: '吉', color: 'bg-blue-500' },
            { name: '生', type: '吉', color: 'bg-green-500' },
            { name: '景', type: '中', color: 'bg-red-500' },
            { name: '杜', type: '中', color: 'bg-purple-500' },
            { name: '伤', type: '凶', color: 'bg-orange-500' },
            { name: '死', type: '凶', color: 'bg-gray-500' },
            { name: '惊', type: '凶', color: 'bg-yellow-500' },
          ].map(item => (
            <div key={item.name} className="flex items-center gap-1 text-[10px]">
              <div className={cn('w-2 h-2 rounded-full', item.color)} />
              <span className="text-muted-foreground">{item.name}门</span>
              <span className={cn(
                'px-1 rounded',
                item.type === '吉' ? 'bg-green-500/20 text-green-600 dark:text-green-400' :
                item.type === '凶' ? 'bg-red-500/20 text-red-600 dark:text-red-400' :
                'bg-yellow-500/20 text-yellow-600 dark:text-yellow-400'
              )}>
                {item.type}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// 奇门时间信息组件
interface QimenTimeInfoProps {
  timeInfo: {
    solar_date: string
    lunar_date: string
    jie_qi: string
    sizhu: { year: string; month: string; day: string; hour: string }
  }
  panInfo: {
    description: string
    yin_yang: string
    ju_shu: number
  }
}

export function QimenTimeInfo({ timeInfo, panInfo }: QimenTimeInfoProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      {/* 局数信息 - 突出显示 */}
      <div className="bg-gradient-to-r from-primary/20 via-primary/10 to-primary/20 rounded-xl p-4 text-center border border-primary/30">
        <p className="text-2xl font-bold text-foreground">
          {panInfo.description}
        </p>
        <p className="text-sm text-muted-foreground mt-1">
          {panInfo.yin_yang} · 第{panInfo.ju_shu}局
        </p>
      </div>
      
      {/* 时间详情 */}
      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="p-3 rounded-lg bg-secondary/50">
          <span className="text-muted-foreground">公历</span>
          <p className="font-medium text-foreground">{timeInfo.solar_date}</p>
        </div>
        <div className="p-3 rounded-lg bg-secondary/50">
          <span className="text-muted-foreground">农历</span>
          <p className="font-medium text-foreground">{timeInfo.lunar_date}</p>
        </div>
        <div className="p-3 rounded-lg bg-secondary/50">
          <span className="text-muted-foreground">节气</span>
          <p className="font-medium text-foreground">{timeInfo.jie_qi}</p>
        </div>
        <div className="p-3 rounded-lg bg-secondary/50 col-span-2">
          <span className="text-muted-foreground">四柱</span>
          <div className="flex justify-center gap-4 mt-1">
            {['year', 'month', 'day', 'hour'].map((key, i) => (
              <div key={key} className="text-center">
                <p className="font-bold text-foreground">
                  {timeInfo.sizhu[key as keyof typeof timeInfo.sizhu]}
                </p>
                <p className="text-[10px] text-muted-foreground">
                  {['年柱', '月柱', '日柱', '时柱'][i]}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  )
}
