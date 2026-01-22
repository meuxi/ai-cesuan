/**
 * 六爻类型定义
 * 移植自源项目 F:\备份\六爻起卦工具源码\types.ts
 */

// 爻类型
// 0: 少阳 (—) 静阳
// 1: 少阴 (--) 静阴
// 2: 老阳 (— O) 动阳→阴
// 3: 老阴 (-- X) 动阴→阳
export type LineType = 0 | 1 | 2 | 3;

// 起卦方法
export enum DivinationMethod {
  COIN = 'coin',
  NUMBER = 'number',
  TIME = 'time'
}

// 摇卦结果
export interface YaoResult {
  lines: LineType[];
  timestamp: number;
  question: string;
  method: DivinationMethod;
}

// 历史记录
export interface HistoryRecord extends YaoResult {
  id: string;
  interpretation: string;
  hexagramName: string;
  hexagramData?: HexagramInfo;  // 保存完整卦象数据，避免重复计算
}

// 八卦
export interface Trigram {
  name: string;
  chineseName: string;
  nature: string;
  number: number; // 1-8 (乾=1...坤=8)
  element: string; // 金木水火土
  binary: string;
}

// 应用设置
export interface AppSettings {
  soundEnabled: boolean;
  hapticEnabled: boolean;
  aiStyle: 'concise' | 'detailed' | 'philosophical';
  autoInterpret: boolean;
}

// 伏神信息（基础，用于爻中）
export interface FuShenInfo {
  stem: string;
  branch: string;
  relation: string;
  element: string;
}

// 伏神详情（高级分析中）
export interface FuShenDetailInfo {
  liuQin: string;          // 六亲
  wuXing: string;          // 五行
  naJia: string;           // 纳甲地支
  feiShenPosition: number; // 飞神位置（1-6）
  feiShenLiuQin: string;   // 飞神六亲
  isAvailable: boolean;    // 是否可用
  availabilityReason: string; // 可用性原因
}

// 爻详情
export interface LineDetails {
  index: number;            // 0-5
  type: LineType;           // 爻类型
  typeName: string;         // 爻名称
  isMoving: boolean;        // 是否动爻

  // 计算属性
  stem: string;             // 天干
  branch: string;           // 地支
  element: string;          // 五行
  sixRelation: string;      // 六亲
  sixBeast: string;         // 六神

  isShi: boolean;           // 是否世爻
  isYing: boolean;          // 是否应爻

  // 伏神 (仅当六亲缺失时存在)
  fuShen?: FuShenInfo;

  // 变爻信息
  changedType?: LineType;
  changedBranch?: string;
  changedStem?: string;
  changedRelation?: string;
}

// 卦象信息
export interface HexagramInfo {
  name: string;             // 卦名
  palaceName: string;       // 宫名
  palaceElement: string;    // 宫五行
  lines: LineDetails[];     // 六爻详情 (0-5 从下到上)
  transformedName?: string; // 变卦名
}

// 摇钱结果
export interface CoinCastResult {
  lineType: number;
  lineName: string;
  backs: number;
}

// API响应
export interface HexagramResponse {
  success: boolean;
  hexagram: HexagramInfo;
  castResults?: CoinCastResult[];
}

export interface InterpretResponse {
  success: boolean;
  interpretation: string;
  provider: string;
}

// AI解卦风格
export type AIStyle = 'concise' | 'detailed' | 'philosophical';

export const AI_STYLE_LABELS: Record<AIStyle, string> = {
  concise: '直断吉凶',
  detailed: '详细分析',
  philosophical: '哲理解读'
};

// ============= 高级分析类型 =============

// 旺衰五态
export type WangShuai = '旺' | '相' | '休' | '囚' | '死';

// 空亡状态
export type KongWangState = '不空' | '真空' | '动空' | '冲空' | '临建';

// 月建日辰作用
export type YaoAction = '生' | '克' | '扶' | '冲' | '合' | '破' | '无';

// 特殊状态
export type SpecialStatus = '无' | '暗动' | '日破';

// 动爻变化类型
export type HuaType = '化进' | '化退' | '回头生' | '回头克' | '化空' | '化墓' | '伏吟' | '反吟' | '无';

// 十二长生
export type ChangShengStage = '长生' | '沐浴' | '冠带' | '临官' | '帝旺' | '衰' | '病' | '死' | '墓' | '绝' | '胎' | '养';

// 月建日辰影响
export interface YaoInfluence {
  monthAction: YaoAction;
  dayAction: YaoAction;
  description: string;
}

// 爻强度
export interface YaoStrength {
  wangShuai: WangShuai;
  score: number;
  factors: string[];
  isStrong: boolean;
  specialStatus: SpecialStatus;
}

// 动爻变化分析
export interface YaoChangeAnalysis {
  huaType: HuaType;
  originalZhi: string;
  changedZhi: string;
  description: string;
}

// 十二长生信息
export interface ChangShengInfo {
  stage: ChangShengStage;
  strength: 'strong' | 'medium' | 'weak';
  description: string;
}

// 扩展爻信息
export interface ExtendedYaoInfo {
  index: number;
  branch: string;
  element: string;
  liuQin: string;
  isMoving: boolean;
  kongWangState: KongWangState;
  influence: YaoInfluence;
  strength: YaoStrength;
  changeAnalysis?: YaoChangeAnalysis;
  changSheng?: ChangShengInfo;
}

// 旬空信息
export interface KongWangInfo {
  xun: string;
  kongDizhi: [string, string];
}

// 三合局分析
export interface SanHeAnalysis {
  hasFullSanHe: boolean;
  fullSanHe?: {
    name: string;
    result: string;
    positions: number[];
  };
  hasBanHe: boolean;
  banHe: Array<{
    branches: [string, string];
    result: string;
    type: 'sheng' | 'mu';
    positions: number[];
  }>;
}

// 六冲卦信息
export interface LiuChongGuaInfo {
  isLiuChongGua: boolean;
  description?: string;
}

// 神系成员
export interface ShenMember {
  liuQin: string;
  wuXing: string;
  positions: number[];
}

// 神系（原神/忌神/仇神）
export interface ShenSystem {
  yuanShen?: ShenMember;
  jiShen?: ShenMember;
  chouShen?: ShenMember;
}

// 应期推断
export interface TimeRecommendation {
  type: 'favorable' | 'unfavorable' | 'critical';
  timeframe: string;
  earthlyBranch?: string;
  description: string;
}

// 高级分析结果
export interface AdvancedAnalysisResult {
  kongWang: KongWangInfo;
  extendedYaos: ExtendedYaoInfo[];
  sanHeAnalysis: SanHeAnalysis;
  liuChongGua: LiuChongGuaInfo;
  shenSystem?: ShenSystem;
  timeRecommendations?: TimeRecommendation[];
  fuShen?: FuShenDetailInfo[];  // 伏神列表（用神不上卦时）
}

// 高级分析响应
export interface AdvancedAnalysisResponse {
  success: boolean;
  hexagramName: string;
  analysis: AdvancedAnalysisResult;
}
