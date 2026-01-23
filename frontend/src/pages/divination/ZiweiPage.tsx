/**
 * 紫微斗数页面
 * 使用iztro库实现完整专业功能
 */

import { useState, useEffect, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import { Solar } from 'lunar-javascript'
import { logger } from '@/utils/logger'
import SEOHead, { SEO_CONFIG } from '@/components/SEOHead'
import { Label } from '@/components/ui/label'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { toast } from 'sonner'
import { saveHistory } from '@/utils/divinationHistory'
import { Compass, Calculator, Sparkles, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

import { ziweiServiceProfessional } from '@/services/ziweiServiceProfessional'
import { ZiweiChartGrid, type HoroscopeHighlight, type HoroscopeInfo } from '@/components/ziwei/ZiweiChartGrid'
import { ZiweiHoroscopePanelEnhanced, type ZiweiHoroscopePanelRef } from '@/components/ziwei/ZiweiHoroscopePanelEnhanced'
import type { ZiweiResult } from '@/types/ziwei'

export default function ZiweiPage() {
    const { t } = useTranslation()
    const [birthday, setBirthday] = useLocalStorage('ziwei_birthday', '2000-08-17T12:00')
    const [gender, setGender] = useLocalStorage('ziwei_gender', 'male')
    const [algorithm, setAlgorithm] = useLocalStorage('ziwei_algorithm', 'default')  // 派别选择
    const [lunarInfo, setLunarInfo] = useState('')
    const [ziweiData, setZiweiData] = useState<ZiweiResult | null>(null)
    const [panLoading, setPanLoading] = useState(false)
    const [horoscopeHighlight, setHoroscopeHighlight] = useState<HoroscopeHighlight>({})
    const [horoscopeInfo, setHoroscopeInfo] = useState<HoroscopeInfo | undefined>(undefined)

    // 运限面板 ref（用于中宫快捷日期切换）
    const horoscopePanelRef = useRef<ZiweiHoroscopePanelRef>(null)

    const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
        useDivination('ziwei')

    // 计算农历
    const computeLunar = (birthdayStr: string) => {
        try {
            const date = new Date(birthdayStr)
            const solar = Solar.fromYmdHms(
                date.getFullYear(),
                date.getMonth() + 1,
                date.getDate(),
                date.getHours(),
                date.getMinutes(),
                0
            )
            const lunar = solar.getLunar()
            const hour = date.getHours()
            const shiZhi = getShiZhi(hour)
            setLunarInfo(`${lunar.getYearInGanZhi()}年 ${lunar.getMonthInChinese()}月 ${lunar.getDayInChinese()} ${shiZhi}时`)
        } catch (error) {
            logger.error('农历转换失败:', error)
            setLunarInfo('转换失败')
        }
    }

    // 监听生日变化
    useEffect(() => {
        computeLunar(birthday)
    }, [birthday])

    // 步骤1：专业排盘计算
    const handleCalculate = async () => {
        const date = new Date(birthday)

        try {
            setPanLoading(true)

            // 使用后端专业服务计算（支持派别选择）
            const ziweiResult = await ziweiServiceProfessional.calculate({
                year: date.getFullYear(),
                month: date.getMonth() + 1,
                day: date.getDate(),
                hour: date.getHours(),
                minute: date.getMinutes(),
                gender: gender as 'male' | 'female',
                language: 'zh-CN',
                algorithm: algorithm as 'default' | 'zhongzhou'  // 派别参数
            })

            setZiweiData(ziweiResult)

            // 保存历史记录
            const fourPillarsStr = `${ziweiResult.basicInfo.fourPillars.year.stem}${ziweiResult.basicInfo.fourPillars.year.branch} ${ziweiResult.basicInfo.fourPillars.month.stem}${ziweiResult.basicInfo.fourPillars.month.branch} ${ziweiResult.basicInfo.fourPillars.day.stem}${ziweiResult.basicInfo.fourPillars.day.branch} ${ziweiResult.basicInfo.fourPillars.hour.stem}${ziweiResult.basicInfo.fourPillars.hour.branch}`
            saveHistory({
                type: 'ziwei',
                title: `${ziweiResult.solarDate} ${gender === 'male' ? '男' : '女'} 紫微排盘`,
                prompt: `生日: ${ziweiResult.solarDate}, 性别: ${gender === 'male' ? '男' : '女'}`,
                result: `**命主**: ${ziweiResult.basicInfo.soul}\n**身主**: ${ziweiResult.basicInfo.body}\n**五行局**: ${ziweiResult.basicInfo.fiveElement}\n**四柱**: ${fourPillarsStr}`,
                metadata: {
                    birthday: ziweiResult.solarDate,
                    gender: gender,
                    lunarDate: `${ziweiResult.lunarDate.year}年${Math.abs(ziweiResult.lunarDate.month)}月${ziweiResult.lunarDate.day}日`,
                    fourPillars: fourPillarsStr,
                }
            })

            toast.success(t('ziwei.paipanSuccess'))
        } catch (error: unknown) {
            const message = error instanceof Error ? error.message : '排盘失败，请重试'
            toast.error(message)
            logger.error('紫微排盘错误:', error)
        } finally {
            setPanLoading(false)
        }
    }

    // 步骤2：AI分析
    const handleAIAnalysis = () => {
        onSubmit({
            prompt: `紫微斗数命盘深度解读`,
            birthday: birthday,
            gender: gender,
            lunar_info: lunarInfo,
            ziwei_data: ziweiData,
        })
    }

    // 渲染专业命盘格子
    const renderProfessionalPalaceGrid = () => {
        if (!ziweiData) return null

        return (
            <div className="mt-6">
                <Card>
                    <CardHeader>
                        <CardTitle className="text-center text-lg font-semibold">
                            {t('ziwei.chartTitle')}
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {/* 基本信息 */}
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3 mb-4 sm:mb-6">
                            <div className="bg-secondary/50 rounded-lg p-2.5 sm:p-3 text-center">
                                <div className="text-[10px] sm:text-xs text-muted-foreground mb-1">{t('ziwei.fiveElementJu')}</div>
                                <div className="font-semibold text-sm sm:text-base text-foreground">{ziweiData.basicInfo.fiveElement}</div>
                            </div>
                            <div className="bg-secondary/50 rounded-lg p-2.5 sm:p-3 text-center">
                                <div className="text-[10px] sm:text-xs text-muted-foreground mb-1">{t('ziwei.mingPalace')}</div>
                                <div className="font-semibold text-sm sm:text-base text-foreground">
                                    {ziweiData.palaces.find(p => p.name === '命宮')?.earthlyBranch || '-'}
                                </div>
                            </div>
                            <div className="bg-secondary/50 rounded-lg p-2.5 sm:p-3 text-center">
                                <div className="text-[10px] sm:text-xs text-muted-foreground mb-1">{t('ziwei.shenPalace')}</div>
                                <div className="font-semibold text-sm sm:text-base text-foreground">
                                    {ziweiData.palaces.find(p => p.isBodyPalace)?.earthlyBranch || '-'}
                                </div>
                            </div>
                            <div className="bg-secondary/50 rounded-lg p-2.5 sm:p-3 text-center">
                                <div className="text-[10px] sm:text-xs text-muted-foreground mb-1">{t('ziwei.hourBranch')}</div>
                                <div className="font-semibold text-sm sm:text-base text-foreground">{ziweiData.basicInfo.fourPillars.hour.branch}时</div>
                            </div>
                        </div>

                        {/* 四柱信息 */}
                        <div className="grid grid-cols-4 gap-1.5 sm:gap-3 mb-4 sm:mb-6">
                            <div className="bg-primary/10 rounded-lg p-2 sm:p-3 text-center">
                                <div className="text-[10px] sm:text-xs text-muted-foreground mb-1">{t('ziwei.yearPillar')}</div>
                                <div className="font-semibold text-sm sm:text-base text-primary">{ziweiData.basicInfo.fourPillars.year.stem}{ziweiData.basicInfo.fourPillars.year.branch}</div>
                            </div>
                            <div className="bg-primary/10 rounded-lg p-2 sm:p-3 text-center">
                                <div className="text-[10px] sm:text-xs text-muted-foreground mb-1">{t('ziwei.monthPillar')}</div>
                                <div className="font-semibold text-sm sm:text-base text-primary">{ziweiData.basicInfo.fourPillars.month.stem}{ziweiData.basicInfo.fourPillars.month.branch}</div>
                            </div>
                            <div className="bg-primary/10 rounded-lg p-2 sm:p-3 text-center">
                                <div className="text-[10px] sm:text-xs text-muted-foreground mb-1">{t('ziwei.dayPillar')}</div>
                                <div className="font-semibold text-sm sm:text-base text-primary">{ziweiData.basicInfo.fourPillars.day.stem}{ziweiData.basicInfo.fourPillars.day.branch}</div>
                            </div>
                            <div className="bg-primary/10 rounded-lg p-2 sm:p-3 text-center">
                                <div className="text-[10px] sm:text-xs text-muted-foreground mb-1">{t('ziwei.hourPillar')}</div>
                                <div className="font-semibold text-sm sm:text-base text-primary">{ziweiData.basicInfo.fourPillars.hour.stem}{ziweiData.basicInfo.fourPillars.hour.branch}</div>
                            </div>
                        </div>

                        {/* 十二宫格 - 专业版 */}
                        <ZiweiChartGrid
                            data={ziweiData}
                            horoscopeHighlight={horoscopeHighlight}
                            horoscopeInfo={horoscopeInfo}
                            onHoroscopeDateChange={(scope, delta) => {
                                // 通过 ref 调用运限面板的日期切换方法
                                horoscopePanelRef.current?.handleDateChange(scope, delta)
                            }}
                        />

                        {/* 运限面板 */}
                        <div className="mt-6">
                            <h3 className="text-sm font-medium mb-3 flex items-center gap-2">
                                <span className="w-1 h-4 bg-primary rounded-full"></span>
                                {t('ziwei.horoscopeAnalysis')}
                            </h3>
                            <ZiweiHoroscopePanelEnhanced
                                ref={horoscopePanelRef}
                                data={ziweiData}
                                onHighlightChange={setHoroscopeHighlight}
                                onHoroscopeInfoChange={setHoroscopeInfo}
                            />
                        </div>

                        {/* 详细信息标签页 */}
                        <Tabs defaultValue="stars" className="mt-4 sm:mt-6">
                            <TabsList className="grid w-full grid-cols-3 text-xs sm:text-sm">
                                <TabsTrigger value="stars" className="px-1 sm:px-3">{t('ziwei.starsDetail')}</TabsTrigger>
                                <TabsTrigger value="decades" className="px-1 sm:px-3">{t('ziwei.decadeInfo')}</TabsTrigger>
                                <TabsTrigger value="mutagen" className="px-1 sm:px-3">{t('ziwei.mutagenAnalysis')}</TabsTrigger>
                            </TabsList>
                            <TabsContent value="stars" className="mt-3 sm:mt-4">
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-4">
                                    {ziweiData.palaces.map((palace, index) => (
                                        <Card key={index} className="p-3">
                                            <div className="font-medium text-sm mb-2">
                                                {palace.name} ({palace.earthlyBranch}宫)
                                                {palace.heavenlyStem && <span className="ml-2 text-xs text-muted-foreground">{palace.heavenlyStem}</span>}
                                            </div>
                                            <div className="space-y-1">
                                                {palace.majorStars.map((star, starIndex) => (
                                                    <div key={starIndex} className="flex items-center gap-2 text-xs">
                                                        <span className="font-medium text-red-600">{star.name}</span>
                                                        {star.brightness && (
                                                            <Badge variant="outline" className="text-xs">
                                                                {star.brightness}
                                                            </Badge>
                                                        )}
                                                    </div>
                                                ))}
                                                {palace.minorStars.slice(0, 3).map((star, starIndex) => (
                                                    <div key={starIndex} className="flex items-center gap-2 text-xs">
                                                        <span className="text-blue-600">{star.name}</span>
                                                        {star.brightness && (
                                                            <Badge variant="outline" className="text-xs">
                                                                {star.brightness}
                                                            </Badge>
                                                        )}
                                                    </div>
                                                ))}
                                            </div>
                                        </Card>
                                    ))}
                                </div>
                            </TabsContent>
                            <TabsContent value="decades" className="mt-3 sm:mt-4">
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-4">
                                    {ziweiData.decades.map((decade, index) => (
                                        <Card key={index} className="p-3">
                                            <div className="font-medium text-sm mb-2">
                                                {decade.startAge}-{decade.endAge}岁 {decade.palaceName}
                                            </div>
                                            <div className="text-xs text-muted-foreground">
                                                天干: {decade.heavenlyStem} 地支: {decade.earthlyBranch}
                                            </div>
                                        </Card>
                                    ))}
                                </div>
                            </TabsContent>
                            <TabsContent value="mutagen" className="mt-4">
                                {ziweiData.mutagenInfo ? (
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                        <Card className="p-3">
                                            <div className="text-sm font-medium mb-2">{t('ziwei.natalMutagen')}</div>
                                            <div className="space-y-1 text-xs">
                                                <div>化禄: {ziweiData.mutagenInfo.natal.lu || '-'}</div>
                                                <div>化权: {ziweiData.mutagenInfo.natal.quan || '-'}</div>
                                                <div>化科: {ziweiData.mutagenInfo.natal.ke || '-'}</div>
                                                <div>化忌: {ziweiData.mutagenInfo.natal.ji || '-'}</div>
                                            </div>
                                        </Card>
                                    </div>
                                ) : (
                                    <div className="text-center text-muted-foreground">{t('ziwei.noMutagenInfo')}</div>
                                )}
                            </TabsContent>
                        </Tabs>
                    </CardContent>
                </Card>
            </div>
        )
    }

    return (
        <DivinationCardHeader
            title={t('ziwei.title')}
            description={t('ziwei.description')}
            icon={Compass}
            divinationType="ziwei"
        >
            <div className="max-w-4xl mx-auto w-full">
                <div className="space-y-4 sm:space-y-5">
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4">
                        <div className="sm:col-span-2 md:col-span-1">
                            <Label className="block mb-2 text-sm font-medium text-foreground">{t('ziwei.birthTime')}</Label>
                            <input
                                type="datetime-local"
                                value={birthday}
                                onChange={(e) => {
                                    setBirthday(e.target.value)
                                    computeLunar(e.target.value)
                                }}
                                className="w-full px-3 py-2.5 text-base sm:text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                            />
                        </div>
                        <div>
                            <Label className="block mb-2 text-sm font-medium text-foreground">{t('ziwei.genderLabel')}</Label>
                            <select
                                value={gender}
                                onChange={(e) => setGender(e.target.value)}
                                className="w-full px-3 py-2.5 text-base sm:text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                            >
                                <option value="male">{t('ziwei.genderMale')}</option>
                                <option value="female">{t('ziwei.genderFemale')}</option>
                            </select>
                        </div>
                        <div>
                            <Label className="block mb-2 text-sm font-medium text-foreground">{t('ziwei.algorithmLabel')}</Label>
                            <select
                                value={algorithm}
                                onChange={(e) => setAlgorithm(e.target.value)}
                                className="w-full px-3 py-2.5 text-base sm:text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                            >
                                <option value="default">{t('ziwei.algorithmDefault')}</option>
                                <option value="zhongzhou">{t('ziwei.algorithmZhongzhou')}</option>
                            </select>
                        </div>
                    </div>

                    <div>
                        <Label className="text-sm font-medium text-foreground">{t('ziwei.lunarLabel')}</Label>
                        <p className="text-sm mt-2 text-muted-foreground">{lunarInfo}</p>
                    </div>
                </div>

                {/* 步骤1：排盘按钮 */}
                {!ziweiData && (
                    <div className="mt-6">
                        <Button
                            onClick={handleCalculate}
                            disabled={panLoading}
                            className="w-full h-12"
                        >
                            {panLoading ? (
                                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />{t('ziwei.paipaning')}</>
                            ) : (
                                <><Calculator className="w-4 h-4 mr-2" />{t('ziwei.startPaipan')}</>
                            )}
                        </Button>
                    </div>
                )}

                {/* 步骤2：命盘展示 + AI分析按钮 */}
                {ziweiData && (
                    <>
                        {renderProfessionalPalaceGrid()}

                        {!result && !loading && (
                            <div className="mt-4">
                                <Button
                                    onClick={handleAIAnalysis}
                                    disabled={loading}
                                    className="w-full h-12"
                                >
                                    <Sparkles className="w-4 h-4 mr-2" />
                                    {t('ziwei.startAIAnalysis')}
                                </Button>
                            </div>
                        )}
                    </>
                )}

                {/* 步骤3：AI分析结果 */}
                <InlineResult
                    result={result}
                    loading={resultLoading}
                    streaming={streaming}
                    title={t('ziwei.aiAnalysis')}
                />
            </div>
        </DivinationCardHeader>
    )
}

// 辅助函数
function getShiZhi(hour: number): string {
    const shiZhiMap = ['子', '丑', '丑', '寅', '寅', '卯', '卯', '辰', '辰', '巳', '巳', '午', '午', '未', '未', '申', '申', '酉', '酉', '戌', '戌', '亥', '亥', '子']
    return shiZhiMap[hour] || '子'
}
