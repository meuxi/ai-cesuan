export default function BambooPattern({
    className = "",
    opacity = 0.05
}: {
    className?: string
    opacity?: number
}) {
    return (
        <svg
            className={className}
            viewBox="0 0 100 200"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            style={{ opacity }}
        >
            {/* 竹子主干 */}
            <rect x="45" y="10" width="10" height="180" fill="currentColor" fillOpacity="0.3" />
            <rect x="44" y="10" width="1" height="180" fill="currentColor" />
            <rect x="55" y="10" width="1" height="180" fill="currentColor" />

            {/* 竹节 */}
            <rect x="40" y="30" width="20" height="2" fill="currentColor" />
            <rect x="40" y="70" width="20" height="2" fill="currentColor" />
            <rect x="40" y="110" width="20" height="2" fill="currentColor" />
            <rect x="40" y="150" width="20" height="2" fill="currentColor" />

            {/* 竹叶 - 右侧 */}
            <path d="M55,40 Q70,35 75,45 Q65,42 55,45 Z" fill="currentColor" fillOpacity="0.6" />
            <path d="M55,42 Q72,30 80,38 Q68,36 55,44 Z" fill="currentColor" fillOpacity="0.5" />

            {/* 竹叶 - 左侧 */}
            <path d="M45,80 Q30,75 25,85 Q35,82 45,85 Z" fill="currentColor" fillOpacity="0.6" />
            <path d="M45,82 Q28,70 20,78 Q32,76 45,84 Z" fill="currentColor" fillOpacity="0.5" />

            {/* 竹叶 - 右侧 */}
            <path d="M55,120 Q70,115 75,125 Q65,122 55,125 Z" fill="currentColor" fillOpacity="0.6" />

            {/* 竹叶 - 左侧 */}
            <path d="M45,160 Q30,155 25,165 Q35,162 45,165 Z" fill="currentColor" fillOpacity="0.6" />
        </svg>
    )
}
