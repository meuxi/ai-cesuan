import { useState } from 'react'
import { Button } from './ui/button'
import { Copy, Share2, Download, Check } from 'lucide-react'
import { toast } from 'sonner'
import html2canvas from 'html2canvas'
import { logger } from '@/utils/logger'

interface ResultActionsProps {
  result: string
  title: string
  elementId?: string
}

export default function ResultActions({ result, title, elementId = 'divination-result' }: ResultActionsProps) {
  const [copied, setCopied] = useState(false)
  const [exporting, setExporting] = useState(false)

  // 复制结果
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result)
      setCopied(true)
      toast.success('已复制到剪贴板')
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      toast.error('复制失败，请手动复制')
    }
  }

  // 分享到社交媒体
  const handleShare = async () => {
    const shareData = {
      title: `AI占卜 - ${title}`,
      text: result.substring(0, 100) + '...',
      url: window.location.href,
    }

    try {
      if (navigator.share) {
        await navigator.share(shareData)
        toast.success('分享成功')
      } else {
        // 降级方案：复制链接
        await navigator.clipboard.writeText(window.location.href)
        toast.success('链接已复制，可以分享给朋友')
      }
    } catch (error: any) {
      if (error.name !== 'AbortError') {
        toast.error('分享失败')
      }
    }
  }

  // 导出为图片
  const handleExportImage = async () => {
    setExporting(true)
    let element = null
    let proseElement = null
    let originalStyle = ''
    let originalClassName = ''
    let originalProseStyle = ''

    try {
      element = document.getElementById(elementId)
      if (!element) {
        toast.error('未找到要导出的内容')
        return
      }

      // 保存原始样式
      originalStyle = element.style.cssText
      originalClassName = element.className

      // 添加导出优化类
      element.className = `${originalClassName} export-optimized`
      element.style.cssText = `
        ${originalStyle}
        padding: 2.5rem !important;
        background: #ffffff !important;
        border-radius: 1rem !important;
        max-width: 800px !important;
        margin: 0 auto !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
      `

      // 临时修改内部prose元素样式
      proseElement = element.querySelector('.prose') as HTMLElement | null
      if (proseElement) {
        originalProseStyle = proseElement.style.cssText
        proseElement.style.cssText = `
          ${originalProseStyle}
          color: #2b2520 !important;
          font-size: 16px !important;
          line-height: 1.7 !important;
        `
      }

      const canvas = await html2canvas(element, {
        backgroundColor: '#ffffff',
        scale: 3,
        logging: false,
        useCORS: true,
        allowTaint: true,
        onclone: (clonedDoc) => {
          // 确保克隆的文档也有导出样式
          const clonedElement = clonedDoc.getElementById(elementId)
          if (clonedElement) {
            clonedElement.className = `${clonedElement.className} export-optimized`
            clonedElement.style.cssText = `
              padding: 2.5rem !important;
              background: #ffffff !important;
              border-radius: 1rem !important;
              max-width: 800px !important;
              margin: 0 auto !important;
              box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
            `

            const clonedProse = clonedElement.querySelector('.prose') as HTMLElement | null
            if (clonedProse) {
              clonedProse.style.cssText = `
                color: #2b2520 !important;
                font-size: 16px !important;
                line-height: 1.7 !important;
              `
            }
          }
        }
      })

      // 转换为图片并下载
      canvas.toBlob((blob) => {
        if (blob) {
          const url = URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.download = `占卜结果-${title}-${Date.now()}.png`
          link.href = url
          link.click()
          URL.revokeObjectURL(url)
          toast.success('图片已保存')
        }
      }, 'image/png')
    } catch (error) {
      logger.error('导出失败:', error)
      toast.error('导出失败，请重试')
    } finally {
      // 恢复原始样式
      if (element) {
        element.style.cssText = originalStyle
        element.className = originalClassName
      }
      if (proseElement && originalProseStyle) {
        proseElement.style.cssText = originalProseStyle
      }
      setExporting(false)
    }
  }

  return (
    <div className="flex flex-wrap gap-2 mt-6 pt-6 border-t border-border">
      <button
        onClick={handleCopy}
        className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium border border-input rounded-md bg-background text-muted-foreground hover:bg-accent transition-colors"
      >
        {copied ? (
          <>
            <Check className="h-4 w-4" />
            已复制
          </>
        ) : (
          <>
            <Copy className="h-4 w-4" />
            复制结果
          </>
        )}
      </button>

      <button
        onClick={handleShare}
        className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium border border-input rounded-md bg-background text-muted-foreground hover:bg-accent transition-colors"
      >
        <Share2 className="h-4 w-4" />
        分享
      </button>

      <button
        onClick={handleExportImage}
        disabled={exporting}
        className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium border border-input rounded-md bg-background text-muted-foreground hover:bg-accent transition-colors disabled:opacity-50"
      >
        <Download className="h-4 w-4" />
        {exporting ? '导出中...' : '导出图片'}
      </button>
    </div>
  )
}

