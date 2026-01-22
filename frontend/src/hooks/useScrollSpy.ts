import { useState, useEffect } from 'react'

const OFFSET_TOP = 100

export const useScrollSpy = (sectionIds: string[]) => {
    const [activeSection, setActiveSection] = useState<string>('')

    useEffect(() => {
        const handleScroll = () => {
            const scrollPosition = window.scrollY + OFFSET_TOP

            for (let i = sectionIds.length - 1; i >= 0; i--) {
                const section = document.getElementById(sectionIds[i])
                if (section) {
                    const sectionTop = section.offsetTop
                    const sectionBottom = sectionTop + section.offsetHeight

                    if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                        setActiveSection(sectionIds[i])
                        break
                    }
                }
            }
        }

        handleScroll()
        window.addEventListener('scroll', handleScroll)
        return () => window.removeEventListener('scroll', handleScroll)
    }, [sectionIds])

    return activeSection
}
