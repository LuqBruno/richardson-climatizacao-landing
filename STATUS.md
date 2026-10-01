# STATUS — Richardson Climatização

**Situação:** prévia comercial 0.2.0 online para visualização do cliente (01/10/2026). Sem contratação nem publicação definitiva registradas. A negociação, se houver, fica no `PIPELINE.md`.

**Publicação da prévia** (pedido do usuário, 01/10/2026):
- Repositório público: https://github.com/LuqBruno/richardson-climatizacao-landing
- Pages: https://luqbruno.github.io/richardson-climatizacao-landing/
- O workflow de deploy (check + build + Pages) terminou com sucesso.
- Conferido no ar: HTTP 200 da página, dos vídeos, pôsteres, logo, favicon e imagem social; cena reproduzindo em 1440 e 390 px; sem rolagem horizontal nem erros; `noindex` ativo.
- Nenhuma mensagem foi enviada ao cliente.

## Decisões vigentes (01/10/2026, pedido desta conversa)

- O pedido autorizou o aprimoramento visual, a instalação de dependências e a cena 3D, adiados na etapa anterior.
- **Identidade:**
  - Azul-marinho `#0f3066` da logo no cabeçalho e no contato; vermelho `#cf2831` só no CTA principal e nos marcadores; azul-gelo como apoio.
  - Fonte Manrope local.
  - Motivo de pastilhas inspirado na faixa azul da fachada.
- **Logo:** recortada do JPG oficial com fundo removido por desmistura de cor e usada apenas sobre azul. O slogan ficou fora do recorte por ser ilegível em 150 px.
- **Hero:** título "Ar-condicionado instalado com cuidado.", CTA de orçamento pelo WhatsApp e cena 3D com três etapas sincronizadas.
- **Cena:** vídeo de 5 s renderizado no Cycles (escolhido em vez de GLB/Three; justificativa em `docs/CENA-3D.md`). Toca uma vez, sem loop, com botão "Rever instalação".
- **Bibliotecas:** nenhuma biblioteca de animação ou 3D instalada. CSS e `IntersectionObserver` bastaram (motivos no README).
- **Conteúdo:**
  - PMOC entrou nos serviços (consta na bio).
  - A menção a "Içara" foi removida (não aparece na publicação).
  - Horário de funcionamento vindo do Google.
  - "15 anos de experiência" não foi usado.
- **Trabalhos:** só há dois registros reais, então são exibidos em composição estática, sem carrossel.

## Verificações executadas nesta etapa

- **Base antes do refinamento:** `npm run build` passou. Os arquivos do AGENTS.md (README, STATUS, HANDOFF, docs/FONTES) não existiam e foram criados.
- **Check e build:** `npm run check` e `npm run build` passaram. Entrada JS 72,9 kB gzip, CSS 10,3 kB gzip, adaptador da cena 0,8 kB gzip (`npm run report:bundle`).
- **Teste funcional** no build (`vite preview`, Edge headless via Playwright, script no scratchpad desta sessão):
  - 360, 390 e 430 px: sem rolagem horizontal; CTA termina entre 456 e 478 px do topo.
  - Menu: abre, Esc fecha e devolve o foco, e um link fecha o menu e navega.
  - Nenhum alvo de toque abaixo de 40 px.
  - Ordem de foco lógica, com contorno visível e "pular para o conteúdo" funcionando.
- **Cena:**
  - Toca sem loop; as três etapas terminam concluídas; "Rever" reinicia o vídeo.
  - O vídeo pausa fora da tela.
  - Com movimento reduzido não há vídeo: o pôster é o aparelho instalado e o conteúdo fica visível.
  - Com o vídeo bloqueado, volta ao pôster instalado.
  - Diferença média entre pôster e quadros do vídeo abaixo de 1/255.
- **Desempenho medido** (Edge, uma execução, máquina de desenvolvimento):
  - Desktop 1440: LCP 0,70 s, CLS 0, 320 kB transferidos.
  - Celular emulado 390 px (CPU 4× mais lenta, ~1,6 Mbps): LCP 1,55 s, CLS 0, 336 kB, 0,9 s de tarefas longas.
  - Durante o vídeo, os quadros ficaram em 6,1 ms (p95 6,3 ms) num monitor de 165 Hz. **Ainda não foi medido em celular real.**
- **Console:** sem erros nem avisos.
- **Capturas de revisão:** `output/revisao-2026-10-01/`.

## Assets da cena

Vídeos: 800 px WebM 150 kB / MP4 189 kB; 1280 px WebM 312 kB / MP4 592 kB. Pôsteres AVIF de 1,5 a 14 kB. Blender e GLB em `blender/` (detalhes em `docs/CENA-3D.md`).

## Pendências reais

1. Confirmar com o cliente: horário, canal oficial (WhatsApp 3411-6107 × telefone do Google 99927-4407) e se a página pode mencionar os "15 anos de experiência".
2. Logo vetorial ou PNG em alta resolução, se existir. A atual vem de um JPG de 150 px e fica um pouco suave em telas densas.
3. Fotos originais sem texto sobreposto para "Na prática" (as capas de reels trazem texto e, numa delas, logos de fabricantes).
4. Domínio final: hoje `og:image` e `og:url` apontam para o GitHub Pages; no domínio definitivo, trocar essas URLs, acrescentar `canonical` e remover o `noindex`. Avaliar pré-renderização do HTML ao publicar (hoje o conteúdo indexável sem JS está no `<noscript>` e no JSON-LD).
5. Testar em celular real (iOS Safari e Android) a reprodução automática do vídeo e a fluidez.

## Próxima ação

Revisão do usuário na prévia local. Depois, levar ao cliente as confirmações da lista acima.
