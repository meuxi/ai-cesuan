export default function CloudPattern({
    className = "",
    opacity = 0.1
}: {
    className?: string
    opacity?: number
}) {
    return (
        <svg
            className={className}
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            style={{ opacity }}
        >
            {/* 祥云纹样 */}
            <path
                d="M10,50 Q20,40 30,50 T50,50 T70,50 T90,50"
                stroke="currentColor"
                strokeWidth="1"
                strokeLinecap="round"
            />
            <path
                d="M10,60 Q25,45 40,60 T70,60 T100,60"
                stroke="currentColor"
                strokeWidth="1"
                strokeLinecap="round"
            />
            <path
                d="M20,70 Q35,55 50,70 T80,70"
                stroke="currentColor"
                strokeWidth="1"
                strokeLinecap="round"
            />
            {/* 云朵主体 */}
            <ellipse cx="50" cy="55" rx="25" ry="12" stroke="currentColor" strokeWidth="0.5" fill="none" />
            <ellipse cx="35" cy="50" rx="15" ry="8" stroke="currentColor" strokeWidth="0.5" fill="none" />
            <ellipse cx="65" cy="50" rx="15" ry="8" stroke="currentColor" strokeWidth="0.5" fill="none" />
        </svg>
    )
}
