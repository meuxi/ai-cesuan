/**
 * 分享卡片工具
 * 来源：MingAI src/lib/share-card.ts
 * 使用html2canvas将DOM元素转换为可分享的图片
 */

import html2canvas from 'html2canvas';

export interface ShareCardOptions {
    /** 卡片容器元素 */
    element: HTMLElement;
    /** 图片质量 (0-1) */
    quality?: number;
    /** 背景色，默认白色 */
    backgroundColor?: string;
    /** 缩放比例，默认 2 以获得高清图 */
    scale?: number;
    /** 忽略的元素选择器 */
    ignoreElements?: (element: Element) => boolean;
}

/**
 * 将 DOM 元素转换为图片 Blob
 */
export async function captureToBlob(options: ShareCardOptions): Promise<Blob> {
    const {
        element,
        quality = 0.95,
        backgroundColor = '#ffffff',
        scale = 2,
        ignoreElements
    } = options;

    const canvas = await html2canvas(element, {
        backgroundColor,
        scale,
        useCORS: true,
        logging: false,
        allowTaint: true,
        ignoreElements
    });

    return new Promise((resolve, reject) => {
        canvas.toBlob(
            (blob) => {
                if (blob) {
                    resolve(blob);
                } else {
                    reject(new Error('无法生成图片'));
                }
            },
            'image/png',
            quality
        );
    });
}

/**
 * 将 DOM 元素转换为 Data URL
 */
export async function captureToDataURL(options: ShareCardOptions): Promise<string> {
    const {
        element,
        quality = 0.95,
        backgroundColor = '#ffffff',
        scale = 2,
        ignoreElements
    } = options;

    const canvas = await html2canvas(element, {
        backgroundColor,
        scale,
        useCORS: true,
        logging: false,
        allowTaint: true,
        ignoreElements
    });

    return canvas.toDataURL('image/png', quality);
}

/**
 * 下载分享卡片图片
 */
export async function downloadShareCard(
    options: ShareCardOptions,
    filename: string = 'divination-card.png'
): Promise<void> {
    const blob = await captureToBlob(options);
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
}

/**
 * 复制图片到剪贴板
 */
export async function copyToClipboard(options: ShareCardOptions): Promise<boolean> {
    try {
        const blob = await captureToBlob(options);

        if (navigator.clipboard && navigator.clipboard.write) {
            const item = new ClipboardItem({ 'image/png': blob });
            await navigator.clipboard.write([item]);
            return true;
        }

        return false;
    } catch (error) {
        console.error('复制到剪贴板失败:', error);
        return false;
    }
}

/**
 * 分享到社交平台（使用 Web Share API，若不支持则下载）
 */
export async function shareCard(
    options: ShareCardOptions,
    shareData: {
        title?: string;
        text?: string;
        filename?: string;
    } = {}
): Promise<{ shared: boolean; method: 'share' | 'download' }> {
    try {
        const blob = await captureToBlob(options);
        const filename = shareData.filename || 'divination-card.png';
        const file = new File([blob], filename, { type: 'image/png' });

        // 检查是否支持 Web Share API
        if (navigator.canShare && navigator.canShare({ files: [file] })) {
            await navigator.share({
                title: shareData.title || '占卜结果',
                text: shareData.text || '查看我的占卜结果',
                files: [file],
            });
            return { shared: true, method: 'share' };
        }

        // 不支持 Web Share API，退回下载
        await downloadShareCard(options, filename);
        return { shared: true, method: 'download' };
    } catch (error) {
        console.error('分享失败:', error);
        throw error;
    }
}

/**
 * 生成分享卡片的默认样式类
 */
export const shareCardStyles = {
    container: 'bg-white dark:bg-gray-900 p-6 rounded-xl shadow-lg',
    title: 'text-xl font-bold text-center mb-4',
    content: 'text-gray-700 dark:text-gray-300',
    footer: 'mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 text-center text-sm text-gray-500',
    watermark: 'text-xs text-gray-400 mt-2',
};

/**
 * 默认水印文字
 */
export const defaultWatermark = '由 AI测算 (cesuan.tech) 生成';
