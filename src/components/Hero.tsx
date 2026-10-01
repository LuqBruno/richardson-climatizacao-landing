import { business, hero } from '../content/site'
import { HeroScene } from '../features/hero-scene/HeroScene'
import { sceneLoader } from '../features/hero-scene/config'
import { ContactButton } from './ContactButton'
import { ArrowDown, Clock, Pin } from './icons'

export function Hero() {
  return <section id="inicio" className="hero" aria-labelledby="hero-title">
    <div className="container hero-grid">
      <div className="hero-copy">
        <p className="eyebrow">{hero.eyebrow}</p>
        <h1 id="hero-title">{hero.title}</h1>
        <p className="hero-description">{hero.description}</p>
        <div className="hero-actions">
          <ContactButton>{hero.cta}</ContactButton>
          <a className="text-link" href="#servicos">{hero.secondary}<ArrowDown className="text-link-icon" /></a>
        </div>
        <ul className="hero-facts" aria-label="Informações de atendimento">
          <li><Pin />{business.region}</li>
          <li><Clock />{business.hours}</li>
        </ul>
      </div>
      <HeroScene loader={sceneLoader} />
    </div>
    <div className="tiles tiles--band" aria-hidden="true" />
  </section>
}
