/**
 * 八字输入表单组件
 * 用于输入四柱信息和大运参数
 */

import React, { useState } from 'react';
import { Gender, LifeKLineInput } from './types';

interface BaziInputFormProps {
    onSubmit: (data: LifeKLineInput) => void;
    isLoading?: boolean;
}

// 天干
const TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
// 地支
const DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

// 生成六十甲子
const generateJiaZi = () => {
    const result: string[] = [];
    for (let i = 0; i < 60; i++) {
        result.push(TIANGAN[i % 10] + DIZHI[i % 12]);
    }
    return result;
};

const JIAZI_60 = generateJiaZi();

const BaziInputForm: React.FC<BaziInputFormProps> = ({ onSubmit, isLoading = false }) => {
    const [formData, setFormData] = useState<LifeKLineInput>({
        name: '',
        gender: Gender.MALE,
        birthYear: new Date().getFullYear() - 30,
        yearPillar: '甲子',
        monthPillar: '甲子',
        dayPillar: '甲子',
        hourPillar: '甲子',
        startAge: 1,
        firstDaYun: '甲子',
        isForward: undefined,
        useAi: true,  // 默认使用AI
        apiKey: '',
        apiBaseUrl: '',
        modelName: '',
    });

    const [showAdvanced, setShowAdvanced] = useState(false);

    const handleChange = (field: keyof LifeKLineInput, value: LifeKLineInput[keyof LifeKLineInput]) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit} className="bg-card rounded-xl shadow-sm border border-border p-6">
            <h3 className="text-lg font-bold text-foreground mb-6">八字信息输入</h3>

            {/* 基本信息 */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div>
                    <label className="block text-sm font-medium text-muted-foreground mb-1">姓名</label>
                    <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => handleChange('name', e.target.value)}
                        className="w-full px-3 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background text-foreground"
                        placeholder="选填"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-muted-foreground mb-1">性别</label>
                    <select
                        value={formData.gender}
                        onChange={(e) => handleChange('gender', e.target.value)}
                        className="w-full px-3 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background text-foreground"
                    >
                        <option value={Gender.MALE}>男</option>
                        <option value={Gender.FEMALE}>女</option>
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-medium text-muted-foreground mb-1">出生年份</label>
                    <input
                        type="number"
                        value={formData.birthYear}
                        onChange={(e) => handleChange('birthYear', parseInt(e.target.value) || 1990)}
                        className="w-full px-3 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background text-foreground"
                        min={1900}
                        max={2100}
                    />
                </div>
            </div>

            {/* 四柱 */}
            <div className="mb-6">
                <label className="block text-sm font-medium text-muted-foreground mb-3">四柱八字</label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {['yearPillar', 'monthPillar', 'dayPillar', 'hourPillar'].map((field, index) => (
                        <div key={field}>
                            <label className="block text-xs text-muted-foreground mb-1">
                                {['年柱', '月柱', '日柱', '时柱'][index]}
                            </label>
                            <select
                                value={formData[field as keyof LifeKLineInput] as string}
                                onChange={(e) => handleChange(field as keyof LifeKLineInput, e.target.value)}
                                className="w-full px-3 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary text-sm bg-background text-foreground"
                            >
                                {JIAZI_60.map(gz => (
                                    <option key={gz} value={gz}>{gz}</option>
                                ))}
                            </select>
                        </div>
                    ))}
                </div>
            </div>

            {/* 大运参数 */}
            <div className="mb-6">
                <label className="block text-sm font-medium text-muted-foreground mb-3">大运参数</label>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label className="block text-xs text-muted-foreground mb-1">起运年龄（虚岁）</label>
                        <input
                            type="number"
                            value={formData.startAge}
                            onChange={(e) => handleChange('startAge', parseInt(e.target.value) || 1)}
                            className="w-full px-3 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background text-foreground"
                            min={1}
                            max={12}
                        />
                    </div>

                    <div>
                        <label className="block text-xs text-muted-foreground mb-1">第一步大运</label>
                        <select
                            value={formData.firstDaYun}
                            onChange={(e) => handleChange('firstDaYun', e.target.value)}
                            className="w-full px-3 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary text-sm bg-background text-foreground"
                        >
                            {JIAZI_60.map(gz => (
                                <option key={gz} value={gz}>{gz}</option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-xs text-muted-foreground mb-1">大运方向</label>
                        <select
                            value={formData.isForward === undefined ? 'auto' : formData.isForward ? 'forward' : 'backward'}
                            onChange={(e) => {
                                const val = e.target.value;
                                handleChange('isForward', val === 'auto' ? undefined : val === 'forward');
                            }}
                            className="w-full px-3 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background text-foreground"
                        >
                            <option value="auto">自动计算</option>
                            <option value="forward">顺行</option>
                            <option value="backward">逆行</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* 高级选项 */}
            <div className="mb-6">
                <button
                    type="button"
                    onClick={() => setShowAdvanced(!showAdvanced)}
                    className="text-sm text-primary hover:text-primary/80 flex items-center gap-1"
                >
                    <span>{showAdvanced ? '收起' : '展开'}高级选项</span>
                    <svg
                        className={`w-4 h-4 transition-transform ${showAdvanced ? 'rotate-180' : ''}`}
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                </button>

                {showAdvanced && (
                    <div className="mt-4 p-4 bg-secondary rounded-lg">
                        <div className="flex items-center mb-4">
                            <input
                                type="checkbox"
                                id="useAi"
                                checked={formData.useAi}
                                onChange={(e) => handleChange('useAi', e.target.checked)}
                                className="w-4 h-4 text-primary border-input rounded focus:ring-primary"
                            />
                            <label htmlFor="useAi" className="ml-2 text-sm text-muted-foreground">
                                使用AI生成详细分析（推荐）
                            </label>
                        </div>

                        {formData.useAi && (
                            <div className="text-sm text-muted-foreground bg-primary/10 p-3 rounded-lg border border-primary/20">
                                <p className="flex items-center gap-2">
                                    <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    将使用项目配置的AI服务自动生成专业命理分析
                                </p>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* 提交按钮 */}
            <button
                type="submit"
                disabled={isLoading}
                className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-colors ${isLoading
                    ? 'bg-muted cursor-not-allowed'
                    : 'bg-primary hover:bg-primary/90'
                    }`}
            >
                {isLoading ? (
                    <span className="flex items-center justify-center gap-2">
                        <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        生成中...
                    </span>
                ) : (
                    '生成人生K线图'
                )}
            </button>
        </form>
    );
};

export default BaziInputForm;
