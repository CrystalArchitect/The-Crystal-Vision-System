import { useMemo, useState } from 'react'
import CardModal from '../components/CardModal'
import CardTile from '../components/CardTile'
import data from '../data/cards.json'
import type { Card } from '../data/types'

export default function GalleryPage() {
  const cards = useMemo(
    () => [...(data.cards as Card[])].sort((a, b) => a.numIndex - b.numIndex),
    [],
  )
  const [open, setOpen] = useState<Card | null>(null)

  return (
    <div>
      <section className="mb-10 max-w-3xl">
        <div className="text-[10px] tracking-[0.35em] uppercase text-[#f9e7b0]">Set Reveal</div>
        <h1 className="mt-2 font-serif text-3xl md:text-5xl text-[#fdf6e3]">
          The Sixteen — Origin, Ancients, Oathbearers
        </h1>
        <p className="mt-4 text-[14px] leading-relaxed text-[#b9aecf]">
          Locked order 0–XV. Click any card to flip into lore, type line, and seal.
          Tokens sit beneath the main deck.
        </p>
      </section>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
        {cards.map((card) => (
          <CardTile key={card.id} card={card} onOpen={setOpen} />
        ))}
      </div>

      <section className="mt-14">
        <h2 className="font-serif text-2xl text-[#fdf6e3]">Tokens</h2>
        <div className="mt-4 grid grid-cols-2 gap-4 md:grid-cols-4">
          {data.tokens.map((t) => (
            <div
              key={t.id}
              className="overflow-hidden rounded-[14px] border border-[#6ec8ff]/25 bg-[#120f1c]"
            >
              <img src={t.image} alt={t.name} className="aspect-[2/3] w-full object-cover" />
              <div className="p-3 text-[12px] tracking-[0.14em] uppercase text-[#9a8ab8]">
                {t.name}
              </div>
            </div>
          ))}
        </div>
      </section>

      <CardModal card={open} onClose={() => setOpen(null)} />
    </div>
  )
}
