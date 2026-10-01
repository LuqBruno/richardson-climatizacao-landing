import { featuredService, services } from '../content/site'
import { ContactButton } from './ContactButton'

/** Desenho de linha do split, ecoando a cena do hero. */
function SplitLine() {
  return <svg className="featured-art" viewBox="0 0 240 120" aria-hidden="true">
    <rect x="20" y="14" width="200" height="54" rx="12" />
    <path d="M32 54h176M150 38h22" />
    <path className="featured-air" d="M60 76c-4 14-10 24-20 34M100 78c-2 14-4 24-8 34M140 78c2 14 4 24 8 34M180 76c4 14 10 24 20 34" />
  </svg>
}

export function Services() {
  return <section id="servicos" className="section services" aria-labelledby="services-title">
    <div className="container services-layout">
      <div className="section-intro" data-reveal>
        <p className="eyebrow">Serviços</p>
        <h2 id="services-title">Do planejamento ao ar ligado.</h2>
        <p>A Richardson atende desde a infraestrutura da obra até a limpeza e a manutenção do aparelho.</p>
      </div>
      <div className="services-body">
        <article className="featured-service" data-reveal>
          <div>
            <span className="item-number">01</span>
            <h3>{featuredService.title}</h3>
            <p>{featuredService.description}</p>
            <ContactButton variant="light">{featuredService.cta}</ContactButton>
          </div>
          <SplitLine />
        </article>
        <ul className="service-list">
          {services.map((service, index) => <li key={service.title} data-reveal>
            <span className="item-number">{String(index + 2).padStart(2, '0')}</span>
            <h3>{service.title}</h3>
            <p>{service.description}</p>
          </li>)}
        </ul>
      </div>
    </div>
  </section>
}
