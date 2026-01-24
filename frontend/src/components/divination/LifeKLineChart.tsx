import React from 'react';
import {
    ComposedChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    ReferenceLine,
    Label
} from 'recharts';

export interface KLinePoint {
    age: number;
    year: number;
    ganZhi: string;
    daYun: string;
    open: number;
    close: number;
    high: number;
    low: number;
    score: number;
    reason: string;
}

interface LifeKLineChartProps {
    data: KLinePoint[];
}

interface TooltipProps {
    active?: boolean;
    payload?: Array<{ payload: KLinePoint }>;
}

const CustomTooltip = ({ active, payload }: TooltipProps) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload as KLinePoint;
        const isUp = data.close >= data.open;
        return (
            <div className="bg-card/95 backdrop-blur-sm p-5 rounded-xl shadow-2xl border border-border z-50 w-[320px] md:w-[400px]">
                <div className="flex justify-between items-start mb-3 border-b border-border pb-2">
                    <div>
                        <p className="text-xl font-bold text-foreground">
                            {data.year} {data.ganZhi}年 <span className="text-base text-muted-foreground">({data.age}岁)</span>
                        </p>
                        <p className="text-sm text-indigo-600 font-medium mt-1">
                            大运：{data.daYun || '未知'}
                        </p>
                    </div>
                    <div className={`text-base font-bold px-2 py-1 rounded ${isUp ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                        {isUp ? '吉 ▲' : '凶 ▼'}
                    </div>
                </div>

                <div className="grid grid-cols-4 gap-2 text-xs text-muted-foreground mb-4 bg-secondary p-2 rounded">
                    <div className="text-center">
                        <span className="block text-[10px]">开盘</span>
                        <span className="font-mono text-foreground font-bold">{data.open}</span>
                    </div>
                    <div className="text-center">
                        <span className="block text-[10px]">收盘</span>
                        <span className="font-mono text-foreground font-bold">{data.close}</span>
                    </div>
                    <div className="text-center">
                        <span className="block text-[10px]">最高</span>
                        <span className="font-mono text-foreground font-bold">{data.high}</span>
                    </div>
                    <div className="text-center">
                        <span className="block text-[10px]">最低</span>
                        <span className="font-mono text-foreground font-bold">{data.low}</span>
                    </div>
                </div>

                <div className="text-sm text-foreground leading-relaxed text-justify max-h-[200px] overflow-y-auto">
                    {data.reason}
                </div>
            </div>
        );
    }
    return null;
};

interface CandleShapeProps {
    x?: number;
    y?: number;
    width?: number;
    height?: number;
    payload?: KLinePoint;
    yAxis?: { scale: (value: number) => number };
}

const CandleShape = (props: CandleShapeProps) => {
    const { x = 0, y = 0, width = 0, height = 0, payload, yAxis } = props;
    
    if (!payload) return null;

    const isUp = payload.close >= payload.open;
    const color = isUp ? '#ef4444' : '#22c55e';
    const strokeColor = isUp ? '#dc2626' : '#16a34a';

    let highY = y;
    let lowY = y + height;

    if (yAxis && typeof yAxis.scale === 'function') {
        try {
            highY = yAxis.scale(payload.high);
            lowY = yAxis.scale(payload.low);
        } catch {
            highY = y;
            lowY = y + height;
        }
    }

    const center = x + width / 2;
    const renderHeight = height < 1 ? 1 : height;

    return (
        <g>
            <line x1={center} y1={highY} x2={center} y2={lowY} stroke={strokeColor} strokeWidth={1.5} />
            <rect
                x={x}
                y={y}
                width={width}
                height={renderHeight}
                fill={color}
                stroke={strokeColor}
                strokeWidth={0.5}
            />
        </g>
    );
};

const LifeKLineChart: React.FC<LifeKLineChartProps> = ({ data }) => {
    const transformedData = data.map(d => ({
        ...d,
        bodyRange: [Math.min(d.open, d.close), Math.max(d.open, d.close)],
    }));

    const daYunChanges = data.filter((d, i) => {
        if (i === 0) return true;
        return d.daYun !== data[i - 1].daYun;
    });

    if (!data || data.length === 0) {
        return <div className="h-[500px] flex items-center justify-center text-muted-foreground">无数据</div>;
    }

    return (
        <div className="w-full h-[600px] bg-card p-2 md:p-6 rounded-xl border border-border shadow-sm relative">
            <div className="mb-6 flex justify-between items-center px-2">
                <h3 className="text-xl font-bold text-foreground">人生流年大运K线图</h3>
                <div className="flex gap-4 text-xs font-medium">
                    <span className="flex items-center text-red-700 bg-red-50 px-2 py-1 rounded">
                        <div className="w-2 h-2 bg-red-500 mr-2 rounded-full"></div> 吉运 (涨)
                    </span>
                    <span className="flex items-center text-green-700 bg-green-50 px-2 py-1 rounded">
                        <div className="w-2 h-2 bg-green-500 mr-2 rounded-full"></div> 凶运 (跌)
                    </span>
                </div>
            </div>

            <ResponsiveContainer width="100%" height="90%">
                <ComposedChart data={transformedData} margin={{ top: 20, right: 10, left: 0, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />

                    <XAxis
                        dataKey="age"
                        tick={{ fontSize: 10, fill: '#6b7280' }}
                        interval={9}
                        axisLine={{ stroke: '#e5e7eb' }}
                        tickLine={false}
                        label={{ value: '年龄', position: 'insideBottomRight', offset: -5, fontSize: 10, fill: '#9ca3af' }}
                    />

                    <YAxis
                        domain={[0, 100]}
                        tick={{ fontSize: 10, fill: '#6b7280' }}
                        axisLine={false}
                        tickLine={false}
                        label={{ value: '运势分', angle: -90, position: 'insideLeft', fontSize: 10, fill: '#9ca3af' }}
                    />

                    <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#9ca3af', strokeWidth: 1, strokeDasharray: '4 4' }} />

                    {daYunChanges.map((point, index) => (
                        <ReferenceLine
                            key={`dayun-${index}`}
                            x={point.age}
                            stroke="#cbd5e1"
                            strokeDasharray="3 3"
                            strokeWidth={1}
                        >
                            <Label
                                value={point.daYun}
                                position="top"
                                fill="#6366f1"
                                fontSize={10}
                                fontWeight="bold"
                            />
                        </ReferenceLine>
                    ))}

                    <Bar
                        dataKey="bodyRange"
                        shape={<CandleShape />}
                        isAnimationActive={true}
                        animationDuration={1500}
                    />

                </ComposedChart>
            </ResponsiveContainer>
        </div>
    );
};

export default LifeKLineChart;
