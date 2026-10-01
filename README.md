# Richardson Climatização — landing page

Landing de uma página para a Richardson Climatização (Criciúma e região). O hero mostra a instalação de um split de parede em 3D, renderizada no Blender. Prévia comercial.

Prévia online para o cliente (01/10/2026): https://luqbruno.github.io/richardson-climatizacao-landing/
Repositório público: https://github.com/LuqBruno/richardson-climatizacao-landing (branch `main`). O GitHub Pages é publicado por `.github/workflows/deploy-pages.yml`, que roda check e build e publica `dist`. A página tem `noindex` enquanto for prévia. O repositório não inclui os 150 quadros brutos do render nem as capturas de revisão.

## Executar

```bash
npm ci
npm run dev        # http://127.0.0.1:3013/
npm run check      # TypeScript
npm run build      # check + build em dist/
npm run preview    # serve dist/ em http://127.0.0.1:3013/ (pare o dev antes)
npm run report:bundle
```

## Stack

React 19 · TypeScript 7 · Tailwind CSS 4 (só tokens e reset; os estilos estão em CSS simples) · Vite 8.
Dependência adicionada nesta etapa: `@fontsource-variable/manrope` (fonte local, sem Google Fonts).

**Bibliotecas de animação e 3D não foram instaladas.** A cena é um vídeo pré-renderizado (veja `docs/CENA-3D.md`). Os demais movimentos usam CSS e um `IntersectionObserver`, então GSAP, Motion, Three, Embla e Lenis não teriam função real aqui:

- GSAP/Motion: as entradas são curtas e independentes; CSS cobre tudo sem adicionar ~25–40 kB.
- Three/Fiber: o vídeo do Cycles tem materiais e sombras melhores que o realtime, com download menor.
- Embla: há só dois registros reais; carrossel quando houver conteúdo suficiente.
- Lenis: rolagem nativa preservada.

## Onde editar

| O quê | Arquivo |
| --- | --- |
| Textos, contatos, serviços, etapas da cena, mensagem do WhatsApp | `src/content/site.ts` |
| Cores, fonte, espaçamentos, bordas, sombras, movimento | `src/styles/tokens.css` |
| Layout e componentes | `src/styles/global.css`, `src/components/*` |
| Cena do hero (pôsteres, vídeo, pausa, fallback) | `src/features/hero-scene/*` |
| SEO, favicon, compartilhamento, dados estruturados | `index.html` |
| Origem de cada dado e imagem | `docs/FONTES.md` |
| Blender: modelagem, render, exportação | `blender/`, `docs/CENA-3D.md` |

Scripts de assets (Python + Pillow):

- `python scripts/assets/logo-transparente.py`: recorta a logo e remove o fundo.
- `python scripts/assets/otimizar-imagens.py`: gera AVIF/WebP/JPG, os pôsteres da cena, a imagem social e os favicons.

## Comportamento da cena

- Com movimento permitido: o pôster mostra a parede vazia (quadro 1). O vídeo de 5 s toca uma vez e termina com o aparelho instalado. Depois aparece o botão "Rever instalação".
- Com `prefers-reduced-motion`, economia de dados (`Save-Data`) ou falha ao carregar o vídeo: mostra o quadro final estático, no mesmo enquadramento.
- O vídeo pausa fora da tela e com a aba oculta. Ao desmontar, a mídia é liberada. As etapas abaixo da cena acompanham o tempo do vídeo.
- O vídeo é escolhido pela largura do quadro: 800 px no celular e em telas comuns, 1280 px em telas densas. WebM VP9 com alternativa MP4 H.264.

Estado, pendências e próximos passos: `STATUS.md` e `HANDOFF.md`.
