/**
 * 卦爻显示组件
 * 完全复刻原工具设计
 */

import React from 'react';
import { HexagramInfo, LineDetails, LineType } from '../types';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';

interface Props {
  info: HexagramInfo;
  showHeaders?: boolean;
}

const HexagramLines: React.FC<Props> = ({ info, showHeaders = true }) => {
  const { theme } = useTheme();
  const isDark = theme === 'dark';
  // Display from top (5) to bottom (0)
  const slots = [5, 4, 3, 2, 1, 0];
  const hasTransformation = !!info.transformedName;
  const hasFuShen = info.lines.some(l => !!l.fuShen);

  return (
    <div className="w-full select-none font-serif max-w-5xl mx-auto">

      {/* Header Labels */}
      {showHeaders && (
        <div className="flex text-[10px] md:text-xs mb-2.5 md:mb-3 px-1 border-b border-border pb-2 md:pb-2.5 items-center text-muted-foreground">
          <div className="flex-1 text-center tracking-[0.3em] font-medium text-primary">本卦</div>
          {hasTransformation && <div className="w-6 shrink-0"></div>}
          {hasTransformation && <div className="flex-1 text-center tracking-[0.3em] font-medium text-primary">变卦</div>}
        </div>
      )}

      <div className="flex flex-col gap-2 md:gap-3 w-full">
        {slots.map((lineIndex) => {
          const line = info.lines[lineIndex];

          return (
            <motion.div
              key={lineIndex}
              initial={{ opacity: 0, x: -5 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: (5 - lineIndex) * 0.05 }}
              className="flex items-stretch justify-center relative min-h-[44px] md:min-h-[56px] w-full"
            >

              {/* --- LEFT SIDE: PRIMARY HEXAGRAM --- */}
              <div className="flex-1 flex items-center rounded-l-md border-r border-border/30 overflow-hidden pr-1 bg-secondary/40">

                {/* 0. Fu Shen (Hidden Spirit) Column */}
                {hasFuShen && (
                  <div className="w-5 md:w-10 flex flex-col items-center justify-center shrink-0 border-r border-border/20 h-full bg-secondary/20">
                    {line.fuShen ? (
                      <div className="flex flex-col items-center opacity-70">
                        <span className="text-[9px] md:text-[11px] leading-none scale-90 md:scale-100 text-muted-foreground">{line.fuShen.relation.substring(0, 1)}</span>
                        <span className="text-[8px] md:text-[10px] scale-75 md:scale-90 leading-none mt-0.5 text-muted-foreground/70">{line.fuShen.branch}</span>
                      </div>
                    ) : null}
                  </div>
                )}

                {/* 1. Meta: Beast & Relation */}
                <div className="w-9 md:w-14 flex flex-col items-end justify-center shrink-0 px-1">
                  <span className="text-[10px] md:text-sm font-medium leading-none mb-0.5 md:mb-1 text-primary">{line.sixBeast}</span>
                  <span className="text-[9px] md:text-xs font-light leading-none scale-95 origin-right text-foreground/80">{line.sixRelation}</span>
                </div>

                {/* 2. Marker: Shi/Ying */}
                <div className="w-5 md:w-8 flex items-center justify-center shrink-0">
                  {line.isShi && (
                    <div className="w-3.5 h-3.5 md:w-5 md:h-5 flex items-center justify-center bg-primary rounded-[2px] shadow-sm">
                      <span className="text-[8px] md:text-[11px] text-primary-foreground font-bold leading-none">世</span>
                    </div>
                  )}
                  {line.isYing && (
                    <div className="w-3.5 h-3.5 md:w-5 md:h-5 flex items-center justify-center border border-primary/30 rounded-[2px] bg-secondary">
                      <span className="text-[8px] md:text-[11px] font-bold leading-none text-primary">应</span>
                    </div>
                  )}
                </div>

                {/* 3. Visual Line (Primary) */}
                <div className="flex-1 min-w-[50px] md:min-w-[80px] h-full flex items-center justify-center px-1 md:px-2">
                  <LineVisual type={line.type} isDark={isDark} />
                </div>

                {/* 4. Meta: Stem & Branch */}
                <div className="w-8 md:w-12 flex flex-col items-center justify-center shrink-0 border-l border-border/10 h-full bg-secondary/10">
                  <div className="flex items-center gap-[1px] text-[9px] md:text-sm leading-none text-foreground">
                    <span className="scale-90 text-muted-foreground">{line.stem}</span>
                    <span>{line.branch}</span>
                  </div>
                  <div className="text-[8px] md:text-[10px] scale-90 mt-0.5 text-muted-foreground">{line.element}</div>
                </div>

              </div>

              {/* --- CENTER: ARROW --- */}
              {hasTransformation && (
                <div className="w-6 md:w-10 flex items-center justify-center shrink-0">
                  {line.isMoving ? (
                    <ArrowRight size={14} className="text-cinnabar md:w-5 md:h-5 opacity-80" />
                  ) : (
                    <div className="w-0.5 h-0.5 rounded-full bg-ink-700 opacity-30"></div>
                  )}
                </div>
              )}

              {/* --- RIGHT SIDE: TRANSFORMED HEXAGRAM --- */}
              {hasTransformation && (
                <div className={`flex-1 flex items-center rounded-r-md border-l border-border/30 overflow-hidden pl-1 bg-secondary/40 ${line.isMoving ? 'opacity-100' : 'opacity-30 grayscale'}`}>

                  {/* 1. Meta: Stem & Branch (Transformed) */}
                  <div className="w-8 md:w-12 flex flex-col items-center justify-center shrink-0 border-r border-border/10 h-full bg-secondary/10">
                    <div className={`flex items-center gap-[1px] text-[9px] md:text-sm ${line.isMoving ? 'text-foreground' : 'text-muted-foreground'}`}>
                      <span className="scale-90 opacity-60">{line.changedStem || line.stem}</span>
                      <span>{line.changedBranch}</span>
                    </div>
                    <div className="text-[8px] md:text-[10px] scale-90 mt-0.5 text-muted-foreground">{line.element}</div>
                  </div>

                  {/* 2. Visual Line (Transformed) */}
                  <div className="flex-1 min-w-[50px] md:min-w-[80px] h-full flex items-center justify-center px-1 md:px-2">
                    <LineVisual type={(line.changedType !== undefined) ? line.changedType : (line.type <= 1 ? line.type : 0)} isDark={isDark} />
                  </div>

                  {/* 3. Meta: Relation (Transformed) */}
                  <div className="w-10 md:w-14 flex flex-col items-start justify-center shrink-0 px-1">
                    <span className="text-[9px] md:text-xs font-light leading-none scale-95 origin-left text-foreground/80">{line.changedRelation}</span>
                  </div>
                </div>
              )}

              {!hasTransformation && (
                /* Placeholder for symmetry if needed */
                null
              )}

            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

const LineVisual: React.FC<{ type: LineType; isDark?: boolean }> = ({ type }) => {
  const h = "h-2.5 md:h-4";
  const yangStyle = "bg-primary shadow-sm rounded-[1px]";
  const yinGap = "w-full flex justify-between items-center";
  const yinSegment = `w-[36%] ${h} ${yangStyle}`;

  return (
    <div className="w-full max-w-[140px] flex items-center justify-center relative opacity-90">
      {(type === 0 || type === 2) && (
        <div className={`w-full ${h} ${yangStyle} relative flex items-center justify-center`}>
          {type === 2 && <div className="absolute w-1.5 h-1.5 md:w-2 md:h-2 rounded-full bg-destructive shadow-sm animate-pulse"></div>}
        </div>
      )}

      {(type === 1 || type === 3) && (
        <div className={yinGap}>
          <div className={yinSegment}></div>
          <div className="flex-1 flex items-center justify-center h-full">
            {type === 3 && <div className="text-destructive text-[10px] md:text-sm font-bold scale-125 leading-none">×</div>}
          </div>
          <div className={yinSegment}></div>
        </div>
      )}
    </div>
  );
};

export default HexagramLines;
