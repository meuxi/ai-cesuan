import { useEffect, useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/sonner'
import { SpeedInsights } from '@vercel/speed-insights/react'
import { useGlobalState } from '@/store'
import MarketPage from '@/pages/Market'
import DivinationHub from '@/pages/DivinationHub'
import ChouqianPage from '@/pages/Chouqian'
import AboutPage from '@/pages/About'
import SettingsPage from '@/pages/Settings'
import LoginPage from '@/pages/Login'
import HistoryPage from '@/pages/History'
import TarotPage from '@/pages/divination/TarotPage'
import BirthdayPage from '@/pages/divination/BirthdayPage'
import NewNamePage from '@/pages/divination/NewNamePage'
import NamePage from '@/pages/divination/NamePage'
import DreamPage from '@/pages/divination/DreamPage'
import PlumFlowerPage from '@/pages/divination/PlumFlowerPage'
import FatePage from '@/pages/divination/FatePage'
import XiaoLiuRenPage from '@/pages/divination/XiaoLiuRenPage'
import LiuYaoPage from '@/features/liuyao'
import LaohuangliPage from '@/pages/divination/LaohuangliPage'
import QimenPage from '@/pages/divination/QimenPage'
import DaliurenPage from '@/pages/divination/DaliurenPage'
import JiriSelectPage from '@/pages/divination/JiriSelectPage'
import JiriDetailPage from '@/pages/divination/JiriDetailPage'
import DailyFortunePage from '@/pages/divination/DailyFortunePage'
import MonthlyFortunePage from '@/pages/divination/MonthlyFortunePage'
import ZodiacPage from '@/pages/divination/ZodiacPage'
import LifeKLinePage from '@/features/life-kline/LifeKLinePage'
import ZiweiPage from '@/pages/divination/ZiweiPage'
import HehunPage from '@/pages/divination/HehunPage'
import ZhugePage from '@/pages/divination/ZhugePage'
import TermsPage from '@/pages/Terms'
import PrivacyPage from '@/pages/Privacy'
import DisclaimerPage from '@/pages/Disclaimer'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Sparkles } from 'lucide-react'
import MainLayout from '@/layouts/MainLayout'
import ErrorBoundary from '@/components/ErrorBoundary'
import OfflineIndicator from '@/components/OfflineIndicator'
import { logger } from '@/utils/logger'

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
        ) : settings.error ? (
          <Alert variant="destructive" className="glass">
            <AlertDescription>{settings.error}</AlertDescription>
          </Alert>
        ) : null}
      </MainLayout>
      <Toaster />
      <SpeedInsights />
    </ErrorBoundary>
  )
}

export default App
