import { cp, mkdir, readdir, access } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const source = fileURLToPath(new URL('..', import.meta.url))
const argument = process.argv[2]
if (!argument) throw new Error('Uso: npm run new:landing -- "C:/caminho/novo-projeto"')
const target = path.resolve(argument)
if (target === source || target.startsWith(source + path.sep)) throw new Error('Escolha uma pasta fora da base.')
let exists = false
try { await access(target); exists = true } catch {}
if (exists) throw new Error('O destino já existe. Nenhum arquivo foi sobrescrito.')
await mkdir(target, { recursive: true })
const ignored = new Set(['node_modules', 'dist', 'artifacts', '.git', 'STATUS.md'])
for (const entry of await readdir(source)) {
  if (!ignored.has(entry)) await cp(path.join(source, entry), path.join(target, entry), { recursive: true, force: false, errorOnExist: true })
}
console.log(`Base copiada para ${target}. Execute npm ci nessa pasta e personalize a identidade.`)
