/**
 * 六爻主题Hook
 * 与全局主题同步
 */

import { useState, useEffect } from 'react';
import { useGlobalState } from '@/store';

export type Theme = 'dark' | 'light';

export const useTheme = () => {
    // 从全局状态获取主题
    const { isDark, toggleDark } = useGlobalState();
    const theme: Theme = isDark ? 'dark' : 'light';

    useEffect(() => {
        // 更新六爻专用类名
        const root = document.documentElement;
        if (!isDark) {
            root.classList.add('liuyao-light');
        } else {
            root.classList.remove('liuyao-light');
        }

        // 清理函数
        return () => {
            root.classList.remove('liuyao-light');
        };
    }, [isDark]);

    const toggleTheme = () => {
        toggleDark();
    };

    return { theme, toggleTheme };
};
