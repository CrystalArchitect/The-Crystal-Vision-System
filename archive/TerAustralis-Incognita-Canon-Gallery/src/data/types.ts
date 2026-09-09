export type Card = {
  num: string
  numIndex: number
  name: string
  typeLine: string
  lore: string
  accent?: string
  image: string
  id: string
  role: string
  powerToughness?: string | null
  artNote?: string | null
  embedIndex?: number | null
  artVar?: string
}

export type Token = {
  id: string
  name: string
  image: string
}

export type CanonData = {
  set: string
  cards: Card[]
  tokens: Token[]
}
