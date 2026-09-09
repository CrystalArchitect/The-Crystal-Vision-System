import type { Card } from '../data/types'

type Props = {
  card: Card
  onOpen: (card: Card) => void
}

export default function CardTile({ card, onOpen }: Props) {
  return (
    <button
      type="button"
      onClick={() => onOpen(card)}
      className="group text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-[#f9e7b0]"
    >
      <div className="relative overflow-hidden rounded-[14px] border border-[#f9e7b0]/25 bg-[#120f1c] shadow-[0_20px_50px_rgba(0,0,0,0.45)] transition duration-300 group-hover:-translate-y-1 group-hover:border-[#f9e7b0]/55">
        <div className="absolute inset-x-0 top-0 z-10 flex items-center justify-between px-3 py-2 text-[10px] tracking-[0.2em] uppercase text-[#f9e7b0]">
          <span>{card.num}</span>
          <span className="text-[#9a8ab8]">{card.role}</span>
        </div>
        <img
          src={card.image}
          alt={card.name}
          className="aspect-[2/3] w-full object-cover"
          loading="lazy"
        />
        <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-[#07060d] via-[#07060d]/85 to-transparent p-3 pt-10">
          <div className="font-serif text-[15px] leading-tight text-[#fdf6e3]">{card.name}</div>
          <div className="mt-1 text-[10px] tracking-[0.14em] uppercase text-[#9a8ab8]">
            {card.typeLine}
          </div>
        </div>
      </div>
    </button>
  )
}
