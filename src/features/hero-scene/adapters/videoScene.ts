import { asset } from '../../../content/site'
import { sceneMedia } from '../config'
import type { SceneAdapter, SceneController } from '../types'

/** Sequência renderizada (WebM VP9 com alternativa MP4 H.264), reproduzida uma vez. */
export const videoScene: SceneAdapter = {
  mount(container, { signal, onTime, onEnded }) {
    return new Promise<SceneController>((resolve, reject) => {
      const width = container.clientWidth * Math.min(devicePixelRatio || 1, 2)
      const file = sceneMedia.videos.find(item => width <= item.maxWidth) ?? sceneMedia.videos[sceneMedia.videos.length - 1]
      const video = document.createElement('video')
      video.muted = true
      video.defaultMuted = true
      video.playsInline = true
      video.preload = 'auto'
      video.disablePictureInPicture = true
      video.setAttribute('aria-hidden', 'true')
      video.tabIndex = -1
      for (const [ext, type] of [['webm', 'video/webm; codecs="vp9"'], ['mp4', 'video/mp4']]) {
        const source = document.createElement('source')
        source.src = asset(`${file.src}.${ext}`)
        source.type = type
        video.append(source)
      }

      let visible = false
      let ended = false
      let frame = 0
      const tick = () => {
        onTime?.(video.currentTime)
        if (!video.paused && !ended) frame = requestAnimationFrame(tick)
      }
      const play = () => {
        if (!visible || ended || document.hidden) return
        video.play().then(() => { cancelAnimationFrame(frame); frame = requestAnimationFrame(tick) }).catch(() => {})
      }
      const handleEnded = () => { ended = true; cancelAnimationFrame(frame); onTime?.(video.duration); onEnded?.() }
      const fail = () => { cleanup(); reject(new Error('Vídeo da cena indisponível')) }
      const ready = () => {
        video.removeEventListener('canplay', ready)
        resolve(controller)
      }
      const cleanup = () => {
        cancelAnimationFrame(frame)
        video.removeEventListener('ended', handleEnded)
        video.removeEventListener('canplay', ready)
        video.removeEventListener('error', fail)
        lastSource.removeEventListener('error', fail)
        video.pause()
        video.removeAttribute('src')
        video.querySelectorAll('source').forEach(source => source.remove())
        video.load() // libera o buffer de mídia
        video.remove()
      }
      const controller: SceneController = {
        dispose: cleanup,
        setVisible(next) {
          visible = next
          if (next) play()
          else { video.pause(); cancelAnimationFrame(frame) }
        },
        replay() {
          ended = false
          video.currentTime = 0
          play()
        },
      }

      video.addEventListener('ended', handleEnded)
      video.addEventListener('canplay', ready)
      // Só a falha da última <source> significa que nenhum formato serviu.
      const lastSource = video.querySelector('source:last-of-type')!
      lastSource.addEventListener('error', fail)
      video.addEventListener('error', fail)
      signal.addEventListener('abort', cleanup, { once: true })
      container.append(video)
    })
  },
}
