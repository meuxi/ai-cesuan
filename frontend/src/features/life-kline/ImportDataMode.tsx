/**
 * 人生K线分步向导组件
 * 移植自 lifekline3 项目
 * 支持手动输入八字信息，生成AI提示词，导入AI返回的JSON数据
 */

import React, { useState } from 'react';
import { LifeKLineResult, KLinePoint } from './types';
import { logger } from '@/utils/logger';

interface ImportDataModeProps {
    onDataImport: (data: LifeKLineResult) => void;
}

type Step = 1 | 2 | 3;

interface BaziInfo {
    name: string;
    gender: 'Male' | 'Female';
    birthYear: string;
    yearPillar: string;
    monthPillar: string;
    dayPillar: string;
    hourPillar: string;
    startAge: string;
    firstDaYun: string;
}

const BAZI_SYSTEM_INSTRUCTION = `你是一位资深八字命理大师，精通《滴天髓》《穷通宝鉴》《子平真诠》《三命通会》等经典命学著作。
根据用户提供的四柱干支和大运信息，生成专业的"人生K线图"数据和命理报告。

**核心规则:**
1. **年龄计算**: 采用虚岁，从 1 岁开始（出生即为1岁）。
2. **K线详批**: 每年的 reason 字段**控制在20-30字**，简洁描述吉凶趋势，需结合流年干支与命局的生克制化关系。
3. **评分机制**: 所有维度给出 0-10 分，基于五行喜忌和十神配置客观评判。
4. **数据起伏**: 让评分呈现明显波动，体现运势高低起伏，禁止输出平滑直线。

**大运规则:**
- 顺行: 甲子 → 乙丑 → 丙寅...（阳年男命、阴年女命顺行）
- 逆行: 甲子 → 癸亥 → 壬戌...（阴年男命、阳年女命逆行）
- 以用户指定的第一步大运为起点，每步管10年。

**专业分析要点:**
1. 日主强弱判断：根据月令、通根、透干情况分析
2. 用神喜忌：明确喜用神和忌神
3. 十神配置：分析官杀、财星、印星、比劫、食伤的力量对比
4. 神煞参考：天乙贵人、驿马、桃花、华盖等辅助参考

**输出JSON格式:**
{
  "bazi": ["年柱", "月柱", "日柱", "时柱"],
  "summary": "命理总评：格局特点、日主强弱、喜用神等（100字）",
  "summaryScore": 8,
  "personality": "性格分析：根据十神配置分析性格特点（80字）",
  "personalityScore": 8,
  "industry": "事业分析：适合行业、发展方向、贵人方位（80字）",
  "industryScore": 7,
  "fengShui": "风水建议：吉利方位、颜色、数字、开运物品（80字）",
  "fengShuiScore": 8,
  "wealth": "财运分析：正财偏财、求财方式、财运高峰期（80字）",
  "wealthScore": 9,
  "marriage": "婚姻分析：配偶特征、婚期预测、婚姻质量（80字）",
  "marriageScore": 6,
  "health": "健康分析：易患疾病、需注意的五行器官（60字）",
  "healthScore": 5,
  "family": "六亲分析：与父母、兄弟、子女的关系（60字）",
  "familyScore": 7,
  "chartPoints": [
    {"age":1,"year":1990,"daYun":"童限","ganZhi":"庚午","open":50,"close":55,"high":60,"low":45,"score":55,"reason":"开局平稳，印星护身"},
    {"age":2,"year":1991,"daYun":"童限","ganZhi":"辛未","open":55,"close":60,"high":65,"low":50,"score":60,"reason":"比劫帮身，学业启蒙"},
    ... (共100条，reason需体现专业命理术语)
  ]
}

**注意事项:**
1. chartPoints 必须包含完整的100条数据（1-100岁）
2. 每年的 ganZhi 必须准确计算（基于出生年份推算）
3. daYun 在起运年龄前为"童限"，之后每10年更换一次
4. reason 需使用专业命理术语，如"财星透出"、"官杀混杂"、"印比相生"等`;

const ImportDataMode: React.FC<ImportDataModeProps> = ({ onDataImport }) => {
    const [step, setStep] = useState<Step>(1);
    const [baziInfo, setBaziInfo] = useState<BaziInfo>({
        name: '',
        gender: 'Male',
        birthYear: '',
        yearPillar: '',
        monthPillar: '',
        dayPillar: '',
        hourPillar: '',
        startAge: '',
        firstDaYun: '',
    });
    const [jsonInput, setJsonInput] = useState('');
    const [copied, setCopied] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // 计算大运方向
    const getDaYunDirection = () => {
        if (!baziInfo.yearPillar) return { isForward: true, text: '顺行' };
        const firstChar = baziInfo.yearPillar.trim().charAt(0);
        const yangStems = ['甲', '丙', '戊', '庚', '壬'];
        const isYangYear = yangStems.includes(firstChar);
        const isForward = baziInfo.gender === 'Male' ? isYangYear : !isYangYear;
        return { isForward, text: isForward ? '顺行' : '逆行' };
    };

    // 生成用户提示词
    const generateUserPrompt = () => {
        const { text: daYunDirectionStr } = getDaYunDirection();
        const genderStr = baziInfo.gender === 'Male' ? '男 (乾造)' : '女 (坤造)';
        const startAgeInt = parseInt(baziInfo.startAge) || 1;

        return `请根据以下八字四柱和大运信息进行分析：

【基本信息】
姓名：${baziInfo.name || "未提供"}
性别：${genderStr}
出生年份：${baziInfo.birthYear}年

【八字四柱】
年柱：${baziInfo.yearPillar}
月柱：${baziInfo.monthPillar}
日柱：${baziInfo.dayPillar}
时柱：${baziInfo.hourPillar}

【大运参数】
起运年龄：${baziInfo.startAge} 岁
第一步大运：${baziInfo.firstDaYun}
排序方向：${daYunDirectionStr}

【任务要求】
1. 生成 1-100 岁的完整流年K线数据
2. daYun 字段填大运干支（10年一变）
3. ganZhi 字段填流年干支（每年一变）
4. 1-${startAgeInt - 1}岁 daYun 填"童限"
5. ${startAgeInt}岁开始填入第一步大运：${baziInfo.firstDaYun}

请严格按照系统指令的 JSON 格式输出。`;
    };

    // 复制完整提示词
    const copyFullPrompt = async () => {
        const fullPrompt = `=== 系统指令 ===\n\n${BAZI_SYSTEM_INSTRUCTION}\n\n=== 用户信息 ===\n\n${generateUserPrompt()}`;
        try {
            await navigator.clipboard.writeText(fullPrompt);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            logger.error('复制失败:', err);
        }
    };

    // 解析导入的 JSON
    const handleImport = () => {
        setError(null);
        if (!jsonInput.trim()) {
            setError('请粘贴 AI 返回的 JSON 数据');
            return;
        }

        try {
            let jsonContent = jsonInput.trim();
            // 提取 ```json ... ``` 中的内容
            const jsonMatch = jsonContent.match(/```(?:json)?\s*([\s\S]*?)```/);
            if (jsonMatch) {
                jsonContent = jsonMatch[1].trim();
            } else {
                const jsonStartIndex = jsonContent.indexOf('{');
                const jsonEndIndex = jsonContent.lastIndexOf('}');
                if (jsonStartIndex !== -1 && jsonEndIndex !== -1) {
                    jsonContent = jsonContent.substring(jsonStartIndex, jsonEndIndex + 1);
                }
            }

            const data = JSON.parse(jsonContent);

            if (!data.chartPoints || !Array.isArray(data.chartPoints)) {
                throw new Error('数据格式不正确：缺少 chartPoints 数组');
            }
            if (data.chartPoints.length < 10) {
                throw new Error('数据不完整：chartPoints 数量太少');
            }

            const result: LifeKLineResult = {
                chartData: data.chartPoints as KLinePoint[],
                analysis: {
                    bazi: data.bazi || [],
                    summary: data.summary || '',
                    summaryScore: data.summaryScore || 5,
                    personality: data.personality || '',
                    personalityScore: data.personalityScore || 5,
                    industry: data.industry || '',
                    industryScore: data.industryScore || 5,
                    fengShui: data.fengShui || '',
                    fengShuiScore: data.fengShuiScore || 5,
                    wealth: data.wealth || '',
                    wealthScore: data.wealthScore || 5,
                    marriage: data.marriage || '',
                    marriageScore: data.marriageScore || 5,
                    health: data.health || '',
                    healthScore: data.healthScore || 5,
                    family: data.family || '',
                    familyScore: data.familyScore || 5,
                },
            };

            onDataImport(result);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : '未知错误'
            setError(`解析失败：${message}`);
        }
    };

    const handleBaziChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setBaziInfo(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const isStep1Valid = baziInfo.birthYear && baziInfo.yearPillar && baziInfo.monthPillar &&
        baziInfo.dayPillar && baziInfo.hourPillar && baziInfo.startAge && baziInfo.firstDaYun;

    return (
        <div className="w-full max-w-2xl bg-card p-6 md:p-8 rounded-2xl shadow-xl border border-border">
            {/* 步骤指示器 */}
            <div className="flex items-center justify-center gap-2 mb-8">
                {[1, 2, 3].map((s) => (
                    <React.Fragment key={s}>
                        <div
                            className={`w-10 h-10 rounded-full flex items-center justify-center font-bold transition-all ${step === s
                                ? 'bg-indigo-600 text-white scale-110'
                                : step > s
                                    ? 'bg-green-500 text-white'
                                    : 'bg-muted text-muted-foreground'
                                }`}
                        >
                            {step > s ? (
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            ) : s}
                        </div>
                        {s < 3 && <div className={`w-12 md:w-16 h-1 rounded ${step > s ? 'bg-green-500' : 'bg-muted'}`} />}
                    </React.Fragment>
                ))}
            </div>

            {/* 步骤 1: 输入八字信息 */}
            {step === 1 && (
                <div className="space-y-6">
                    <div className="text-center">
                        <h2 className="text-xl md:text-2xl font-bold text-foreground mb-2">第一步：输入八字信息</h2>
                        <p className="text-muted-foreground text-sm">填写四柱与大运信息</p>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-xs font-bold text-muted-foreground mb-1">姓名 (可选)</label>
                            <input
                                type="text"
                                name="name"
                                value={baziInfo.name}
                                onChange={handleBaziChange}
                                className="w-full px-3 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary outline-none bg-background text-foreground"
                                placeholder="姓名"
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-bold text-muted-foreground mb-1">性别</label>
                            <select
                                name="gender"
                                value={baziInfo.gender}
                                onChange={handleBaziChange}
                                className="w-full px-3 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary outline-none bg-background text-foreground"
                            >
                                <option value="Male">乾造 (男)</option>
                                <option value="Female">坤造 (女)</option>
                            </select>
                        </div>
                    </div>

                    <div className="bg-amber-50 p-4 rounded-xl border border-amber-100">
                        <div className="flex items-center gap-2 mb-3 text-amber-800 text-sm font-bold">
                            <span>✨</span>
                            <span>四柱干支</span>
                        </div>

                        <div className="mb-4">
                            <label className="block text-xs font-bold text-muted-foreground mb-1">出生年份 (阳历)</label>
                            <input
                                type="number"
                                name="birthYear"
                                value={baziInfo.birthYear}
                                onChange={handleBaziChange}
                                placeholder="如: 2003"
                                className="w-full px-3 py-2 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-500 outline-none bg-background font-bold text-foreground"
                            />
                        </div>

                        <div className="grid grid-cols-4 gap-2 md:gap-3">
                            {(['yearPillar', 'monthPillar', 'dayPillar', 'hourPillar'] as const).map((field, i) => (
                                <div key={field}>
                                    <label className="block text-xs font-bold text-muted-foreground mb-1">{['年柱', '月柱', '日柱', '时柱'][i]}</label>
                                    <input
                                        type="text"
                                        name={field}
                                        value={baziInfo[field]}
                                        onChange={handleBaziChange}
                                        placeholder={['甲子', '乙丑', '丙寅', '丁卯'][i]}
                                        className="w-full px-2 py-2 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-500 outline-none bg-background text-center font-bold text-foreground"
                                    />
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="bg-indigo-50 p-4 rounded-xl border border-indigo-100">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-xs font-bold text-muted-foreground mb-1">起运年龄 (虚岁)</label>
                                <input
                                    type="number"
                                    name="startAge"
                                    value={baziInfo.startAge}
                                    onChange={handleBaziChange}
                                    placeholder="如: 8"
                                    className="w-full px-3 py-2 border border-indigo-200 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none bg-background text-center font-bold text-foreground"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-bold text-muted-foreground mb-1">第一步大运</label>
                                <input
                                    type="text"
                                    name="firstDaYun"
                                    value={baziInfo.firstDaYun}
                                    onChange={handleBaziChange}
                                    placeholder="如: 辛酉"
                                    className="w-full px-3 py-2 border border-indigo-200 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none bg-background text-center font-bold text-foreground"
                                />
                            </div>
                        </div>
                        <p className="text-xs text-indigo-600/70 mt-2 text-center">
                            大运方向：<span className="font-bold text-indigo-900">{getDaYunDirection().text}</span>
                        </p>
                    </div>

                    <button
                        onClick={() => setStep(2)}
                        disabled={!isStep1Valid}
                        className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-bold py-3.5 rounded-xl shadow-lg transition-all flex items-center justify-center gap-2"
                    >
                        下一步：生成提示词
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                        </svg>
                    </button>
                </div>
            )}

            {/* 步骤 2: 复制提示词 */}
            {step === 2 && (
                <div className="space-y-6">
                    <div className="text-center">
                        <h2 className="text-xl md:text-2xl font-bold text-foreground mb-2">第二步：复制提示词</h2>
                        <p className="text-muted-foreground text-sm">将提示词粘贴到任意 AI 聊天工具</p>
                    </div>

                    <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 md:p-6 rounded-xl border border-blue-200">
                        <div className="flex items-center gap-3 mb-4">
                            <span className="text-2xl">💬</span>
                            <div>
                                <h3 className="font-bold text-gray-800">支持的 AI 工具</h3>
                                <p className="text-sm text-gray-600">ChatGPT、Claude、Gemini、通义千问、文心一言 等</p>
                            </div>
                        </div>

                        <div className="bg-background rounded-lg p-4 border border-border max-h-48 overflow-y-auto mb-4">
                            <pre className="text-xs text-muted-foreground whitespace-pre-wrap font-mono">
                                {generateUserPrompt().substring(0, 400)}...
                            </pre>
                        </div>

                        <button
                            onClick={copyFullPrompt}
                            className={`w-full py-3 rounded-xl font-bold flex items-center justify-center gap-2 transition-all ${copied
                                ? 'bg-green-500 text-white'
                                : 'bg-indigo-600 hover:bg-indigo-700 text-white'
                                }`}
                        >
                            {copied ? (
                                <>
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                    </svg>
                                    已复制到剪贴板！
                                </>
                            ) : (
                                <>
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                    </svg>
                                    复制完整提示词
                                </>
                            )}
                        </button>
                    </div>

                    <div className="bg-amber-50 p-4 rounded-xl border border-amber-200">
                        <h4 className="font-bold text-amber-800 mb-2">📝 使用说明</h4>
                        <ol className="text-sm text-amber-700 space-y-1 list-decimal list-inside">
                            <li>点击上方按钮复制提示词</li>
                            <li>打开任意 AI 聊天工具（如 ChatGPT）</li>
                            <li>粘贴提示词并发送</li>
                            <li>等待 AI 生成完整的 JSON 数据</li>
                            <li>复制 AI 的回复，回到这里进行下一步</li>
                        </ol>
                    </div>

                    <div className="flex gap-4">
                        <button
                            onClick={() => setStep(1)}
                            className="flex-1 py-3 rounded-xl font-bold border-2 border-input text-foreground hover:bg-accent transition-all"
                        >
                            ← 上一步
                        </button>
                        <button
                            onClick={() => setStep(3)}
                            className="flex-1 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-bold py-3 rounded-xl shadow-lg transition-all flex items-center justify-center gap-2"
                        >
                            下一步：导入数据
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                            </svg>
                        </button>
                    </div>
                </div>
            )}

            {/* 步骤 3: 导入 JSON */}
            {step === 3 && (
                <div className="space-y-6">
                    <div className="text-center">
                        <h2 className="text-xl md:text-2xl font-bold text-foreground mb-2">第三步：导入 AI 回复</h2>
                        <p className="text-muted-foreground text-sm">粘贴 AI 返回的 JSON 数据</p>
                    </div>

                    <div className="bg-secondary p-4 rounded-xl border border-border">
                        <label className="block text-sm font-bold text-foreground mb-2">
                            <span className="inline-block mr-2">📤</span>
                            粘贴 AI 返回的 JSON 数据
                        </label>
                        <textarea
                            value={jsonInput}
                            onChange={(e) => setJsonInput(e.target.value)}
                            placeholder={'将 AI 返回的 JSON 数据粘贴到这里...\n\n例如:\n{\n  "bazi": ["癸未", "壬戌", "丙子", "庚寅"],\n  "chartPoints": [...],\n  ...\n}'}
                            className="w-full h-56 md:h-64 px-4 py-3 border border-input rounded-lg focus:ring-2 focus:ring-primary outline-none font-mono text-xs resize-none bg-background text-foreground"
                        />
                    </div>

                    {error && (
                        <div className="flex items-center gap-2 text-red-600 bg-red-50 px-4 py-3 rounded-lg border border-red-200">
                            <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                            <p className="text-sm">{error}</p>
                        </div>
                    )}

                    <div className="flex gap-4">
                        <button
                            onClick={() => setStep(2)}
                            className="flex-1 py-3 rounded-xl font-bold border-2 border-input text-foreground hover:bg-accent transition-all"
                        >
                            ← 上一步
                        </button>
                        <button
                            onClick={handleImport}
                            className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-bold py-3 rounded-xl shadow-lg transition-all flex items-center justify-center gap-2"
                        >
                            <span className="text-lg">✨</span>
                            生成人生K线
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ImportDataMode;
