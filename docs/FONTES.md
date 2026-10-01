# Fontes dos dados e imagens — Richardson Climatização

Conferência feita em 01/10/2026, nas páginas públicas abaixo e sem login. O conteúdo editável fica em `src/content/site.ts`.

## Dados comerciais

| Dado | Valor usado | Origem | Situação |
| --- | --- | --- | --- |
| Nome | Richardson Climatização | Instagram oficial (nome do perfil), placa da fachada | Confirmado |
| Proposta | "Soluções em ar-condicionado" | Bio do Instagram e slogan da logo ("Soluções em Ar Condicionado") | Confirmado |
| Região | Criciúma e região | Bio do Instagram | Confirmado |
| Serviços | Instalação, higienização, vendas, manutenção, pré-instalação, PMOC | Bio do Instagram; a vitrine da fachada lista os cinco primeiros | Confirmado. As descrições curtas são texto de orientação, sem promessa de prazo, garantia ou preço |
| WhatsApp | wa.me/4834116107, exibido como (48) 3411-6107 | Link "FALE CONOSCO" da bio. O código do país (55) foi acrescentado ao link; nenhum dígito foi alterado | Confirmado |
| Endereço | Av. Centenário, 850, sala 01, Pinheirinho, Criciúma/SC, 88804-000 | Perfil da empresa no Google Maps, aberto pelo link "CAMERA 360°" da bio | Confirmado |
| Link do mapa | maps.app.goo.gl/BR8sacTVnzWs2bWy9 | Bio do Instagram | Confirmado |
| Horário | Segunda a sexta, 8h–11h30 e 13h–18h; sábado e domingo fechado | Perfil da empresa no Google Maps | Publicado pela empresa no Google. Confirmar com o cliente antes de publicar |
| Instagram | @richardson_climatizacao | Perfil oficial | Confirmado |

### Encontrado, mas não usado na página

- **"15 anos de experiência"** (bio do Instagram): é uma afirmação da própria empresa, mas tempo de mercado só entra com confirmação do cliente.
- **Telefone (48) 99927-4407** (Google Maps): diverge do WhatsApp da bio. Perguntar ao cliente qual é o canal oficial.
- **Destaques "AUTORIZADA" e "SEMINOVOS"**: não foram abertos. Sem saber de quais marcas a empresa é autorizada nem o que vende como seminovo, a informação não aparece na página.
- **Logos de fabricantes** (vitrine da fachada e vídeo da condensadora): marcas atendidas não são listadas na página.
- **Avaliações do Google**: não foram usadas. A página não exibe notas, depoimentos nem número de clientes.

## Imagens

| Arquivo | Conteúdo | Origem | Uso |
| --- | --- | --- | --- |
| `public/images/logo-oficial.jpg` | Logo sobre azul, 150×150 | Foto de perfil do Instagram oficial | Original preservado |
| `public/images/logo-richardson.png` e `@2x` | Logo recortada sem o slogan, com fundo transparente | Derivada do JPG acima por `scripts/assets/logo-transparente.py`. A versão @2x foi ampliada por interpolação Lanczos, sem redesenho | Cabeçalho e rodapé (sempre sobre azul-marinho) |
| `public/favicon-32.png`, `public/apple-touch-icon.png` | Marca "R" e floco | Recorte do JPG oficial | Favicon |
| `public/images/fachada-oficial.jpg` | Fachada da loja | Publicação do perfil oficial (registrada na etapa anterior) | Seção Contato, recortada em `images/opt/fachada-*` |
| `public/images/projeto-residencial.jpg` | Capa do vídeo em obra residencial | Reel oficial `DKo818GOFt-` (08/06/2025). Legenda: agradecimento a um cliente pela participação na construção do novo lar | "Na prática". A cidade citada antes ("Içara") não aparece na publicação e foi removida |
| `public/images/servico-condensadora.jpg` | Condensadora em suporte de parede | Reel oficial `DdwOYghgMny` (26/09/2026). Legenda: "Solução certa é solução segura !!!" | "Na prática" |
| `public/scene/*`, `public/og-richardson.jpg` | Aparelho split genérico em 3D | Produzido nesta etapa no Blender (`blender/`) | Hero e compartilhamento. Identificado na página como ilustração 3D sem marca, não como trabalho realizado |

As capas dos reels mantêm o texto original sobreposto (e, no segundo, os logos de fabricantes exibidos no vídeo). Para trocar por fotos limpas, peça ao cliente os arquivos originais.

## Paleta

A empresa não forneceu manual de marca. As cores vêm da amostragem da logo: fundo `#0f3066`, "R" `#cf2831`, floco branco e marcas em azul-gelo. A faixa de pastilhas azuis da fachada inspirou o motivo gráfico de pastilhas. Os tokens estão em `src/styles/tokens.css`.
