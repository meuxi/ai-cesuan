/**
 * 导出工具集
 * 支持JSON、HTML报告、打印等多种导出格式
 * 移植自 lifekline3 项目
 */

import { SITE_CONFIG } from '@/config/constants';

// 通用数据导出接口
export interface ExportableData {
    title: string;
    date: string;
    type: string;
    data: Record<string, unknown>;
}

/**
 * 导出为JSON文件
 */
export function exportToJson<T = unknown>(data: T, filename: string): void {
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8' });
    downloadBlob(blob, `${filename}.json`);
}

/**
 * 导出为HTML报告
 */
export function exportToHtmlReport(content: ExportableData): void {
    const htmlContent = generateHtmlReport(content);
    const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
    downloadBlob(blob, `${content.title}_${content.date}.html`);
}

/**
 * 生成HTML报告内容
 */
function generateHtmlReport(content: ExportableData): string {
    return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${content.title} - 占卜报告</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(to right, #ffd700, #ff8c00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .header .meta {
            color: #a0a0c0;
            font-size: 0.9rem;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            border-left: 4px solid #8E2DE2;
        }
        .section h2 {
            color: #ffd700;
            font-size: 1.3rem;
            margin-bottom: 15px;
        }
        .section p {
            line-height: 1.8;
            color: #d0d0d0;
        }
        .score-bar {
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            margin: 10px 0;
            overflow: hidden;
        }
        .score-bar-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        .score-high { background: linear-gradient(to right, #22c55e, #16a34a); }
        .score-mid { background: linear-gradient(to right, #6366f1, #4f46e5); }
        .score-low { background: linear-gradient(to right, #ef4444, #dc2626); }
        .luck-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        .luck-great { background: rgba(255, 215, 0, 0.2); color: #ffd700; border: 1px solid #ffd700; }
        .luck-good { background: rgba(34, 197, 94, 0.2); color: #22c55e; border: 1px solid #22c55e; }
        .luck-bad { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #808080;
            font-size: 0.8rem;
        }
        @media print {
            body { background: white; color: #333; }
            .container { box-shadow: none; border: 1px solid #ddd; }
            .section { border-left-color: #8E2DE2; background: #f9f9f9; }
            .header h1 { color: #333; -webkit-text-fill-color: #333; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔮 ${content.title}</h1>
            <p class="meta">占卜类型：${content.type} | 生成日期：${content.date}</p>
        </div>
        
        ${renderDataSections(content.data)}
        
        <div class="footer">
            <p>🔮 ${SITE_CONFIG.name} | <a href="${SITE_CONFIG.url}" style="color: #ffd700;">${SITE_CONFIG.url}</a></p>
            <p>${SITE_CONFIG.slogan}</p>
            <p style="margin-top: 10px;">${SITE_CONFIG.copyright} | 仅供娱乐参考，命理不可全信</p>
        </div>
    </div>
</body>
</html>
    `.trim();
}

/**
 * 渲染数据段落
 */
function renderDataSections(data: Record<string, unknown>): string {
    let html = '';

    for (const [key, value] of Object.entries(data)) {
        if (typeof value === 'object' && value !== null) {
            if (Array.isArray(value)) {
                html += `
                <div class="section">
                    <h2>${formatKey(key)}</h2>
                    <ul>
                        ${value.map(item => `<li>${typeof item === 'object' ? JSON.stringify(item) : item}</li>`).join('')}
                    </ul>
                </div>`;
            } else if ('content' in value && 'score' in value) {
                const scoreClass = value.score >= 7 ? 'score-high' : value.score >= 4 ? 'score-mid' : 'score-low';
                html += `
                <div class="section">
                    <h2>${formatKey(key)} <span style="float:right">${value.score}/10</span></h2>
                    <div class="score-bar"><div class="score-bar-fill ${scoreClass}" style="width: ${value.score * 10}%"></div></div>
                    <p>${value.content}</p>
                </div>`;
            } else {
                html += `
                <div class="section">
                    <h2>${formatKey(key)}</h2>
                    <p>${JSON.stringify(value, null, 2)}</p>
                </div>`;
            }
        } else {
            html += `
            <div class="section">
                <h2>${formatKey(key)}</h2>
                <p>${value}</p>
            </div>`;
        }
    }

    return html;
}

/**
 * 格式化键名
 */
function formatKey(key: string): string {
    const keyMap: Record<string, string> = {
        summary: '命理总评',
        industry: '事业运势',
        wealth: '财富运势',
        marriage: '婚姻运势',
        health: '健康运势',
        family: '六亲运势',
        bazi: '四柱八字',
        personality: '性格分析',
        fengShui: '风水建议',
        crypto: '投资建议',
    };
    return keyMap[key] || key;
}

/**
 * 下载Blob文件
 */
function downloadBlob(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/**
 * 打印当前页面
 */
export function printPage(): void {
    window.print();
}

/**
 * 复制文本到剪贴板
 */
export async function copyToClipboard(text: string): Promise<boolean> {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        const success = document.execCommand('copy');
        document.body.removeChild(textarea);
        return success;
    }
}

/**
 * 从JSON文件导入数据
 */
export function importFromJson<T>(file: File): Promise<T> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const content = e.target?.result as string;
                const data = JSON.parse(content) as T;
                resolve(data);
            } catch (err) {
                reject(new Error('JSON解析失败'));
            }
        };
        reader.onerror = () => reject(new Error('文件读取失败'));
        reader.readAsText(file);
    });
}

/**
 * 生成分享文本（带网站信息）
 */
export function generateShareText(data: ExportableData): string {
    let text = `🔮 ${data.title}\n`;
    text += `📅 ${data.date}\n`;
    text += `━━━━━━━━━━━━━━━\n`;

    for (const [key, value] of Object.entries(data.data)) {
        if (typeof value === 'string') {
            text += `【${formatKey(key)}】\n${value}\n\n`;
        } else if (typeof value === 'object' && 'content' in value) {
            text += `【${formatKey(key)}】${value.score}/10分\n${value.content}\n\n`;
        }
    }

    text += `━━━━━━━━━━━━━━━\n`;
    text += `🔮 ${SITE_CONFIG.name} | ${SITE_CONFIG.url}\n`;
    text += `${SITE_CONFIG.slogan}\n`;
    text += `${SITE_CONFIG.copyright}`;

    return text;
}

/**
 * 人生K线专用HTML报告导出
 * 参考 lifekline3 项目的 handleSaveHtml
 */
export interface KLinePoint {
    age: number;
    year: number;
    ganZhi: string;
    daYun: string;
    score: number;
    open: number;
    close: number;
    high: number;
    low: number;
    reason: string;
}

export interface LifeKLineExportData {
    userName?: string;
    chartData: KLinePoint[];
    analysis?: Record<string, unknown>;
}

export function exportLifeKLineHtmlReport(data: LifeKLineExportData): void {
    const now = new Date();
    const timeString = now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });

    // 找出巅峰和低谷
    const peakYear = data.chartData.reduce((max, curr) => curr.score > max.score ? curr : max, data.chartData[0]);
    const valleyYear = data.chartData.reduce((min, curr) => curr.score < min.score ? curr : min, data.chartData[0]);

    // 生成流年详批表格
    const tableRows = data.chartData.map(item => {
        const scoreColor = item.close >= item.open ? 'color: #22c55e;' : 'color: #ef4444;';
        const trendIcon = item.close >= item.open ? '▲' : '▼';
        const isPeak = item.age === peakYear.age;
        const isValley = item.age === valleyYear.age;
        const rowBg = isPeak ? 'background: #f0fdf4;' : isValley ? 'background: #fef2f2;' : '';

        return `
            <tr style="${rowBg} border-bottom: 1px solid #e5e7eb;">
                <td style="padding: 12px; text-align: center; font-family: monospace;">
                    ${item.age}岁 ${isPeak ? '👑' : isValley ? '🌊' : ''}
                </td>
                <td style="padding: 12px; text-align: center; font-weight: bold;">${item.year} ${item.ganZhi}</td>
                <td style="padding: 12px; text-align: center; color: #6366f1;">${item.daYun || '-'}</td>
                <td style="padding: 12px; text-align: center; font-weight: bold; ${scoreColor}">
                    ${item.score} <span style="font-size: 10px;">${trendIcon}</span>
                </td>
                <td style="padding: 12px; font-size: 13px; color: #374151; line-height: 1.6;">${item.reason}</td>
            </tr>
        `;
    }).join('');

    // 生成分析结果HTML
    let analysisHtml = '';
    if (data.analysis) {
        for (const [key, value] of Object.entries(data.analysis)) {
            if (typeof value === 'string' && value.length > 0) {
                analysisHtml += `
                    <div style="margin-bottom: 24px; padding: 20px; background: #f8fafc; border-radius: 12px; border-left: 4px solid #6366f1;">
                        <h3 style="color: #1e293b; font-size: 16px; margin-bottom: 12px;">${formatKey(key)}</h3>
                        <p style="color: #475569; line-height: 1.8;">${value}</p>
                    </div>
                `;
            }
        }
    }

    const htmlContent = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${data.userName || '用户'} - 人生K线命理报告</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; 
            background: #f8fafc; 
            color: #1e293b;
            line-height: 1.6;
        }
        .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
        .header { text-align: center; padding: 40px 0; border-bottom: 2px solid #e2e8f0; margin-bottom: 40px; }
        .header h1 { font-size: 2.5rem; color: #1e293b; margin-bottom: 8px; }
        .header .subtitle { color: #64748b; font-size: 14px; }
        .peak-info { 
            display: flex; justify-content: center; gap: 20px; margin-top: 20px; flex-wrap: wrap;
        }
        .peak-badge {
            padding: 8px 16px; border-radius: 8px; font-size: 14px; font-weight: bold;
        }
        .peak-high { background: #dcfce7; color: #15803d; border: 1px solid #86efac; }
        .peak-low { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }
        .section { margin-bottom: 40px; }
        .section-title { 
            font-size: 20px; font-weight: bold; color: #1e293b; 
            padding-bottom: 12px; border-bottom: 2px solid #6366f1; 
            margin-bottom: 20px; display: flex; align-items: center; gap: 8px;
        }
        .section-title::before { content: ''; width: 4px; height: 24px; background: #6366f1; border-radius: 2px; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th { background: #f1f5f9; padding: 14px 12px; text-align: center; font-size: 13px; color: #475569; font-weight: 600; text-transform: uppercase; }
        .footer { text-align: center; padding: 40px 0; color: #94a3b8; font-size: 12px; border-top: 1px solid #e2e8f0; margin-top: 40px; }
        @media print {
            body { background: white; }
            .container { padding: 20px; }
            table { page-break-inside: auto; }
            tr { page-break-inside: avoid; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 ${data.userName ? data.userName + '的' : ''}人生K线命理报告</h1>
            <p class="subtitle">生成时间：${timeString}</p>
            <div class="peak-info">
                <span class="peak-badge peak-high">🏔️ 人生巅峰：${peakYear.year}年(${peakYear.age}岁) ${peakYear.score}分</span>
                <span class="peak-badge peak-low">🌊 人生低谷：${valleyYear.year}年(${valleyYear.age}岁) ${valleyYear.score}分</span>
            </div>
        </div>

        ${analysisHtml ? `
        <div class="section">
            <h2 class="section-title">命理分析</h2>
            ${analysisHtml}
        </div>
        ` : ''}

        <div class="section">
            <h2 class="section-title">流年详批全表 (${data.chartData.length}年)</h2>
            <table>
                <thead>
                    <tr>
                        <th style="width: 80px;">年龄</th>
                        <th style="width: 120px;">流年</th>
                        <th style="width: 100px;">大运</th>
                        <th style="width: 80px;">评分</th>
                        <th>运势批断与建议</th>
                    </tr>
                </thead>
                <tbody>
                    ${tableRows}
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>🔮 ${SITE_CONFIG.name} | <a href="${SITE_CONFIG.url}" style="color: #6366f1;">${SITE_CONFIG.url}</a></p>
            <p style="margin-top: 8px;">${SITE_CONFIG.slogan} | ${SITE_CONFIG.copyright}</p>
            <p style="margin-top: 8px; color: #94a3b8;">命理仅供参考，人生路径最终取决于个人选择与努力</p>
        </div>
    </div>
</body>
</html>
    `.trim();

    const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
    downloadBlob(blob, `${data.userName || 'User'}_LifeKLine_Report_${now.getTime()}.html`);
}
