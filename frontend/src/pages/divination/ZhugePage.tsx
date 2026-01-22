/**
 * 诸葛神算页面
 * 基于后端 zhuge 模块实现
 */

import { useState } from 'react'
import { Label } from '@/components/ui/label'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { toast } from 'sonner'
import { BookOpen, Sparkles, Calculator, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'

const API_BASE = import.meta.env.VITE_API_BASE || ''

interface ZhugeResult {
    success: boolean
    input_chars: string[]
    bihua_list: number[]
    qian_number: number
    qian_id: string
    title: string
    content: string
    error?: string
}

export default function ZhugePage() {
    const [inputText, setInputText] = useState('')
    const [zhugeData, setZhugeData] = useState<ZhugeResult | null>(null)
    const [calcLoading, setCalcLoading] = useState(false)

    const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
        useDivination('zhuge')

    // 提取前三个汉字
    const getThreeChars = (text: string): string[] => {
        const chars = text.replace(/\s/g, '').split('')
        const hanziRegex = /[\u4e00-\u9fa5]/
        return chars.filter(c => hanziRegex.test(c)).slice(0, 3)
    }

    // 步骤1：计算签数
    const handleCalculate = async () => {
        const chars = getThreeChars(inputText)

        if (chars.length < 3) {
            toast.error('请输入至少三个汉字')
            return
        }

        try {
            setCalcLoading(true)

            const bihua = await getBihuaFromAI(chars)

            const response = await fetch(`${API_BASE}/api/zhuge/divine`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: chars.join(''),
                    bihua1: bihua[0],
                    bihua2: bihua[1],
                    bihua3: bihua[2],
                }),
            })

            if (!response.ok) {
                throw new Error('诸葛神算计算失败')
            }

            const zhugeResult = await response.json()

            if (!zhugeResult.success) {
                throw new Error(zhugeResult.error || '计算失败')
            }

            setZhugeData(zhugeResult)
        } catch (error: any) {
            toast.error(error.message || '诸葛神算失败，请重试')
            console.error('诸葛神算错误:', error)
        } finally {
            setCalcLoading(false)
        }
    }

    // 步骤2：AI解签
    const handleAIAnalysis = async () => {
        const chars = getThreeChars(inputText)
        const bihua = await getBihuaFromAI(chars)

        onSubmit({
            prompt: `诸葛神算解签`,
            input_text: inputText,
            chars: chars,
            bihua: bihua,
            qian_number: zhugeData?.qian_number,
            qian_title: zhugeData?.title,
        })
    }

    // 简化的笔画获取（实际应通过AI）
    const getBihuaFromAI = async (chars: string[]): Promise<number[]> => {
        // 常用汉字笔画表（简化版）
        const bihuaMap: Record<string, number> = {
            '一': 1, '二': 2, '三': 3, '四': 5, '五': 4, '六': 4, '七': 2, '八': 2, '九': 2, '十': 2,
            '天': 4, '地': 6, '人': 2, '和': 8, '平': 5, '安': 6, '福': 13, '禄': 12, '寿': 7, '喜': 12,
            '大': 3, '小': 3, '中': 4, '上': 3, '下': 3, '左': 5, '右': 5, '前': 9, '后': 6, '内': 4,
            '日': 4, '月': 4, '年': 6, '时': 7, '分': 4, '秒': 9, '春': 9, '夏': 10, '秋': 9, '冬': 5,
            '山': 3, '水': 4, '火': 4, '木': 4, '金': 8, '土': 3, '风': 4, '云': 4, '雨': 8, '雪': 11,
            '龙': 5, '虎': 8, '凤': 4, '龟': 7, '马': 3, '牛': 4, '羊': 6, '猪': 11, '狗': 8, '鸡': 7,
            '爱': 10, '情': 11, '心': 4, '意': 13, '志': 7, '思': 9, '想': 13, '念': 8, '感': 13, '觉': 9,
            '我': 7, '你': 7, '他': 5, '她': 6, '它': 5, '们': 5, '的': 8, '是': 9, '在': 6, '有': 6,
        }

        return chars.map(char => {
            if (bihuaMap[char]) {
                return bihuaMap[char]
            }
            // 默认返回随机笔画数（5-15）
            return Math.floor(Math.random() * 11) + 5
        })
    }

    const displayChars = getThreeChars(inputText)

    return (
        <DivinationCardHeader
            title="诸葛神算"
            description="三字测吉凶，诸葛亮神机妙算"
            icon={BookOpen}
            divinationType="zhuge"
        >
            <div className="max-w-2xl mx-auto w-full">
                <div className="space-y-6">
                    {/* 说明 */}
                    <div className="p-4 bg-secondary rounded-lg border border-border text-sm">
                        <p className="font-medium mb-2 text-foreground">诸葛神算使用说明</p>
                        <p className="text-muted-foreground">心诚则灵，请在心中默念所问之事，然后随意写下三个汉字。</p>
                        <p className="mt-1 text-muted-foreground">诸葛神数共384签，每签皆有玄机。</p>
                    </div>

                    {/* 输入区域 */}
                    <div>
                        <Label className="block mb-2 text-sm font-medium text-foreground">请输入三个汉字</Label>
                        <input
                            type="text"
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            placeholder="心诚默念后，随意写三个字..."
                            className="w-full px-3 py-2 text-lg text-center tracking-widest border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                            maxLength={10}
                        />

                        {/* 实时显示提取的汉字 */}
                        {displayChars.length > 0 && (
                            <div className="mt-3 flex justify-center gap-4">
                                {displayChars.map((char, index) => (
                                    <div
                                        key={index}
                                        className="w-16 h-16 flex items-center justify-center bg-secondary rounded-lg border border-border"
                                    >
                                        <span className="text-2xl font-bold text-foreground">
                                            {char}
                                        </span>
                                    </div>
                                ))}
                                {[...Array(3 - displayChars.length)].map((_, index) => (
                                    <div
                                        key={`empty-${index}`}
                                        className="w-16 h-16 flex items-center justify-center bg-secondary rounded-lg border-2 border-dashed border-border"
                                    >
                                        <span className="text-muted-foreground">?</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* 诸葛神算结果 */}
                    {zhugeData && zhugeData.success && (
                        <div className="p-6 bg-card rounded-xl border border-border">
                            <div className="text-center mb-4">
                                <Sparkles className="w-8 h-8 mx-auto text-muted-foreground mb-2" />
                                <h3 className="text-xl font-bold text-foreground">
                                    {zhugeData.title}
                                </h3>
                                <p className="text-sm text-muted-foreground mt-1">
                                    签号：第 {zhugeData.qian_number} 签
                                </p>
                            </div>

                            {/* 笔画信息 */}
                            <div className="grid grid-cols-3 gap-2 mb-4">
                                {zhugeData.input_chars.map((char, index) => (
                                    <div key={index} className="bg-secondary rounded-lg p-2 text-center">
                                        <div className="text-lg font-bold text-foreground">{char}</div>
                                        <div className="text-xs text-muted-foreground">
                                            {zhugeData.bihua_list[index]} 画
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* 计算过程 */}
                            <div className="text-center text-sm text-foreground bg-secondary rounded-lg p-3">
                                <p>
                                    笔画取个位：
                                    {zhugeData.bihua_list.map((b, i) => (
                                        <span key={i}>
                                            {b % 10 === 0 ? 1 : b % 10}
                                            {i < 2 ? ' → ' : ''}
                                        </span>
                                    ))}
                                </p>
                                <p className="mt-1">
                                    组成三位数后取签：第 <strong>{zhugeData.qian_number}</strong> 签
                                </p>
                            </div>
                        </div>
                    )}
                </div>

                {/* 步骤1：计算按钮 */}
                {!zhugeData && (
                    <div className="mt-6">
                        <Button
                            onClick={handleCalculate}
                            disabled={displayChars.length < 3 || calcLoading}
                            className="w-full h-12"
                        >
                            {calcLoading ? (
                                <><Loader2 className="w-4 h-4 mr-2 animate-spin" />正在计算...</>
                            ) : (
                                <><Calculator className="w-4 h-4 mr-2" />开始计算签数</>
                            )}
                        </Button>
                    </div>
                )}

                {/* 步骤2：AI解签按钮 */}
                {zhugeData && !result && !loading && (
                    <div className="mt-4">
                        <Button
                            onClick={handleAIAnalysis}
                            disabled={loading}
                            className="w-full h-12"
                        >
                            <Sparkles className="w-4 h-4 mr-2" />
                            开始 AI 解签
                        </Button>
                    </div>
                )}

                {/* 步骤3：AI解签结果 */}
                <InlineResult
                    result={result}
                    loading={resultLoading}
                    streaming={streaming}
                    title="诸葛神签解读"
                />
            </div>
        </DivinationCardHeader>
    )
}
