import { asset, business } from '../content/site'

/** Logo oficial recortada do JPG da marca (fundo removido). Usar apenas sobre azul-marinho. */
export function Logo({ className = '' }: { className?: string }) {
  return <img className={`logo ${className}`.trim()} src={asset(business.logo)} srcSet={`${asset(business.logo)} 1x, ${asset(business.logo2x)} 2x`}
    width="150" height="86" alt="Richardson Climatização" decoding="async" />
}
