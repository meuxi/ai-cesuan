import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { useGlobalState } from '@/store'
import { Save, Settings as SettingsIcon, ExternalLink, CheckCircle2, ArrowLeft } from 'lucide-react'

export default function SettingsPage() {
  const navigate = useNavigate()
  const { customOpenAISettings, setCustomOpenAISettings, settings } = useGlobalState()

  const [tempSettings, setTempSettings] = useState({
    enable: false,
    baseUrl: '',
    apiKey: '',
    model: '',
  })

  const [loading, setLoading] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    setTempSettings({
      enable: customOpenAISettings.enable,
      baseUrl: customOpenAISettings.baseUrl || settings.default_api_base || '',
      apiKey: customOpenAISettings.apiKey || '',
      model: customOpenAISettings.model || settings.default_model || '',
    })
  }, [customOpenAISettings, settings])

  const goToPurchase = () => {
    if (settings.purchase_url) {
      window.open(settings.purchase_url, '_blank')
    }
  }

  const saveSettings = async () => {
    setLoading(true)
    setSaved(false)
    try {
      setCustomOpenAISettings(tempSettings)
      setSaved(true)
      setTimeout(() => setSaved(false), 3000)
    } finally {
      setLoading(false)
    }
  }

  const hasPurchaseUrl = settings.purchase_url && settings.purchase_url !== ''

  return (
    <div className="space-y-6">
      {/* 返回按钮 */}
      <button
        onClick={() => navigate('/')}
        className="flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        返回
      </button>

      {/* 标题区域 */}
      <div className="text-center py-6">
        <div className="flex items-center justify-center gap-3 mb-3">
          <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center">
            <SettingsIcon className="w-5 h-5 text-muted-foreground" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-foreground">
            API 设置
          </h1>
        </div>
        <p className="text-muted-foreground">
          自定义您的 OpenAI API 配置
        </p>
      </div>

      {/* 内容卡片 */}
      <div className="rounded-xl border border-border bg-card p-6 md:p-8">
        <div className="max-w-xl mx-auto space-y-6">
          {/* 保存按钮 */}
          <div className="flex justify-end">
            <button
              onClick={saveSettings}
              disabled={loading}
              className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50"
            >
              {saved ? (
                <>
                  <CheckCircle2 className="h-4 w-4" />
                  已保存
                </>
              ) : loading ? (
                '保存中...'
              ) : (
                <>
                  <Save className="h-4 w-4" />
                  保存设置
                </>
              )}
            </button>
          </div>

          {/* 保存成功提示 */}
          {saved && (
            <div className="flex items-center gap-2 p-3 text-sm text-green-700 dark:text-green-400 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <CheckCircle2 className="h-4 w-4" />
              设置已成功保存
            </div>
          )}

          {/* 表单 */}
          <div className="space-y-5">
            {/* 启用开关 */}
            <div className="flex items-center justify-between p-4 rounded-lg border border-border bg-secondary">
              <div className="space-y-0.5">
                <Label htmlFor="enable-custom" className="text-sm font-medium text-foreground">
                  启用自定义 API
                </Label>
                <p className="text-xs text-muted-foreground">使用您自己的 API 配置</p>
              </div>
              <Switch
                id="enable-custom"
                checked={tempSettings.enable}
                onCheckedChange={(checked) =>
                  setTempSettings({ ...tempSettings, enable: checked })
                }
              />
            </div>

            {/* API 地址 */}
            <div className="space-y-2">
              <Label htmlFor="base-url" className="text-sm font-medium text-foreground">
                API 地址
              </Label>
              <input
                id="base-url"
                value={tempSettings.baseUrl}
                onChange={(e) =>
                  setTempSettings({ ...tempSettings, baseUrl: e.target.value })
                }
                placeholder="https://api.openai.com"
                className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
              />
            </div>

            {/* API 密钥 */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="api-key" className="text-sm font-medium text-foreground">
                  API 密钥
                </Label>
                {hasPurchaseUrl && (
                  <button
                    onClick={goToPurchase}
                    className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    获取 API KEY
                    <ExternalLink className="h-3 w-3" />
                  </button>
                )}
              </div>
              <input
                id="api-key"
                type="password"
                value={tempSettings.apiKey}
                onChange={(e) =>
                  setTempSettings({ ...tempSettings, apiKey: e.target.value })
                }
                placeholder="sk-..."
                className="w-full px-3 py-2 text-sm font-mono border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
              />
            </div>

            {/* 模型 */}
            <div className="space-y-2">
              <Label htmlFor="model" className="text-sm font-medium text-foreground">
                模型
              </Label>
              <input
                id="model"
                value={tempSettings.model}
                onChange={(e) =>
                  setTempSettings({ ...tempSettings, model: e.target.value })
                }
                placeholder="gpt-4"
                className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
