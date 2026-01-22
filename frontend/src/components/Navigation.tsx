import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { Menu, X, Sun, Moon, Settings, LogIn, LogOut, ArrowRight } from 'lucide-react'
import { useGlobalState } from '@/store'
import { useSmoothScroll } from '@/hooks'

export default function Navigation() {
    const navigate = useNavigate()
    const location = useLocation()
    const { isDark, toggleDark, settings, setJwt } = useGlobalState()
    const { scrollToAnchor } = useSmoothScroll()
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

    const logOut = () => {
        setJwt('')
        window.location.reload()
    }

    const handleNavClick = (href: string, e: React.MouseEvent) => {
        if (href.startsWith('#')) {
            e.preventDefault()
            if (location.pathname !== '/divination') {
                navigate('/divination')
                setTimeout(() => {
                    scrollToAnchor(href.replace('#', ''))
                }, 100)
            } else {
                scrollToAnchor(href.replace('#', ''))
            }
        }
        setMobileMenuOpen(false)
    }

    const navLinks = [
        { href: '/', label: '首页' },
        { href: '/divination', label: '占卜' },
        { href: '/about', label: '关于' },
    ]

    return (
        <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-sm border-b border-border">
            <nav className="container mx-auto px-4 py-4 md:px-6 md:py-6">
                <div className="flex items-center justify-between">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-1.5">
                        <span className="font-bold text-lg md:text-xl text-foreground">
                            AI 占卜
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden lg:flex flex-1 items-center justify-center gap-8">
                        {navLinks.map((link) => (
                            <Link
                                key={link.href}
                                to={link.href}
                                className="text-sm font-semibold leading-6 text-foreground hover:text-muted-foreground transition-colors"
                            >
                                {link.label}
                            </Link>
                        ))}
                    </div>

                    {/* Right Actions */}
                    <div className="flex items-center gap-2">
                        {settings.enable_login && (
                            settings.user_name ? (
                                <button
                                    onClick={logOut}
                                    className="hidden sm:flex items-center gap-1.5 text-sm font-semibold text-muted-foreground hover:text-foreground transition-colors"
                                >
                                    <LogOut className="h-4 w-4" />
                                    登出
                                </button>
                            ) : (
                                <button
                                    onClick={() => navigate('/login')}
                                    className="hidden sm:flex items-center gap-1.5 text-sm font-semibold leading-6 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                                >
                                    <LogIn className="h-4 w-4" />
                                    登录
                                </button>
                            )
                        )}

                        <button
                            onClick={() => navigate('/settings')}
                            title="设置"
                            className="p-2 hover:bg-accent rounded-md transition-colors"
                        >
                            <Settings className="h-5 w-5 text-muted-foreground" />
                        </button>

                        <button
                            onClick={toggleDark}
                            title="切换主题"
                            className="p-2 hover:bg-accent rounded-md transition-colors"
                        >
                            {isDark ? (
                                <Sun className="h-5 w-5 text-muted-foreground" />
                            ) : (
                                <Moon className="h-5 w-5 text-muted-foreground" />
                            )}
                        </button>

                        {/* CTA Button - Desktop */}
                        <Link
                            to="/divination"
                            className="hidden md:flex items-center gap-1.5 text-sm font-semibold leading-6 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                        >
                            开始占卜
                            <ArrowRight className="h-4 w-4" />
                        </Link>

                        {/* Mobile Menu Button */}
                        <button
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                            className="lg:hidden p-2 hover:bg-accent rounded-md transition-colors"
                        >
                            {mobileMenuOpen ? (
                                <X className="h-5 w-5" />
                            ) : (
                                <Menu className="h-5 w-5" />
                            )}
                        </button>
                    </div>
                </div>

                {/* Mobile Menu */}
                {mobileMenuOpen && (
                    <div className="lg:hidden mt-4 pb-4 border-t border-border pt-4">
                        <div className="flex flex-col gap-4">
                            {navLinks.map((link) => (
                                <Link
                                    key={link.href}
                                    to={link.href}
                                    onClick={() => setMobileMenuOpen(false)}
                                    className="text-base font-semibold text-foreground hover:text-muted-foreground transition-colors"
                                >
                                    {link.label}
                                </Link>
                            ))}
                            <Link
                                to="/divination"
                                onClick={() => setMobileMenuOpen(false)}
                                className="flex items-center justify-center gap-1.5 text-sm font-semibold px-4 py-2.5 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                            >
                                开始占卜
                                <ArrowRight className="h-4 w-4" />
                            </Link>
                        </div>
                    </div>
                )}

                {/* Rate Limit Warning */}
                {settings.fetched && !settings.user_name && settings.enable_rate_limit && (
                    <div className="mt-3 flex items-center justify-between text-xs text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 px-3 py-2 rounded-md">
                        <span className="flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse" />
                            游客限流模式 ({settings.rate_limit})
                        </span>
                        <Link to="/settings" className="hover:underline font-medium">
                            自定义配置 →
                        </Link>
                    </div>
                )}
            </nav>
        </header>
    )
}
