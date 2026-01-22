import { useState, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';
import { logger } from '@/utils/logger';
import { saveHistory } from '@/utils/divinationHistory';
import { Sparkles, RefreshCw, CheckCircle, XCircle, Hand, Bot, Loader2 } from 'lucide-react';

interface ChouqianResult {
    id: number;
    number: number;
    title: string;
    content: string;
    image: string;
    type: string;
    type_name: string;
}

type GameStage = 'select' | 'drawing' | 'drawn' | 'shengbei' | 'result';

// 圣杯结果类型：shengbei=圣杯(一阳一阴), xiaobei=笑杯(二阳), yinbei=阴杯(二阴)
type BeiResult = 'shengbei' | 'xiaobei' | 'yinbei';

interface ShengbeiState {
    count: number;
    history: BeiResult[];
    isFailed: boolean;
    lastResult?: BeiResult;
    // 两枚铜钱的状态
    coin1Yang: boolean;
    coin2Yang: boolean;
}

const QIAN_TYPES = [
    { key: 'guanyin', name: '观音灵签', count: 100, color: 'from-red-600 to-orange-600', hasImage: true, prayer: '救苦救难观音菩萨' },
    { key: 'guandi', name: '关帝灵签', count: 100, color: 'from-green-600 to-teal-600', hasImage: true, prayer: '关圣帝君' },
    { key: 'lvzu', name: '吕祖灵签', count: 100, color: 'from-blue-600 to-indigo-600', hasImage: true, prayer: '纯阳吕祖' },
    { key: 'tianhou', name: '天后灵签', count: 60, color: 'from-pink-600 to-rose-600', hasImage: true, prayer: '天上圣母妈祖' },
    { key: 'huangdaxian', name: '黄大仙灵签', count: 100, color: 'from-yellow-600 to-amber-600', hasImage: false, prayer: '黄大仙师' },
];

// 圣杯组件 - 按源码HTML结构，优化尺寸适配
const ShengbeiImage = ({ isAnimating, result }: { isAnimating: boolean; result?: BeiResult }) => {
    // 掷杯动画GIF - 适配容器高度
    if (isAnimating) {
        return (
            <div className="flex justify-center items-center h-full">
                <img
                    src="/images/qian/shengbei/shengbeidonghua.gif"
                    alt="正在掷杯"
                    className="max-h-[108px] sm:max-h-[126px] w-auto object-contain"
                />
            </div>
        );
    }

    // 掷杯结果静态图 - 统一尺寸控制
    if (result) {
        const imageMap = {
            shengbei: '/images/qian/shengbei/shengbei.png',
            xiaobei: '/images/qian/shengbei/xiaobei.png',
            yinbei: '/images/qian/shengbei/yinbei.png'
        };

        return (
            <div className="flex justify-center items-center h-full">
                <img
                    src={imageMap[result]}
                    alt={result === 'shengbei' ? '圣杯' : result === 'xiaobei' ? '笑杯' : '阴杯'}
                    className="max-h-[108px] sm:max-h-[126px] w-auto object-contain"
                />
            </div>
        );
    }

    return null;
};

// 祥云粒子组件
const AuspiciousParticles = ({ isActive }: { isActive: boolean }) => (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {isActive && [...Array(12)].map((_, i) => (
            <motion.div
                key={i}
                className="absolute w-2 h-2 rounded-full"
                style={{
                    left: `${20 + Math.random() * 60}%`,
                    bottom: '20%',
                    background: `radial-gradient(circle, ${['#FFD700', '#FFA500', '#FF6B6B', '#E8D4A8'][i % 4]} 0%, transparent 70%)`,
                }}
                initial={{ opacity: 0, y: 0, scale: 0 }}
                animate={{
                    opacity: [0, 0.8, 0.6, 0],
                    y: [-20, -80 - Math.random() * 60],
                    x: [0, (Math.random() - 0.5) * 40],
                    scale: [0, 1.5, 1, 0.5],
                }}
                transition={{
                    duration: 2 + Math.random(),
                    delay: i * 0.15,
                    repeat: Infinity,
                    ease: 'easeOut',
                }}
            />
        ))}
    </div>
);

// 签筒组件 - 按源码HTML结构，优化响应式尺寸
const QianTong = ({ isShaking }: { isShaking: boolean }) => {
    return (
        <div className="flex justify-center items-center min-h-[250px]">
            <img
                src="/images/qian/qiantong/qiuqian.gif"
                alt="求签"
                style={{ width: '200px', height: '200px' }}
            />
        </div>
    );
};

export default function Chouqian() {
    const { t } = useTranslation();
    const [stage, setStage] = useState<GameStage>('select');
    const [result, setResult] = useState<ChouqianResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [userName, setUserName] = useState('');
    const [question, setQuestion] = useState('');
    const [selectedType, setSelectedType] = useState('guanyin');
    const [qianNumber, setQianNumber] = useState<number>(0);
    const [shengbei, setShengbei] = useState<ShengbeiState>({ count: 0, history: [], isFailed: false, coin1Yang: true, coin2Yang: true });
    const [throwingBei, setThrowingBei] = useState(false);
    const [beiAnimating, setBeiAnimating] = useState(false);
    const [beiResult, setBeiResult] = useState<{ left: boolean; right: boolean } | null>(null);
    const [showStick, setShowStick] = useState(false);
    const [showQianAnimation, setShowQianAnimation] = useState(false);

    // AI解签状态
    const [aiJieqian, setAiJieqian] = useState('');
    const [aiLoading, setAiLoading] = useState(false);
    const [showAiPanel, setShowAiPanel] = useState(false);
    const aiContentRef = useRef<HTMLDivElement>(null);

    const currentType = QIAN_TYPES.find(t => t.key === selectedType) || QIAN_TYPES[0];

    const handleTypeChange = (typeKey: string) => {
        setSelectedType(typeKey);
        setStage('select');
        setResult(null);
        setQianNumber(0);
        setShowStick(false);
        setShowQianAnimation(false);
        setShengbei({ count: 0, history: [], isFailed: false, coin1Yang: true, coin2Yang: true });
        setAiJieqian('');
        setShowAiPanel(false);
        setUserName('');
        setQuestion('');
    };

    const handleStartDraw = async () => {
        setLoading(true);
        setStage('drawing');
        setShowStick(false);
        setShowQianAnimation(true);

        try {
            const response = await fetch('/api/chouqian/draw_start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: selectedType, user_name: userName, question })
            });
            if (!response.ok) throw new Error('抽签失败');
            const data = await response.json();
            setQianNumber(data.qian_number);

            // 播放求签动画3秒
            await new Promise(r => setTimeout(r, 3000));

            // 动画结束，显示签条
            setShowQianAnimation(false);
            setShowStick(true);
            setStage('drawn');
            setShengbei({ count: 0, history: [], isFailed: false, coin1Yang: true, coin2Yang: true });
            setBeiResult(null);
        } catch (error) {
            logger.error('抽签错误:', error);
            alert('抽签失败，请重试');
            setStage('select');
        } finally {
            setLoading(false);
        }
    };

    const handleThrowShengbei = async () => {
        setThrowingBei(true);
        setBeiAnimating(true);
        setBeiResult(null);

        try {
            // 两枚铜钱随机结果
            const coin1 = Math.random() > 0.5; // true=阳面(平), false=阴面(凸)
            const coin2 = Math.random() > 0.5;

            // 判定结果：一阳一阴=圣杯, 二阳=笑杯, 二阴=阴杯
            let beiType: BeiResult;
            if (coin1 !== coin2) {
                beiType = 'shengbei'; // 一阳一阴 = 圣杯
            } else if (coin1 && coin2) {
                beiType = 'xiaobei'; // 二阳 = 笑杯
            } else {
                beiType = 'yinbei'; // 二阴 = 阴杯
            }

            // 等待动画完成
            await new Promise(r => setTimeout(r, 2200));

            // 动画停止时立即设置结果，避免结果变动
            setBeiAnimating(false);
            setBeiResult({ left: coin1, right: coin2 });

            // 立即更新lastResult显示正确的结果图片
            if (beiType === 'shengbei') {
                const newCount = shengbei.count + 1;
                const isComplete = newCount >= 3;
                setShengbei({
                    count: newCount,
                    history: [...shengbei.history, 'shengbei'],
                    isFailed: false,
                    lastResult: 'shengbei',
                    coin1Yang: coin1,
                    coin2Yang: coin2
                });
                // 延迟跳转到结果页面
                if (isComplete) {
                    setTimeout(() => handleViewResult(), 1500);
                }
            } else if (beiType === 'yinbei') {
                setShengbei({
                    count: 0,
                    history: [...shengbei.history, 'yinbei'],
                    isFailed: true,
                    lastResult: 'yinbei',
                    coin1Yang: coin1,
                    coin2Yang: coin2
                });
            } else {
                setShengbei({
                    ...shengbei,
                    history: [...shengbei.history, 'xiaobei'],
                    lastResult: 'xiaobei',
                    coin1Yang: coin1,
                    coin2Yang: coin2
                });
            }
        } catch (error) {
            logger.error('掷杯错误:', error);
        } finally {
            setThrowingBei(false);
        }
    };

    const handleViewResult = async () => {
        try {
            const response = await fetch(`/api/chouqian/detail/${selectedType}/${qianNumber}`);
            const data = await response.json();
            setResult(data);
            setStage('result');

            // 保存历史记录
            saveHistory({
                type: 'chouqian',
                title: `${data.type_name || currentType.name} 第${data.number}签`,
                prompt: question || '未填写问题',
                result: `**${data.title}**\n\n${data.content}`,
                metadata: {
                    userName: userName || undefined,
                    question: question || undefined,
                    qianType: selectedType,
                    qianNumber: data.number,
                    signTitle: data.title,
                }
            });
        } catch (error) {
            logger.error('获取签文错误:', error);
        }
    };

    const handleReset = () => {
        setStage('select');
        setResult(null);
        setQianNumber(0);
        setShengbei({ count: 0, history: [], isFailed: false, coin1Yang: true, coin2Yang: true });
        setAiJieqian('');
        setShowAiPanel(false);
    };

    // AI解签功能
    const handleAiJieqian = async () => {
        if (!result) return;

        setAiLoading(true);
        setAiJieqian('');
        setShowAiPanel(true);

        try {
            const response = await fetch('/api/chouqian/ai_jieqian', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    qian_type: selectedType,
                    qian_number: result.number,
                    user_name: userName,
                    question: question
                })
            });

            if (!response.ok) {
                throw new Error('AI解签失败');
            }

            const reader = response.body?.getReader();
            const decoder = new TextDecoder();

            if (reader) {
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\n');

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.slice(6));
                                if (typeof data === 'string') {
                                    setAiJieqian(prev => prev + data);
                                    // 自动滚动到底部
                                    if (aiContentRef.current) {
                                        aiContentRef.current.scrollTop = aiContentRef.current.scrollHeight;
                                    }
                                }
                            } catch {
                                // 忽略解析错误
                            }
                        }
                    }
                }
            }
        } catch (error) {
            logger.error('AI解签错误:', error);
            setAiJieqian('AI解签服务暂时不可用，请稍后重试。');
        } finally {
            setAiLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background relative overflow-hidden">
            {/* 背景装饰 - 简化古风质感 */}
            <div className="fixed inset-0 pointer-events-none overflow-hidden">
                {/* 纸张纹理效果 */}
                <div className="absolute inset-0 opacity-30" style={{
                    backgroundImage: `repeating-linear-gradient(0deg, transparent, transparent 2px, hsl(var(--muted)/0.1) 2px, hsl(var(--muted)/0.1) 4px)`
                }}>
                </div>

                {/* 顶部柔和光晕 */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-96">
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-muted/20 rounded-full blur-3xl" />
                </div>

                {/* 浮动光点 - 减少数量和透明度 */}
                {[...Array(5)].map((_, i) => (
                    <motion.div
                        key={i}
                        className="absolute w-1 h-1 rounded-full"
                        style={{
                            left: `${20 + i * 15}%`,
                            top: `${25 + (i % 2) * 30}%`,
                            background: 'radial-gradient(circle, hsl(var(--primary)/0.4) 0%, transparent 70%)'
                        }}
                        animate={{
                            y: [0, -15, 0],
                            opacity: [0.3, 0.5, 0.3],
                            scale: [1, 1.3, 1],
                        }}
                        transition={{
                            duration: 4 + i * 0.5,
                            repeat: Infinity,
                            delay: i * 0.5,
                            ease: 'easeInOut',
                        }}
                    />
                ))}

                {/* 柔和装饰光晕 */}
                <div className="absolute top-32 left-1/4 w-64 h-64 bg-primary/10 rounded-full blur-3xl" />
                <div className="absolute bottom-1/4 right-1/4 w-48 h-48 bg-primary/5 rounded-full blur-3xl" />

                {/* 轻烟缭绕效果 - 降低透明度 */}
                <motion.div
                    className="absolute top-1/4 left-1/2 w-[400px] h-32 rounded-full blur-2xl"
                    style={{ background: 'linear-gradient(to top, transparent, hsl(var(--primary)/0.08), transparent)' }}
                    animate={{
                        x: ['-50%', '-45%', '-55%', '-50%'],
                        y: [0, -15, 8, 0],
                        opacity: [0.4, 0.6, 0.5, 0.4]
                    }}
                    transition={{ duration: 15, repeat: Infinity, ease: 'easeInOut' }}
                />

                {/* 边缘渐变 */}
                <div className="absolute inset-0 bg-gradient-to-b from-muted-foreground/5 via-transparent to-muted-foreground/8" />
            </div>

            <div className="container mx-auto px-3 sm:px-4 py-6 sm:py-12 relative">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="max-w-4xl mx-auto"
                >
                    {/* 标题 - 响应式 */}
                    <div className="text-center mb-6 sm:mb-8">
                        <h1 className="text-2xl sm:text-4xl md:text-5xl font-bold text-foreground mb-2 sm:mb-4 flex items-center justify-center gap-2 sm:gap-3">
                            <Sparkles className="w-6 h-6 sm:w-10 sm:h-10 text-primary" />
                            {t('chouqian.title')}
                            <Sparkles className="w-6 h-6 sm:w-10 sm:h-10 text-primary" />
                        </h1>
                        <p className="text-sm sm:text-lg text-muted-foreground">{t('chouqian.subtitle')}</p>
                    </div>

                    {/* 灵签类型选择 - 紧凑卡片布局 */}
                    <div className="flex flex-wrap justify-center gap-2 sm:gap-3 mb-6 sm:mb-8">
                        {QIAN_TYPES.map((type) => (
                            <button
                                key={type.key}
                                onClick={() => handleTypeChange(type.key)}
                                className={`px-3 py-2 sm:px-4 sm:py-2.5 rounded-lg transition-all transform hover:scale-105 active:scale-95 ${selectedType === type.key
                                    ? `bg-gradient-to-r ${type.color} text-white shadow-md ring-2 ring-offset-1 ring-primary/30`
                                    : 'bg-card text-foreground hover:bg-accent shadow-sm border border-border'
                                    }`}
                            >
                                <div className="font-medium text-xs sm:text-sm whitespace-nowrap">{type.name}</div>
                                <div className="text-[10px] sm:text-xs opacity-70">{type.count}{t('chouqian.signs')}</div>
                            </button>
                        ))}
                    </div>

                    <AnimatePresence mode="wait">
                        {/* 抽签阶段 - 播放求签动画 */}
                        {stage === 'drawing' && (
                            <motion.div
                                key="drawing"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="text-center"
                            >
                                <div>
                                    {/* 求签动画 - 按原图200x200像素显示 */}
                                    <div className="flex justify-center items-center min-h-[250px]">
                                        <img
                                            src="/images/qian/qiantong/qiuqian.gif"
                                            alt="求签"
                                            style={{ width: '200px', height: '200px' }}
                                        />
                                    </div>

                                    <motion.p
                                        className="mt-6 text-primary text-lg font-medium"
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        transition={{ delay: 0.5 }}
                                    >
                                        {t('chouqian.drawingSign')}
                                    </motion.p>
                                </div>
                            </motion.div>
                        )}

                        {/* 显示签条阶段 - 对应原网站stepQian状态 */}
                        {stage === 'drawn' && (
                            <motion.div
                                key="drawn"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="text-center"
                            >
                                <div>
                                    {/* stepQianTop - 顶部文字 */}
                                    <motion.p
                                        className="text-foreground text-lg mb-6"
                                        initial={{ opacity: 0, y: -20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                    >
                                        {currentType.name} #{qianNumber}
                                    </motion.p>

                                    {/* stepQianId - 签条（按原图尺寸44x230像素）*/}
                                    <motion.div
                                        initial={{ opacity: 0, y: -30 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.2, type: "spring" }}
                                        className="flex justify-center my-8"
                                    >
                                        <div
                                            className="relative"
                                            style={{
                                                width: '44px',
                                                height: '230px',
                                                backgroundImage: 'url(/images/qian/qiantong/qian.png)',
                                                backgroundSize: '44px 230px',
                                                backgroundRepeat: 'no-repeat',
                                                filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.2))'
                                            }}
                                        >
                                            {/* 竖排文字容器："第 X 签" */}
                                            <div
                                                className="absolute inset-0 flex flex-col items-center justify-center"
                                                style={{
                                                    paddingTop: '55px',
                                                    paddingBottom: '15px',
                                                }}
                                            >
                                                {/* "第"字 */}
                                                <span
                                                    style={{
                                                        fontSize: '16px',
                                                        color: '#8B4513',
                                                        fontWeight: '700',
                                                        fontFamily: '"STKaiti", "KaiTi", "楷体", serif',
                                                        lineHeight: 1.2,
                                                    }}
                                                >
                                                    第
                                                </span>
                                                {/* 签号数字 - 竖排显示每个数字 */}
                                                <div
                                                    className="flex flex-col items-center"
                                                    style={{
                                                        margin: '2px 0',
                                                    }}
                                                >
                                                    {String(qianNumber).split('').map((digit, idx) => (
                                                        <span
                                                            key={idx}
                                                            style={{
                                                                fontSize: '20px',
                                                                color: '#C62828',
                                                                fontWeight: '900',
                                                                fontFamily: '"STKaiti", "KaiTi", "楷体", Arial, sans-serif',
                                                                lineHeight: 1.1,
                                                            }}
                                                        >
                                                            {digit}
                                                        </span>
                                                    ))}
                                                </div>
                                                {/* "签"字 */}
                                                <span
                                                    style={{
                                                        fontSize: '16px',
                                                        color: '#8B4513',
                                                        fontWeight: '700',
                                                        fontFamily: '"STKaiti", "KaiTi", "楷体", serif',
                                                        lineHeight: 1.2,
                                                    }}
                                                >
                                                    签
                                                </span>
                                            </div>
                                        </div>
                                    </motion.div>

                                    {/* stepBeiLast - 底部提示 */}
                                    <motion.p
                                        className="text-muted-foreground text-base mb-6"
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        transition={{ delay: 0.4 }}
                                    >
                                        {t('chouqian.needThreeShengbei')}
                                    </motion.p>

                                    {/* stepQianBtn - 开始掷杯按钮 */}
                                    <motion.button
                                        onClick={() => setStage('shengbei')}
                                        className="px-10 py-3 bg-primary hover:bg-primary/90 text-primary-foreground text-lg font-medium rounded transition-colors"
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        transition={{ delay: 0.6 }}
                                        whileHover={{ scale: 1.02 }}
                                        whileTap={{ scale: 0.98 }}
                                    >
                                        开始掷杯
                                    </motion.button>
                                </div>
                            </motion.div>
                        )}

                        {stage === 'select' && (
                            <motion.div
                                key="select"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="max-w-xl mx-auto"
                            >

                                <h2 className="text-2xl font-bold text-center mb-6 text-foreground">
                                    {currentType.name}
                                </h2>
                                <div className="text-center mb-6 text-muted-foreground text-base">
                                    <p>{t('chouqian.beforeDraw')}</p>
                                    <p className="font-semibold text-primary my-2 text-lg">
                                        "{currentType.prayer}"
                                    </p>
                                    <p>{t('chouqian.threeTimesChant')}</p>
                                </div>
                                <div className="space-y-4">
                                    <div>
                                        <label className="block text-sm font-medium text-foreground mb-2">{t('chouqian.nameOptional')}</label>
                                        <input type="text" value={userName} onChange={(e) => setUserName(e.target.value)}
                                            className="w-full px-4 py-3 border border-border rounded bg-background/60 focus:bg-background focus:border-primary outline-none text-foreground"
                                            placeholder={t('chouqian.namePlaceholder')} />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-foreground mb-2">{t('chouqian.questionOptional')}</label>
                                        <textarea value={question} onChange={(e) => setQuestion(e.target.value)} rows={3}
                                            className="w-full px-4 py-3 border border-border rounded bg-background/60 focus:bg-background focus:border-primary outline-none resize-none text-foreground"
                                            placeholder={t('chouqian.questionPlaceholder')} />
                                    </div>
                                    <button
                                        onClick={handleStartDraw}
                                        disabled={loading}
                                        className="w-full bg-primary hover:bg-primary/90 text-primary-foreground py-4 rounded font-semibold text-lg disabled:opacity-50 transition-colors"
                                    >
                                        {loading ? <span className="flex items-center justify-center gap-2"><RefreshCw className="w-5 h-5 animate-spin" />{t('chouqian.drawing')}</span>
                                            : <span className="flex items-center justify-center gap-2"><Sparkles className="w-5 h-5" />{t('chouqian.startDraw')}</span>}
                                    </button>
                                </div>
                            </motion.div>
                        )}

                        {stage === 'shengbei' && (
                            <motion.div key="shengbei" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                                className="text-center max-w-2xl mx-auto">
                                <h2 className="text-3xl font-bold mb-2 text-foreground">
                                    第 {qianNumber} 签
                                </h2>
                                <p className="text-muted-foreground mb-6 text-sm">{t('chouqian.needThreeConsecutive')}</p>

                                {/* 圣杯进度指示器 - 只显示圣杯计数 */}
                                <div className="flex justify-center gap-2 sm:gap-3 mb-4 sm:mb-6">
                                    {[0, 1, 2].map((i) => (
                                        <motion.div
                                            key={i}
                                            className={`w-10 h-10 sm:w-12 sm:h-12 rounded-full flex items-center justify-center text-base sm:text-lg font-bold border-2 transition-all ${i < shengbei.count
                                                ? 'bg-green-500 border-green-600 text-white shadow-lg shadow-green-200'
                                                : 'bg-muted border-border text-muted-foreground'
                                                }`}
                                            initial={false}
                                            animate={i < shengbei.count ? { scale: [1, 1.2, 1] } : {}}
                                        >
                                            {i < shengbei.count
                                                ? <CheckCircle className="w-5 h-5 sm:w-6 sm:h-6" />
                                                : i + 1
                                            }
                                        </motion.div>
                                    ))}
                                </div>

                                {/* 圣杯规则说明 */}
                                <div className="text-center text-xs text-muted-foreground mb-3 space-y-0.5">
                                    <p>🟢 {t('chouqian.shengbeiRule')}</p>
                                    <p>🟡 {t('chouqian.xiaobeiRule')}</p>
                                    <p>⚫ {t('chouqian.yinbeiRule')}</p>
                                </div>

                                {/* 圣杯掷出动画区域 */}
                                <div className="relative h-40 sm:h-48 mb-4 sm:mb-6">
                                    <div className="absolute inset-0" />

                                    {/* 装饰边框 */}
                                    <div className="absolute inset-2 border-2 border-primary/30 rounded-lg">
                                        <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 px-4 bg-muted">
                                            <span className="text-primary/80 text-xs">{t('chouqian.throwBei')}</span>
                                        </div>
                                    </div>

                                    {/* 木台表面 */}
                                    <div className="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-primary/30 via-primary/20 to-primary/10 shadow-inner">
                                        <div className="absolute inset-x-4 top-1 h-px bg-primary/20" />
                                    </div>

                                    {/* 圣杯展示区 */}
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        {beiAnimating || shengbei.lastResult ? (
                                            <ShengbeiImage
                                                isAnimating={beiAnimating}
                                                result={shengbei.lastResult}
                                            />
                                        ) : (
                                            <motion.div
                                                className="flex flex-col items-center gap-2"
                                                animate={{ opacity: [0.5, 1, 0.5] }}
                                                transition={{ duration: 2, repeat: Infinity }}
                                            >
                                                <Hand className="w-8 h-8 text-primary/60" />
                                                <span className="text-primary/60 text-sm">{t('chouqian.throwBei')}</span>
                                            </motion.div>
                                        )}
                                    </div>

                                    {/* 结果提示 - 精致徽章样式 */}
                                    {beiResult && !beiAnimating && (
                                        <motion.div
                                            className={`absolute top-6 left-1/2 -translate-x-1/2 px-6 py-2 rounded-full text-white font-bold shadow-lg ${shengbei.lastResult === 'shengbei'
                                                ? 'bg-gradient-to-r from-green-500 to-emerald-600'
                                                : shengbei.lastResult === 'yinbei'
                                                    ? 'bg-gradient-to-r from-gray-600 to-gray-700'
                                                    : 'bg-gradient-to-r from-yellow-500 to-amber-600'
                                                }`}
                                            initial={{ opacity: 0, scale: 0.5, y: -30 }}
                                            animate={{ opacity: 1, scale: 1, y: 0 }}
                                            transition={{ type: 'spring', damping: 15 }}
                                        >
                                            <span className="flex items-center gap-2">
                                                {shengbei.lastResult === 'shengbei'
                                                    ? <><CheckCircle className="w-5 h-5" /> {t('chouqian.shengbeiResult')}</>
                                                    : shengbei.lastResult === 'yinbei'
                                                        ? <><XCircle className="w-5 h-5" /> {t('chouqian.yinbeiResult')}</>
                                                        : <><RefreshCw className="w-5 h-5" /> {t('chouqian.xiaobeiResult')}</>
                                                }
                                            </span>
                                        </motion.div>
                                    )}
                                </div>

                                {/* 操作区域 */}
                                {shengbei.isFailed ? (
                                    <motion.div
                                        className="space-y-4"
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                    >
                                        <p className="text-foreground text-lg font-semibold">⚫ {t('chouqian.yinbeiResult')}</p>
                                        <p className="text-muted-foreground text-sm">{t('chouqian.redraw')}</p>
                                        <button onClick={handleReset}
                                            className="bg-gradient-to-r from-gray-600 to-gray-700 text-white px-8 py-3 rounded-lg font-semibold hover:from-gray-700 hover:to-gray-800 transition-all">
                                            {t('chouqian.redraw')}
                                        </button>
                                    </motion.div>
                                ) : shengbei.count >= 3 ? (
                                    <p className="text-green-600 text-xl font-semibold">
                                        ✨ {t('chouqian.shengbeiResult')}
                                    </p>
                                ) : (
                                    <button
                                        onClick={handleThrowShengbei}
                                        disabled={throwingBei}
                                        className="bg-primary hover:bg-primary/90 text-primary-foreground px-10 py-4 rounded font-semibold text-lg disabled:opacity-50 transition-colors"
                                    >
                                        {throwingBei
                                            ? <span className="flex items-center gap-2"><RefreshCw className="w-5 h-5 animate-spin" />{t('chouqian.throwing')}</span>
                                            : <span className="flex items-center gap-2"><Hand className="w-5 h-5" />{t('chouqian.throwBei')} ({shengbei.count}/3)</span>
                                        }
                                    </button>
                                )}
                            </motion.div>
                        )}

                        {stage === 'result' && result && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="max-w-4xl mx-auto"
                            >
                                <h2 className="text-2xl md:text-3xl font-bold text-center mb-2 text-foreground">
                                    {result.type_name} 第 {result.number} 签
                                </h2>
                                <p className="text-center mb-6 text-muted-foreground text-lg">
                                    {result.title}
                                </p>

                                {/* 签图 */}
                                {result.image && result.image.trim() !== '' && (
                                    <div className="flex justify-center mb-6">
                                        <img
                                            src={result.image}
                                            alt={`${result.type_name}第${result.number}签`}
                                            className="max-w-full h-auto max-h-[500px] object-contain"
                                            onError={(e) => {
                                                e.currentTarget.style.display = 'none';
                                            }}
                                        />
                                    </div>
                                )}

                                {/* 签文内容 */}
                                <div className="mb-6">
                                    <h3 className="text-lg font-semibold text-foreground mb-3">
                                        {t('chouqian.signText')}
                                    </h3>
                                    <p className="text-foreground leading-relaxed whitespace-pre-line">
                                        {result.content || '签文内容加载中...'}
                                    </p>
                                </div>

                                {/* AI解签按钮 - 华丽风格 */}
                                <div className="mt-6">
                                    <motion.button
                                        onClick={handleAiJieqian}
                                        disabled={aiLoading}
                                        className="w-full bg-black dark:bg-white text-white dark:text-black py-3.5 rounded-xl font-semibold disabled:opacity-50 transition-all flex items-center justify-center gap-2 shadow-lg relative overflow-hidden hover:bg-gray-800 dark:hover:bg-gray-200"
                                        style={{ backgroundSize: '200% 100%' }}
                                        whileHover={{ scale: 1.02 }}
                                        whileTap={{ scale: 0.98 }}
                                    >
                                        {/* 按钮流光效果 */}
                                        <motion.div
                                            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/25 to-transparent"
                                            initial={{ x: '-100%' }}
                                            animate={{ x: '100%' }}
                                            transition={{ duration: 2, repeat: Infinity, repeatDelay: 0.5 }}
                                        />
                                        {aiLoading ? (
                                            <span className="flex items-center gap-2 relative">
                                                <Loader2 className="w-5 h-5 animate-spin" />
                                                {t('chouqian.aiInterpreting')}
                                            </span>
                                        ) : (
                                            <span className="flex items-center gap-2 relative">
                                                <Bot className="w-5 h-5" />
                                                ✨ {t('chouqian.aiInterpret')}
                                            </span>
                                        )}
                                    </motion.button>
                                </div>

                                {/* AI解签结果面板 - 神秘风格 */}
                                <AnimatePresence>
                                    {showAiPanel && (
                                        <motion.div
                                            initial={{ opacity: 0, height: 0, y: 20 }}
                                            animate={{ opacity: 1, height: 'auto', y: 0 }}
                                            exit={{ opacity: 0, height: 0, y: -10 }}
                                            transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
                                            className="mt-4 bg-muted rounded-xl border border-border overflow-hidden shadow-lg"
                                        >
                                            <div className="px-4 py-3 bg-black dark:bg-white text-white dark:text-black flex items-center gap-2 relative overflow-hidden">
                                                {/* 标题栏动态背景 */}
                                                <motion.div
                                                    className="absolute inset-0 opacity-30"
                                                    style={{ backgroundImage: 'radial-gradient(circle at 50% 50%, rgba(255,255,255,0.3) 0%, transparent 50%)' }}
                                                    animate={{ scale: [1, 1.2, 1], opacity: [0.2, 0.4, 0.2] }}
                                                    transition={{ duration: 3, repeat: Infinity }}
                                                />
                                                <Bot className="w-5 h-5 relative" />
                                                <span className="font-semibold relative">🔮 {t('chouqian.aiInterpret')}</span>
                                                {aiLoading && <Loader2 className="w-4 h-4 animate-spin ml-auto relative" />}
                                            </div>
                                            <div
                                                ref={aiContentRef}
                                                className="p-4 max-h-96 overflow-y-auto scrollbar-thin scrollbar-thumb-purple-300 scrollbar-track-transparent"
                                            >
                                                {aiJieqian ? (
                                                    <motion.p
                                                        className="text-foreground leading-relaxed whitespace-pre-wrap text-sm"
                                                        initial={{ opacity: 0 }}
                                                        animate={{ opacity: 1 }}
                                                    >
                                                        {aiJieqian}
                                                    </motion.p>
                                                ) : aiLoading ? (
                                                    <div className="flex flex-col items-center gap-3 py-4 text-purple-600">
                                                        <motion.div
                                                            animate={{ rotate: 360 }}
                                                            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                                                        >
                                                            <Loader2 className="w-8 h-8" />
                                                        </motion.div>
                                                        <span className="text-sm">{t('chouqian.aiInterpreting')}</span>
                                                        <div className="flex gap-1">
                                                            {[0, 1, 2].map(i => (
                                                                <motion.div
                                                                    key={i}
                                                                    className="w-2 h-2 bg-purple-400 rounded-full"
                                                                    animate={{ y: [0, -8, 0] }}
                                                                    transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.15 }}
                                                                />
                                                            ))}
                                                        </div>
                                                    </div>
                                                ) : null}
                                            </div>
                                        </motion.div>
                                    )}
                                </AnimatePresence>

                                {/* {t('chouqian.redraw')}按钮 */}
                                <div className="mt-8 text-center">
                                    <button
                                        onClick={handleReset}
                                        className="bg-primary hover:bg-primary/90 text-primary-foreground px-10 py-3 rounded font-semibold transition-colors inline-flex items-center gap-2"
                                    >
                                        <RefreshCw className="w-5 h-5" />
                                        {t('chouqian.redraw')}
                                    </button>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* 说明文字 - 响应式 */}
                    <div className="mt-6 sm:mt-8 text-center text-xs sm:text-sm text-muted-foreground">
                        <p>{t('chouqian.subtitle')}</p>
                    </div>
                </motion.div>
            </div >
        </div >
    );
}
