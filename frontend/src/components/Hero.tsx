import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

export default function Hero() {
    return (
        <section className="text-center pt-20 sm:pt-24 mb-20">
            <h1 className="text-5xl sm:text-6xl font-bold mb-4 text-foreground">
                AI 智能占卜
            </h1>
            <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
                融合传统智慧与人工智能，探索命运的奥秘
            </p>

            {/* CTA按钮组 */}
            <div className="flex flex-col sm:flex-row justify-center gap-4 sm:gap-8 items-center">
                <Link
                    to="/divination/tarot"
                    className="w-[220px] sm:w-44 inline-flex items-center justify-center text-sm font-semibold leading-6 px-6 py-3 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                >
                    塔罗牌占卜
                    <ArrowRight className="ml-1.5 h-3.5 w-3.5 sm:h-5 sm:w-5" />
                </Link>

                <div className="hidden sm:block h-12 w-px bg-border"></div>

                <Link
                    to="/divination/birthday"
                    className="w-[220px] sm:w-44 inline-flex items-center justify-center text-sm font-semibold leading-6 px-6 py-3 border border-input text-foreground rounded-md hover:bg-accent transition-colors"
                >
                    生辰八字
                    <ArrowRight className="ml-1.5 h-3.5 w-3.5 sm:h-5 sm:w-5" />
                </Link>
            </div>
        </section>
    )
}
