import { useEffect } from 'react'

/**
 * Revela elementos [data-reveal] uma vez, ao entrarem na tela.
 * Só esconde algo depois que o observador existe (classe .reveal-ready no <html>);
 * com movimento reduzido, nada é escondido.
 */
export function useReveal() {
  useEffect(() => {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return
    const root = document.documentElement
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue
        entry.target.classList.add('is-revealed')
        observer.unobserve(entry.target)
      }
    }, { rootMargin: '0px 0px -8% 0px', threshold: .12 })
    const items = document.querySelectorAll('[data-reveal]')
    items.forEach(item => {
      // atraso curto entre irmãos para uma entrada coordenada
      const siblings = item.parentElement ? [...item.parentElement.children].filter(child => child.hasAttribute('data-reveal')) : []
      ;(item as HTMLElement).style.setProperty('--reveal-delay', `${Math.min(siblings.indexOf(item), 4) * 70}ms`)
      observer.observe(item)
    })
    root.classList.add('reveal-ready')
    return () => { observer.disconnect(); root.classList.remove('reveal-ready') }
  }, [])
}
