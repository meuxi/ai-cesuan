import React, { useMemo } from 'react';
import {
    ComposedChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    ReferenceLine,
    Label,
    LabelList
} from 'recharts';
import { KLinePoint } from './types';

// 从 CSS 变量获取 HSL 颜色值并转换为 hex（运行时获取主题色）
const getThemeColor = (cssVar: string, fallback: string): string => {
    if (typeof window === 'undefined') return fallback;
    const root = document.documentElement;
    const value = getComputedStyle(root).getPropertyValue(cssVar).trim();
    if (!value) return fallback;
    // HSL 格式: "142 71% 45%" -> hsl(142, 71%, 45%)
    const [h, s, l] = value.split(' ').map(v => v.trim());
    if (h && s && l) {
        return `hsl(${h}, ${s}, ${l})`;
    }
    return fallback;
};

// 主题颜色常量（作为 CSS 变量的回退值）
const THEME_COLORS = {
    up: 'hsl(142, 71%, 45%)',           // --kline-up
    upStroke: 'hsl(142, 76%, 36%)',     // --kline-up-stroke
    down: 'hsl(0, 84%, 60%)',           // --kline-down
    downStroke: 'hsl(0, 70%, 41%)',     // --kline-down-stroke
    grid: 'hsl(220, 14%, 96%)',         // --kline-grid
    axis: 'hsl(220, 13%, 91%)',         // --kline-axis
    text: 'hsl(220, 9%, 46%)',          // --kline-text
    textMuted: 'hsl(220, 9%, 64%)',     // --kline-text-muted
    ref: 'hsl(215, 13%, 84%)',          // --kline-ref
    dayun: 'hsl(239, 84%, 67%)',        // --kline-dayun
};

interface LifeKLineChartProps {
    data: KLinePoint[];
}

// Recharts Tooltip 组件属性类型
interface TooltipProps {
    active?: boolean;
    payload?: Array<{ payload: KLinePoint }>;
}

// Recharts 自定义 Shape 属性类型
interface CandleShapeProps {
    x: number;
    y: number;
    width: number;
    height: number;
    payload: KLinePoint;
    yAxis?: { scale: (value: number) => number };
}

// Recharts LabelList 属性类型
interface LabelProps {
    x: number;
    y: number;
    width: number;
    value: number;
    maxHigh: number;
}

const CustomTooltip = ({ active, payload }: TooltipProps) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload as KLinePoint;
        const isUp = data.close >= data.open;
        return (
            <div className="bg-card/95 backdrop-blur-sm p-5 rounded-xl shadow-2xl border border-border z-50 w-[320px] md:w-[400px]">
                {/* Header */}
                <div className="flex justify-between items-start mb-3 border-b border-border pb-2">
                    <div>
                        <p className="text-xl font-bold text-foreground font-serif-sc">
                            {data.year} {data.ganZhi}年 <span className="text-base text-muted-foreground font-sans">({data.age}岁)</span>
                        </p>
                        <p className="text-sm text-indigo-600 font-medium mt-1">
                            大运：{data.daYun || '未知'}
                        </p>
                    </div>
                    <div className={`text-base font-bold px-2 py-1 rounded ${isUp ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                        {isUp ? '吉 ▲' : '凶 ▼'}
                    </div>
                </div>

                {/* Data Grid */}
                <div className="grid grid-cols-4 gap-2 text-xs text-muted-foreground mb-4 bg-muted p-2 rounded">
                    <div className="text-center">
                        <span className="block scale-90">开盘</span>
                        <span className="font-mono text-foreground font-bold">{data.open}</span>
                    </div>
                    <div className="text-center">
                        <span className="block scale-90">收盘</span>
                        <span className="font-mono text-foreground font-bold">{data.close}</span>
                    </div>
                    <div className="text-center">
                        <span className="block scale-90">最高</span>
                        <span className="font-mono text-foreground font-bold">{data.high}</span>
                    </div>
                    <div className="text-center">
                        <span className="block scale-90">最低</span>
                        <span className="font-mono text-foreground font-bold">{data.low}</span>
                    </div>
                </div>

                {/* Detailed Reason */}
                <div className="text-sm text-foreground leading-relaxed text-justify max-h-[200px] overflow-y-auto custom-scrollbar">
                    {data.reason}
                </div>
            </div>
        );
    }
    return null;
};

// CandleShape with cleaner wicks - 使用主题颜色
const CandleShape = (props: CandleShapeProps) => {
    const { x, y, width, height, payload, yAxis } = props;

    const isUp = payload.close >= payload.open;
    // 使用主题感知的颜色
    const color = isUp 
        ? getThemeColor('--kline-up', THEME_COLORS.up) 
        : getThemeColor('--kline-down', THEME_COLORS.down);
    const strokeColor = isUp 
        ? getThemeColor('--kline-up-stroke', THEME_COLORS.upStroke) 
        : getThemeColor('--kline-down-stroke', THEME_COLORS.downStroke);

    let highY = y;
    let lowY = y + height;

    if (yAxis && typeof yAxis.scale === 'function') {
        try {
            highY = yAxis.scale(payload.high);
            lowY = yAxis.scale(payload.low);
        } catch (e) {
            highY = y;
            lowY = y + height;
        }
    }

    const center = x + width / 2;

    // Enforce minimum body height so flat doji candles are visible
    const renderHeight = height < 2 ? 2 : height;

    return (
        <g>
            {/* Wick - made slightly thicker for visibility */}
            <line x1={center} y1={highY} x2={center} y2={lowY} stroke={strokeColor} strokeWidth={2} />
            {/* Body */}
            <rect
                x={x}
                y={y}
                width={width}
                height={renderHeight}
                fill={color}
                stroke={strokeColor}
                strokeWidth={1}
                rx={1} // Slight border radius
            />
        </g>
    );
};

// Custom Label Component for the Peak Star - 使用主题颜色
const PeakLabel = (props: LabelProps) => {
    const { x, y, width, value, maxHigh } = props;

    // Only render if this value equals the global max high
    if (value !== maxHigh) return null;

    const starFill = getThemeColor('--kline-down', THEME_COLORS.down);
    const starStroke = getThemeColor('--kline-down-stroke', THEME_COLORS.downStroke);

    return (
        <g>
            {/* Red Star Icon */}
            <path
                d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
                transform={`translate(${x + width / 2 - 6}, ${y - 24}) scale(0.5)`}
                fill={starFill}
                stroke={starStroke}
                strokeWidth="1"
            />
            {/* Score Text */}
            <text
                x={x + width / 2}
                y={y - 28}
                fill={starStroke}
                fontSize={10}
                fontWeight="bold"
                textAnchor="middle"
            >
                {value}
            </text>
        </g>
    );
};

const LifeKLineChart: React.FC<LifeKLineChartProps> = ({ data }) => {
    // 获取主题颜色（运行时）
    const chartColors = useMemo(() => ({
        grid: getThemeColor('--kline-grid', THEME_COLORS.grid),
        axis: getThemeColor('--kline-axis', THEME_COLORS.axis),
        text: getThemeColor('--kline-text', THEME_COLORS.text),
        textMuted: getThemeColor('--kline-text-muted', THEME_COLORS.textMuted),
        ref: getThemeColor('--kline-ref', THEME_COLORS.ref),
        dayun: getThemeColor('--kline-dayun', THEME_COLORS.dayun),
    }), []);

    const transformedData = data.map(d => ({
        ...d,
        bodyRange: [Math.min(d.open, d.close), Math.max(d.open, d.close)],
        // Helper for labelling: we label the 'high' point
        labelPoint: d.high
    }));

    // Identify Da Yun change points to draw reference lines
    const daYunChanges = data.filter((d, i) => {
        if (i === 0) return true;
        return d.daYun !== data[i - 1].daYun;
    });

    // Calculate Global Max High for the peak label
    const maxHigh = data.length > 0 ? Math.max(...data.map(d => d.high)) : 100;

    if (!data || data.length === 0) {
        return <div className="h-[500px] flex items-center justify-center text-muted-foreground">无数据</div>;
    }

    return (
        <div className="w-full h-[600px] bg-card p-2 md:p-6 rounded-xl border border-border shadow-sm relative">
            <div className="mb-6 flex justify-between items-center px-2">
                <h3 className="text-xl font-bold text-foreground font-serif-sc">人生流年大运K线图</h3>
                <div className="flex gap-4 text-xs font-medium">
                    <span className="flex items-center text-green-700 bg-green-50 px-2 py-1 rounded"><div className="w-2 h-2 bg-green-500 mr-2 rounded-full"></div> 吉运 (涨)</span>
                    <span className="flex items-center text-red-700 bg-red-50 px-2 py-1 rounded"><div className="w-2 h-2 bg-red-500 mr-2 rounded-full"></div> 凶运 (跌)</span>
                </div>
            </div>

            <ResponsiveContainer width="100%" height="90%">
                <ComposedChart data={transformedData} margin={{ top: 30, right: 10, left: 0, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke={chartColors.grid} />

                    <XAxis
                        dataKey="age"
                        tick={{ fontSize: 10, fill: chartColors.text }}
                        interval={9}
                        axisLine={{ stroke: chartColors.axis }}
                        tickLine={false}
                        label={{ value: '年龄', position: 'insideBottomRight', offset: -5, fontSize: 10, fill: chartColors.textMuted }}
                    />

                    <YAxis
                        domain={[0, 'auto']}
                        tick={{ fontSize: 10, fill: chartColors.text }}
                        axisLine={false}
                        tickLine={false}
                        label={{ value: '运势分', angle: -90, position: 'insideLeft', fontSize: 10, fill: chartColors.textMuted }}
                    />

                    <Tooltip content={<CustomTooltip />} cursor={{ stroke: chartColors.textMuted, strokeWidth: 1, strokeDasharray: '4 4' }} />

                    {/* Da Yun Reference Lines */}
                    {daYunChanges.map((point, index) => (
                        <ReferenceLine
                            key={`dayun-${index}`}
                            x={point.age}
                            stroke={chartColors.ref}
                            strokeDasharray="3 3"
                            strokeWidth={1}
                        >
                            <Label
                                value={point.daYun}
                                position="top"
                                fill={chartColors.dayun}
                                fontSize={10}
                                fontWeight="bold"
                                className="hidden md:block"
                            />
                        </ReferenceLine>
                    ))}

                    <Bar
                        dataKey="bodyRange"
                        shape={<CandleShape />}
                        isAnimationActive={true}
                        animationDuration={1500}
                    >
                        {/* 
              Only show label for the global Peak 
              We pass the computed maxHigh to the custom label component
            */}
                        <LabelList
                            dataKey="high"
                            position="top"
                            content={<PeakLabel maxHigh={maxHigh} />}
                        />
                    </Bar>

                </ComposedChart>
            </ResponsiveContainer>
        </div>
    );
};

export default LifeKLineChart;
