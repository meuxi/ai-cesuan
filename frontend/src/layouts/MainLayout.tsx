import { ReactNode, useEffect, useState } from 'react'
import { useGlobalState } from '@/store'
import { useIsMobile } from '@/hooks'
import Sidebar from '@/components/Sidebar'
import Footer from '@/components/Footer'
import { Menu } from 'lucide-react'

interface MainLayoutProps {
    children: ReactNode
}

export default function MainLayout({ children }: MainLayoutProps) {
    const isMobile = useIsMobile()
    const { isDark } = useGlobalState()
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

    useEffect(() => {
        if (isDark) {
            document.documentElement.classList.add('dark')
        } else {
            document.documentElement.classList.remove('dark')
        }
    }, [isDark])

    return (
        <div className="min-h-screen bg-background text-foreground">
            {/* Sidebar */}
            <Sidebar
                mobileOpen={mobileMenuOpen}
                onMobileClose={() => setMobileMenuOpen(false)}
            />

            {/* Main Content Area */}
            <div className="lg:ml-[220px] min-h-screen flex flex-col">
                {/* Mobile Header */}
                <header className="lg:hidden sticky top-0 z-30 bg-card border-b border-border px-4 py-3 flex items-center gap-3">
                    <button
                        onClick={() => setMobileMenuOpen(true)}
                        className="p-2 hover:bg-accent rounded-lg transition-colors"
                    >
                        <Menu className="w-5 h-5 text-muted-foreground" />
                    </button>
                    <span className="font-semibold text-foreground">AI 占卜</span>
                </header>

                {/* Page Content */}
                <main className="flex-1 p-4 md:p-8 lg:p-12">
                    <div className="max-w-4xl mx-auto">
                        {children}
                    </div>
                </main>

                {/* Footer */}
                <Footer />
            </div>
        </div>
    )
}
