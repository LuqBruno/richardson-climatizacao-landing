import { asset, business, projects } from '../content/site'
import { ArrowUpRight } from './icons'

const set = (name: string, ext: string) => [360, 540].map(w => `${asset(`images/opt/${name}-${w}.${ext}`)} ${w}w`).join(', ')
const sizes = '(min-width: 1024px) 270px, 44vw'

/** Dois registros reais: composição estática (carrossel só com mais conteúdo). */
export function Projects() {
  return <section id="trabalhos" className="section projects" aria-labelledby="projects-title">
    <div className="container projects-layout">
      <div className="section-intro" data-reveal>
        <p className="eyebrow">Na prática</p>
        <h2 id="projects-title">Registros da própria equipe.</h2>
        <p>Publicações do perfil oficial da Richardson. As capas mantêm o texto original de cada vídeo.</p>
        <a className="text-link" href={business.instagram} target="_blank" rel="noopener noreferrer">Ver mais no Instagram<ArrowUpRight className="text-link-icon" /></a>
      </div>
      <div className="project-pair">
        {projects.map(project => <article className="project" key={project.url} data-reveal>
          <a className="project-media" href={project.url} target="_blank" rel="noopener noreferrer" tabIndex={-1} aria-hidden="true">
            <picture>
              <source type="image/avif" srcSet={set(project.image, 'avif')} sizes={sizes} />
              <source type="image/webp" srcSet={set(project.image, 'webp')} sizes={sizes} />
              <img src={asset(`images/opt/${project.image}-540.jpg`)} srcSet={set(project.image, 'jpg')} sizes={sizes} alt={project.alt} width="540" height="960" loading="lazy" decoding="async" />
            </picture>
          </a>
          <div className="project-caption">
            <p className="project-date">{project.date}</p>
            <h3>{project.title}</h3>
            <p>{project.description}</p>
            <a className="text-link" href={project.url} target="_blank" rel="noopener noreferrer">Ver publicação<span className="visually-hidden">: {project.title}</span><ArrowUpRight className="text-link-icon" /></a>
          </div>
        </article>)}
      </div>
    </div>
  </section>
}
