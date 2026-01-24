/**
 * 历史记录视图
 * 完整优化版 - 修复卦名显示、主题适配、排版问题
 */

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Trash2, Calendar, ChevronRight, Clock, ArrowLeft } from 'lucide-react';
import { HistoryRecord, HexagramInfo } from '../types';
import { getHistory, clearHistory } from '../utils/storage';
import HexagramLines from '../components/HexagramLines';
import { calculateHexagram } from '../utils/liuyao';
import { useTheme } from '../hooks/useTheme';
import { logger } from '@/utils/logger';
import { formatShortDateTime } from '@/utils/dateUtils';

const HistoryView: React.FC = () => {
  const [records, setRecords] = useState<HistoryRecord[]>([]);
  const [selectedRecord, setSelectedRecord] = useState<HistoryRecord | null>(null);

  useEffect(() => {
    setRecords(getHistory());
  }, []);

  // 使用统一的日期格式化工具
  const formatDate = (ts: number) => {
    // 使用导入的工具函数
    return formatShortDateTime(ts);
  };

  // 获取起卦方法的中文名
  const getMethodName = (method: string) => {
    switch (method) {
      case 'coin': return '灵动';
      case 'number': return '数理';
      case 'time': return '时空';
      default: return '灵动';
    }
  };

  const handleClear = () => {
    if (confirm("确定要清空所有记录吗？")) {
      clearHistory();
      setRecords([]);
    }
  };

  if (selectedRecord) {
    // 安全地获取卦象数据，添加错误处理
    let hexagramData: HexagramInfo | null = null;
    try {
      if (selectedRecord.hexagramData) {
        hexagramData = selectedRecord.hexagramData;
      } else if (selectedRecord.lines && selectedRecord.lines.length === 6) {
        hexagramData = calculateHexagram(selectedRecord.lines);
      }
    } catch (err) {
      logger.error('Failed to calculate hexagram:', err);
    }

    return (
      <div className="p-4 md:p-6 pt-4 min-h-full transition-colors bg-background">
        {/* 返回按钮 - 更紧凑 */}
        <button
          onClick={() => setSelectedRecord(null)}
          className="mb-3 flex items-center gap-1.5 text-xs transition-colors text-primary hover:text-foreground"
        >
          <ArrowLeft size={14} />
          <span>返回</span>
        </button>

        <div className="max-w-2xl mx-auto pb-32">
          {/* 问事标题 - 更紧凑 */}
          <div className="text-center mb-4 pb-3 border-b border-border">
            <h2 className="text-xl md:text-2xl mb-2 tracking-wide leading-relaxed text-foreground">
              {selectedRecord.question || "无问之卦"}
            </h2>
            <div className="flex items-center justify-center gap-3 text-[10px] md:text-xs text-muted-foreground">
              <span className="flex items-center gap-1">
                <Clock size={10} className="text-primary" />
                {formatDate(selectedRecord.timestamp)}
              </span>
              <span className="px-1.5 py-0.5 rounded-full text-[9px] bg-secondary text-primary">
                {getMethodName(selectedRecord.method)}
              </span>
            </div>
          </div>

          {/* 如果没有卦象数据，显示提示 */}
          {!hexagramData ? (
            <div className="text-center py-12 text-muted-foreground">
              <p>卦象数据不完整</p>
              <p className="text-xs mt-2">无法显示详细信息</p>
            </div>
          ) : (
            <>
              {/* 卦名显示区域 */}
              <div className="flex items-center justify-center gap-6 md:gap-10 mb-8">
                {/* 主卦 */}
                <div className="flex flex-col items-center">
                  <span className="text-xs tracking-[0.15em] mb-2 px-3 py-1 rounded-full bg-secondary text-muted-foreground">
                    主卦
                  </span>
                  <h2 className="text-3xl md:text-4xl leading-snug tracking-wide text-foreground">
                    {hexagramData.name}
                  </h2>
                  <span className="text-[11px] md:text-xs mt-2 tracking-wider text-muted-foreground">
                    {hexagramData.palaceName} · {hexagramData.palaceElement}
                  </span>
                </div>

                {/* 变卦箭头和变卦 */}
                {hexagramData.transformedName && (
                  <>
                    <div className="flex flex-col items-center justify-center pt-4">
                      <ChevronRight className="text-muted-foreground" size={24} />
                    </div>
                    <div className="flex flex-col items-center">
                      <span className="text-xs tracking-[0.15em] mb-2 px-3 py-1 rounded-full bg-secondary text-muted-foreground">
                        变卦
                      </span>
                      <h2 className="text-3xl md:text-4xl leading-snug tracking-wide opacity-90 text-foreground">
                        {hexagramData.transformedName}
                      </h2>
                      <span className="text-[11px] md:text-xs mt-2 tracking-wider opacity-0 select-none">占位</span>
                    </div>
                  </>
                )}
              </div>

              {/* 卦象显示 */}
              <div className="mb-8 p-4 md:p-6 rounded-xl border border-border shadow-lg bg-card">
                <div className="w-full flex justify-center">
                  <HexagramLines info={hexagramData} showHeaders={true} />
                </div>
              </div>
            </>
          )}

          {/* 解卦内容 - 无论是否有卦象数据都显示 */}
          <div className="rounded-xl p-5 md:p-8 bg-card border border-border shadow-sm">
            <h3 className="text-base md:text-lg font-medium mb-5 flex items-center gap-2 text-primary">
              <span className="w-1 h-5 rounded-full bg-primary"></span>
              大师断语
            </h3>
            <div className="whitespace-pre-line leading-8 md:leading-9 text-justify text-sm md:text-base text-muted-foreground">
              {selectedRecord.interpretation || (
                <span className="italic opacity-50">
                  暂无解卦记录，可在设置中开启“自动解卦”功能。
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // 历史列表视图
  return (
    <div className="p-4 md:p-8 pt-12 space-y-6 max-w-lg mx-auto">
      {/* 标题栏 */}
      <div className="flex justify-between items-end mb-4">
        <div>
          <h2 className="text-3xl tracking-wide text-foreground">
            卦录
          </h2>
          <p className="text-xs mt-1 text-muted-foreground">
            共 {records.length} 条记录
          </p>
        </div>
        {records.length > 0 && (
          <button
            onClick={handleClear}
            className="p-2 transition-colors text-muted-foreground hover:text-destructive"
            title="清空记录"
          >
            <Trash2 size={18} />
          </button>
        )}
      </div>

      {records.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-28 text-muted-foreground">
          <Calendar size={48} className="mb-4 opacity-40" strokeWidth={1} />
          <p className="text-sm tracking-widest">暂无卜卦记录</p>
          <p className="text-xs mt-2 opacity-70">
            前往"卜"页面开始起卦
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {records.map((rec, index) => {
            const hexData = rec.hexagramData || (rec.hexagramName ? { name: rec.hexagramName } : null);

            return (
              <motion.div
                key={rec.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                onClick={() => setSelectedRecord(rec)}
                className="rounded-lg p-4 md:p-5 flex items-center gap-4 cursor-pointer transition-all group bg-card border border-border hover:border-primary/50"
              >
                {/* 左侧卦名标识 */}
                <div className="w-14 h-14 rounded-lg flex flex-col items-center justify-center shrink-0 bg-secondary">
                  <span className="text-lg leading-none text-primary">
                    {hexData?.name?.slice(0, 2) || '卦'}
                  </span>
                  <span className="text-[9px] mt-1 text-muted-foreground">
                    {getMethodName(rec.method)}
                  </span>
                </div>

                {/* 中间内容 */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1.5">
                    <h3 className="text-sm md:text-base truncate transition-colors text-foreground group-hover:text-primary">
                      {rec.question || "心念所至"}
                    </h3>
                  </div>
                  <div className="flex items-center gap-3">
                    <p className="text-[11px] md:text-xs flex items-center gap-1 text-muted-foreground">
                      <Clock size={10} className="text-primary" />
                      {formatDate(rec.timestamp)}
                    </p>
                    {hexData?.name && (
                      <span className="text-[10px] px-2 py-0.5 rounded bg-secondary text-primary">
                        {hexData.name}
                      </span>
                    )}
                  </div>
                </div>

                {/* 右侧箭头 */}
                <ChevronRight
                  size={16}
                  className="shrink-0 transition-colors text-muted-foreground group-hover:text-primary"
                />
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default HistoryView;
