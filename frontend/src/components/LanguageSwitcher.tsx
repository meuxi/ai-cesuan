/**
 * 语言切换器组件
 * 支持：简体中文、繁體中文、English、日本語
 */

import { useState, useRef, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { Globe, ChevronDown } from 'lucide-react'

const languages = [
    { code: 'zh', label: '简体中文' },
    { code: 'zh-TW', label: '繁體中文' },
    { code: 'en', label: 'English' },
    { code: 'ja', label: '日本語' },
]

export default function LanguageSwitcher() {
    const { i18n } = useTranslation()
    const [isOpen, setIsOpen] = useState(false)
    const dropdownRef = useRef<HTMLDivElement>(null)

    // 获取当前语言
    const getCurrentLang = () => {
        const lang = i18n.language
        // 精确匹配
        const exact = languages.find(l => l.code === lang)
        if (exact) return exact
        // 前缀匹配
        if (lang.startsWith('zh-TW') || lang.startsWith('zh-HK')) return languages[1]
        if (lang.startsWith('zh')) return languages[0]
        if (lang.startsWith('en')) return languages[2]
        if (lang.startsWith('ja')) return languages[3]
        return languages[0]
    }

    const currentLang = getCurrentLang()

    // 点击外部关闭下拉菜单
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    const changeLanguage = (code: string) => {
        i18n.changeLanguage(code)
        setIsOpen(false)
    }

    return (
        <div className="relative" ref={dropdownRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm text-sidebar-foreground/70 hover:bg-sidebar-accent rounded-lg transition-colors"
            >
                <Globe className="w-4 h-4" />
                <span>{currentLang.label}</span>
                <ChevronDown className={`w-3 h-3 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>

            {isOpen && (
                <div className="absolute bottom-full left-0 right-0 mb-1 bg-popover border border-border rounded-lg shadow-lg overflow-hidden z-50">
                    {languages.map((lang) => (
                        <button
                            key={lang.code}
                            onClick={() => changeLanguage(lang.code)}
                            className={`w-full px-4 py-2 text-sm text-left hover:bg-accent transition-colors ${currentLang.code === lang.code ? 'bg-accent text-accent-foreground' : 'text-popover-foreground'
                                }`}
                        >
                            {lang.label}
                        </button>
                    ))}
                </div>
            )}
        </div>
    )
}
