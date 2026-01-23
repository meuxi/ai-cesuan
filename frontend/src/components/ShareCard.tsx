/**
 * 分享卡片组件
 * 提供可分享的占卜结果卡片UI
 */

import React, { useRef, useState } from 'react';
import { Download, Share2, Copy, Check, Loader2 } from 'lucide-react';
import { downloadShareCard, copyToClipboard, shareCard } from '../utils/shareCard';
import { logger } from '@/utils/logger';
import { SITE_CONFIG } from '@/config/constants';

interface ShareCardProps {
    title: string;
    children: React.ReactNode;
    watermark?: string;
    showShareButton?: boolean;
    showDownloadButton?: boolean;
    showCopyButton?: boolean;
    className?: string;
    onShare?: () => void;
    onDownload?: () => void;
}

export const ShareCard: React.FC<ShareCardProps> = ({
    title,
    children,
    watermark = SITE_CONFIG.watermark,
    showShareButton = true,
    showDownloadButton = true,
    showCopyButton = true,
    className = '',
    onShare,
    onDownload,
}) => {
    const cardRef = useRef<HTMLDivElement>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [copied, setCopied] = useState(false);

    const handleDownload = async () => {
        if (!cardRef.current) return;

        setIsLoading(true);
        try {
            await downloadShareCard(
                { element: cardRef.current },
                `${title}-${Date.now()}.png`
            );
            onDownload?.();
        } catch (error) {
            logger.error('下载失败:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCopy = async () => {
        if (!cardRef.current) return;

        setIsLoading(true);
        try {
            const success = await copyToClipboard({ element: cardRef.current });
            if (success) {
                setCopied(true);
                setTimeout(() => setCopied(false), 2000);
            }
        } catch (error) {
            logger.error('复制失败:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleShare = async () => {
        if (!cardRef.current) return;

        setIsLoading(true);
        try {
            await shareCard(
                { element: cardRef.current },
                { title: `${SITE_CONFIG.name} - ${title}`, text: `查看我的${title}结果 | ${SITE_CONFIG.url}` }
            );
            onShare?.();
        } catch (error) {
            logger.error('分享失败:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="space-y-4">
            {/* 可截图的卡片区域 */}
            <div
                ref={cardRef}
                className={`bg-gradient-to-br from-amber-50 to-orange-50 dark:from-gray-800 dark:to-gray-900 
                    p-6 rounded-xl shadow-lg border border-amber-200 dark:border-border ${className}`}
            >
                {/* 标题 */}
                <h3 className="text-xl font-bold text-center text-amber-800 dark:text-amber-400 mb-4">
                    {title}
                </h3>

                {/* 内容 */}
                <div className="text-muted-foreground">
                    {children}
                </div>

                {/* 水印 */}
                {watermark && (
                    <div className="mt-4 pt-4 border-t border-amber-200 dark:border-border text-center">
                        <span className="text-xs text-muted-foreground/70">
                            {watermark}
                        </span>
                    </div>
                )}
            </div>

            {/* 操作按钮 */}
            <div className="flex justify-center gap-3">
                {showDownloadButton && (
                    <button
                        onClick={handleDownload}
                        disabled={isLoading}
                        className="flex items-center gap-2 px-4 py-2 bg-amber-600 hover:bg-amber-700 
                       text-white rounded-lg transition-colors disabled:opacity-50"
                    >
                        {isLoading ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                            <Download className="w-4 h-4" />
                        )}
                        <span>下载图片</span>
                    </button>
                )}

                {showCopyButton && (
                    <button
                        onClick={handleCopy}
                        disabled={isLoading}
                        className="flex items-center gap-2 px-4 py-2 bg-secondary hover:bg-secondary/80 
                       text-secondary-foreground rounded-lg transition-colors disabled:opacity-50"
                    >
                        {copied ? (
                            <>
                                <Check className="w-4 h-4" />
                                <span>已复制</span>
                            </>
                        ) : (
                            <>
                                <Copy className="w-4 h-4" />
                                <span>复制图片</span>
                            </>
                        )}
                    </button>
                )}

                {showShareButton && (
                    <button
                        onClick={handleShare}
                        disabled={isLoading}
                        className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 
                       text-white rounded-lg transition-colors disabled:opacity-50"
                    >
                        <Share2 className="w-4 h-4" />
                        <span>分享</span>
                    </button>
                )}
            </div>
        </div>
    );
};

/**
 * 占卜结果分享卡片
 */
interface DivinationShareCardProps {
    type: string;
    result: string;
    interpretation?: string;
    date?: string;
}

export const DivinationShareCard: React.FC<DivinationShareCardProps> = ({
    type,
    result,
    interpretation,
    date = new Date().toLocaleDateString('zh-CN'),
}) => {
    return (
        <ShareCard title={type}>
            <div className="space-y-4">
                {/* 结果 */}
                <div className="text-center">
                    <div className="text-2xl font-bold text-amber-700 dark:text-amber-400 mb-2">
                        {result}
                    </div>
                </div>

                {/* 解读 */}
                {interpretation && (
                    <div className="bg-white/50 dark:bg-card/50 rounded-lg p-4">
                        <p className="text-sm leading-relaxed">{interpretation}</p>
                    </div>
                )}

                {/* 日期 */}
                <div className="text-right text-xs text-muted-foreground">
                    {date}
                </div>
            </div>
        </ShareCard>
    );
};

export default ShareCard;
