/** Contrato do renderizador opcional do hero. Cada adaptador faz o próprio cleanup. */
export interface SceneController {
  dispose(): void
  setVisible?(visible: boolean): void
  /** Reinicia a sequência a pedido do visitante (sem loop automático). */
  replay?(): void
}
export interface SceneOptions {
  signal: AbortSignal
  reducedMotion: boolean
  /** Tempo atual da sequência, em segundos. */
  onTime?(seconds: number): void
  /** Sequência terminou no último quadro (aparelho instalado). */
  onEnded?(): void
}
export interface SceneAdapter {
  mount(container: HTMLElement, options: SceneOptions): Promise<SceneController>
}
export type SceneLoader = () => Promise<SceneAdapter>
