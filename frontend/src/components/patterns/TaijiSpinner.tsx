import { Sparkles } from 'lucide-react'

interface TaijiSpinnerProps {
    size?: 'sm' | 'md' | 'lg'
    className?: string
}

export default function TaijiSpinner({ size = 'md', className = '' }: TaijiSpinnerProps) {
    const sizeMap = {
        sm: 'w-12 h-12',
        md: 'w-16 h-16',
        lg: 'w-24 h-24'
    }

    const sparkleSize = {
        sm: 'h-4 w-4',
        md: 'h-6 w-6',
        lg: 'h-8 w-8'
    }

    return (
        <div className={`relative ${className}`}>
            <div className="animate-spin" style={{ animationDuration: '3s' }}>
                <svg
                    className={`${sizeMap[size]} text-primary/40`}
                    viewBox="0 0 100 100"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    {/* 外圆 */}
                    <circle cx="50" cy="50" r="48" stroke="currentColor" strokeWidth="2" />

                    {/* 阴阳鱼 - 阳（白） */}
                    <path
                        d="M50,2 A48,48 0 0,1 50,98 A24,24 0 0,1 50,50 A24,24 0 0,0 50,2"
                        fill="currentColor"
                        opacity="0.15"
                    />

                    {/* 阴阳鱼 - 阴（黑） */}
                    <path
                        d="M50,98 A48,48 0 0,1 50,2 A24,24 0 0,0 50,50 A24,24 0 0,1 50,98"
                        fill="currentColor"
                        opacity="0.35"
                    />

                    {/* 阳眼 */}
                    <circle cx="50" cy="26" r="6" fill="currentColor" opacity="0.35" />

                    {/* 阴眼 */}
                    <circle cx="50" cy="74" r="6" fill="currentColor" opacity="0.15" />
                </svg>
            </div>

            {/* 中心闪烁点 */}
            <div className="absolute inset-0 flex items-center justify-center">
                <Sparkles className={`${sparkleSize[size]} text-primary animate-pulse`} />
            </div>
        </div>
    )
}
