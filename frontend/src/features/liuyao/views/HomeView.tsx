/**
 * 首页视图
 * 完全复刻原工具设计
 */

import React from 'react';
import { motion } from 'framer-motion';
import { useTheme } from '../hooks/useTheme';

interface Props {
    onStart: () => void;
}

const HomeView: React.FC<Props> = ({ onStart }) => {
    return (
        <div className="h-full w-full relative flex flex-col items-center overflow-y-auto overflow-x-hidden no-scrollbar">

            {/* Background Decorative Seals - Fixed position */}
            <div className="absolute top-10 right-8 opacity-20 pointer-events-none fixed z-0">
                <div className="w-16 h-16 border border-primary/30 rounded-sm flex items-center justify-center rotate-12">
                    <span className="text-2xl writing-vertical-rl text-primary/50">大衍</span>
                </div>
            </div>

            {/* Hero Section */}
            <div className="min-h-[85vh] w-full flex flex-col items-center justify-center relative shrink-0 z-10">

                {/* Main Title Area */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1.2 }}
                    className="flex flex-col items-center gap-6"
                >
                    <h1 className="text-5xl md:text-6xl tracking-[0.1em] drop-shadow-2xl text-center leading-tight text-foreground">
                        六爻<span className="text-primary">神</span>课
                    </h1>
                    <p className="text-xs tracking-[0.4em] uppercase text-center text-muted-foreground">
                        The Divine Hexagram
                    </p>
                </motion.div>

                {/* Center Action Button */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.5, duration: 0.8 }}
                    className="my-16 relative"
                >
                    <button
                        onClick={onStart}
                        className="group relative w-24 h-24 rounded-full flex items-center justify-center outline-none"
                    >
                        {/* Rotating Rings */}
                        <div className="absolute inset-0 border border-primary/30 rounded-full animate-spin-slow transition-colors group-hover:border-primary/60"></div>
                        <div className="absolute inset-2 border border-dashed border-border rounded-full animate-[spin_12s_linear_infinite_reverse]"></div>

                        {/* Core */}
                        <div className="absolute inset-0 rounded-full transition-shadow duration-500 flex items-center justify-center bg-card border border-border shadow-lg group-hover:shadow-xl group-hover:border-primary/50">
                            <span className="text-2xl font-bold group-hover:scale-110 transition-transform text-primary">卜</span>
                        </div>
                    </button>
                    <div className="text-center mt-6">
                        <p className="text-[10px] tracking-widest uppercase opacity-60 group-hover:opacity-100 transition-opacity text-muted-foreground">点击起卦</p>
                    </div>
                </motion.div>

                {/* Scroll Hint */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1.5, duration: 1 }}
                    className="absolute bottom-10 flex flex-col items-center gap-2 opacity-40"
                >
                    <span className="text-[10px] writing-vertical-rl tracking-widest text-muted-foreground">六爻缘起</span>
                    <div className="w-[1px] h-8 bg-border"></div>
                </motion.div>
            </div>

            {/* Origin Content Section */}
            <div className="w-full max-w-sm px-6 pb-24 z-10 relative">
                <div className="relative py-8 border-t border-border">
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 px-4 border border-border rounded-full shadow-lg bg-card">
                        <span className="text-xl text-primary">源流</span>
                    </div>

                    <div className="prose prose-sm pt-4">
                        <p className="leading-loose text-justify indent-8 mb-6 text-foreground">
                            六爻，又称纳甲筮法，肇端于西汉易学大师<span className="text-primary font-medium">京房</span>。其法以《周易》六十四卦为体，将干支、五行、六亲纳于六爻之中，不仅继承了古筮法的象数精髓，更开创了以五行生克推演万物盈虚消长的新纪元。
                        </p>
                        <p className="leading-loose text-justify indent-8 mb-6 text-muted-foreground">
                            古人云："吉凶悔吝，生乎动者也。" 六爻之妙，在于捕捉时空交汇的瞬间灵感，即所谓的"外应"。通过钱币摇动或心念感应生成卦象，洞察天机。
                        </p>
                        <p className="leading-loose text-justify indent-8 text-muted-foreground">
                            本应用承袭古法，融合现代科技。无论是以指尖灵动模拟铜钱翻转，还是以数理、时空为引，皆旨在为用户提供一方静心问道的数字净土。
                        </p>
                    </div>

                    <div className="mt-12 flex justify-center opacity-30">
                        <div className="w-16 h-16 border border-border rounded-full flex items-center justify-center">
                            <span className="text-2xl text-muted-foreground">易</span>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    );
};

export default HomeView;
