/**
 * 六爻起卦页面 - 融入网站主题版
 * 仅保留核心算法和功能，使用网站统一样式
 */

import React, { useState } from 'react';
import { AppSettings } from './types';
import DivinationView from './views/DivinationView';
import { DivinationCardHeader } from '../../components/DivinationCardHeader';

const LiuYaoPage: React.FC = () => {
    const [settings] = useState<AppSettings>({
        soundEnabled: true,
        hapticEnabled: true,
        aiStyle: 'detailed',
        autoInterpret: true
    });

    return (
        <div className="max-w-4xl mx-auto px-4 py-6">
            <DivinationCardHeader
                title="六爻占卦"
                description="诚心问卦，铜钱起卦或数理起卦，AI智能解读"
                divinationType="liuyao"
            >
                <DivinationView settings={settings} />
            </DivinationCardHeader>
        </div>
    );
};

export default LiuYaoPage;
