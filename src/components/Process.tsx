import { steps } from '../content/site'
import { ContactButton } from './ContactButton'

export function Process() {
  return <section id="atendimento" className="section process" aria-labelledby="process-title">
    <div className="container">
      <div className="section-intro section-intro--wide" data-reveal>
        <p className="eyebrow">Como pedir</p>
        <h2 id="process-title">Orçamento em três passos.</h2>
      </div>
      <ol className="steps">
        {steps.map((step, index) => <li key={step.title} data-reveal>
          <span className="step-number">{index + 1}</span>
          <h3>{step.title}</h3>
          <p>{step.description}</p>
        </li>)}
      </ol>
      <div className="process-cta" data-reveal>
        <p>A conversa abre no WhatsApp com uma mensagem pronta para você completar e revisar antes de enviar.</p>
        <ContactButton>Começar pelo WhatsApp</ContactButton>
      </div>
    </div>
  </section>
}
