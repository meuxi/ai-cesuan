/**
 * AI大师头像组件
 * 显示虚拟大师的头像（支持图片/Emoji/图标）
 */

import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'
import type { Master } from '@/config/masters'

interface MasterAvatarProps {
    master: Master
    size?: 'sm' | 'md' | 'lg' | 'xl'
    className?: string
    showName?: boolean
    showDynasty?: boolean
    animated?: boolean
}

const sizeClasses = {
    sm: 'w-8 h-8 text-lg',
    md: 'w-12 h-12 text-2xl',
    lg: 'w-16 h-16 text-3xl',
    xl: 'w-24 h-24 text-5xl',
}

const nameSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
    xl: 'text-lg',
}

export function MasterAvatar({
    master,
    size = 'md',
    className,
    showName = false,
    showDynasty = false,
    animated = true,
}: MasterAvatarProps) {
    const Icon = master.icon

    const avatarContent = (
        <div
            className={cn(
                'rounded-full flex items-center justify-center bg-gradient-to-br from-primary/20 to-primary/40 border-2 border-primary/30',
                sizeClasses[size],
                className
            )}
        >
            {master.avatar ? (
                // 优先显示自定义头像图片
                <img
                    src={master.avatar}
                    alt={master.name}
                    className="w-full h-full rounded-full object-cover"
                />
            ) : master.avatarEmoji ? (
                // 其次显示Emoji头像
                <span className="select-none">{master.avatarEmoji}</span>
            ) : (
                // 最后使用图标
                <Icon className="w-1/2 h-1/2 text-primary" />
            )}
        </div>
    )

    return (
        <div className="flex flex-col items-center gap-1">
            {animated ? (
                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    whileHover={{ scale: 1.05 }}
                    transition={{ duration: 0.2 }}
                >
                    {avatarContent}
                </motion.div>
            ) : (
                avatarContent
            )}
            
            {(showName || showDynasty) && (
                <div className="text-center">
                    {showName && (
                        <div className={cn('font-medium text-foreground', nameSizeClasses[size])}>
                            {master.name}
                        </div>
                    )}
                    {showDynasty && (
                        <div className={cn('text-muted-foreground', size === 'sm' ? 'text-[10px]' : 'text-xs')}>
                            {master.dynasty}
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

/**
 * 大师头像列表组件
 * 用于显示一组大师头像
 */
interface MasterAvatarListProps {
    masters: Master[]
    selectedMaster?: Master
    onSelectMaster?: (master: Master) => void
    size?: 'sm' | 'md' | 'lg'
    showNames?: boolean
}

export function MasterAvatarList({
    masters,
    selectedMaster,
    onSelectMaster,
    size = 'md',
    showNames = false,
}: MasterAvatarListProps) {
    return (
        <div className="flex flex-wrap gap-3 justify-center">
            {masters.map((master) => (
                <motion.button
                    key={master.id}
                    onClick={() => onSelectMaster?.(master)}
                    className={cn(
                        'p-1 rounded-xl transition-colors',
                        selectedMaster?.id === master.id
                            ? 'bg-primary/20 ring-2 ring-primary'
                            : 'hover:bg-secondary'
                    )}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                >
                    <MasterAvatar
                        master={master}
                        size={size}
                        showName={showNames}
                        showDynasty={showNames}
                        animated={false}
                    />
                </motion.button>
            ))}
        </div>
    )
}

/**
 * AI解读头部组件
 * 显示正在解读的大师信息
 */
interface MasterInterpretHeaderProps {
    master: Master
    loading?: boolean
    title?: string
}

export function MasterInterpretHeader({
    master,
    loading = false,
    title,
}: MasterInterpretHeaderProps) {
    return (
        <div className="flex items-center gap-3 p-4 bg-secondary/50 rounded-lg border border-border">
            <MasterAvatar master={master} size="lg" animated={false} />
            
            <div className="flex-1">
                <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-foreground">{master.name}</h3>
                    <span className="text-xs text-muted-foreground px-2 py-0.5 bg-background rounded">
                        {master.dynasty}
                    </span>
                </div>
                <p className="text-sm text-muted-foreground mt-1 line-clamp-1">
                    {master.description}
                </p>
                {loading && (
                    <div className="flex items-center gap-2 mt-2">
                        <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '0ms' }} />
                        <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '150ms' }} />
                        <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '300ms' }} />
                        <span className="text-xs text-muted-foreground ml-2">
                            {title || `${master.name}正在解读...`}
                        </span>
                    </div>
                )}
            </div>
        </div>
    )
}

export default MasterAvatar
