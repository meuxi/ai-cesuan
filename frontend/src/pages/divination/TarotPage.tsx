import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { logger } from '@/utils/logger'
import SEOHead, { SEO_CONFIG } from '@/components/SEOHead'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { getDivinationOption } from '@/config/constants'
import { TarotCard } from '@/components/TarotCard'
import { ShuffleAnimation } from '@/components/tarot/ShuffleAnimation'
import { MasterSelector } from '@/components/MasterSelector'
import { MASTERS, getDefaultMaster, type Master } from '@/config/masters'
import { Shuffle, RotateCcw, Layers, Sparkles } from 'lucide-react'
import { fetchAllCards, fetchSpreads, type TarotCard as TarotCardData, type TarotSpread } from '@/services/tarotApi'

const CONFIG = getDivinationOption('tarot')!

interface DrawnCard {
  card: TarotCardData
  revealed: boolean
  isReversed: boolean
}

export default function TarotPage() {
  const { t } = useTranslation()
  const [prompt, setPrompt] = useLocalStorage('tarot_prompt', '')
  const [selectedMaster, setSelectedMaster] = useState<Master>(getDefaultMaster())
  const [isShuffling, setIsShuffling] = useState(false)
  const [drawnCards, setDrawnCards] = useState<DrawnCard[]>([])
  const [phase, setPhase] = useState<'input' | 'shuffle' | 'reveal' | 'result'>('input')

  // API数据
  const [allCards, setAllCards] = useState<TarotCardData[]>([])
  const [spreads, setSpreads] = useState<TarotSpread[]>([])
  const [selectedSpread, setSelectedSpread] = useState<TarotSpread | null>(null)
  const [useMajorOnly, setUseMajorOnly] = useState(false)
  const [loading78, setLoading78] = useState(true)

  const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
    useDivination('tarot')

  // 加载牌数据和牌阵
  useEffect(() => {
    const loadData = async () => {
      try {
        const [cardsRes, spreadsRes] = await Promise.all([
          fetchAllCards(true),
          fetchSpreads()
        ])
        setAllCards(cardsRes.cards)
        setSpreads(spreadsRes.spreads)
        // 默认选择三牌阵
        const threeCard = spreadsRes.spreads.find(s => s.code === 'three_card')
        if (threeCard) setSelectedSpread(threeCard)
      } catch (error) {
        logger.error('加载塔罗牌数据失败:', error)
      } finally {
        setLoading78(false)
      }
    }
    loadData()
  }, [])

  // 获取可用的牌
  const availableCards = useMajorOnly
    ? allCards.filter(c => c.suit === 'MAJOR')
    : allCards

  // 洗牌
  const handleShuffle = () => {
    if (!prompt.trim() || !selectedSpread || availableCards.length === 0) {
      return
    }
    setPhase('shuffle')
    setIsShuffling(true)

    setTimeout(() => {
      // 随机抽牌（数量取决于牌阵）
      const cardCount = selectedSpread.positions.length
      const shuffled = [...availableCards].sort(() => Math.random() - 0.5)
      const drawn = shuffled.slice(0, cardCount).map(card => ({
        card,
        revealed: false,
        isReversed: Math.random() > 0.7 // 30%概率逆位
      }))
      setDrawnCards(drawn)
      setIsShuffling(false)
      setPhase('reveal')
    }, 2000)
  }

  // 翻牌
  const handleRevealCard = (index: number) => {
    setDrawnCards(prev => prev.map((item, i) =>
      i === index ? { ...item, revealed: true } : item
    ))
  }

  // 提交解读
  const handleSubmit = () => {
    const allRevealed = drawnCards.every(c => c.revealed)
    if (!allRevealed || !selectedSpread) {
      return
    }

    setPhase('result')
    onSubmit({
      prompt: prompt,
      cards: drawnCards.map((c, i) => ({
        position: selectedSpread.positions[i]?.name || `位置${i + 1}`,
        name: c.card.name,
        code: c.card.code,
        isReversed: c.isReversed,
        meaning: c.isReversed ? c.card.reversed_meaning : c.card.upright_meaning
      })),
      spread: {
        code: selectedSpread.code,
        name: selectedSpread.name
      },
      master: {
        id: selectedMaster.id,
        name: selectedMaster.name,
        prompt: selectedMaster.prompt,
        gamePrompt: selectedMaster.gamePrompts.tarot
      }
    })
  }

  // 重新开始
  const handleReset = () => {
    setDrawnCards([])
    setPhase('input')
  }

  const allRevealed = drawnCards.length > 0 && drawnCards.every(c => c.revealed)

  return (
    <>
      <SEOHead {...SEO_CONFIG.tarot} />
      <DivinationCardHeader
        title={t('tarot.title')}
        description={t('tarot.description')}
        icon={CONFIG.icon}
        divinationType="tarot"
      >
        <div className="w-full max-w-3xl mx-auto">
          <div className="space-y-6">
            {/* 加载中 */}
            {loading78 && (
              <div className="text-center py-8">
                <div className="animate-spin w-8 h-8 border-2 border-muted border-t-foreground rounded-full mx-auto"></div>
                <p className="text-sm text-muted-foreground mt-2">{t('tarot.loading')}</p>
              </div>
            )}

            {/* 问题输入 */}
            {!loading78 && phase === 'input' && (
              <div className="space-y-5">
                <div>
                  <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder={t('tarot.questionPlaceholder')}
                    maxLength={100}
                    rows={3}
                    className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 resize-none"
                  />
                  <p className="text-xs text-muted-foreground mt-2">
                    {t('tarot.questionTip')}
                  </p>
                </div>

                {/* 牌阵选择 */}
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center gap-2 text-foreground">
                    <Layers className="w-4 h-4" />
                    {t('tarot.selectSpread')}
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {spreads.map(spread => (
                      <button
                        key={spread.code}
                        onClick={() => setSelectedSpread(spread)}
                        className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${selectedSpread?.code === spread.code
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-secondary text-secondary-foreground hover:bg-accent'
                          }`}
                      >
                        {spread.name} ({spread.positions.length}{t('tarot.cards')})
                      </button>
                    ))}
                  </div>
                </div>

                {/* 牌组选择 */}
                <div className="flex items-center gap-4">
                  <label className="flex items-center gap-2 text-sm text-foreground">
                    <input
                      type="checkbox"
                      checked={useMajorOnly}
                      onChange={(e) => setUseMajorOnly(e.target.checked)}
                      className="rounded border-input"
                    />
                    {t('tarot.majorOnly')}
                  </label>
                  <span className="text-xs text-muted-foreground">
                    {t('tarot.currentDeck')}: {availableCards.length}{t('tarot.cards')}
                  </span>
                </div>

                {/* 大师选择 */}
                <MasterSelector
                  selectedMaster={selectedMaster}
                  onSelectMaster={setSelectedMaster}
                />

                {/* 洗牌按钮 */}
                <button
                  onClick={handleShuffle}
                  disabled={!prompt.trim() || !selectedSpread}
                  className="w-full py-3 bg-primary text-primary-foreground hover:bg-primary/90 disabled:bg-muted disabled:text-muted-foreground rounded-md font-semibold flex items-center justify-center gap-2 transition-colors"
                >
                  <Shuffle className="w-5 h-5" />
                  {t('tarot.startShuffle')} ({selectedSpread?.name || t('tarot.selectSpreadFirst')})
                </button>
              </div>
            )}

            {/* 洗牌动画 - 使用新版沉浸式动画 */}
            <ShuffleAnimation 
              isShuffling={phase === 'shuffle' && isShuffling}
              duration={2000}
              cardCount={selectedSpread?.positions.length || 3}
            />

            {/* 翻牌阶段 */}
            {(phase === 'reveal' || phase === 'result') && drawnCards.length > 0 && selectedSpread && (
              <div className="space-y-6">
                {/* 问题回显 */}
                <div className="p-4 bg-secondary rounded-lg text-center border border-border">
                  <p className="text-sm text-foreground">
                    "{prompt}"
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {selectedSpread.name}
                  </p>
                </div>

                {/* 牌阵展示 */}
                <div className="flex flex-col items-center gap-4">
                  <div className="flex gap-4 sm:gap-6 justify-center flex-wrap">
                    {drawnCards.map((item, index) => (
                      <div key={index} className="flex flex-col items-center gap-2">
                        <TarotCard
                          cardCode={item.card.code}
                          cardName={item.card.name}
                          isRevealed={item.revealed}
                          isReversed={item.isReversed}
                          onReveal={() => handleRevealCard(index)}
                          delay={index * 0.2}
                          size="lg"
                        />
                        <span className="text-xs text-muted-foreground">
                          {selectedSpread.positions[index]?.name || `${t('tarot.position')}${index + 1}`}
                        </span>
                      </div>
                    ))}
                  </div>

                  {!allRevealed && (
                    <p className="text-sm text-muted-foreground animate-pulse">
                      {t('tarot.clickToReveal')}
                    </p>
                  )}
                </div>

                {/* 操作按钮 */}
                {allRevealed && phase === 'reveal' && !result && !loading && (
                  <div className="flex gap-3 justify-center">
                    <button
                      onClick={handleReset}
                      className="px-4 py-2 border border-border rounded-md text-sm font-medium text-foreground hover:bg-secondary flex items-center gap-2 transition-colors"
                    >
                      <RotateCcw className="w-4 h-4" />
                      {t('tarot.redraw')}
                    </button>
                    <button
                      onClick={handleSubmit}
                      className="px-6 py-2 bg-primary text-primary-foreground hover:bg-primary/90 rounded-md text-sm font-semibold flex items-center gap-2 transition-colors"
                    >
                      <Sparkles className="w-4 h-4" />
                      {t('tarot.askMaster', { master: selectedMaster.name })}
                    </button>
                  </div>
                )}

                {/* AI分析结果内嵌展示 */}
                <InlineResult
                  result={result}
                  loading={resultLoading}
                  streaming={streaming}
                  title={t('tarot.interpretation', { master: selectedMaster.name })}
                />
              </div>
            )}
          </div>
        </div>
      </DivinationCardHeader>
    </>
  )
}
