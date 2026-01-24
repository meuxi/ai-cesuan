import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { Solar } from 'lunar-javascript'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { DivinationCardHeader } from '@/components/DivinationCardHeader'
import { InlineResult } from '@/components/InlineResult'
import { useDivination } from '@/hooks/useDivination'
import { useLocalStorage } from '@/hooks'
import { getDivinationOption } from '@/config/constants'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import { Sparkles } from 'lucide-react'
import { logger } from '@/utils/logger'

const CONFIG = getDivinationOption('new_name')!

export default function NewNamePage() {
  const { t } = useTranslation()
  const [birthday, setBirthday] = useLocalStorage('birthday', '2000-08-17T00:00')
  const [sex, setSex] = useState('')
  const [surname, setSurname] = useState('')
  const [newNamePrompt, setNewNamePrompt] = useState('')
  const [lunarBirthday, setLunarBirthday] = useState('')
  const { result, loading, resultLoading, streaming, showDrawer, setShowDrawer, onSubmit } =
    useDivination('new_name')

  const computeLunarBirthday = (birthdayStr: string) => {
    try {
      const date = new Date(birthdayStr)
      const solar = Solar.fromYmdHms(
        date.getFullYear(),
        date.getMonth() + 1,
        date.getDate(),
        date.getHours(),
        date.getMinutes(),
        date.getSeconds()
      )
      setLunarBirthday(solar.getLunar().toFullString())
    } catch (error) {
      logger.error('农历转换失败:', error)
      setLunarBirthday('转换失败')
    }
  }

  useEffect(() => {
    computeLunarBirthday(birthday)
  }, [birthday])

  const handleSubmit = () => {
    // 验证必填字段
    if (!surname || !sex) {
      toast.error('请填写姓氏和性别')
      return
    }

    // 将日期格式从 ISO 格式转换为后端期望的格式
    const date = new Date(birthday)
    const formattedBirthday = date.getFullYear() + '-' +
      String(date.getMonth() + 1).padStart(2, '0') + '-' +
      String(date.getDate()).padStart(2, '0') + ' ' +
      String(date.getHours()).padStart(2, '0') + ':' +
      String(date.getMinutes()).padStart(2, '0') + ':' +
      String(date.getSeconds()).padStart(2, '0')

    onSubmit({
      prompt: `${surname} ${sex} ${formattedBirthday}`,
      birthday: formattedBirthday,  // 添加顶层 birthday 字段
      new_name: {
        surname,
        sex,
        birthday: formattedBirthday,
        new_name_prompt: newNamePrompt,
      },
    })
  }

  return (
    <DivinationCardHeader
      title={CONFIG.title}
      description={CONFIG.description}
      icon={CONFIG.icon}
      divinationType="new_name"
    >
      <div className="max-w-2xl mx-auto w-full">
        <div className="space-y-5">
          <div>
            <Label className="text-sm font-medium text-foreground">{t('newName.surnameLabel')}</Label>
            <input
              value={surname}
              onChange={(e) => setSurname(e.target.value)}
              placeholder={t('newName.surnamePlaceholder')}
              maxLength={2}
              className="w-full px-3 py-2 mt-2 text-sm border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            />
          </div>
          <div>
            <Label className="text-sm font-medium text-foreground">{t('newName.genderLabel')}</Label>
            <Select value={sex} onValueChange={setSex}>
              <SelectTrigger className="mt-2 border-input">
                <SelectValue placeholder={t('newName.genderPlaceholder')} />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="男">男</SelectItem>
                <SelectItem value="女">女</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label className="block mb-2 text-sm font-medium text-foreground">生日</Label>
            <input
              type="datetime-local"
              value={birthday}
              onChange={(e) => setBirthday(e.target.value)}
              className="px-3 py-2 text-sm border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            />
          </div>
          <div>
            <Label className="text-sm font-medium text-foreground">附加要求</Label>
            <input
              value={newNamePrompt}
              onChange={(e) => setNewNamePrompt(e.target.value)}
              maxLength={20}
              placeholder="例如：希望名字带水"
              className="w-full px-3 py-2 mt-2 text-sm border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            />
          </div>
          <p className="text-sm text-muted-foreground">农历: {lunarBirthday}</p>
        </div>

        {!result && !loading && (
          <div className="mt-6">
            <Button
              onClick={handleSubmit}
              disabled={!surname || !sex || loading}
              className="w-full h-12"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              AI 智能起名
            </Button>
          </div>
        )}

        <InlineResult
          result={result}
          loading={resultLoading}
          streaming={streaming}
          title={CONFIG.title}
        />
      </div>
    </DivinationCardHeader>
  )
}
