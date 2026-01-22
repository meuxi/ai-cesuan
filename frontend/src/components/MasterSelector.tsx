/**
 * 虚拟大师选择器组件
 * 支持选择不同风格的AI大师进行占卜解读
 */

import { useState } from 'react'
import { MASTERS, type Master } from '@/config/masters'
import { ChevronDown, Check } from 'lucide-react'

interface MasterSelectorProps {
    selectedMaster: Master
    onSelectMaster: (master: Master) => void
    compact?: boolean
}

export function MasterSelector({ selectedMaster, onSelectMaster, compact = false }: MasterSelectorProps) {
    const [isOpen, setIsOpen] = useState(false)

    const Icon = selectedMaster.icon

    if (compact) {
        return (
            <div className="relative">
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="flex items-center gap-2 px-3 py-2 rounded-md bg-secondary border border-input hover:border-muted-foreground transition-colors"
                >
                    <Icon className="w-4 h-4 text-muted-foreground" />
                    <span className="text-sm font-medium text-foreground">
                        {selectedMaster.name}
                    </span>
                    <ChevronDown className={`w-4 h-4 text-muted-foreground transition-transform ${isOpen ? 'rotate-180' : ''}`} />
                </button>

                {isOpen && (
                    <>
                        <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)} />
                        <div className="absolute top-full left-0 mt-1 w-64 bg-popover rounded-lg shadow-lg border border-border z-50 overflow-hidden">
                            <div className="max-h-80 overflow-y-auto">
                                {MASTERS.map((master) => {
                                    const MasterIcon = master.icon
                                    const isSelected = master.id === selectedMaster.id
                                    return (
                                        <button
                                            key={master.id}
                                            onClick={() => {
                                                onSelectMaster(master)
                                                setIsOpen(false)
                                            }}
                                            className={`w-full flex items-center gap-3 px-4 py-3 hover:bg-accent transition-colors ${isSelected ? 'bg-accent' : ''
                                                }`}
                                        >
                                            <MasterIcon className={`w-5 h-5 ${isSelected ? 'text-foreground' : 'text-muted-foreground'}`} />
                                            <div className="flex-1 text-left">
                                                <div className={`text-sm font-medium ${isSelected ? 'text-foreground' : 'text-muted-foreground'}`}>
                                                    {master.name}
                                                    <span className="ml-2 text-xs text-muted-foreground">{master.dynasty}</span>
                                                </div>
                                            </div>
                                            {isSelected && <Check className="w-4 h-4 text-foreground" />}
                                        </button>
                                    )
                                })}
                            </div>
                        </div>
                    </>
                )}
            </div>
        )
    }

    return (
        <div className="space-y-3">
            <div className="flex items-center justify-between">
                <h3 className="text-sm font-medium text-foreground">选择解读大师</h3>
                <span className="text-xs text-muted-foreground">
                    {MASTERS.length} 位大师可选
                </span>
            </div>

            <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-2">
                {MASTERS.map((master) => {
                    const MasterIcon = master.icon
                    const isSelected = master.id === selectedMaster.id
                    return (
                        <button
                            key={master.id}
                            onClick={() => onSelectMaster(master)}
                            className={`flex flex-col items-center gap-1 p-3 rounded-lg transition-all ${isSelected
                                ? 'bg-primary text-primary-foreground'
                                : 'bg-secondary border border-input hover:border-muted-foreground'
                                }`}
                            title={master.description}
                        >
                            <MasterIcon className={`w-5 h-5 ${isSelected ? 'text-primary-foreground' : 'text-muted-foreground'}`} />
                            <span className={`text-xs font-medium ${isSelected ? 'text-primary-foreground' : 'text-muted-foreground'}`}>
                                {master.name}
                            </span>
                            <span className={`text-[10px] ${isSelected ? 'text-primary-foreground/70' : 'text-muted-foreground/70'}`}>
                                {master.dynasty}
                            </span>
                        </button>
                    )
                })}
            </div>

            {/* 当前选中大师的描述 */}
            <div className="p-4 bg-secondary rounded-lg border border-border">
                <div className="flex items-start gap-3">
                    <Icon className="w-6 h-6 text-muted-foreground flex-shrink-0" />
                    <div>
                        <div className="font-medium text-foreground">
                            {selectedMaster.name}
                            <span className="ml-2 text-xs font-normal text-muted-foreground">
                                {selectedMaster.dynasty}
                            </span>
                        </div>
                        <p className="text-sm text-muted-foreground mt-1">
                            {selectedMaster.description}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default MasterSelector
