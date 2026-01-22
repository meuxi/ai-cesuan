/**
 * AI分析结果内嵌组件
 * 使用网站统一主题样式
 */

import DOMPurify from 'dompurify'
import ResultActions from './ResultActions'

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
            {loading ? (
                <div className="flex flex-col items-center justify-center space-y-3 py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-2 border-muted border-t-primary"></div>
                    <p className="text-sm text-muted-foreground">AI 正在为您解读...</p>
                </div>
            ) : result ? (
                <>
                    <div id="inline-result" className={streaming ? 'streaming-content' : ''}>
                        <div
                            className="prose prose-neutral max-w-none dark:prose-invert prose-headings:font-semibold prose-headings:text-foreground prose-p:text-muted-foreground prose-p:leading-relaxed prose-li:text-muted-foreground"
                            dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(result) }}
                        />
                        {streaming && (
                            <span className="inline-flex w-1 h-5 ml-1 bg-foreground cursor-blink align-middle rounded-sm"></span>
                        )}
                    </div>
                    {!streaming && (
                        <ResultActions
                            result={result.replace(/<[^>]*>/g, '')}
                            title={title}
                            elementId="inline-result"
                        />
                    )}
                </>
            ) : null}
        </div>
    )
}
