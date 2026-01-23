import { useState } from 'react'
import { Button } from './ui/button'
import { Copy, Share2, Download, Check } from 'lucide-react'
import { toast } from 'sonner'
import html2canvas from 'html2canvas'
import { logger } from '@/utils/logger'
import { SITE_CONFIG } from '@/config/constants'

interface ResultActionsProps {
  result: string
  title: string
  elementId?: string
}

export default function ResultActions({ result, title, elementId = 'divination-result' }: ResultActionsProps) {
  const [copied, setCopied] = useState(false)
  const [exporting, setExporting] = useState(false)

  // 复制结果（带网站信息）
  const handleCopy = async () => {
    try {
      const textWithSiteInfo = `${result}\n\n━━━━━━━━━━━━━━━\n🔮 ${SITE_CONFIG.name} | ${SITE_CONFIG.url}\n${SITE_CONFIG.slogan}\n${SITE_CONFIG.copyright}`
      await navigator.clipboard.writeText(textWithSiteInfo)
      setCopied(true)
      toast.success('已复制到剪贴板')
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      toast.error('复制失败，请手动复制')
    }
  }

  // 分享到社交媒体（带网站信息）
  const handleShare = async () => {
    const shareData = {
      title: `${SITE_CONFIG.name} - ${title}`,
      text: `${result.substring(0, 100)}...\n\n🔮 来自 ${SITE_CONFIG.name}`,
      url: SITE_CONFIG.url,
    }

    try {
      if (navigator.share) {
        await navigator.share(shareData)
        toast.success('分享成功')
      } else {
        // 降级方案：复制链接
        await navigator.clipboard.writeText(`${shareData.text}\n${SITE_CONFIG.url}`)
        toast.success('链接已复制，可以分享给朋友')
      }
    } catch (error: any) {
      if (error.name !== 'AbortError') {
        toast.error('分享失败')
      }
    }
  }

  // 导出为图片（带网站信息和二维码）
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

      // 动态导入 qrcode 库
      const QRCode = await import('qrcode')

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

      // 捕获内容区域
      const contentCanvas = await html2canvas(element, {
        backgroundColor: '#ffffff',
        scale: 3,
        logging: false,
        useCORS: true,
        allowTaint: true,
        onclone: (clonedDoc) => {
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

      // 生成二维码
      const qrCodeDataUrl = await QRCode.toDataURL(SITE_CONFIG.url, {
        width: 240,
        margin: 1,
        color: { dark: '#1a1a2e', light: '#ffffff' }
      })

      // 加载二维码图片
      const qrImage = new Image()
      qrImage.src = qrCodeDataUrl
      await new Promise((resolve) => { qrImage.onload = resolve })

      // 创建最终画布（内容 + 底部信息栏）
      const footerHeight = 180 * 3  // 底部信息栏高度（考虑scale=3）
      const finalCanvas = document.createElement('canvas')
      finalCanvas.width = contentCanvas.width
      finalCanvas.height = contentCanvas.height + footerHeight
      const ctx = finalCanvas.getContext('2d')!

      // 绘制内容区域
      ctx.drawImage(contentCanvas, 0, 0)

      // 绘制底部信息栏背景（渐变）
      const gradient = ctx.createLinearGradient(0, contentCanvas.height, 0, finalCanvas.height)
      gradient.addColorStop(0, '#f8f5f0')
      gradient.addColorStop(1, '#f0ebe4')
      ctx.fillStyle = gradient
      ctx.fillRect(0, contentCanvas.height, finalCanvas.width, footerHeight)

      // 绘制分隔线
      ctx.strokeStyle = '#d4a574'
      ctx.lineWidth = 3
      ctx.beginPath()
      ctx.moveTo(60, contentCanvas.height + 30)
      ctx.lineTo(finalCanvas.width - 60, contentCanvas.height + 30)
      ctx.stroke()

      // 绘制二维码（右侧）
      const qrSize = 140 * 3
      const qrX = finalCanvas.width - qrSize - 60
      const qrY = contentCanvas.height + 60
      ctx.drawImage(qrImage, qrX, qrY, qrSize, qrSize)

      // 绘制网站信息（左侧）
      const textX = 80
      let textY = contentCanvas.height + 100

      // 网站名称
      ctx.fillStyle = '#8b4513'
      ctx.font = 'bold 72px "Noto Serif SC", serif'
      ctx.fillText(`🔮 ${SITE_CONFIG.name}`, textX, textY)

      // 网站域名
      textY += 90
      ctx.fillStyle = '#6b4423'
      ctx.font = '54px "Noto Serif SC", serif'
      ctx.fillText(SITE_CONFIG.url, textX, textY)

      // slogan
      textY += 80
      ctx.fillStyle = '#8b7355'
      ctx.font = '42px "Noto Serif SC", serif'
      ctx.fillText(SITE_CONFIG.slogan, textX, textY)

      // 扫码提示
      textY += 70
      ctx.fillStyle = '#a08060'
      ctx.font = '36px "Noto Serif SC", serif'
      ctx.fillText('扫码访问 →', textX, textY)

      // 版权信息（底部居中）
      ctx.fillStyle = '#999'
      ctx.font = '30px "Noto Serif SC", serif'
      ctx.textAlign = 'center'
      ctx.fillText(SITE_CONFIG.copyright, finalCanvas.width / 2, finalCanvas.height - 40)

      // 转换为图片并下载
      finalCanvas.toBlob((blob) => {
        if (blob) {
          const url = URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.download = `${SITE_CONFIG.name}-${title}-${Date.now()}.png`
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

