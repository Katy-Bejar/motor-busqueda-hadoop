import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET(request) {
  const { searchParams } = new URL(request.url)
  const query = searchParams.get('q')?.toLowerCase()

  if (!query) {
    return NextResponse.json({ error: 'Falta parámetro q' }, { status: 400 })
  }

  const filePath = path.join(process.cwd(), 'api/data/inverted_index.txt')

  if (!fs.existsSync(filePath)) {
    return NextResponse.json({ error: 'No hay datos' }, { status: 500 })
  }

  const lines = fs.readFileSync(filePath, 'utf-8').split('\n')
  const results = []

  for (let line of lines) {
    const [object, videos] = line.split('\t')
    if (object.toLowerCase() === query) {
      results.push(...videos.split(','))
    }
  }

  return NextResponse.json({ query, results })
}
