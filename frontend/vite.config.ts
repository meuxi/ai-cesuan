import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    // HTML 环境变量替换插件 - 支持多种统计服务
    {
      name: 'html-transform',
      transformIndexHtml(html) {
        return html
          .replace(/%VITE_ANALYTICS_AIZHAN%/g, process.env.VITE_ANALYTICS_AIZHAN || '')
          .replace(/%VITE_ANALYTICS_BAIDU%/g, process.env.VITE_ANALYTICS_BAIDU || '')
          .replace(/%VITE_ANALYTICS_CLARITY%/g, process.env.VITE_ANALYTICS_CLARITY || '')
          .replace(/%VITE_ANALYTICS_CUSTOM%/g, process.env.VITE_ANALYTICS_CUSTOM || '')
      }
    }
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  // 生产构建时移除console和debugger语句
  esbuild: {
    drop: process.env.NODE_ENV === 'production' ? ['console', 'debugger'] : []
  },
  // 构建优化配置
  build: {
    // 输出目录
    outDir: 'dist',
    // 生成静态资源的存放路径
    assetsDir: 'assets',
    // 小于此阈值的导入或引用资源将内联为 base64 编码
    assetsInlineLimit: 4096,
    // 启用/禁用 CSS 代码拆分
    cssCodeSplit: true,
    // 构建后是否生成 source map 文件
    sourcemap: false,
    // chunk 大小警告的限制（以 kbs 为单位）
    chunkSizeWarningLimit: 1000,
    // Rollup 打包配置
    rollupOptions: {
      output: {
        // 静态资源分类打包
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
        // 代码分割策略
        manualChunks: {
          // React 核心库
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          // UI 组件库
          'ui-vendor': ['framer-motion', 'lucide-react', '@radix-ui/react-dropdown-menu', '@radix-ui/react-tabs'],
          // 工具库
          'utils-vendor': ['zustand', 'date-fns', 'clsx', 'dompurify'],
        }
      }
    },
    // 压缩配置
    minify: 'esbuild',
    // 目标浏览器兼容性
    target: 'es2015',
  },
  // 依赖优化选项
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      'framer-motion',
      'lucide-react',
      'zustand',
    ],
  },
  server: {
    host: '0.0.0.0',
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
