import { useEffect, useState } from 'react'
import type { Card } from '../data/types'

type Props = {
  card: Card | null
  onClose: () => void
}

export default function CardModal({ card, onClose }: Props) {
  const [flipped, setFlipped] = useState(false)

  useEffect(() => {
    setFlipped(false)
    if (!card) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
      if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault()
        setFlipped((v) => !v)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [card, onClose])

  if (!card) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-label={card.name}
      onClick={onClose}
    >
      <div
        className="w-full max-w-md perspective"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-3 flex items-center justify-between text-[10px] tracking-[0.22em] uppercase text-[#9a8ab8]">
          <span>Click card to flip · Esc closes</span>
          <button type="button" className="text-[#f9e7b0]" onClick={onClose}>
            Close
          </button>
        </div>
        <button
          type="button"
          className="relative w-full preserve-3d transition-transform duration-500"
          style={{ transform: flipped ? 'rotateY(180deg)' : 'rotateY(0deg)' }}
          onClick={() => setFlipped((v) => !v)}
        >
          <div className="backface-hidden overflow-hidden rounded-[18px] border border-[#f9e7b0]/35 bg-[#120f1c] shadow-2xl">
            <img src={card.image} alt="" className="aspect-[2/3] w-full object-cover" />
          </div>
          <div className="absolute inset-0 rotate-y-180 backface-hidden overflow-auto rounded-[18px] border border-[#f9e7b0]/35 bg-gradient-to-b from-[#1a1430] to-[#0c0a16] p-5 text-left shadow-2xl">
            <div className="text-[10px] tracking-[0.3em] uppercase text-[#f9e7b0]">
              {card.num} — {card.role}
            </div>
            <h2 className="mt-2 font-serif text-2xl leading-tight text-[#fdf6e3]">{card.name}</h2>
            <div className="mt-2 text-[11px] tracking-[0.16em] uppercase text-[#9a8ab8]">
              {card.typeLine}
            </div>
            {card.powerToughness && (
              <div className="mt-4 inline-block rounded-lg border border-[#2a2540] bg-[#14122a] px-3 py-2 font-serif text-xl text-[#f9e7b0]">
                {card.powerToughness}
              </div>
            )}
            <div className="mt-4 h-px bg-gradient-to-r from-[#f9e7b0]/35 to-transparent" />
            <p className="mt-4 text-[13px] leading-relaxed text-[#b9aecf]">{card.lore}</p>
            {card.accent && (
              <div className={`mt-6 h-2 rounded-full bg-gradient-to-r ${card.accent} opacity-80`} />
            )}
            <p className="mt-6 text-[10px] tracking-[0.2em] uppercase text-[#5a4a7a]">
              TerAustralis Incognita · Mythic
            </p>
          </div>
        </button>
      </div>
    </div>
  )
}
