import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Menu,
    X,
    Sparkles,
    Sun,
    Moon,
    Star,
    Compass,
    Calendar,
    Heart,
    Brain,
    Coins,
    Flame,
    Wind,
    Droplets,
    Mountain,
    Users,
    BookOpen,
    History,
    Dice1,
    Layers,
    TrendingUp,
    FileText,
    Home
} from 'lucide-react';

interface DivinationItem {
    name: string;
    icon: React.ReactNode;
    path: string;
    description?: string;
}

interface DivinationCategory {
    title: string;
    items: DivinationItem[];
}

const DIVINATION_CATEGORIES: DivinationCategory[] = [
    {
        title: '🌟 东方玄学',
        items: [
            { name: '生辰八字', icon: <Calendar className="w-5 h-5" />, path: '/divination/bazi', description: '四柱命理推算' },
            { name: '紫微斗数', icon: <Star className="w-5 h-5" />, path: '/divination/ziwei', description: '星曜命盘分析' },
            { name: '梅花易数', icon: <Flame className="w-5 h-5" />, path: '/divination/plum-flower', description: '以数起卦' },
            { name: '六爻占卜', icon: <Layers className="w-5 h-5" />, path: '/divination/liuyao', description: '铜钱摇卦' },
            { name: '奇门遁甲', icon: <Compass className="w-5 h-5" />, path: '/divination/qimen', description: '时空奇门局' },
            { name: '大六壬', icon: <Droplets className="w-5 h-5" />, path: '/divination/daliuren', description: '课传神算' },
            { name: '小六壬', icon: <Dice1 className="w-5 h-5" />, path: '/divination/xiaoliu', description: '掐指一算' },
            { name: '诸葛神算', icon: <BookOpen className="w-5 h-5" />, path: '/divination/zhuge', description: '三百八十四签' },
        ]
    },
    {
        title: '🔮 西方神秘学',
        items: [
            { name: '塔罗占卜', icon: <FileText className="w-5 h-5" />, path: '/divination/tarot', description: '78张神秘牌' },
            { name: '星座运势', icon: <Sun className="w-5 h-5" />, path: '/divination/zodiac', description: '十二星座详解' },
        ]
    },
    {
        title: '📊 运势分析',
        items: [
            { name: '人生K线', icon: <TrendingUp className="w-5 h-5" />, path: '/divination/life-kline', description: '百年运势图' },
            { name: '每日运势', icon: <Sun className="w-5 h-5" />, path: '/divination/daily-fortune', description: '今日吉凶' },
            { name: '每月运势', icon: <Moon className="w-5 h-5" />, path: '/divination/monthly-fortune', description: '本月运程' },
        ]
    },
    {
        title: '🎯 实用工具',
        items: [
            { name: '姓名测算', icon: <Users className="w-5 h-5" />, path: '/divination/name', description: '五格剖象' },
            { name: '择吉日', icon: <Calendar className="w-5 h-5" />, path: '/divination/jiri', description: '黄道吉日' },
            { name: '老黄历', icon: <BookOpen className="w-5 h-5" />, path: '/divination/laohuangli', description: '每日宜忌' },
            { name: '周公解梦', icon: <Brain className="w-5 h-5" />, path: '/divination/dream', description: '梦境解析' },
            { name: '抽签求卦', icon: <Sparkles className="w-5 h-5" />, path: '/chouqian', description: '观音灵签' },
        ]
    }
];

interface MysticalSidebarProps {
    isOpen: boolean;
    onClose: () => void;
}

const MysticalSidebar: React.FC<MysticalSidebarProps> = ({ isOpen, onClose }) => {
    const navigate = useNavigate();
    const location = useLocation();

    const handleNavigate = (path: string) => {
        navigate(path);
        onClose();
    };

    return (
        <>
            {/* 遮罩层 */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
                        onClick={onClose}
                    />
                )}
            </AnimatePresence>

            {/* 侧边栏 */}
            <AnimatePresence>
                {isOpen && (
                    <motion.aside
                        initial={{ x: -300, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        exit={{ x: -300, opacity: 0 }}
                        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                        className="fixed left-0 top-0 h-full w-72 bg-gradient-to-b from-slate-900 via-purple-950 to-slate-900 z-50 flex flex-col border-r border-purple-500/30 shadow-2xl shadow-purple-900/50"
                    >
                        {/* 头部 */}
                        <div className="flex items-center justify-between p-4 border-b border-purple-500/20">
                            <div className="flex items-center gap-3">
                                <span className="text-2xl">🔮</span>
                                <h2 className="text-lg font-bold bg-gradient-to-r from-amber-400 to-yellow-200 bg-clip-text text-transparent">
                                    玄学宝典
                                </h2>
                            </div>
                            <button
                                onClick={onClose}
                                className="p-2 rounded-lg text-purple-300 hover:text-white hover:bg-purple-500/30 transition-all"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        {/* 首页链接 */}
                        <div className="px-3 py-2">
                            <button
                                onClick={() => handleNavigate('/')}
                                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${location.pathname === '/'
                                        ? 'bg-purple-600/50 text-white border border-purple-400/50'
                                        : 'text-purple-200 hover:bg-purple-500/20 hover:text-white'
                                    }`}
                            >
                                <Home className="w-5 h-5" />
                                <span className="font-medium">占卜首页</span>
                            </button>
                        </div>

                        {/* 分类导航 */}
                        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-4 scrollbar-thin scrollbar-thumb-purple-600/50 scrollbar-track-transparent">
                            {DIVINATION_CATEGORIES.map((category, catIndex) => (
                                <div key={catIndex} className="space-y-2">
                                    <h3 className="text-xs font-semibold text-purple-400 px-2 py-1 border-b border-purple-500/20 text-center">
                                        {category.title}
                                    </h3>
                                    <div className="space-y-1">
                                        {category.items.map((item, itemIndex) => {
                                            const isActive = location.pathname === item.path;
                                            return (
                                                <motion.button
                                                    key={itemIndex}
                                                    whileHover={{ x: 5 }}
                                                    whileTap={{ scale: 0.98 }}
                                                    onClick={() => handleNavigate(item.path)}
                                                    className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-all group ${isActive
                                                            ? 'bg-gradient-to-r from-purple-600/60 to-indigo-600/60 text-white border border-purple-400/40'
                                                            : 'text-purple-200 hover:bg-purple-500/20 hover:text-white border border-transparent'
                                                        }`}
                                                >
                                                    <span className={`${isActive ? 'text-amber-400' : 'text-purple-400 group-hover:text-purple-300'}`}>
                                                        {item.icon}
                                                    </span>
                                                    <div className="flex-1 min-w-0">
                                                        <span className="block text-sm font-medium truncate">{item.name}</span>
                                                        {item.description && (
                                                            <span className="block text-xs text-purple-400/70 truncate">{item.description}</span>
                                                        )}
                                                    </div>
                                                </motion.button>
                                            );
                                        })}
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* 底部信息 */}
                        <div className="p-3 border-t border-purple-500/20">
                            <div className="bg-purple-500/10 rounded-xl p-3 text-center">
                                <p className="text-xs text-purple-300">
                                    🌙 命理仅供参考
                                </p>
                                <p className="text-xs text-purple-400/60 mt-1">
                                    人生路径取决于个人选择
                                </p>
                            </div>
                        </div>
                    </motion.aside>
                )}
            </AnimatePresence>
        </>
    );
};

// 侧边栏触发按钮
export const SidebarTrigger: React.FC<{ onClick: () => void }> = ({ onClick }) => {
    return (
        <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onClick}
            className="p-2.5 rounded-xl bg-gradient-to-br from-purple-600/80 to-indigo-600/80 text-white shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50 transition-shadow"
        >
            <Menu className="w-5 h-5" />
        </motion.button>
    );
};

export default MysticalSidebar;
