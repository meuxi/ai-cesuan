import { useNavigate } from 'react-router-dom'
import { DIVINATION_OPTIONS } from '@/config/constants'
import { ArrowRight, BookOpen } from 'lucide-react'
import Hero from '@/components/Hero'

export default function MarketPage() {
  const navigate = useNavigate()

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <Hero />

      {/* Quote Section */}
      <div className="text-center py-16 my-16 bg-secondary rounded-2xl">
        <div className="max-w-2xl mx-auto px-4">
          <blockquote className="text-2xl md:text-3xl text-foreground italic font-serif">
            "除非你意识到你的潜意识，否则潜意识将主导你的人生，而你将其称为命运。"
          </blockquote>
          <cite className="block text-base text-muted-foreground mt-6 not-italic">
            — 卡尔·荣格
          </cite>
        </div>
      </div>

      {/* Section Divider */}
      <div className="flex items-center mb-8">
        <div className="flex-1 h-px bg-border"></div>
        <h2 className="text-xl font-semibold mx-4 text-foreground">选择占卜方式</h2>
        <div className="flex-1 h-px bg-border"></div>
      </div>

      {/* Divination Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {DIVINATION_OPTIONS.map((option) => {
          const Icon = option.icon
          return (
            <div
              key={option.key}
              className="group"
            >
              <div
                className="rounded-xl h-full border border-border hover:border-foreground transition-all bg-card hover:shadow-md cursor-pointer shadow"
                onClick={() => navigate(`/divination/${option.key}`)}
              >
                <div className="flex flex-col space-y-1.5 p-6">
                  <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center mb-3">
                    <Icon className="w-5 h-5 text-muted-foreground" />
                  </div>
                  <h4 className="font-semibold tracking-tight text-lg group-hover:text-foreground transition-colors text-foreground">
                    {option.label}
                  </h4>
                </div>
                <div className="p-6 pt-0 pb-4">
                  <p className="text-muted-foreground text-sm">
                    {option.description}
                  </p>
                </div>
                <div className="flex items-center p-6 pt-0">
                  <span className="flex items-center text-sm text-muted-foreground group-hover:text-foreground transition-colors">
                    进入分析
                    <ArrowRight className="ml-1 h-4 w-4 transform group-hover:translate-x-1 transition-transform" />
                  </span>
                </div>
              </div>
            </div>
          )
        })}

        {/* About Card */}
        <div className="group">
          <div
            className="rounded-xl h-full border border-border hover:border-foreground transition-all bg-card hover:shadow-md cursor-pointer shadow"
            onClick={() => navigate('/about')}
          >
            <div className="flex flex-col space-y-1.5 p-6">
              <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center mb-3">
                <BookOpen className="w-5 h-5 text-muted-foreground" />
              </div>
              <h4 className="font-semibold tracking-tight text-lg group-hover:text-foreground transition-colors text-foreground">
                关于占卜
              </h4>
            </div>
            <div className="p-6 pt-0 pb-4">
              <p className="text-muted-foreground text-sm">
                了解各种占卜方式的起源与含义
              </p>
            </div>
            <div className="flex items-center p-6 pt-0">
              <span className="flex items-center text-sm text-muted-foreground group-hover:text-foreground transition-colors">
                查看详情
                <ArrowRight className="ml-1 h-4 w-4 transform group-hover:translate-x-1 transition-transform" />
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
