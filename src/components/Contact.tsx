import { asset, business, contactUrl } from '../content/site'
import { ContactButton } from './ContactButton'
import { Clock, Instagram, Pin, WhatsApp } from './icons'

const set = (ext: string) => [480, 800].map(w => `${asset(`images/opt/fachada-${w}.${ext}`)} ${w}w`).join(', ')
const sizes = '(min-width: 1024px) 460px, 92vw'

export function Contact() {
  return <section id="contato" className="contact" aria-labelledby="contact-title">
    <div className="tiles tiles--ice" aria-hidden="true" />
    <div className="container contact-grid">
      <div className="contact-copy" data-reveal>
        <p className="eyebrow">Contato</p>
        <h2 id="contact-title">Fale com a Richardson.</h2>
        <p>Atendimento em {business.region}. Conte o serviço, a cidade e, se puder, envie fotos do local.</p>
        <ContactButton variant="light">Pedir orçamento pelo WhatsApp</ContactButton>
        <ul className="contact-list">
          <li><WhatsApp /><a href={contactUrl} target="_blank" rel="noopener noreferrer">WhatsApp {business.phoneDisplay}</a></li>
          <li><Pin /><a href={business.maps} target="_blank" rel="noopener noreferrer">{business.address}<span className="visually-hidden"> (abre o mapa)</span></a></li>
          <li><Clock /><span>{business.hours}</span></li>
          <li><Instagram /><a href={business.instagram} target="_blank" rel="noopener noreferrer">{business.instagramHandle}</a></li>
        </ul>
      </div>
      <figure className="storefront" data-reveal>
        <picture>
          <source type="image/avif" srcSet={set('avif')} sizes={sizes} />
          <source type="image/webp" srcSet={set('webp')} sizes={sizes} />
          <img src={asset('images/opt/fachada-800.jpg')} srcSet={set('jpg')} sizes={sizes} width="800" height="1067" loading="lazy" decoding="async"
            alt="Fachada da loja Richardson Climatização: placa azul com a logo e vitrine listando instalação, higienização, manutenção, pré-instalação e vendas" />
        </picture>
        <figcaption>Loja na Av. Centenário, em Criciúma · foto do perfil oficial</figcaption>
      </figure>
    </div>
  </section>
}
