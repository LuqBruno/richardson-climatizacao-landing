import { useEffect, useRef, useState } from 'react'
import { navigation } from '../content/site'
import { ContactButton } from './ContactButton'
import { Close, Menu } from './icons'
import { Logo } from './Logo'

export function Header() {
  const [open, setOpen] = useState(false)
  const trigger = useRef<HTMLButtonElement>(null)
  useEffect(() => {
    if (!open) return
    const close = (event: KeyboardEvent) => { if (event.key === 'Escape') { setOpen(false); trigger.current?.focus() } }
    document.addEventListener('keydown', close)
    return () => document.removeEventListener('keydown', close)
  }, [open])
  useEffect(() => {
    const media = matchMedia('(min-width: 900px)')
    const reset = () => { if (media.matches) setOpen(false) }
    media.addEventListener('change', reset)
    return () => media.removeEventListener('change', reset)
  }, [])
  return <header className="site-header" data-open={open || undefined}>
    <div className="container header-inner">
      <a className="brand" href="#inicio" aria-label="Richardson Climatização, ir para o início"><Logo /></a>
      <nav className="desktop-nav" aria-label="Navegação principal">{navigation.map(item => <a key={item.href} href={item.href}>{item.label}</a>)}</nav>
      <ContactButton className="header-cta" />
      <button ref={trigger} type="button" className="menu-toggle" aria-expanded={open} aria-controls="mobile-nav" onClick={() => setOpen(!open)}>
        {open ? <Close /> : <Menu />}<span className="visually-hidden">{open ? 'Fechar menu' : 'Abrir menu'}</span>
      </button>
    </div>
    <div id="mobile-nav" className="mobile-nav" inert={!open}>
      <nav className="container" aria-label="Navegação móvel">
        {navigation.map(item => <a key={item.href} href={item.href} onClick={() => setOpen(false)}>{item.label}</a>)}
        <ContactButton className="mobile-cta">Pedir orçamento pelo WhatsApp</ContactButton>
      </nav>
    </div>
  </header>
}
