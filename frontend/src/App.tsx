import { useEffect, useState, lazy, Suspense } from 'react'
import { Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/sonner'
import { Analytics } from '@vercel/analytics/react'
import { useGlobalState } from '@/store'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Sparkles } from 'lucide-react'
import MainLayout from '@/layouts/MainLayout'
import ErrorBoundary from '@/components/ErrorBoundary'
import OfflineIndicator from '@/components/OfflineIndicator'
import { logger } from '@/utils/logger'

// 懒加载页面组件 - 优化首屏加载速度
const MarketPage = lazy(() => import('@/pages/Market'))
const DivinationHub = lazy(() => import('@/pages/DivinationHub'))
const ChouqianPage = lazy(() => import('@/pages/Chouqian'))
const AboutPage = lazy(() => import('@/pages/About'))
const SettingsPage = lazy(() => import('@/pages/Settings'))
const LoginPage = lazy(() => import('@/pages/Login'))
const HistoryPage = lazy(() => import('@/pages/History'))

// 占卜页面
const TarotPage = lazy(() => import('@/pages/divination/TarotPage'))
const BirthdayPage = lazy(() => import('@/pages/divination/BirthdayPage'))
const NewNamePage = lazy(() => import('@/pages/divination/NewNamePage'))
const NamePage = lazy(() => import('@/pages/divination/NamePage'))
const DreamPage = lazy(() => import('@/pages/divination/DreamPage'))
const PlumFlowerPage = lazy(() => import('@/pages/divination/PlumFlowerPage'))
const FatePage = lazy(() => import('@/pages/divination/FatePage'))
const XiaoLiuRenPage = lazy(() => import('@/pages/divination/XiaoLiuRenPage'))
const LiuYaoPage = lazy(() => import('@/features/liuyao'))
const LaohuangliPage = lazy(() => import('@/pages/divination/LaohuangliPage'))
const QimenPage = lazy(() => import('@/pages/divination/QimenPage'))
const DaliurenPage = lazy(() => import('@/pages/divination/DaliurenPage'))
const JiriSelectPage = lazy(() => import('@/pages/divination/JiriSelectPage'))
const JiriDetailPage = lazy(() => import('@/pages/divination/JiriDetailPage'))
const DailyFortunePage = lazy(() => import('@/pages/divination/DailyFortunePage'))
const MonthlyFortunePage = lazy(() => import('@/pages/divination/MonthlyFortunePage'))
const ZodiacPage = lazy(() => import('@/pages/divination/ZodiacPage'))
const LifeKLinePage = lazy(() => import('@/features/life-kline/LifeKLinePage'))
const ZiweiPage = lazy(() => import('@/pages/divination/ZiweiPage'))
const HehunPage = lazy(() => import('@/pages/divination/HehunPage'))
const ZhugePage = lazy(() => import('@/pages/divination/ZhugePage'))

// 静态页面
const TermsPage = lazy(() => import('@/pages/Terms'))
const PrivacyPage = lazy(() => import('@/pages/Privacy'))
const DisclaimerPage = lazy(() => import('@/pages/Disclaimer'))

// 页面加载骨架
function PageLoader() {
  return (
    <div className="flex items-center justify-center min-h-[50vh]">
      <div className="text-center space-y-4">
        <div className="animate-spin rounded-full h-10 w-10 border-2 border-primary/20 border-t-primary mx-auto"></div>
        <p className="text-sm text-muted-foreground">加载中...</p>
      </div>
    </div>
  )
}

const API_BASE = import.meta.env.VITE_API_BASE || ''

function App() {
  const {
    jwt,
    setSettings,
    settings
  } = useGlobalState()

  const [loading, setLoading] = useState(false)

  const fetchSettings = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/api/v1/settings`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${jwt || 'xxx'}`,
          'Content-Type': 'application/json',
        },
      })
      if (response.ok) {
        const data = await response.json()
        setSettings({ ...data, fetched: true, error: null })
      } else {
        setSettings({
          fetched: true,
          error: `Failed to fetch settings: ${response.status} ${response.statusText}`,
        })
      }
    } catch (error: unknown) {
      logger.error(error)
      const message = error instanceof Error ? error.message : '未知错误'
      setSettings({
        fetched: true,
        error: `Failed to fetch settings: ${message}`,
      })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSettings()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <ErrorBoundary>
      <OfflineIndicator />

      {loading && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-background/80 backdrop-blur-sm">
          <div className="text-center space-y-4">
            <div className="relative">
              <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary/20 border-t-primary mx-auto"></div>
              <Sparkles className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-6 w-6 text-primary animate-pulse" />
            </div>
            <p className="text-sm font-medium text-muted-foreground animate-pulse">
              星辰指引中...
            </p>
          </div>
        </div>
      )}

      <MainLayout>
        {settings.fetched && !settings.error ? (
          <Suspense fallback={<PageLoader />}>
            <Routes>
              <Route path="/" element={<MarketPage />} />
              <Route path="/divination" element={<DivinationHub />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/divination/tarot" element={<TarotPage />} />
              <Route path="/divination/xiaoliu" element={<XiaoLiuRenPage />} />
              <Route path="/divination/birthday" element={<BirthdayPage />} />
              <Route path="/divination/new_name" element={<NewNamePage />} />
              <Route path="/divination/name" element={<NamePage />} />
              <Route path="/divination/dream" element={<DreamPage />} />
              <Route path="/divination/plum_flower" element={<PlumFlowerPage />} />
              <Route path="/divination/fate" element={<FatePage />} />
              <Route path="/divination/liuyao" element={<LiuYaoPage />} />
              <Route path="/divination/chouqian" element={<ChouqianPage />} />
              <Route path="/divination/laohuangli" element={<LaohuangliPage />} />
              <Route path="/divination/laohuangli/select" element={<JiriSelectPage />} />
              <Route path="/divination/laohuangli/detail" element={<JiriDetailPage />} />
              <Route path="/divination/qimen" element={<QimenPage />} />
              <Route path="/divination/daliuren" element={<DaliurenPage />} />
              <Route path="/divination/daily" element={<DailyFortunePage />} />
              <Route path="/divination/monthly" element={<MonthlyFortunePage />} />
              <Route path="/divination/zodiac" element={<ZodiacPage />} />
              <Route path="/divination/life-kline" element={<LifeKLinePage />} />
              <Route path="/divination/ziwei" element={<ZiweiPage />} />
              <Route path="/divination/hehun" element={<HehunPage />} />
              <Route path="/divination/zhuge" element={<ZhugePage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/login/:login_type" element={<LoginPage />} />
              <Route path="/history/:type" element={<HistoryPage />} />
              <Route path="/terms" element={<TermsPage />} />
              <Route path="/privacy" element={<PrivacyPage />} />
              <Route path="/disclaimer" element={<DisclaimerPage />} />
            </Routes>
          </Suspense>
        ) : settings.error ? (
          <Alert variant="destructive" className="glass">
            <AlertDescription>{settings.error}</AlertDescription>
          </Alert>
        ) : null}
      </MainLayout>
      <Toaster />
      <Analytics />
    </ErrorBoundary>
  )
}

export default App
