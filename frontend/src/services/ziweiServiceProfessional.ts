/**
 * 紫微斗数专业计算服务
 * 核心算法在后端执行（使用iztro-py库）
 * 前端只负责调用API和展示
 */

import { ZiweiInput, ZiweiResult } from '@/types/ziwei'
import { logger } from '@/utils/logger'

const API_BASE = import.meta.env.VITE_API_BASE || ''

export class ZiweiServiceProfessional {
    private static instance: ZiweiServiceProfessional

    static getInstance(): ZiweiServiceProfessional {
        if (!ZiweiServiceProfessional.instance) {
            ZiweiServiceProfessional.instance = new ZiweiServiceProfessional()
        }
        return ZiweiServiceProfessional.instance
    }

    /**
     * 计算紫微斗数命盘 - 调用后端API
     * 支持派别选择（全书派/中州派）
     */
    async calculate(input: ZiweiInput): Promise<ZiweiResult> {
        try {
            const response = await fetch(`${API_BASE}/api/ziwei/paipan`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    year: input.year,
                    month: input.month,
                    day: input.day,
                    hour: input.hour,
                    minute: input.minute || 0,
                    gender: input.gender,
                    language: input.language || 'zh-CN',
                    algorithm: input.algorithm || 'default'  // 派别参数
                })
            })

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}))
                throw new Error(errorData.detail || `HTTP ${response.status}`)
            }

            const result = await response.json()

            // 后端返回格式: { success: true, basicInfo: ..., palaces: ... }
            // 需要处理success字段，返回ZiweiResult格式
            if (result.success === false) {
                throw new Error(result.message || '排盘失败')
            }

            // 移除success字段，返回ZiweiResult
            const { success, ...ziweiResult } = result
            return ziweiResult as ZiweiResult

        } catch (error: unknown) {
            logger.error('紫微斗数计算失败:', error)
            const message = error instanceof Error ? error.message : '未知错误'
            throw new Error(`紫微斗数计算失败: ${message}`)
        }
    }

}


// 导出单例
export const ziweiServiceProfessional = ZiweiServiceProfessional.getInstance()
