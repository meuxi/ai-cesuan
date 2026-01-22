import { useCallback } from 'react'

const OFFSET_TOP = 80

export const useSmoothScroll = () => {
    const scrollToAnchor = useCallback((anchorId: string) => {
        const element = document.getElementById(anchorId)
        if (!element) return

        const targetPosition = element.getBoundingClientRect().top + window.scrollY - OFFSET_TOP

        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth',
        })
    }, [])

    const scrollToTop = useCallback(() => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth',
        })
    }, [])

    return { scrollToAnchor, scrollToTop }
}
