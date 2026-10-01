/** Ícones de traço simples, herdando a cor do texto. Sempre decorativos. */
type Props = { className?: string }
const base = { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.8, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const, 'aria-hidden': true }

export const ArrowUpRight = ({ className }: Props) => <svg {...base} className={className}><path d="M7 17 17 7M8 7h9v9" /></svg>
export const ArrowDown = ({ className }: Props) => <svg {...base} className={className}><path d="M12 5v14M6 13l6 6 6-6" /></svg>
export const ArrowUp = ({ className }: Props) => <svg {...base} className={className}><path d="M12 19V5M6 11l6-6 6 6" /></svg>
export const Pin = ({ className }: Props) => <svg {...base} className={className}><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z" /><circle cx="12" cy="9.5" r="2.5" /></svg>
export const Clock = ({ className }: Props) => <svg {...base} className={className}><circle cx="12" cy="12" r="8.5" /><path d="M12 7.5V12l3 2" /></svg>
export const Instagram = ({ className }: Props) => <svg {...base} className={className}><rect x="3.5" y="3.5" width="17" height="17" rx="5" /><circle cx="12" cy="12" r="4" /><circle cx="17.2" cy="6.8" r=".6" fill="currentColor" /></svg>
export const Phone = ({ className }: Props) => <svg {...base} className={className}><path d="M5 4h3.5l1.7 4.3-2.2 1.4a11 11 0 0 0 6.3 6.3l1.4-2.2L20 15.5V19a1.5 1.5 0 0 1-1.6 1.5C10.6 20 4 13.4 3.5 5.6A1.5 1.5 0 0 1 5 4Z" /></svg>
export const WhatsApp = ({ className }: Props) => <svg viewBox="0 0 24 24" aria-hidden="true" className={className}><path fill="currentColor" d="M12 2.2a9.8 9.8 0 0 0-8.4 14.8L2.2 21.8l4.9-1.3A9.8 9.8 0 1 0 12 2.2Zm0 17.9a8.1 8.1 0 0 1-4.1-1.1l-.3-.2-2.9.8.8-2.8-.2-.3A8.1 8.1 0 1 1 12 20.1Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z" /></svg>
export const Menu = ({ className }: Props) => <svg {...base} className={className}><path d="M4 8h16M4 16h16" /></svg>
export const Close = ({ className }: Props) => <svg {...base} className={className}><path d="M6 6l12 12M18 6 6 18" /></svg>
