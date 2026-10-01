import type { ReactNode } from 'react'
import { contactUrl } from '../content/site'
import { WhatsApp } from './icons'

/** Abre o WhatsApp com a mensagem editável; nada é enviado automaticamente. */
export function ContactButton({ children = 'Pedir orçamento', variant = 'primary', className = '' }: { children?: ReactNode; variant?: 'primary' | 'light'; className?: string }) {
  return <a className={`button button--${variant} ${className}`.trim()} href={contactUrl} target="_blank" rel="noopener noreferrer">
    <WhatsApp className="button-icon" />{children}<span className="visually-hidden"> (abre o WhatsApp em nova aba)</span>
  </a>
}
