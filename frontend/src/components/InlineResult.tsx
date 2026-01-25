/**
 * AI分析结果内嵌组件
 * 使用网站统一主题样式
 */

import ResultActions from './ResultActions'
import { ResultContent } from '@/components/common'

interface InlineResultProps {
    result: string | null
    loading: boolean
    streaming?: boolean
    title: string
}

export function InlineResult({ result, loading, streaming, title }: InlineResultProps) {
    if (!result && !loading) {
        return null
    }

    return (
        <div className="mt-6">
            <ResultContent
                result={result}
                loading={loading}
                streaming={streaming}
                contentType="markdown"
                id="inline-result"
                loadingConfig={{
                    text: 'AI 正在为您解读...',
                    size: 'md'
                }}
                className={loading ? 'py-8' : ''}
                actions={
                    result ? (
                        <ResultActions
                            result={result.replace(/<[^>]*>/g, '')}
                            title={title}
                            elementId="inline-result"
                        />
                    ) : null
                }
            />
        </div>
    )
}
