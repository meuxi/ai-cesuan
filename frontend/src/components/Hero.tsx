import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

export default function Hero() {
    return (
        <section className="text-center pt-12 sm:pt-20 md:pt-24 mb-12 sm:mb-20 px-2">
            <h1 className="text-3xl sm:text-5xl md:text-6xl font-bold mb-3 sm:mb-4 text-foreground">
                AI 智能占卜
            </h1>
            <p className="text-base sm:text-xl text-muted-foreground mb-6 sm:mb-10 max-w-2xl mx-auto px-2">
                融合传统智慧与人工智能，探索命运的奥秘
            </p>

            {/* CTA按钮组 */}
            <div className="flex flex-col sm:flex-row justify-center gap-3 sm:gap-8 items-center">
                <Link
                    to="/divination/tarot"
                    className="w-full max-w-[220px] sm:w-44 inline-flex items-center justify-center text-sm font-semibold leading-6 px-6 py-3 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                >
                    塔罗牌占卜
                    <ArrowRight className="ml-1.5 h-3.5 w-3.5 sm:h-5 sm:w-5" />
                </Link>

                <div className="hidden sm:block h-12 w-px bg-border"></div>

                <Link
                    to="/divination/birthday"
                    className="w-full max-w-[220px] sm:w-44 inline-flex items-center justify-center text-sm font-semibold leading-6 px-6 py-3 border border-input text-foreground rounded-md hover:bg-accent transition-colors"
                >
                    生辰八字
                    <ArrowRight className="ml-1.5 h-3.5 w-3.5 sm:h-5 sm:w-5" />
                </Link>
            </div>
        </section>
    )
}
