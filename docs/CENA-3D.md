# Cena 3D do hero — split de parede

## O que é

Um split hi-wall genérico (0,82 × 0,28 × 0,21 m, proporções de um aparelho residencial), sem marca, logotipo ou especificação. Foi modelado por código no Blender 5.2.2 LTS a partir do aspecto dos aparelhos brancos que aparecem na fachada e nas publicações da Richardson. Não representa um modelo comercial específico.

Modelagem:

- **Corpo**: perfil lateral com cantos arredondados, extrudado e chanfrado (7 segmentos) nas extremidades.
- **Painel frontal**: peça separada, com junta visível.
- **Saída de ar**: recesso escuro com 36 defletores verticais.
- **Aleta**: articulada perto da borda traseira.
- **Visor e LED**: pequenos, sem texto.
- **Suporte**: chapa galvanizada com furos oblongos e dois ganchos.
- **Ambiente**: parede de reboco fino azul-gelo e teto.

Materiais e luz:

- **Plástico**: o corpo é acetinado com variação de rugosidade (0,28–0,40); o painel e a aleta são mais lisos, com leve verniz.
- **Outros materiais**: aço metálico, visor de vidro escuro e LED com emissão.
- **Iluminação**: luz principal quente vinda do alto à esquerda, preenchimento frio à direita, recorte superior e mundo azulado. Cycles com motion blur e AgX (Medium High Contrast).
- **Câmera**: 52 mm, um pouco abaixo e à esquerda (perspectiva moderada, leitura de quem está no ambiente).

## Sequência (30 fps, 150 quadros = 5 s)

| Quadros | Tempo | Ação |
| --- | --- | --- |
| 1–18 | 0–0,6 s | Suporte aparece na parede (opacidade e aproximação de 16 mm) |
| 12–60 | 0,4–2 s | Aparelho desce do alto e da frente até a posição (ease-out cúbico, leve rotação corrigida) |
| 60–74 | 2–2,5 s | Encaixe: últimos 12 mm de profundidade e descida nos ganchos |
| 80–104 | 2,7–3,5 s | Aleta abre (−42°) |
| 84–96 | 2,8–3,2 s | LED acende |
| 94–140 | 3,1–4,7 s | Fitas de ar translúcidas avançam e ficam discretas |
| 140–150 | até 5 s | Quadro final estável: aparelho instalado |

As etapas exibidas abaixo da cena (`sceneStages` em `src/content/site.ts`) usam os tempos 0 s, 2 s e 3,2 s.

## Escolha do formato: vídeo pré-renderizado

| Critério | GLB + Three.js (tempo real) | Vídeo do Cycles (escolhido) |
| --- | --- | --- |
| Materiais, sombras de contato, oclusão | O EEVEE (proxy rasterizado, `renders/eevee-150.png`) chega perto, mas escurece o teto e endurece sombras e luz rebatida. Um WebGL no navegador ficaria abaixo do EEVEE sem baking de luz | Path tracing completo (`renders/still-150.png`) |
| Fluxo de ar translúcido | Shader próprio em WebGL | Já está no render |
| Download | GLB 39 kB (Draco) + chunk Three/Fiber/Drei de ~246 kB gzip (medido na Landing_Premium_Base) + decodificador Draco | Vídeo e pôster (tamanhos em STATUS.md) |
| Custo no aparelho | GPU ativa durante a cena, com variação entre celulares | Decodificação de vídeo por hardware |
| Interatividade | Possível (girar, parallax) | Reprodução única e botão "Rever" |

Como o briefing pede uma sequência curta, sem interação obrigatória e com acabamento de material, o vídeo entrega mais qualidade com menos peso e risco. O GLB foi exportado para uma etapa futura interativa.

## Arquivos

| Caminho | Conteúdo |
| --- | --- |
| `blender/build_scene.py` | Script que cria tudo (geometria, materiais, luz, câmera, animação) e renderiza/exporta |
| `blender/richardson-split.blend` | Cena gerada pelo script |
| `blender/encode_video.py` | Codifica os PNGs em WebM/MP4 com o FFmpeg do Blender |
| `blender/renders/still-001.png`, `still-150.png` | Primeiro e último quadro em 1600×1280 (fontes dos pôsteres) |
| `blender/renders/eevee-150.png` | Comparação rasterizada |
| `blender/renders/frames/` | 150 PNGs 1280×1024 (fora do git; regeneráveis) |
| `blender/export/richardson-split.glb` | Modelo com animação de transformações (sem fitas de ar nem luzes) |
| `public/scene/` | Vídeos e pôsteres usados pela página |

**Texturas:** todos os materiais são procedurais (ruído para rugosidade e reboco); não há arquivos de textura. O GLB leva apenas cores e rugosidades base.

## Reproduzir

```bash
B="C:/Program Files/Blender Foundation/Blender 5.2/blender.exe"
"$B" -b -P blender/build_scene.py -- anim          # ~35 min numa RTX 3050 (64 amostras + OptiX)
"$B" -b -P blender/build_scene.py -- still 1 256
"$B" -b -P blender/build_scene.py -- still 150 256
"$B" -b --factory-startup -P blender/encode_video.py
python scripts/assets/otimizar-imagens.py           # pôsteres AVIF/WebP/JPG + imagem social
"$B" -b -P blender/build_scene.py -- glb            # opcional
```

Para ajustar o tempo, altere os quadros em `animate(...)` no fim de `build()` e os tempos de `sceneStages`.
