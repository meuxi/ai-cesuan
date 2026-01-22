/**
 * 设置视图
 * 完整优化版 - 支持明暗主题切换
 */

import React from 'react';
import { Volume2, VolumeX, Smartphone, Zap, Trash2 } from 'lucide-react';
import { AppSettings } from '../types';
import { clearHistory } from '../utils/storage';
import { useTheme } from '../hooks/useTheme';

interface Props {
    settings: AppSettings;
    onUpdate: (s: AppSettings) => void;
}

const SettingsView: React.FC<Props> = ({ settings, onUpdate }) => {
    const toggle = (key: keyof AppSettings) => {
        onUpdate({ ...settings, [key]: !settings[key] });
    };

    const setModel = (model: AppSettings['aiStyle']) => {
        onUpdate({ ...settings, aiStyle: model });
    };

    const handleClearHistory = () => {
        if (confirm('确定清空历史记录？此操作无法撤销。')) {
            clearHistory();
            alert('记录已清空');
        }
    };

    return (
        <div className="p-6 md:p-8 pt-12 space-y-8 max-w-lg mx-auto">
            <h2 className="text-3xl tracking-wide pb-5 border-b border-border text-foreground">
                设置
            </h2>

            {/* Preferences */}
            <section className="space-y-3">
                <h3 className="text-[11px] font-bold uppercase tracking-widest pl-1 text-primary">
                    交互体验
                </h3>

                <SettingItem
                    icon={settings.soundEnabled ? <Volume2 size={18} /> : <VolumeX size={18} />}
                    label="沉浸音效"
                    desc="起卦时的金石之声"
                    active={settings.soundEnabled}
                    onClick={() => toggle('soundEnabled')}
                />

                <SettingItem
                    icon={<Smartphone size={18} />}
                    label="触感反馈"
                    desc="模拟真实的摇卦震动"
                    active={settings.hapticEnabled}
                    onClick={() => toggle('hapticEnabled')}
                />
            </section>

            {/* AI Config */}
            <section className="space-y-3">
                <h3 className="text-[11px] font-bold uppercase tracking-widest pl-1 text-primary">
                    大师风格
                </h3>

                <div className="grid grid-cols-1 gap-2">
                    <ModelOption
                        active={settings.aiStyle === 'concise'}
                        onClick={() => setModel('concise')}
                        title="直断"
                        desc="吉凶立判，言简意赅"
                    />
                    <ModelOption
                        active={settings.aiStyle === 'detailed'}
                        onClick={() => setModel('detailed')}
                        title="详解"
                        desc="剖析爻辞，全面推演"
                    />
                    <ModelOption
                        active={settings.aiStyle === 'philosophical'}
                        onClick={() => setModel('philosophical')}
                        title="悟道"
                        desc="引经据典，指点迷津"
                    />
                </div>

                <div className="pt-2">
                    <SettingItem
                        icon={<Zap size={18} />}
                        label="自动解卦"
                        desc="成卦后立即进行推演"
                        active={settings.autoInterpret}
                        onClick={() => toggle('autoInterpret')}
                    />
                </div>
            </section>

            {/* Data Management */}
            <section className="pt-6">
                <button
                    onClick={handleClearHistory}
                    className="w-full flex items-center justify-center gap-2 text-xs py-4 rounded-lg transition-colors text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                >
                    <Trash2 size={14} /> 清空所有卜卦记录
                </button>
            </section>

            <div className="text-center pt-6 pb-8">
                <p className="text-[10px] tracking-widest text-muted-foreground">
                    六爻神课 v1.2
                </p>
            </div>
        </div>
    );
};

interface SettingItemProps {
    icon: React.ReactNode;
    label: string;
    desc: string;
    active: boolean;
    onClick: () => void;
}

const SettingItem: React.FC<SettingItemProps> = ({ icon, label, desc, active, onClick }) => (
    <button
        onClick={onClick}
        className="w-full flex items-center justify-between p-4 rounded-lg border transition-all group bg-card border-border hover:border-primary/50"
    >
        <div className="flex items-center gap-4">
            <div className="transition-colors text-muted-foreground group-hover:text-primary">
                {icon}
            </div>
            <div className="text-left">
                <div className="text-sm text-foreground">
                    {label}
                </div>
                <div className="text-[10px] text-muted-foreground">
                    {desc}
                </div>
            </div>
        </div>
        {/* Toggle Switch */}
        <div className={`w-10 h-5 rounded-full relative transition-colors ${active
            ? 'bg-primary'
            : 'bg-secondary'
            }`}>
            <div className={`absolute top-0.5 w-4 h-4 bg-background rounded-full shadow-sm transition-all ${active ? 'left-5' : 'left-0.5'
                }`}></div>
        </div>
    </button>
);

interface ModelOptionProps {
    active: boolean;
    onClick: () => void;
    title: string;
    desc: string;
}

const ModelOption: React.FC<ModelOptionProps> = ({ active, onClick, title, desc }) => (
    <button
        onClick={onClick}
        className={`px-4 py-3 rounded-lg border text-left transition-all relative overflow-hidden flex items-center justify-between ${active
            ? 'bg-primary/10 border-primary/50 text-primary'
            : 'bg-card border-border text-muted-foreground hover:border-primary/30'
            }`}
    >
        <div>
            <div className="text-sm">{title}</div>
            <div className={`text-[10px] mt-0.5 ${active ? 'opacity-80' : 'opacity-70'}`}>
                {desc}
            </div>
        </div>
        {active && (
            <div className="w-2 h-2 rounded-full bg-primary"></div>
        )}
    </button>
);

export default SettingsView;
