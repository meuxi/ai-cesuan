/**
 * 六爻高级分析展示面板
 * 显示空亡、旺衰、神系、三合六冲等专业分析信息
 */

import React from 'react';
import { motion } from 'framer-motion';
import { Info, Zap, Target, Users, Triangle, AlertTriangle, Clock, CheckCircle, XCircle, Eye, EyeOff } from 'lucide-react';
import { AdvancedAnalysisResult, ExtendedYaoInfo, FuShenDetailInfo } from '../types';

interface Props {
    analysis: AdvancedAnalysisResult;
    isDark?: boolean;
}

const YAO_NAMES = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻'];

// 旺衰颜色映射
const WANG_SHUAI_COLORS: Record<string, string> = {
    '旺': 'text-green-500',
    '相': 'text-emerald-400',
    '休': 'text-yellow-500',
    '囚': 'text-orange-500',
    '死': 'text-red-500',
};

// 空亡状态颜色
const KONG_WANG_COLORS: Record<string, string> = {
    '不空': 'text-ink-400',
    '真空': 'text-red-400',
    '动空': 'text-yellow-400',
    '冲空': 'text-blue-400',
    '临建': 'text-green-400',
};

// 特殊状态颜色
const SPECIAL_STATUS_COLORS: Record<string, string> = {
    '暗动': 'text-purple-400',
    '日破': 'text-red-500',
    '无': 'text-ink-500',
};

const AdvancedAnalysisPanel: React.FC<Props> = ({ analysis, isDark = true }) => {
    const { kongWang, extendedYaos, sanHeAnalysis, liuChongGua, shenSystem, timeRecommendations, fuShen } = analysis;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`rounded-xl border p-4 space-y-4 ${isDark ? 'bg-ink-900/50 border-ink-700/50' : 'bg-white/80 border-ink-200'
                }`}
        >
            {/* 标题 */}
            <div className="flex items-center gap-2 pb-2 border-b border-ink-700/30">
                <Info size={16} className="text-gold-500" />
                <h3 className={`text-sm font-serif tracking-wider ${isDark ? 'text-gold-400' : 'text-gold-700'}`}>
                    专业分析
                </h3>
            </div>

            {/* 旬空信息 */}
            <div className="space-y-2">
                <div className="flex items-center gap-2">
                    <Target size={14} className="text-gold-600/70" />
                    <span className={`text-xs font-medium ${isDark ? 'text-ink-300' : 'text-ink-600'}`}>旬空</span>
                </div>
                <div className={`text-sm pl-5 ${isDark ? 'text-ink-400' : 'text-ink-500'}`}>
                    <span className="text-gold-500">{kongWang.xun}</span>
                    <span className="mx-2">·</span>
                    空亡：
                    <span className="text-red-400 font-medium">{kongWang.kongDizhi.join('、')}</span>
                </div>
            </div>

            {/* 六冲卦 / 三合局 */}
            {(liuChongGua.isLiuChongGua || sanHeAnalysis.hasFullSanHe || sanHeAnalysis.hasBanHe) && (
                <div className="space-y-2">
                    <div className="flex items-center gap-2">
                        <Triangle size={14} className="text-gold-600/70" />
                        <span className={`text-xs font-medium ${isDark ? 'text-ink-300' : 'text-ink-600'}`}>卦象特征</span>
                    </div>
                    <div className="pl-5 space-y-1">
                        {liuChongGua.isLiuChongGua && (
                            <div className="flex items-center gap-2">
                                <AlertTriangle size={12} className="text-red-400" />
                                <span className="text-sm text-red-400">六冲卦</span>
                                {liuChongGua.description && (
                                    <span className="text-xs text-ink-500">（{liuChongGua.description}）</span>
                                )}
                            </div>
                        )}
                        {sanHeAnalysis.hasFullSanHe && sanHeAnalysis.fullSanHe && (
                            <div className="flex items-center gap-2">
                                <Zap size={12} className="text-green-400" />
                                <span className="text-sm text-green-400">{sanHeAnalysis.fullSanHe.name}</span>
                                <span className="text-xs text-ink-500">（合力强大）</span>
                            </div>
                        )}
                        {sanHeAnalysis.hasBanHe && sanHeAnalysis.banHe.length > 0 && (
                            <div className="flex items-center gap-2">
                                <Zap size={12} className="text-yellow-400" />
                                <span className="text-sm text-yellow-400">
                                    {sanHeAnalysis.banHe[0].branches.join('')}半合{sanHeAnalysis.banHe[0].result}
                                </span>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* 神系分析 */}
            {shenSystem && (shenSystem.yuanShen || shenSystem.jiShen || shenSystem.chouShen) && (
                <div className="space-y-2">
                    <div className="flex items-center gap-2">
                        <Users size={14} className="text-gold-600/70" />
                        <span className={`text-xs font-medium ${isDark ? 'text-ink-300' : 'text-ink-600'}`}>神系</span>
                    </div>
                    <div className="pl-5 grid grid-cols-3 gap-2 text-xs">
                        {shenSystem.yuanShen && (
                            <div className={`p-2 rounded ${isDark ? 'bg-green-900/20' : 'bg-green-50'}`}>
                                <div className="text-green-400 font-medium">原神</div>
                                <div className={isDark ? 'text-ink-400' : 'text-ink-600'}>
                                    {shenSystem.yuanShen.liuQin}（{shenSystem.yuanShen.wuXing}）
                                </div>
                                {shenSystem.yuanShen.positions.length > 0 && (
                                    <div className="text-ink-500 text-[10px]">
                                        {shenSystem.yuanShen.positions.map(p => YAO_NAMES[p]).join('、')}
                                    </div>
                                )}
                            </div>
                        )}
                        {shenSystem.jiShen && (
                            <div className={`p-2 rounded ${isDark ? 'bg-red-900/20' : 'bg-red-50'}`}>
                                <div className="text-red-400 font-medium">忌神</div>
                                <div className={isDark ? 'text-ink-400' : 'text-ink-600'}>
                                    {shenSystem.jiShen.liuQin}（{shenSystem.jiShen.wuXing}）
                                </div>
                                {shenSystem.jiShen.positions.length > 0 && (
                                    <div className="text-ink-500 text-[10px]">
                                        {shenSystem.jiShen.positions.map(p => YAO_NAMES[p]).join('、')}
                                    </div>
                                )}
                            </div>
                        )}
                        {shenSystem.chouShen && (
                            <div className={`p-2 rounded ${isDark ? 'bg-orange-900/20' : 'bg-orange-50'}`}>
                                <div className="text-orange-400 font-medium">仇神</div>
                                <div className={isDark ? 'text-ink-400' : 'text-ink-600'}>
                                    {shenSystem.chouShen.liuQin}（{shenSystem.chouShen.wuXing}）
                                </div>
                                {shenSystem.chouShen.positions.length > 0 && (
                                    <div className="text-ink-500 text-[10px]">
                                        {shenSystem.chouShen.positions.map(p => YAO_NAMES[p]).join('、')}
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* 六爻旺衰详情 */}
            <div className="space-y-2">
                <div className="flex items-center gap-2">
                    <Zap size={14} className="text-gold-600/70" />
                    <span className={`text-xs font-medium ${isDark ? 'text-ink-300' : 'text-ink-600'}`}>爻位分析</span>
                </div>
                <div className="pl-5 space-y-1">
                    {extendedYaos.map((yao, idx) => (
                        <YaoStrengthRow key={idx} yao={yao} isDark={isDark} />
                    ))}
                </div>
            </div>

            {/* 伏神分析 */}
            {fuShen && fuShen.length > 0 && (
                <div className="space-y-2">
                    <div className="flex items-center gap-2">
                        <EyeOff size={14} className="text-gold-600/70" />
                        <span className={`text-xs font-medium ${isDark ? 'text-ink-300' : 'text-ink-600'}`}>伏神</span>
                        <span className="text-[10px] text-ink-500">（用神不上卦时）</span>
                    </div>
                    <div className="pl-5 grid grid-cols-2 gap-2">
                        {fuShen.map((fs, idx) => (
                            <div
                                key={idx}
                                className={`p-2 rounded text-xs ${fs.isAvailable
                                        ? (isDark ? 'bg-green-900/20 border border-green-700/30' : 'bg-green-50 border border-green-200')
                                        : (isDark ? 'bg-red-900/20 border border-red-700/30' : 'bg-red-50 border border-red-200')
                                    }`}
                            >
                                <div className="flex items-center gap-2 mb-1">
                                    {fs.isAvailable ? (
                                        <Eye size={12} className="text-green-400" />
                                    ) : (
                                        <EyeOff size={12} className="text-red-400" />
                                    )}
                                    <span className={`font-medium ${fs.isAvailable ? 'text-green-400' : 'text-red-400'}`}>
                                        伏{fs.liuQin}
                                    </span>
                                    <span className={isDark ? 'text-ink-400' : 'text-ink-600'}>
                                        {fs.naJia}{fs.wuXing}
                                    </span>
                                </div>
                                <div className={`text-[10px] ${isDark ? 'text-ink-500' : 'text-ink-400'}`}>
                                    飞神：{YAO_NAMES[fs.feiShenPosition - 1]} {fs.feiShenLiuQin}
                                </div>
                                <div className={`text-[10px] mt-1 ${fs.isAvailable ? 'text-green-400/80' : 'text-red-400/80'}`}>
                                    {fs.availabilityReason}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* 应期推断 */}
            {timeRecommendations && timeRecommendations.length > 0 && (
                <div className="space-y-2">
                    <div className="flex items-center gap-2">
                        <Clock size={14} className="text-gold-600/70" />
                        <span className={`text-xs font-medium ${isDark ? 'text-ink-300' : 'text-ink-600'}`}>应期推断</span>
                    </div>
                    <div className="pl-5 space-y-2">
                        {timeRecommendations.map((rec, idx) => (
                            <div key={idx} className={`flex items-start gap-2 text-xs p-2 rounded ${rec.type === 'favorable'
                                    ? (isDark ? 'bg-green-900/20' : 'bg-green-50')
                                    : rec.type === 'unfavorable'
                                        ? (isDark ? 'bg-red-900/20' : 'bg-red-50')
                                        : (isDark ? 'bg-yellow-900/20' : 'bg-yellow-50')
                                }`}>
                                {rec.type === 'favorable' ? (
                                    <CheckCircle size={12} className="text-green-400 mt-0.5 shrink-0" />
                                ) : rec.type === 'unfavorable' ? (
                                    <XCircle size={12} className="text-red-400 mt-0.5 shrink-0" />
                                ) : (
                                    <AlertTriangle size={12} className="text-yellow-400 mt-0.5 shrink-0" />
                                )}
                                <div>
                                    <span className={`font-medium ${rec.type === 'favorable' ? 'text-green-400' :
                                            rec.type === 'unfavorable' ? 'text-red-400' : 'text-yellow-400'
                                        }`}>
                                        [{rec.timeframe}]
                                    </span>
                                    <span className={isDark ? 'text-ink-400 ml-1' : 'text-ink-600 ml-1'}>
                                        {rec.description}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </motion.div>
    );
};

// 单爻强度行
const YaoStrengthRow: React.FC<{ yao: ExtendedYaoInfo; isDark: boolean }> = ({ yao, isDark }) => {
    const wangShuaiColor = WANG_SHUAI_COLORS[yao.strength.wangShuai] || 'text-ink-400';
    const kongWangColor = KONG_WANG_COLORS[yao.kongWangState] || 'text-ink-400';
    const specialColor = SPECIAL_STATUS_COLORS[yao.strength.specialStatus] || 'text-ink-500';

    return (
        <div className={`flex items-center gap-3 text-xs py-1 border-b last:border-b-0 ${isDark ? 'border-ink-800/30' : 'border-ink-100'
            }`}>
            {/* 爻位 */}
            <span className={`w-10 font-medium ${isDark ? 'text-ink-400' : 'text-ink-600'}`}>
                {YAO_NAMES[yao.index]}
            </span>

            {/* 地支五行 */}
            <span className={`w-16 ${isDark ? 'text-gold-400' : 'text-gold-600'}`}>
                {yao.branch}{yao.element}
            </span>

            {/* 旺衰 */}
            <span className={`w-8 font-medium ${wangShuaiColor}`}>
                {yao.strength.wangShuai}
            </span>

            {/* 空亡状态 */}
            {yao.kongWangState !== '不空' && (
                <span className={`text-[10px] px-1.5 py-0.5 rounded ${kongWangColor} ${isDark ? 'bg-ink-800/50' : 'bg-ink-100'
                    }`}>
                    {yao.kongWangState}
                </span>
            )}

            {/* 特殊状态 */}
            {yao.strength.specialStatus !== '无' && (
                <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${specialColor} ${isDark ? 'bg-ink-800/50' : 'bg-ink-100'
                    }`}>
                    {yao.strength.specialStatus}
                </span>
            )}

            {/* 动爻变化 */}
            {yao.changeAnalysis && yao.changeAnalysis.huaType !== '无' && (
                <span className={`text-[10px] px-1.5 py-0.5 rounded ${['化进', '回头生'].includes(yao.changeAnalysis.huaType)
                    ? 'text-green-400'
                    : ['化退', '回头克', '化空', '化墓'].includes(yao.changeAnalysis.huaType)
                        ? 'text-red-400'
                        : 'text-yellow-400'
                    } ${isDark ? 'bg-ink-800/50' : 'bg-ink-100'}`}>
                    {yao.changeAnalysis.huaType}
                </span>
            )}

            {/* 十二长生 */}
            {yao.changSheng && (
                <span className={`text-[10px] ${yao.changSheng.strength === 'strong'
                    ? 'text-green-400'
                    : yao.changSheng.strength === 'weak'
                        ? 'text-red-400'
                        : 'text-yellow-400'
                    }`}>
                    {yao.changSheng.stage}
                </span>
            )}

            {/* 强度分数 */}
            <div className="ml-auto flex items-center gap-1">
                <div className={`w-16 h-1.5 rounded-full overflow-hidden ${isDark ? 'bg-ink-800' : 'bg-ink-200'}`}>
                    <div
                        className={`h-full rounded-full transition-all ${yao.strength.score >= 70 ? 'bg-green-500' :
                            yao.strength.score >= 50 ? 'bg-yellow-500' :
                                yao.strength.score >= 30 ? 'bg-orange-500' : 'bg-red-500'
                            }`}
                        style={{ width: `${yao.strength.score}%` }}
                    />
                </div>
                <span className={`text-[10px] w-6 text-right ${isDark ? 'text-ink-500' : 'text-ink-400'}`}>
                    {yao.strength.score}
                </span>
            </div>
        </div>
    );
};

export default AdvancedAnalysisPanel;
