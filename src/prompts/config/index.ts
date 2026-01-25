/**
 * 玄学AI提示词配置系统 - 导出索引
 */

export {
  // 枚举类型
  DivinationType,
  
  // 接口类型
  type DivinationPrompt,
  type BaziInputData,
  type ZiweiInputData,
  type LiuyaoInputData,
  type XiaoliuInputData,
  type DreamInputData,
  type ZodiacInputData,
  type DivinationInputData,
  type FormatCheckResult,
  
  // 系统角色提示词
  FORMAT_CONSTRAINT_INSTRUCTION,
  BAZI_SYSTEM_ROLE,
  ZIWEI_SYSTEM_ROLE,
  LIUYAO_SYSTEM_ROLE,
  XIAOLIU_SYSTEM_ROLE,
  DREAM_SYSTEM_ROLE,
  ZODIAC_SYSTEM_ROLE,
  
  // 用户提示词模板
  BAZI_USER_TEMPLATE,
  ZIWEI_USER_TEMPLATE,
  LIUYAO_USER_TEMPLATE,
  XIAOLIU_USER_TEMPLATE,
  DREAM_USER_TEMPLATE,
  ZODIAC_USER_TEMPLATE,
  
  // 提示词映射
  PROMPT_TEMPLATES,
  
  // 工具函数
  buildPrompt,
  replaceVariables,
  flattenObject,
  validateOutputFormat,
  
  // 默认导出
  default as promptConfig,
} from './promptConfig';
