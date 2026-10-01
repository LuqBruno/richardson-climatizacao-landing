import { readdir, readFile, writeFile, mkdir } from 'node:fs/promises'
import { gzipSync } from 'node:zlib'
import path from 'node:path'

const rows = []
for (const name of await readdir('dist/assets')) {
  if (!/\.(js|css)$/.test(name)) continue
  const data = await readFile(path.join('dist/assets', name))
  rows.push({ file: name, bytes: data.length, gzipBytes: gzipSync(data).length })
}
rows.sort((a, b) => b.bytes - a.bytes)
await mkdir('artifacts', { recursive: true })
await writeFile('artifacts/bundle-report.json', JSON.stringify(rows, null, 2))
console.table(rows.map(row => ({ file: row.file, 'KB': (row.bytes / 1024).toFixed(1), 'gzip KB': (row.gzipBytes / 1024).toFixed(1) })))
