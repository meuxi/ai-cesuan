/**
 * 宫位详情弹窗组件
 * 显示选中宫位的完整星曜信息和解读
 */

import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import type { EnhancedPalace, StarWithMutagen } from '@/types/ziwei'

interface PalaceDetailDialogProps {
    palace: EnhancedPalace | null
    open: boolean
    onOpenChange: (open: boolean) => void
}

// 星曜亮度说明
const BRIGHTNESS_DESC: Record<string, { label: string; color: string; desc: string }> = {
    '庙': { label: '庙', color: 'bg-red-500 text-white', desc: '最旺，星曜力量发挥到极致' },
    '旺': { label: '旺', color: 'bg-orange-500 text-white', desc: '次旺，力量强劲' },
    '得': { label: '得', color: 'bg-amber-500 text-white', desc: '得地，力量适中偏强' },
    '利': { label: '利', color: 'bg-green-500 text-white', desc: '得利，力量适中' },
    '平': { label: '平', color: 'bg-slate-500 text-white', desc: '平和，力量一般' },
    '不': { label: '不', color: 'bg-blue-500 text-white', desc: '不得，力量偏弱' },
    '陷': { label: '陷', color: 'bg-purple-500 text-white', desc: '落陷，力量最弱' },
}

// 四化说明
const MUTAGEN_DESC: Record<string, { label: string; color: string; desc: string }> = {
    '禄': { label: '化禄', color: 'bg-green-600 text-white', desc: '财禄、顺遂、增益' },
    '权': { label: '化权', color: 'bg-red-600 text-white', desc: '权力、主导、掌控' },
    '科': { label: '化科', color: 'bg-blue-600 text-white', desc: '名声、贵人、文采' },
    '忌': { label: '化忌', color: 'bg-purple-600 text-white', desc: '困扰、阻碍、执念' },
}

// 宫位基本含义
const PALACE_MEANINGS: Record<string, string> = {
    '命宫': '个人性格、气质、天赋能力、一生运势总论',
    '兄弟宫': '兄弟姐妹、朋友关系、同事合作',
    '夫妻宫': '婚姻感情、配偶特质、恋爱运势',
    '子女宫': '子女缘分、生育、下属关系、投资运',
    '财帛宫': '正财收入、理财能力、金钱态度',
    '疾厄宫': '健康状况、潜在疾病、意外灾厄',
    '迁移宫': '出外运势、旅行、外地发展、人际交往',
    '交友宫': '交友状况、贵人运、社交圈',
    '官禄宫': '事业发展、工作能力、职业成就',
    '田宅宫': '不动产、家庭环境、居住运势',
    '福德宫': '精神状态、思想境界、享受运、晚年运',
    '父母宫': '父母缘分、长辈关系、遗传特质',
}

function StarItem({ star, showDesc = false }: { star: StarWithMutagen; showDesc?: boolean }) {
    const brightness = star.brightness ? BRIGHTNESS_DESC[star.brightness] : null
    const isMajor = star.type === 'major'

    return (
        <div className={`flex items-center justify-between p-2 rounded-lg ${isMajor ? 'bg-red-50 dark:bg-red-950/30' : 'bg-slate-50 dark:bg-slate-900/30'}`}>
            <div className="flex items-center gap-2">
                <span className={`font-medium ${isMajor ? 'text-red-600 dark:text-red-400 text-base' : 'text-blue-600 dark:text-blue-400 text-sm'}`}>
                    {star.name}
                </span>
                {brightness && (
                    <Badge className={`text-xs ${brightness.color}`}>
                        {brightness.label}
                    </Badge>
                )}
                {star.mutagen?.map((m, i) => {
                    const key = m.replace(/[本限年月日时]/g, '')
                    const info = MUTAGEN_DESC[key]
                    return info ? (
                        <Badge key={i} className={`text-xs ${info.color}`}>
                            {m}
                        </Badge>
                    ) : null
                })}
            </div>
            {showDesc && brightness && (
                <span className="text-xs text-muted-foreground">{brightness.desc}</span>
            )}
        </div>
    )
}

export function PalaceDetailDialog({ palace, open, onOpenChange }: PalaceDetailDialogProps) {
    if (!palace) return null

    const meaning = PALACE_MEANINGS[palace.name] || '宫位含义'

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="max-w-md max-h-[85vh]">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <span className="text-xl">{palace.name}</span>
                        <span className="text-base text-muted-foreground">
                            {palace.heavenlyStem}{palace.earthlyBranch}
                        </span>
                        {palace.isBodyPalace && (
                            <Badge variant="outline" className="bg-amber-100 text-amber-700 border-amber-300">
                                身宫
                            </Badge>
                        )}
                    </DialogTitle>
                </DialogHeader>

                <ScrollArea className="max-h-[65vh] pr-4">
                    <div className="space-y-4">
                        {/* 宫位含义 */}
                        <div className="p-3 bg-secondary/50 rounded-lg">
                            <div className="text-xs text-muted-foreground mb-1">宫位含义</div>
                            <div className="text-sm">{meaning}</div>
                        </div>

                        {/* 主星 */}
                        {palace.majorStars.length > 0 && (
                            <div>
                                <div className="text-sm font-medium mb-2 flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-red-500"></span>
                                    主星 ({palace.majorStars.length})
                                </div>
                                <div className="space-y-2">
                                    {palace.majorStars.map((star, idx) => (
                                        <StarItem key={idx} star={star} showDesc />
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* 辅星 */}
                        {palace.minorStars.length > 0 && (
                            <div>
                                <div className="text-sm font-medium mb-2 flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-blue-500"></span>
                                    辅星与杂曜 ({palace.minorStars.length})
                                </div>
                                <div className="space-y-1.5">
                                    {palace.minorStars.map((star, idx) => (
                                        <StarItem key={idx} star={star} />
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* 大限信息 */}
                        {palace.decadeInfo && (
                            <div className="p-3 bg-primary/10 rounded-lg">
                                <div className="text-xs text-muted-foreground mb-1">大限</div>
                                <div className="text-sm font-medium">
                                    {palace.decadeInfo.startAge}-{palace.decadeInfo.endAge}岁
                                    {palace.decadeInfo.isCurrent && (
                                        <Badge className="ml-2 bg-primary text-primary-foreground">当前大限</Badge>
                                    )}
                                </div>
                            </div>
                        )}

                        {/* 小限年龄 */}
                        {palace.extras?.ages && palace.extras.ages.length > 0 && (
                            <div className="p-3 bg-blue-50 dark:bg-blue-950/30 rounded-lg">
                                <div className="text-xs text-muted-foreground mb-1">小限年龄</div>
                                <div className="text-sm">
                                    {palace.extras.ages.join('、')}岁
                                </div>
                            </div>
                        )}

                        {/* 四化说明 */}
                        <div className="p-3 bg-secondary/30 rounded-lg">
                            <div className="text-xs text-muted-foreground mb-2">四化说明</div>
                            <div className="grid grid-cols-2 gap-2 text-xs">
                                {Object.entries(MUTAGEN_DESC).map(([key, info]) => (
                                    <div key={key} className="flex items-center gap-1">
                                        <Badge className={`text-xs ${info.color}`}>{info.label}</Badge>
                                        <span className="text-muted-foreground">{info.desc}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </ScrollArea>
            </DialogContent>
        </Dialog>
    )
}
