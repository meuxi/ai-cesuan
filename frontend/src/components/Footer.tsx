/**
 * 网站页脚组件
 * 简洁版：版权 + 链接 + 声明
 */

import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

export default function Footer() {
    const { t } = useTranslation()
    const currentYear = new Date().getFullYear()

    return (
        <footer className="border-t border-border mt-auto">
            <div className="max-w-6xl mx-auto px-3 sm:px-4 py-3 sm:py-4">
                <div className="flex flex-col items-center gap-1.5 sm:gap-2 text-[10px] sm:text-xs text-muted-foreground">
                    {/* 版权 + 链接 */}
                    <div className="flex flex-wrap items-center justify-center gap-x-2 sm:gap-x-4 gap-y-1">
                        <span>© {currentYear} {t('common.appName')}</span>
                        <span className="hidden sm:inline text-border">|</span>
                        <Link to="/about" className="hover:text-foreground transition-colors">
                            {t('footer.about')}
                        </Link>
                        <span className="text-border">|</span>
                        <Link to="/terms" className="hover:text-foreground transition-colors">
                            {t('footer.terms')}
                        </Link>
                        <span className="text-border">|</span>
                        <Link to="/privacy" className="hover:text-foreground transition-colors">
                            {t('footer.privacy')}
                        </Link>
                        <span className="text-border">|</span>
                        <Link to="/disclaimer" className="hover:text-foreground transition-colors">
                            {t('footer.disclaimer')}
                        </Link>
                    </div>
                    {/* 声明 */}
                    <p className="text-center leading-relaxed px-2">
                        {t('footer.notice')}
                    </p>
                </div>
            </div>
        </footer>
    )
}
