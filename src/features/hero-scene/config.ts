import type { SceneLoader } from './types'

// A cena é um vídeo renderizado no Blender (Cycles); ver docs/CENA-3D.md.
// O adaptador é carregado sob demanda pelo HeroScene.
export const sceneLoader: SceneLoader | null = () => import('./adapters/videoScene').then(module => module.videoScene)

/** Arquivos em public/scene. Vídeo escolhido pela largura do quadro em pixels do aparelho. */
export const sceneMedia = {
  width: 1280,
  height: 1024,
  duration: 5,
  start: 'scene/cena-inicio',
  end: 'scene/cena-instalada',
  videos: [
    { maxWidth: 900, src: 'scene/richardson-instalacao-800' },
    { maxWidth: Infinity, src: 'scene/richardson-instalacao-1280' },
  ],
}
