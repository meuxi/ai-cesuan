/**
 * 塔罗牌API服务
 * 调用后端API获取牌数据
 */

const API_BASE = import.meta.env.VITE_API_BASE || ''

export interface TarotCard {
    code: string
    name: string
    name_en: string
    number: number
    suit: string
    element: string
    keywords: string[]
    upright_meaning: string
    reversed_meaning: string
    image_desc: string
    advice: string
}

export interface TarotSpread {
    code: string
    name: string
    name_en: string
    positions: { index: number; name: string; description: string }[]
    description: string
    suitable_for: string[]
}

export interface CardsResponse {
    total: number
    major_count?: number
    minor_count?: number
    cards: TarotCard[]
}

export interface SpreadsResponse {
    total: number
    spreads: TarotSpread[]
}

// 卡牌code到图片文件名的映射
const CARD_IMAGE_MAP: Record<string, string> = {
    // 大阿尔卡那
    'FOOL': 'thefool.jpeg',
    'MAGICIAN': 'themagician.jpeg',
    'HIGH_PRIESTESS': 'thehighpriestess.jpeg',
    'EMPRESS': 'theempress.jpeg',
    'EMPEROR': 'theemperor.jpeg',
    'HIEROPHANT': 'thehierophant.jpeg',
    'LOVERS': 'TheLovers.jpg',
    'CHARIOT': 'thechariot.jpeg',
    'STRENGTH': 'thestrength.jpeg',
    'HERMIT': 'thehermit.jpeg',
    'WHEEL_OF_FORTUNE': 'wheeloffortune.jpeg',
    'JUSTICE': 'justice.jpeg',
    'HANGED_MAN': 'thehangedman.jpeg',
    'DEATH': 'death.jpeg',
    'TEMPERANCE': 'temperance.jpeg',
    'DEVIL': 'thedevil.jpeg',
    'TOWER': 'thetower.jpeg',
    'STAR': 'thestar.jpeg',
    'MOON': 'themoon.jpeg',
    'SUN': 'thesun.jpeg',
    'JUDGEMENT': 'judgement.jpeg',
    'WORLD': 'theworld.jpeg',
    // 权杖牌组
    'WANDS_ACE': 'aceofwands.jpeg',
    'WANDS_TWO': 'twoofwands.jpeg',
    'WANDS_THREE': 'threeofwands.jpeg',
    'WANDS_FOUR': 'fourofwands.jpeg',
    'WANDS_FIVE': 'fiveofwands.jpeg',
    'WANDS_SIX': 'sixofwands.jpeg',
    'WANDS_SEVEN': 'sevenofwands.jpeg',
    'WANDS_EIGHT': 'eightofwands.jpeg',
    'WANDS_NINE': 'nineofwands.jpeg',
    'WANDS_TEN': 'tenofwands.jpeg',
    'WANDS_PAGE': 'pageofwands.jpeg',
    'WANDS_KNIGHT': 'knightofwands.jpeg',
    'WANDS_QUEEN': 'queenofwands.jpeg',
    'WANDS_KING': 'kingofwands.jpeg',
    // 圣杯牌组
    'CUPS_ACE': 'aceofcups.jpeg',
    'CUPS_TWO': 'twoofcups.jpeg',
    'CUPS_THREE': 'threeofcups.jpeg',
    'CUPS_FOUR': 'fourofcups.jpeg',
    'CUPS_FIVE': 'fiveofcups.jpeg',
    'CUPS_SIX': 'sixofcups.jpeg',
    'CUPS_SEVEN': 'sevenofcups.jpeg',
    'CUPS_EIGHT': 'eightofcups.jpeg',
    'CUPS_NINE': 'nineofcups.jpeg',
    'CUPS_TEN': 'tenofcups.jpeg',
    'CUPS_PAGE': 'pageofcups.jpeg',
    'CUPS_KNIGHT': 'knightofcups.jpeg',
    'CUPS_QUEEN': 'queenofcups.jpeg',
    'CUPS_KING': 'kingofcups.jpeg',
    // 宝剑牌组
    'SWORDS_ACE': 'aceofswords.jpeg',
    'SWORDS_TWO': 'twoofswords.jpeg',
    'SWORDS_THREE': 'threeofswords.jpeg',
    'SWORDS_FOUR': 'fourofswords.jpeg',
    'SWORDS_FIVE': 'fiveofswords.jpeg',
    'SWORDS_SIX': 'sixofswords.jpeg',
    'SWORDS_SEVEN': 'sevenofswords.jpeg',
    'SWORDS_EIGHT': 'eightofswords.jpeg',
    'SWORDS_NINE': 'nineofswords.jpeg',
    'SWORDS_TEN': 'tenofswords.jpeg',
    'SWORDS_PAGE': 'pageofswords.jpeg',
    'SWORDS_KNIGHT': 'knightofswords.jpeg',
    'SWORDS_QUEEN': 'queenofswords.jpeg',
    'SWORDS_KING': 'kingofswords.jpeg',
    // 星币牌组
    'PENTACLES_ACE': 'aceofpentacles.jpeg',
    'PENTACLES_TWO': 'twoofpentacles.jpeg',
    'PENTACLES_THREE': 'threeofpentacles.jpeg',
    'PENTACLES_FOUR': 'fourofpentacles.jpeg',
    'PENTACLES_FIVE': 'fiveofpentacles.jpeg',
    'PENTACLES_SIX': 'sixofpentacles.jpeg',
    'PENTACLES_SEVEN': 'sevenofpentacles.jpeg',
    'PENTACLES_EIGHT': 'eightofpentacles.jpeg',
    'PENTACLES_NINE': 'nineofpentacles.jpeg',
    'PENTACLES_TEN': 'tenofpentacles.jpeg',
    'PENTACLES_PAGE': 'pageofpentacles.jpeg',
    'PENTACLES_KNIGHT': 'knightofpentacles.jpeg',
    'PENTACLES_QUEEN': 'queenofpentacles.jpeg',
    'PENTACLES_KING': 'kingofpentacles.jpeg',
}

export function getCardImageUrl(code: string): string {
    const filename = CARD_IMAGE_MAP[code]
    if (filename) {
        return `/images/tarot_cards/${filename}`
    }
    return '/images/tarot_cards/thefool.jpeg'
}

export async function fetchAllCards(includeMinor = true): Promise<CardsResponse> {
    const response = await fetch(`${API_BASE}/api/tarot/cards?include_minor=${includeMinor}`)
    if (!response.ok) {
        throw new Error('获取塔罗牌数据失败')
    }
    return response.json()
}

export async function fetchMajorArcana(): Promise<CardsResponse> {
    const response = await fetch(`${API_BASE}/api/tarot/cards`)
    if (!response.ok) {
        throw new Error('获取大阿尔卡那数据失败')
    }
    return response.json()
}

export async function fetchSpreads(): Promise<SpreadsResponse> {
    const response = await fetch(`${API_BASE}/api/tarot/spreads`)
    if (!response.ok) {
        throw new Error('获取牌阵数据失败')
    }
    return response.json()
}

export async function fetchCardDetail(code: string): Promise<TarotCard> {
    const response = await fetch(`${API_BASE}/api/tarot/cards/${code}`)
    if (!response.ok) {
        throw new Error('获取卡牌详情失败')
    }
    return response.json()
}
