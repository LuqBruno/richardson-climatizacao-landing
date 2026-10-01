# HANDOFF — Richardson Climatização

Leia `STATUS.md` (estado e pendências), `docs/FONTES.md` (origem dos dados) e `docs/CENA-3D.md` (Blender).

## Abrir a prévia

```bash
npm ci
npm run dev    # http://127.0.0.1:3013/
```

## Mudanças comuns

- **Texto, serviço, contato, mensagem do WhatsApp:** só `src/content/site.ts`. Registre a origem de dado novo em `docs/FONTES.md`.
- **Cores e espaçamentos:** `src/styles/tokens.css`.
- **Trocar uma foto de "Na prática":** coloque o original em `public/images/`, acrescente uma chamada `variants(...)` em `scripts/assets/otimizar-imagens.py`, rode o script e aponte `image` no `site.ts`.
- **Carrossel:** só quando houver 4 ou mais registros reais. Nesse caso, avaliar Embla (já usado na `Landing_Premium_Base`).
- **Logo nova (vetorial/PNG):** substitua `public/images/logo-richardson*.png` mantendo a proporção ou ajuste `width`/`height` em `src/components/Logo.tsx`. Se a logo vier com fundo transparente pensado para fundo claro, revise o contraste do cabeçalho.

## Cena 3D

- **Ajustar tempos ou movimentos:** edite `blender/build_scene.py` e siga os comandos de `docs/CENA-3D.md` (render ~35 min, codificação ~2 min). Atualize `sceneStages` no `site.ts` se os tempos mudarem.
- **Contrato:** `src/features/hero-scene/types.ts`. O adaptador atual é `adapters/videoScene.ts`. Uma cena interativa futura (GLB em `blender/export/`) pode ser outro adaptador com o mesmo contrato, sem mexer no `Hero`.

## Antes de publicar

Ver a lista "Pendências reais" em `STATUS.md`. Não publicar nem enviar ao cliente sem autorização registrada.
