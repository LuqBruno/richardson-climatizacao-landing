/** Conteúdo do cliente. Origem e limites de cada dado: docs/FONTES.md. */
export const asset = (path: string) => `${import.meta.env.BASE_URL}${path}`

export const business = {
  name: 'Richardson Climatização',
  tagline: 'Soluções em ar-condicionado',
  region: 'Criciúma e região',
  // Google Maps (perfil da empresa), conferido em 01/10/2026
  address: 'Av. Centenário, 850, sala 01 · Pinheirinho, Criciúma/SC',
  addressShort: 'Av. Centenário, 850 · Criciúma/SC',
  hours: 'Segunda a sexta, 8h–11h30 e 13h–18h',
  instagram: 'https://www.instagram.com/richardson_climatizacao/',
  instagramHandle: '@richardson_climatizacao',
  // Link "CAMERA 360°" publicado na bio do Instagram
  maps: 'https://maps.app.goo.gl/BR8sacTVnzWs2bWy9',
  phoneDisplay: '(48) 3411-6107',
  // A bio publica wa.me/4834116107; apenas o código do país (55) foi acrescentado.
  whatsapp: 'https://wa.me/554834116107',
  // Mensagem pré-preenchida: o visitante revisa e envia por conta própria.
  message: 'Olá! Gostaria de um orçamento com a Richardson Climatização.\nServiço: \nCidade: ',
  logo: 'images/logo-richardson.png',
  logo2x: 'images/logo-richardson@2x.png',
} as const

export const contactUrl = `${business.whatsapp}?text=${encodeURIComponent(business.message)}`

export const navigation = [
  { label: 'Serviços', href: '#servicos' },
  { label: 'Na prática', href: '#trabalhos' },
  { label: 'Como pedir', href: '#atendimento' },
  { label: 'Contato', href: '#contato' },
]

export const hero = {
  eyebrow: 'Soluções em ar-condicionado · Criciúma e região',
  // \u2060 impede a quebra de linha depois do hífen
  title: 'Ar-\u2060condicionado instalado com cuidado.',
  description:
    'Instalação, pré-instalação, higienização, manutenção, PMOC e venda de aparelhos. Conte o que você precisa e a Richardson orienta o próximo passo.',
  cta: 'Pedir orçamento',
  secondary: 'Ver serviços',
}

/** Etapas ilustradas pela cena do hero (tempos em segundos do vídeo de 5 s). */
export const sceneStages = [
  { label: 'Suporte fixado', at: 0 },
  { label: 'Aparelho encaixado', at: 2.0 },
  { label: 'Ar em funcionamento', at: 3.2 },
]

export const scene = {
  alt: 'Ilustração 3D de um aparelho split branco instalado em parede clara, com a aleta aberta e linhas suaves indicando o fluxo de ar.',
  altSequence: 'Ilustração 3D de uma parede clara onde um aparelho split é instalado: o suporte aparece, o aparelho encaixa, a aleta abre e o ar começa a circular.',
  note: 'Ilustração 3D · modelo genérico, sem marca',
  replay: 'Rever instalação',
}

/** Serviços listados na bio oficial do Instagram e na vitrine da fachada. */
export const featuredService = {
  title: 'Instalação',
  description:
    'Do posicionamento do suporte ao primeiro funcionamento. Envie fotos do ambiente e o modelo do aparelho, se já tiver, para conversar sobre o serviço.',
  cta: 'Pedir orçamento de instalação',
}

export const services = [
  { title: 'Pré-instalação', description: 'Infraestrutura planejada durante a obra ou reforma, para receber o aparelho depois.' },
  { title: 'Higienização', description: 'Limpeza do equipamento. Informe quantos aparelhos e onde estão instalados.' },
  { title: 'Manutenção', description: 'Conte o que está acontecendo com o aparelho para consultar o atendimento técnico.' },
  { title: 'PMOC', description: 'Plano de Manutenção, Operação e Controle para ambientes climatizados. Consulte as condições para o seu caso.' },
  { title: 'Venda de aparelhos', description: 'Consulte os modelos disponíveis e a opção adequada para o ambiente que você quer climatizar.' },
]

/** Registros publicados pela própria Richardson. Legendas descrevem só o que a publicação mostra. */
export const projects = [
  {
    title: 'Obra residencial',
    description: 'Publicação de agradecimento a um cliente pela participação na construção do novo lar.',
    image: 'projeto-residencial',
    alt: 'Capa de vídeo da Richardson em uma obra residencial com o texto "Não quer encher sua casa de ar-condicionado na lateral e frente da casa?"',
    url: 'https://www.instagram.com/richardson_climatizacao/reel/DKo818GOFt-/',
    date: 'Junho de 2025',
  },
  {
    title: 'Unidade externa',
    description: 'Condensadora fixada em suporte de parede, em vídeo publicado com a legenda "Solução certa é solução segura".',
    image: 'servico-condensadora',
    alt: 'Unidade condensadora de ar-condicionado fixada em suporte na parede externa de uma casa, sob céu azul',
    url: 'https://www.instagram.com/richardson_climatizacao/reel/DdwOYghgMny/',
    date: 'Setembro de 2026',
  },
]

export const steps = [
  { title: 'Diga o serviço', description: 'Instalação, pré-instalação, limpeza, manutenção, PMOC ou compra de um aparelho.' },
  { title: 'Mostre o local', description: 'Informe a cidade e envie fotos do ambiente ou do equipamento. Se souber, diga o modelo ou a capacidade.' },
  { title: 'Combine com a equipe', description: 'Orçamento, disponibilidade e próximos passos são acertados diretamente com a Richardson.' },
]
