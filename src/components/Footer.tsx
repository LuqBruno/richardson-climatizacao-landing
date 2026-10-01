import { business, contactUrl, navigation } from '../content/site'
import { ArrowUp } from './icons'
import { Logo } from './Logo'

export function Footer() {
  return <footer className="site-footer">
    <div className="container footer-grid">
      <div className="footer-brand">
        <Logo />
        <p>{business.tagline} em {business.region}.</p>
      </div>
      <nav aria-label="Seções">
        <p className="footer-title">Navegar</p>
        <ul>{navigation.map(item => <li key={item.href}><a href={item.href}>{item.label}</a></li>)}</ul>
      </nav>
      <div>
        <p className="footer-title">Contato</p>
        <ul>
          <li><a href={contactUrl} target="_blank" rel="noopener noreferrer">WhatsApp {business.phoneDisplay}</a></li>
          <li><a href={business.instagram} target="_blank" rel="noopener noreferrer">{business.instagramHandle}</a></li>
          <li><a href={business.maps} target="_blank" rel="noopener noreferrer">{business.addressShort}</a></li>
        </ul>
      </div>
    </div>
    <div className="container footer-bottom">
      <p>© {new Date().getFullYear()} {business.name}</p>
      <a className="text-link" href="#inicio">Voltar ao início<ArrowUp className="text-link-icon" /></a>
    </div>
  </footer>
}
