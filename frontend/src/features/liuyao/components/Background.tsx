/**
 * 背景特效组件
 * 支持明暗主题切换
 */

import React from 'react';
import { motion } from 'framer-motion';
import { useTheme } from '../hooks/useTheme';

const Background: React.FC = () => {
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  return (
    <div className={`absolute inset-0 z-0 overflow-hidden pointer-events-none transition-colors duration-300 ${isDark ? 'bg-ink-900' : 'bg-paper-100'
      }`}>

      {/* Noise Texture */}
      <div
        className={`absolute inset-0 mix-blend-overlay ${isDark ? 'opacity-10' : 'opacity-5'}`}
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.5'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Ambient Glows */}
      <motion.div
        className={`absolute bottom-[-10%] left-[-10%] w-[80%] h-[60%] blur-[120px] rounded-full ${isDark ? 'bg-gold-900/10' : 'bg-gold-400/10'
          }`}
        animate={{ scale: [1, 1.05, 1], opacity: [0.1, 0.15, 0.1] }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
      />

      {/* Subtle Smoke/Incense effect */}
      <div className={`absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l to-transparent ${isDark ? 'from-ink-800/20' : 'from-gold-200/20'
        }`}></div>

      {/* Abstract Zen Circle / Enso suggestion */}
      <svg className={`absolute top-[10%] right-[-10%] w-[600px] h-[600px] rotate-12 ${isDark ? 'opacity-[0.03]' : 'opacity-[0.08]'
        }`} viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="80" fill="none" stroke="hsl(var(--liuyao-gold))" strokeWidth="40" strokeDasharray="300 100" strokeLinecap="round" />
      </svg>

      {/* Vignette */}
      <div className={`absolute inset-0 pointer-events-none ${isDark
        ? 'bg-radial-gradient from-transparent via-ink-900/50 to-ink-950'
        : 'bg-radial-gradient from-transparent via-paper-100/30 to-paper-200/50'
        }`} />

    </div>
  );
};

export default Background;
