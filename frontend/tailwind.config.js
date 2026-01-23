/** @type {import('tailwindcss').Config} */
export default {
	darkMode: ['class'],
	content: [
		'./index.html',
		'./src/**/*.{js,ts,jsx,tsx}',
	],
	theme: {
		container: {
			center: true,
			padding: {
				DEFAULT: '1rem',
				md: '1.5rem',
			},
		},
		extend: {
			borderRadius: {
				lg: 'var(--radius)',
				md: 'calc(var(--radius) - 2px)',
				sm: 'calc(var(--radius) - 4px)',
				xl: 'calc(var(--radius) + 4px)',
			},
			fontFamily: {
				sans: ['var(--font-geist-sans)', 'ui-sans-serif', 'system-ui', 'sans-serif'],
				mono: ['var(--font-geist-mono)', 'ui-monospace', 'SFMono-Regular', 'monospace'],
			},
			fontSize: {
				'5xl': ['3rem', { lineHeight: '1.1' }],
				'6xl': ['3.75rem', { lineHeight: '1.1' }],
			},
			animation: {
				'spin-slow': 'spin 20s linear infinite',
			},
			colors: {
				background: 'hsl(var(--background))',
				foreground: 'hsl(var(--foreground))',
				// 六爻专用颜色
				ink: {
					400: '#a1a1aa',
					500: '#737373',
					600: '#525252',
					700: '#404040',
					800: '#262626',
					850: '#1f1f1f',
					900: '#171717',
					950: '#0a0a0a',
				},
				paper: {
					100: '#fafafa',
					200: '#f5f5f5',
					300: '#e5e5e5',
				},
				gold: {
					200: '#f0dca8',
					300: '#e6c88a',
					400: '#d4a853',
					500: '#c9972f',
					600: '#b8860b',
					700: '#a07a0c',
					800: '#8b6914',
					900: '#6b5210',
				},
				cinnabar: '#c53030',
				card: {
					DEFAULT: 'hsl(var(--card))',
					foreground: 'hsl(var(--card-foreground))'
				},
				popover: {
					DEFAULT: 'hsl(var(--popover))',
					foreground: 'hsl(var(--popover-foreground))'
				},
				primary: {
					DEFAULT: 'hsl(var(--primary))',
					foreground: 'hsl(var(--primary-foreground))'
				},
				secondary: {
					DEFAULT: 'hsl(var(--secondary))',
					foreground: 'hsl(var(--secondary-foreground))'
				},
				muted: {
					DEFAULT: 'hsl(var(--muted))',
					foreground: 'hsl(var(--muted-foreground))'
				},
				accent: {
					DEFAULT: 'hsl(var(--accent))',
					foreground: 'hsl(var(--accent-foreground))'
				},
				destructive: {
					DEFAULT: 'hsl(var(--destructive))',
					foreground: 'hsl(var(--destructive-foreground))'
				},
				border: 'hsl(var(--border))',
				input: 'hsl(var(--input))',
				ring: 'hsl(var(--ring))',
				chart: {
					'1': 'hsl(var(--chart-1))',
					'2': 'hsl(var(--chart-2))',
					'3': 'hsl(var(--chart-3))',
					'4': 'hsl(var(--chart-4))',
					'5': 'hsl(var(--chart-5))'
				},
				// 侧边栏颜色 - 修复移动端背景透明问题
				sidebar: {
					DEFAULT: 'hsl(var(--sidebar-background))',
					foreground: 'hsl(var(--sidebar-foreground))',
					primary: 'hsl(var(--sidebar-primary))',
					'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
					accent: 'hsl(var(--sidebar-accent))',
					'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
					border: 'hsl(var(--sidebar-border))',
					ring: 'hsl(var(--sidebar-ring))'
				}
			}
		}
	},
	plugins: [
		require('tailwindcss-animate'),
		require('@tailwindcss/typography'),
		function ({ addUtilities }) {
			addUtilities({
				/* FateMaster 风格卡片 - shadcn/ui 样式 */
				'.fm-card': {
					'border-radius': '0.75rem',
					'border': '1px solid hsl(var(--border))',
					'background-color': 'hsl(var(--card))',
					'color': 'hsl(var(--card-foreground))',
					'box-shadow': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
					'transition': 'all 150ms ease',
				},
				'.fm-card:hover': {
					'box-shadow': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
				},
				/* 可点击卡片 */
				'.fm-card-clickable': {
					'border-radius': '0.75rem',
					'border': '1px solid #f3f4f6',
					'background-color': 'white',
					'box-shadow': '0 1px 3px 0 rgb(0 0 0 / 0.1)',
					'transition': 'all 150ms ease',
					'cursor': 'pointer',
				},
				'.fm-card-clickable:hover': {
					'border-color': 'black',
					'box-shadow': '0 4px 6px -1px rgb(0 0 0 / 0.1)',
				},
				/* 主按钮 - 黑色 */
				'.fm-btn': {
					'background-color': 'black',
					'color': 'white',
					'border-radius': '0.375rem',
					'padding': '0.5rem 1rem',
					'font-size': '0.875rem',
					'font-weight': '600',
					'line-height': '1.5',
					'transition': 'background-color 150ms ease',
					'border': 'none',
					'cursor': 'pointer',
				},
				'.fm-btn:hover': {
					'background-color': '#1f2937',
				},
				/* 输入框 */
				'.fm-input': {
					'border': '1px solid hsl(var(--border))',
					'border-radius': '0.375rem',
					'padding': '0.5rem 0.75rem',
					'background-color': 'hsl(var(--background))',
					'color': 'hsl(var(--foreground))',
					'font-size': '0.875rem',
					'transition': 'border-color 150ms ease',
					'outline': 'none',
				},
				'.fm-input:focus': {
					'border-color': 'hsl(var(--ring))',
					'box-shadow': '0 0 0 2px hsl(var(--ring) / 0.1)',
				},
				/* 图标尺寸 */
				'.fm-icon': {
					'height': '1.25rem',
					'width': '1.25rem',
				},
				'.fm-icon-lg': {
					'height': '1.5rem',
					'width': '1.5rem',
				},
				/* 兼容旧类名 */
				'.flat-card': {
					'border-radius': '0.75rem',
					'border': '1px solid #f3f4f6',
					'background-color': 'white',
					'box-shadow': '0 1px 3px 0 rgb(0 0 0 / 0.1)',
					'transition': 'all 150ms ease',
				},
				'.flat-card:hover': {
					'border-color': 'black',
					'box-shadow': '0 4px 6px -1px rgb(0 0 0 / 0.1)',
				},
				'.flat-btn': {
					'background-color': 'black',
					'color': 'white',
					'border-radius': '0.375rem',
					'padding': '0.5rem 1rem',
					'font-size': '0.875rem',
					'font-weight': '600',
					'transition': 'background-color 150ms ease',
					'border': 'none',
					'cursor': 'pointer',
				},
				'.flat-btn:hover': {
					'background-color': '#1f2937',
				},
				'.flat-btn-secondary': {
					'background-color': '#f5f5f5',
					'color': '#171717',
					'border-radius': '0.375rem',
					'padding': '0.5rem 1rem',
					'font-size': '0.875rem',
					'font-weight': '600',
					'transition': 'background-color 150ms ease',
					'border': 'none',
					'cursor': 'pointer',
				},
				'.flat-btn-secondary:hover': {
					'background-color': '#e5e5e5',
				},
				'.flat-icon': {
					'height': '1.25rem',
					'width': '1.25rem',
				},
			})
		},
	],
}
