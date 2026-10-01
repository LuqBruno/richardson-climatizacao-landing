import { useEffect, useRef, useState } from 'react'
import { asset, scene, sceneStages } from '../../content/site'
import { sceneMedia } from './config'
import type { SceneController, SceneLoader } from './types'

type Phase = 'idle' | 'playing' | 'done'

const saveData = () => Boolean((navigator as Navigator & { connection?: { saveData?: boolean } }).connection?.saveData)
const prefersStatic = () => matchMedia('(prefers-reduced-motion: reduce)').matches || saveData()

function Poster({ base, alt, hidden, priority }: { base: string; alt: string; hidden: boolean; priority?: boolean }) {
  const set = (ext: string) => [800, 1280, 1600].map(w => `${asset(`${base}-${w}.${ext}`)} ${w}w`).join(', ')
  const sizes = '(min-width: 1024px) 56vw, 100vw'
  return <picture className={hidden ? 'scene-poster scene-poster--hidden' : 'scene-poster'} aria-hidden={hidden || undefined}>
    <source type="image/avif" srcSet={set('avif')} sizes={sizes} />
    <source type="image/webp" srcSet={set('webp')} sizes={sizes} />
    <img src={asset(`${base}-1280.jpg`)} srcSet={set('jpg')} sizes={sizes} width={sceneMedia.width} height={sceneMedia.height}
      alt={hidden ? '' : alt} fetchPriority={priority ? 'high' : undefined} decoding="async" />
  </picture>
}

export function HeroScene({ loader = null }: { loader?: SceneLoader | null }) {
  const container = useRef<HTMLDivElement>(null)
  const controllerRef = useRef<SceneController | undefined>(undefined)
  // Sem movimento (preferência, economia de dados, sem loader ou falha): mostra o aparelho instalado.
  const [animated, setAnimated] = useState(() => Boolean(loader) && !prefersStatic())
  const [ready, setReady] = useState(false)
  const [phase, setPhase] = useState<Phase>('idle')
  const [stage, setStage] = useState(-1)

  useEffect(() => {
    const element = container.current
    if (!element || !loader || !animated) return
    const abort = new AbortController()
    const motion = matchMedia('(prefers-reduced-motion: reduce)')
    let started = false
    let visible = false
    const sync = () => controllerRef.current?.setVisible?.(visible && !document.hidden)
    const stopForMotion = () => { if (motion.matches) setAnimated(false) }
    const observer = new IntersectionObserver(async entries => {
      visible = entries[0].isIntersecting
      sync()
      if (!visible || started) return
      started = true
      try {
        const adapter = await loader()
        if (abort.signal.aborted) return
        const instance = await adapter.mount(element, {
          signal: abort.signal,
          reducedMotion: motion.matches,
          onTime: seconds => {
            let current = -1
            sceneStages.forEach((item, index) => { if (seconds >= item.at) current = index })
            setStage(previous => previous === current ? previous : current)
          },
          onEnded: () => { setStage(sceneStages.length - 1); setPhase('done') },
        })
        if (abort.signal.aborted) { instance.dispose(); return }
        controllerRef.current = instance
        setReady(true)
        setPhase('playing')
        sync()
      } catch {
        if (!abort.signal.aborted) setAnimated(false)
      }
    }, { rootMargin: '160px' })
    observer.observe(element)
    motion.addEventListener('change', stopForMotion)
    document.addEventListener('visibilitychange', sync)
    return () => {
      abort.abort()
      observer.disconnect()
      motion.removeEventListener('change', stopForMotion)
      document.removeEventListener('visibilitychange', sync)
      controllerRef.current?.dispose()
      controllerRef.current = undefined
      setReady(false)
    }
  }, [loader, animated])

  const finished = !animated || phase === 'done'
  const activeStage = finished ? sceneStages.length - 1 : stage
  const replay = () => { setPhase('playing'); setStage(-1); controllerRef.current?.replay?.() }

  return <figure className="hero-scene" data-ready={ready || undefined}>
    <div className="scene-frame">
      {/* Com animação, o pôster é a parede vazia (quadro 1); sem animação, o aparelho instalado. */}
      <Poster base={animated ? sceneMedia.start : sceneMedia.end} alt={animated ? scene.altSequence : scene.alt} hidden={ready} priority />
      <div ref={container} className="scene-mount" aria-hidden="true" />
      {animated && phase === 'done' && <button type="button" className="scene-replay" onClick={replay}>
        <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4.5 10a5.5 5.5 0 1 0 1.7-4M4.5 3.5V7H8" /></svg>{scene.replay}
      </button>}
    </div>
    <figcaption className="scene-caption">
      <ol className="scene-stages" aria-label="Etapas ilustradas">
        {sceneStages.map((item, index) => <li key={item.label} data-state={index < activeStage || (finished && index === activeStage) ? 'done' : index === activeStage ? 'active' : undefined}>
          <span aria-hidden="true" />{item.label}
        </li>)}
      </ol>
      <span className="scene-note">{scene.note}</span>
    </figcaption>
  </figure>
}
