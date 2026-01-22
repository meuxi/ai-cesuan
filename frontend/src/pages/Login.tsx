import { useState, useEffect } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useGlobalState } from '@/store'
import { Github, LogIn, ArrowLeft } from 'lucide-react'
import { logger } from '@/utils/logger'

const API_BASE = import.meta.env.VITE_API_BASE || ''

export default function LoginPage() {
  const { login_type } = useParams()
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { setJwt } = useGlobalState()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (login_type === 'github') {
      const code = searchParams.get('code')
      if (code) {
        handleGithubCallback(code)
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [login_type, searchParams])

  const handleGithubCallback = async (code: string) => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/api/v1/oauth`, {
        method: 'POST',
        body: JSON.stringify({
          login_type: 'github',
          code: code,
        }),
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        const text = await response.text()
        throw new Error(`${response.status} ${text}`)
      }

      const token = await response.json()
      setJwt(token)
      window.location.href = '/'
    } catch (err: any) {
      logger.error(err)
      setError(`登录失败: ${err.message || '未知错误'}`)
    } finally {
      setLoading(false)
    }
  }

  const onGithubLogin = async () => {
    try {
      setLoading(true)
      setError('')
      const response = await fetch(
        `${API_BASE}/api/v1/login?login_type=github&redirect_url=${window.location.origin}/login/github`,
        {
          method: 'GET',
        }
      )

      if (!response.ok) {
        const text = await response.text()
        throw new Error(`${response.status} ${text}`)
      }

      const redirectUrl = await response.json()
      window.location.href = redirectUrl
    } catch (err: any) {
      logger.error(err)
      setError(err.message || '登录失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex justify-center items-center min-h-[60vh] px-4">
      <div className="w-full max-w-md">
        {/* 返回按钮 */}
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors mb-8"
        >
          <ArrowLeft className="h-4 w-4" />
          返回
        </button>

        {/* 登录卡片 */}
        <div className="rounded-xl border border-border bg-card overflow-hidden">
          <div className="text-center p-6 border-b border-border">
            <div className="flex justify-center mb-4">
              <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center">
                <LogIn className="w-6 h-6 text-muted-foreground" />
              </div>
            </div>
            <h1 className="text-2xl font-bold text-foreground mb-2">登录账户</h1>
            <p className="text-sm text-muted-foreground">使用 GitHub 账户快速登录</p>
          </div>

          <div className="space-y-4 p-6">
            {loading && (
              <div className="flex flex-col items-center justify-center py-12 space-y-4">
                <div className="relative">
                  <div className="animate-spin rounded-full h-12 w-12 border-2 border-muted border-t-foreground"></div>
                  <Github className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                </div>
                <p className="text-sm text-muted-foreground">正在登录...</p>
              </div>
            )}

            {error && (
              <div className="p-3 text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 rounded-lg">
                {error}
              </div>
            )}

            {!loading && (
              <>
                <button
                  onClick={onGithubLogin}
                  disabled={loading}
                  className="w-full inline-flex items-center justify-center gap-2 px-4 py-3 text-sm font-semibold bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                >
                  <Github className="h-5 w-5" />
                  使用 GitHub 登录
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
