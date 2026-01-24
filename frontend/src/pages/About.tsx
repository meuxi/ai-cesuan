import { ABOUT } from '@/config/constants'
import { ArrowLeft } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'

const md = new MarkdownIt()

// 安全渲染 Markdown：先渲染再 sanitize，防止 XSS
const safeRenderMarkdown = (content: string): string => {
  return DOMPurify.sanitize(md.render(content))
}

export default function AboutPage() {
  const navigate = useNavigate()

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          返回
        </button>
      </div>

      {/* Page Title */}
      <div className="text-center py-8">
        <h1 className="text-4xl md:text-5xl font-bold mb-4 text-foreground">
          关于占卜
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          了解各种占卜方式的起源与含义
        </p>
      </div>

      {/* Content Card */}
      <div className="rounded-xl border border-border bg-card p-6 md:p-10">
        <div
          className="prose prose-neutral max-w-none dark:prose-invert 
            prose-headings:font-semibold prose-headings:text-foreground
            prose-h1:text-2xl prose-h1:mb-6 prose-h1:mt-8 prose-h1:border-b prose-h1:border-border prose-h1:pb-4
            prose-h2:text-xl prose-h2:mb-4 prose-h2:mt-6
            prose-p:text-muted-foreground prose-p:leading-relaxed
            prose-li:text-muted-foreground
            prose-strong:text-foreground
            prose-ul:my-4 prose-li:my-1"
          dangerouslySetInnerHTML={{ __html: safeRenderMarkdown(ABOUT) }}
        />
      </div>
    </div>
  )
}
