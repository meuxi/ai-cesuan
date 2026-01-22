/**
 * 六爻应用主布局
 * 完全复刻原工具设计，添加主题切换功能
 */

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Home, Compass, Settings, BookOpen, Sun, Moon, LucideIcon } from 'lucide-react';
import Background from './Background';
import { useTheme } from '../hooks/useTheme';

interface Props {
    children: React.ReactNode;
    activeTab: string;
    onTabChange: (tab: string) => void;
}

interface NavButtonProps {
    active: boolean;
    onClick: () => void;
    icon: React.ReactElement;
    label: string;
    isDark?: boolean;
}

const Layout: React.FC<Props> = ({ children, activeTab, onTabChange }) => {
    const { theme, toggleTheme } = useTheme();

    return (
        <div className="relative w-full min-h-[calc(100vh-80px)] font-sans flex justify-center overflow-hidden bg-background text-foreground">
            <Background />

            {/* Container - 在顶部导航下方显示 */}
            <div className="w-full h-full md:max-w-5xl lg:max-w-7xl relative flex flex-col md:bg-card/30 md:shadow-2xl md:border-x md:border-border/30 transition-all duration-300">

                {/* Main Content Area */}
                <main className="flex-1 relative overflow-hidden flex flex-col">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={activeTab}
                            initial={{ opacity: 0, filter: 'blur(10px)' }}
                            animate={{ opacity: 1, filter: 'blur(0px)' }}
                            exit={{ opacity: 0, filter: 'blur(10px)' }}
                            transition={{
                                duration: 0.6,
                                ease: [0.22, 1, 0.36, 1]
                            }}
                            className="h-full w-full overflow-y-auto overflow-x-hidden no-scrollbar pb-24"
                        >
                            {children}
                        </motion.div>
                    </AnimatePresence>
                </main>

                {/* Bottom Navigation Bar */}
                <div className="fixed bottom-6 left-0 right-0 lg:left-[220px] flex justify-center z-50 pointer-events-none">
                    <nav className="pointer-events-auto h-[72px] w-[92%] max-w-md rounded-full backdrop-blur-xl border shadow-2xl flex items-center justify-around px-4 bg-card/90 border-border">
                        <NavButton
                            active={activeTab === 'home'}
                            onClick={() => onTabChange('home')}
                            icon={<Home />}
                            label="缘起"
                            isDark={theme === 'dark'}
                        />
                        <NavButton
                            active={activeTab === 'divination'}
                            onClick={() => onTabChange('divination')}
                            icon={<Compass />}
                            label="起卦"
                            isDark={theme === 'dark'}
                        />
                        <NavButton
                            active={activeTab === 'history'}
                            onClick={() => onTabChange('history')}
                            icon={<BookOpen />}
                            label="卦录"
                            isDark={theme === 'dark'}
                        />
                        <NavButton
                            active={activeTab === 'settings'}
                            onClick={() => onTabChange('settings')}
                            icon={<Settings />}
                            label="设置"
                            isDark={theme === 'dark'}
                        />
                    </nav>

                    {/* Theme Toggle Button */}
                    <button
                        onClick={toggleTheme}
                        className="pointer-events-auto fixed bottom-28 right-6 p-3 rounded-full backdrop-blur-xl border shadow-lg transition-colors bg-card/90 border-border text-muted-foreground hover:text-primary"
                        title={theme === 'dark' ? '切换到明亮模式' : '切换到暗色模式'}
                    >
                        {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
                    </button>
                </div>
            </div>
        </div>
    );
};

const NavButton = ({ active, onClick, icon, label }: NavButtonProps) => {
    const activeColor = 'hsl(var(--primary))';
    const inactiveColor = 'hsl(var(--muted-foreground))';

    return (
        <button
            onClick={onClick}
            className="relative flex flex-col items-center justify-center w-14 h-full outline-none group"
        >
            <div className="relative z-10 p-2">
                <motion.div
                    animate={{
                        scale: active ? 1.1 : 0.9,
                        color: active ? activeColor : inactiveColor,
                    }}
                    transition={{ duration: 0.4 }}
                    className="group-hover:text-primary transition-colors"
                >
                    {React.cloneElement(icon, { size: 20, strokeWidth: active ? 2 : 1.5 })}
                </motion.div>
            </div>

            {/* 导航标签 */}
            <span className={`text-[10px] tracking-wider transition-colors ${active
                ? 'text-primary'
                : 'text-muted-foreground'
                }`}>{label}</span>

            {active && (
                <motion.div
                    layoutId="nav-indicator"
                    className="absolute bottom-1.5 w-1 h-1 rounded-full bg-primary shadow-sm"
                />
            )}
        </button>
    );
};

export default Layout;
