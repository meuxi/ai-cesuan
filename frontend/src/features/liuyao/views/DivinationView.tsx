/**
 * 起卦视图
 * 完全复刻原工具设计，使用后端API计算卦象
 */

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { RefreshCw, ChevronRight, Clock, Hash, Disc, Sparkles, ScrollText, ChevronDown, ChevronUp } from 'lucide-react';
import { logger } from '@/utils/logger';
import { AppSettings, LineType, DivinationMethod, HistoryRecord, HexagramInfo } from '../types';
import HexagramLines from '../components/HexagramLines';
import AdvancedAnalysisPanel from '../components/AdvancedAnalysisPanel';
import { useLiuYao } from '../hooks/useLiuYao';
import { useAIInterpretation } from '../hooks/useAIInterpretation';
import { useAdvancedAnalysis } from '../hooks/useAdvancedAnalysis';
import { saveRecord, getHistory } from '../utils/storage';
import { useTheme } from '../hooks/useTheme';

interface Props {
  settings: AppSettings;
}

const DivinationView: React.FC<Props> = ({ settings }) => {
  const [method, setMethod] = useState<DivinationMethod>(DivinationMethod.COIN);
  const [question, setQuestion] = useState('');
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  // 后端API状态
  const {
    coinCast,
    numberCast,
    timeCast,
    loading: apiLoading,
    hexagram,
    error
  } = useLiuYao();

  // AI解卦状态
  const {
    interpret,
    loading: aiLoading,
    streaming: aiStreaming,
    interpretation,
    reset: resetAI
  } = useAIInterpretation();

  // AI内容区域引用，用于自动滚动
  const aiContentRef = useRef<HTMLDivElement>(null);

  // 高级分析状态
  const {
    analyze: runAdvancedAnalysis,
    analysis: advancedAnalysis,
    loading: analysisLoading
  } = useAdvancedAnalysis();

  const [showResult, setShowResult] = useState(false);
  const [numberInput, setNumberInput] = useState('');
  const [currentRecordId, setCurrentRecordId] = useState<string | null>(null);
  const [showAdvancedPanel, setShowAdvancedPanel] = useState(false);
  const [showAIInterpretation, setShowAIInterpretation] = useState(false);

  // 重置状态
  const handleReset = () => {
    setShowResult(false);
    setShowAIInterpretation(false);
    setQuestion('');
    setNumberInput('');
    setCurrentRecordId(null);
    resetAI(); // 重置AI解读状态
  };

  // 处理摇钱卦
  const handleCoinCast = async () => {
    if (apiLoading) return;

    try {
      await coinCast(question || "心念所至");
      const id = Date.now().toString();
      setCurrentRecordId(id);
      setShowResult(true);

      if (settings.hapticEnabled && navigator.vibrate) navigator.vibrate([50, 50, 100]);
    } catch (err) {
      logger.error('摇钱卦起卦失败:', err);
      alert('起卦失败，请重试');
    }
  };

  // 处理数理卦
  const handleNumberSubmit = async () => {
    if (!numberInput) return;
    const digits = numberInput.replace(/\D/g, '').split('').map(Number);
    if (digits.length < 2) {
      alert("至少输入两位数字");
      return;
    }

    let upper, lower;
    const sum = digits.reduce((a, b) => a + b, 0);

    if (digits.length === 2) {
      upper = digits[0];
      lower = digits[1];
    } else {
      const midpoint = Math.floor(digits.length / 2);
      upper = digits.slice(0, midpoint).reduce((a, b) => a + b, 0);
      lower = digits.slice(midpoint).reduce((a, b) => a + b, 0);
    }

    try {
      await numberCast(upper, lower, sum, question || "心念所至");
      const id = Date.now().toString();
      setCurrentRecordId(id);
      setShowResult(true);
    } catch (err) {
      logger.error('数理卦起卦失败:', err);
      alert('起卦失败，请重试');
    }
  };

  // 处理时空卦
  const handleTimeCast = async () => {
    try {
      await timeCast(question || "心念所至");
      const id = Date.now().toString();
      setCurrentRecordId(id);
      setShowResult(true);
    } catch (err) {
      logger.error('时空卦起卦失败:', err);
      alert('起卦失败，请重试');
    }
  };

  // 自动执行高级分析
  useEffect(() => {
    if (showResult && hexagram && currentRecordId && !advancedAnalysis) {
      runAdvancedAnalysis(hexagram);
    }
  }, [showResult, hexagram, currentRecordId]);

  // AI流式输出时自动滚动到底部
  useEffect(() => {
    if (aiStreaming && aiContentRef.current) {
      aiContentRef.current.scrollTop = aiContentRef.current.scrollHeight;
    }
  }, [interpretation, aiStreaming]);

  // 手动触发AI解卦
  const handleAIInterpret = () => {
    if (hexagram && !interpretation) {
      setShowAIInterpretation(true);
      interpret(hexagram, question || "此卦何解？", settings.aiStyle);
    } else if (interpretation) {
      setShowAIInterpretation(true);
    }
  };

  // 保存记录
  useEffect(() => {
    if (showResult && hexagram && currentRecordId) {
      const lines = hexagram.lines.map(l => l.type);
      const record: HistoryRecord = {
        id: currentRecordId,
        lines,
        question: question || "心念所至",
        timestamp: parseInt(currentRecordId),
        method,
        interpretation: interpretation || "",
        hexagramName: hexagram.name,
        hexagramData: hexagram
      };
      saveRecord(record);
    }
  }, [showResult, hexagram, question, method, interpretation, currentRecordId]);

  // 加载错误提示
  if (error) {
    return (
      <div className="h-full w-full flex items-center justify-center">
        <div className="text-center">
          <p className="text-destructive text-lg mb-4">起卦失败</p>
          <p className="text-muted-foreground text-sm">{error}</p>
          <button
            onClick={handleReset}
            className="mt-6 px-6 py-2 bg-primary text-primary-foreground rounded-full text-sm hover:bg-primary/90"
          >
            重试
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full flex flex-col relative">

      {/* 问题输入框 */}
      <div className="mb-6">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="所问何事..."
          disabled={apiLoading || showResult}
          className="w-full bg-secondary/50 px-4 py-3 rounded-lg border border-border focus:outline-none focus:border-primary text-center text-sm md:text-base tracking-wide transition-all text-foreground placeholder:text-muted-foreground"
        />
      </div>

      {/* 主区域 */}
      <div className="flex-1 relative w-full flex flex-col">
        <AnimatePresence mode="wait">
          {!showResult ? (
            <motion.div
              key="casting"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="flex-1 flex flex-col items-center justify-center mt-4 md:mt-8"
            >
              {method === DivinationMethod.COIN && (
                <div className="flex flex-col items-center gap-10 relative scale-90 md:scale-100">
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full blur-3xl pointer-events-none bg-primary/5"></div>
                  <motion.button
                    onClick={handleCoinCast}
                    whileTap={{ scale: 0.98 }}
                    className="relative w-52 h-52 md:w-56 md:h-56 rounded-full flex items-center justify-center transition-all duration-500 cursor-pointer bg-card border border-border shadow-lg hover:shadow-xl hover:border-primary/50"
                  >
                    <div className="absolute inset-2 rounded-full border border-border/50"></div>
                    <div className={`absolute inset-0 rounded-full border border-dashed border-primary/20 ${apiLoading ? 'animate-spin-slow' : ''}`}></div>
                    <div className="relative z-10 w-20 h-20 md:w-24 md:h-24 rounded-full flex items-center justify-center overflow-hidden bg-secondary">
                      <AnimatePresence mode="wait">
                        {apiLoading ? (
                          <motion.div
                            key="loading"
                            initial={{ opacity: 0, scale: 0.5 }}
                            animate={{ opacity: 1, scale: 1.2 }}
                            className="absolute inset-0 flex items-center justify-center"
                          >
                            <div className="absolute inset-0 blur-xl animate-pulse bg-primary/20"></div>
                            <Sparkles className="animate-spin text-primary" size={24} />
                          </motion.div>
                        ) : (
                          <motion.div
                            key="idle"
                            initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                            className="text-3xl select-none text-primary"
                          >
                            <span>起</span>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                    {apiLoading && (
                      <div className="absolute inset-0 rounded-full border animate-ping border-primary/20" />
                    )}
                  </motion.button>
                  <div className="h-6 text-center">
                    <p className="text-[11px] md:text-xs tracking-[0.3em] uppercase leading-relaxed text-muted-foreground">
                      {apiLoading ? "推演天机..." : (question ? "点击起卦" : "诚心问道")}
                    </p>
                  </div>
                </div>
              )}
              {method === DivinationMethod.NUMBER && (
                <div className="flex flex-col items-center gap-8">
                  <div className="relative px-10 py-8 bg-card border border-border rounded-lg shadow-lg flex flex-col items-center gap-4">
                    <Hash className="text-muted-foreground" size={20} />
                    <input type="tel" placeholder="三数" value={numberInput} onChange={(e) => setNumberInput(e.target.value)} className="w-40 text-4xl md:text-5xl text-foreground bg-transparent text-center outline-none border-b border-border pb-2 focus:border-primary transition-colors placeholder:text-muted-foreground leading-tight" />
                  </div>
                  <button onClick={handleNumberSubmit} disabled={!numberInput} className="w-14 h-14 rounded-full bg-primary text-primary-foreground flex items-center justify-center shadow-lg active:scale-95 transition-all disabled:opacity-30 disabled:scale-100 hover:bg-primary/90">
                    <ChevronRight size={24} />
                  </button>
                </div>
              )}
              {method === DivinationMethod.TIME && (
                <div className="flex flex-col items-center gap-8">
                  <div className="w-48 h-48 rounded-full border border-border bg-card flex items-center justify-center relative">
                    <div className="absolute inset-0 rounded-full border border-border/50 scale-90"></div>
                    <Clock className="text-muted-foreground w-12 h-12" strokeWidth={1} />
                    <div className="absolute bottom-12 text-xs md:text-sm text-foreground tracking-widest font-bold leading-none">
                      {new Date().getHours()}:{new Date().getMinutes().toString().padStart(2, '0')}
                    </div>
                  </div>
                  <button onClick={handleTimeCast} className="px-8 py-3 bg-primary text-primary-foreground rounded-lg text-xs tracking-[0.2em] hover:bg-primary/90 transition-colors">此刻感应</button>
                </div>
              )}
            </motion.div>
          ) : (
            /* --- 结果显示 --- */
            <motion.div
              key="result"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="w-full"
            >
              <div className="flex flex-col gap-6">

                {/* 排盘结果区域 */}
                <div className="flex flex-col gap-6">

                  <div className="flex justify-between items-center border-b border-border pb-3 md:pb-4">
                    <span className="text-[10px] md:text-xs tracking-widest uppercase text-primary">卦象</span>
                    <button onClick={handleReset} className="p-2 transition-colors flex items-center gap-2 text-muted-foreground hover:text-primary">
                      <span className="text-xs">重置</span>
                      <RefreshCw size={14} />
                    </button>
                  </div>

                  {hexagram && (
                    <div className="flex flex-col items-center justify-center gap-4 py-2">
                      <div className="flex items-center gap-4 md:gap-6">
                        <div className="flex flex-col items-center">
                          <h2 className="text-3xl md:text-4xl lg:text-5xl leading-tight tracking-wide text-foreground">{hexagram.name}</h2>
                          <span className="text-xs md:text-sm mt-1.5 text-muted-foreground">{hexagram.palaceName} · {hexagram.palaceElement}</span>
                        </div>
                        {hexagram.transformedName && (
                          <>
                            <ChevronRight className="opacity-50 text-muted-foreground" size={20} />
                            <div className="flex flex-col items-center">
                              <h2 className="text-3xl md:text-4xl lg:text-5xl leading-tight tracking-wide text-foreground/80">{hexagram.transformedName}</h2>
                              <span className="text-xs md:text-sm mt-1.5 text-muted-foreground">变卦</span>
                            </div>
                          </>
                        )}
                      </div>
                    </div>
                  )}

                  <div className="w-full flex flex-col relative">
                    <div className="w-full flex justify-center">
                      {hexagram && <HexagramLines info={hexagram} />}
                    </div>
                  </div>

                  {/* 高级分析折叠面板 */}
                  <div className="mt-4">
                    <button
                      onClick={() => setShowAdvancedPanel(!showAdvancedPanel)}
                      className="w-full flex items-center justify-center gap-2 py-2 rounded-lg transition-colors bg-secondary hover:bg-secondary/80 text-foreground"
                    >
                      <span className="text-xs tracking-wider">
                        {analysisLoading ? '分析中...' : '专业分析'}
                      </span>
                      {showAdvancedPanel ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                    </button>

                    <AnimatePresence>
                      {showAdvancedPanel && advancedAnalysis && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="overflow-hidden mt-2"
                        >
                          <AdvancedAnalysisPanel analysis={advancedAnalysis} isDark={isDark} />
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>

                {/* AI解读按钮 - 排盘后显示 */}
                {!showAIInterpretation && (
                  <div className="lg:col-span-12 flex justify-center mt-4">
                    <button
                      onClick={handleAIInterpret}
                      disabled={aiLoading}
                      className="w-full max-w-md px-8 py-3 bg-primary text-primary-foreground rounded-lg text-sm tracking-wide hover:bg-primary/90 transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
                    >
                      <Sparkles size={16} />
                      <span>开始 AI 解读</span>
                    </button>
                  </div>
                )}

                {/* AI解读内容 - 点击按钮后显示 */}
                {showAIInterpretation && (
                  <div className="lg:col-span-12 flex flex-col gap-4 mt-4">
                    <div className="flex justify-between items-center border-b border-border pb-3">
                      <span className="text-[10px] md:text-xs tracking-widest uppercase text-primary">AI 解读</span>
                      <div className="text-xs md:text-sm text-muted-foreground"><ScrollText size={14} className="inline mr-1" /> 大师断语</div>
                    </div>

                    <div
                      ref={aiContentRef}
                      className="w-full rounded-xl p-4 md:p-6 border border-border bg-secondary/30 min-h-[200px] max-h-[500px] overflow-y-auto"
                    >
                      {interpretation ? (
                        <motion.div
                          initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                          className="max-w-none"
                        >
                          <div className="whitespace-pre-line leading-7 md:leading-8 text-justify text-sm md:text-base tracking-wide text-muted-foreground">
                            {interpretation}
                            {aiStreaming && (
                              <span className="inline-block w-2 h-5 ml-1 bg-primary animate-pulse align-middle" />
                            )}
                          </div>
                        </motion.div>
                      ) : aiLoading ? (
                        <div className="flex flex-col items-center justify-center gap-4 py-12 h-full">
                          <div className="animate-spin rounded-full h-8 w-8 border-2 border-muted border-t-primary"></div>
                          <p className="text-sm text-muted-foreground">AI 正在为您解读...</p>
                        </div>
                      ) : (
                        <div className="flex items-center justify-center h-full py-12">
                          <span className="italic text-muted-foreground opacity-50">点击上方按钮开始AI解读</span>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {!showResult && (
          <div className="mt-8 flex items-center justify-center">
            <div className="flex p-1 rounded-full bg-secondary border border-border">
              {[
                { id: DivinationMethod.COIN, icon: <Disc size={14} />, label: '灵动' },
                { id: DivinationMethod.NUMBER, icon: <Hash size={14} />, label: '数理' },
                { id: DivinationMethod.TIME, icon: <Clock size={14} />, label: '时空' },
              ].map(m => {
                const isActive = method === m.id;
                return (
                  <button
                    key={m.id}
                    onClick={() => setMethod(m.id as DivinationMethod)}
                    className={`relative px-4 md:px-5 py-2 rounded-full flex items-center gap-1.5 transition-all duration-300 ${isActive
                      ? 'bg-primary text-primary-foreground shadow-sm'
                      : 'text-muted-foreground hover:text-foreground'
                      }`}
                  >
                    {m.icon}
                    <span className="text-[10px] md:text-xs font-medium tracking-wider">{m.label}</span>
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DivinationView;
