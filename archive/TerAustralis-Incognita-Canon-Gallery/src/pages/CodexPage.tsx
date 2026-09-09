import data from '../data/cards.json'
import type { Card } from '../data/types'

export default function CodexPage() {
  const cards = [...(data.cards as Card[])].sort((a, b) => a.numIndex - b.numIndex)

  return (
    <article className="prose-invert max-w-3xl">
      <div className="text-[10px] tracking-[0.35em] uppercase text-[#f9e7b0]">Lore Codex</div>
      <h1 className="mt-2 font-serif text-4xl text-[#fdf6e3]">World History</h1>
      <p className="mt-4 text-[#b9aecf] leading-relaxed">
        Vision / Dreamed layer. TerAustralis Incognita is a Mars worldbuilding mythos:
        red dust, lattice geometry, rockets, and the vow that keeps dreaming safe.
      </p>

      <section className="mt-10 space-y-4">
        <h2 className="font-serif text-2xl text-[#fdf6e3]">The Lattice</h2>
        <p className="text-[#b9aecf] leading-relaxed">
          The Lattice is the living geometry that holds TerAustralis — wall, heart, library, and veil.
          It is structure that remembers. When the Lattice Heart beats, continents inhale.
          (Engineering name CrystalCore.Lattice is a separate locked project term; here Lattice is mythos.)
        </p>
      </section>

      <section className="mt-10 space-y-4">
        <h2 className="font-serif text-2xl text-[#fdf6e3]">The Ancients</h2>
        <p className="text-[#b9aecf] leading-relaxed">
          Thirteen Ancients span first spark to next-world seed: dust, tide, forge, map, silence,
          unfinished scale, council, launch, memory, heart, veil, dream. They keep a Mars-dream honest.
        </p>
      </section>

      <section className="mt-10 space-y-4">
        <h2 className="font-serif text-2xl text-[#fdf6e3]">The Oath</h2>
        <p className="text-[#b9aecf] leading-relaxed">
          Oathbearers hold the line so dreaming stays safe. The Martian Oath Seed is the compact vow;
          Dream Seeds are compressed maybes. The Oathbearer breaks only if the oath breaks.
          Chingona keeps the final promise under starlight.
        </p>
      </section>

      <section className="mt-12 space-y-8">
        <h2 className="font-serif text-2xl text-[#fdf6e3]">Card Codex</h2>
        {cards.map((c) => (
          <div key={c.id} className="rounded-2xl border border-[#2a2540] bg-[#120f1c]/70 p-5">
            <div className="text-[10px] tracking-[0.25em] uppercase text-[#f9e7b0]">
              {c.num} · {c.role}
            </div>
            <h3 className="mt-1 font-serif text-xl text-[#fdf6e3]">{c.name}</h3>
            <div className="mt-1 text-[11px] uppercase tracking-[0.14em] text-[#9a8ab8]">{c.typeLine}</div>
            <p className="mt-3 text-[13px] leading-relaxed text-[#b9aecf]">{c.lore}</p>
          </div>
        ))}
      </section>
    </article>
  )
}
