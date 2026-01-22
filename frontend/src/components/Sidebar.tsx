import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import {
    Calculator, Heart, Calendar, Compass, Sparkles, Star, Sun, Moon,
    BookOpen, Flower2, Users, Baby, Zap, Clock, TrendingUp, Menu, X,
    Settings, LogIn, LogOut, ChevronDown, ChevronRight, Unlock, Home
} from 'lucide-react'
import { useGlobalState } from '@/store'
import { useTranslation } from 'react-i18next'
import LanguageSwitcher from './LanguageSwitcher'

interface NavItem {
    href: string
    label: string
    icon: React.ElementType
}

interface NavGroup {
    title: string
    items: NavItem[]
}

const getNavGroups = (t: (key: string) => string): NavGroup[] => [
    {
        title: t('nav.baziGroup'),
        items: [
            { href: '/divination/birthday', label: t('nav.birthday'), icon: Calculator },
            { href: '/divination/hehun', label: t('nav.hehun'), icon: Heart },
            { href: '/divination/daily', label: t('nav.daily'), icon: Calendar },
        ]
    },
    {
        title: t('nav.ziweiGroup'),
        items: [
            { href: '/divination/ziwei', label: t('nav.ziwei'), icon: Compass },
        ]
    },
    {
        title: t('nav.zhouyiGroup'),
        items: [
            { href: '/divination/plum_flower', label: t('nav.plumFlower'), icon: Flower2 },
            { href: '/divination/monthly', label: t('nav.monthly'), icon: TrendingUp },
            { href: '/divination/liuyao', label: t('nav.liuyao'), icon: Zap },
            { href: '/divination/xiaoliu', label: t('nav.xiaoliu'), icon: Clock },
        ]
    },
    {
        title: t('nav.dreamGroup'),
        items: [
            { href: '/divination/dream', label: t('nav.dream'), icon: Moon },
            { href: '/divination/tarot', label: t('nav.tarot'), icon: Star },
        ]
    },
    {
        title: t('nav.nameGroup'),
        items: [
            { href: '/divination/name', label: t('nav.name'), icon: BookOpen },
            { href: '/divination/new_name', label: t('nav.newName'), icon: Baby },
        ]
    },
    {
        title: t('nav.calendarGroup'),
        items: [
            { href: '/divination/laohuangli', label: t('nav.laohuangli'), icon: Calendar },
            { href: '/divination/laohuangli/select', label: t('nav.selectDate'), icon: Calendar },
        ]
    },
    {
        title: t('nav.zodiacGroup'),
        items: [
            { href: '/divination/zodiac', label: t('nav.zodiac'), icon: Sun },
            { href: '/divination/fate', label: t('nav.fate'), icon: Users },
        ]
    },
    {
        title: t('nav.traditionalGroup'),
        items: [
            { href: '/divination/chouqian', label: t('nav.chouqian'), icon: Sparkles },
            { href: '/divination/zhuge', label: t('nav.zhuge'), icon: BookOpen },
            { href: '/divination/qimen', label: t('nav.qimen'), icon: Compass },
            { href: '/divination/daliuren', label: t('nav.daliuren'), icon: Zap },
            { href: '/divination/life-kline', label: t('nav.lifeKline'), icon: TrendingUp },
        ]
    },
]

interface SidebarProps {
    mobileOpen: boolean
    onMobileClose: () => void
}

export default function Sidebar({ mobileOpen, onMobileClose }: SidebarProps) {
    const location = useLocation()
    const navigate = useNavigate()
    const { isDark, toggleDark, settings, setJwt } = useGlobalState()
    const { t } = useTranslation()
    const navGroups = getNavGroups(t)
    const [expandedGroups, setExpandedGroups] = useState<string[]>(navGroups.map(g => g.title))

    const logOut = () => {
        setJwt('')
        window.location.reload()
    }

    const toggleGroup = (title: string) => {
        setExpandedGroups(prev =>
            prev.includes(title)
                ? prev.filter(t => t !== title)
                : [...prev, title]
        )
    }

    const isActive = (href: string) => location.pathname === href

    const handleNavClick = (href: string) => {
        navigate(href)
        onMobileClose()
    }

    return (
        <>
            {/* Mobile Overlay */}
            {mobileOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-40 lg:hidden"
                    onClick={onMobileClose}
                />
            )}

            {/* Sidebar */}
            <aside
                className={`
          fixed top-0 left-0 h-full w-[220px] bg-sidebar dark:bg-sidebar
          border-r border-sidebar-border
          flex flex-col z-50
          transition-transform duration-300
          lg:translate-x-0
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
            >
                {/* Logo */}
                <div className="p-4 border-b border-sidebar-border flex items-center justify-between">
                    <Link to="/" className="flex items-center gap-2" onClick={onMobileClose}>
                        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                            <Sparkles className="w-5 h-5 text-primary-foreground" />
                        </div>
                        <span className="font-bold text-xl text-sidebar-foreground">{t('common.appName')}</span>
                    </Link>
                    <button
                        onClick={onMobileClose}
                        className="lg:hidden p-1 hover:bg-sidebar-accent rounded"
                    >
                        <X className="w-5 h-5 text-muted-foreground" />
                    </button>
                </div>

                {/* Navigation Groups */}
                <div className="flex-1 overflow-y-auto py-2">
                    {navGroups.map((group) => (
                        <div key={group.title} className="mb-1">
                            <button
                                onClick={() => toggleGroup(group.title)}
                                className="w-full flex items-center justify-between px-4 py-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider hover:text-sidebar-foreground"
                            >
                                {group.title}
                                {expandedGroups.includes(group.title) ? (
                                    <ChevronDown className="w-3 h-3" />
                                ) : (
                                    <ChevronRight className="w-3 h-3" />
                                )}
                            </button>

                            {expandedGroups.includes(group.title) && (
                                <div className="mt-1">
                                    {group.items.map((item) => (
                                        <button
                                            key={item.href}
                                            onClick={() => handleNavClick(item.href)}
                                            className={`
                        w-full flex items-center gap-3 px-4 py-2.5 text-sm
                        transition-colors
                        ${isActive(item.href)
                                                    ? 'bg-sidebar-accent text-sidebar-accent-foreground font-medium'
                                                    : 'text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground'
                                                }
                      `}
                                        >
                                            <item.icon className="w-4 h-4" />
                                            {item.label}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>

                {/* Footer */}
                <div className="p-4 border-t border-sidebar-border space-y-3">
                    {/* Language Switcher */}
                    <LanguageSwitcher />

                    {/* Theme Toggle */}
                    <button
                        onClick={toggleDark}
                        className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm text-sidebar-foreground/70 hover:bg-sidebar-accent rounded-lg transition-colors"
                    >
                        {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
                        {isDark ? t('common.lightMode') : t('common.darkMode')}
                    </button>

                    {/* Settings */}
                    <button
                        onClick={() => { navigate('/settings'); onMobileClose() }}
                        className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm text-sidebar-foreground/70 hover:bg-sidebar-accent rounded-lg transition-colors"
                    >
                        <Settings className="w-4 h-4" />
                        {t('common.settings')}
                    </button>

                    {/* Login/Logout */}
                    {settings.enable_login && (
                        settings.user_name ? (
                            <button
                                onClick={logOut}
                                className="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-sm border border-sidebar-border rounded-lg hover:bg-sidebar-accent transition-colors"
                            >
                                <LogOut className="w-4 h-4" />
                                {t('common.logout')} ({settings.user_name})
                            </button>
                        ) : (
                            <button
                                onClick={() => { navigate('/login'); onMobileClose() }}
                                className="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-sm border border-sidebar-border rounded-lg hover:bg-sidebar-accent transition-colors"
                            >
                                <LogIn className="w-4 h-4" />
                                {t('common.login')} / {t('common.register')}
                            </button>
                        )
                    )}
                </div>
            </aside>
        </>
    )
}
