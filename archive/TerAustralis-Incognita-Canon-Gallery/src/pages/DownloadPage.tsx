export default function DownloadPage() {
  return (
    <div className="max-w-xl">
      <div className="text-[10px] tracking-[0.35em] uppercase text-[#f9e7b0]">Download Pack</div>
      <h1 className="mt-2 font-serif text-4xl text-[#fdf6e3]">16 cards + tokens</h1>
      <p className="mt-4 text-[#b9aecf] leading-relaxed">
        WebP pack at 1024×1536 — Origin through Chingona, plus Martian Oath Seed and Magical Dream Seeds.
      </p>
      <a
        href="/teraustralis-incognita-canon-pack.zip"
        download
        className="mt-8 inline-flex items-center rounded-full border border-[#f9e7b0]/50 bg-[#f9e7b0]/10 px-6 py-3 text-[11px] tracking-[0.22em] uppercase text-[#f9e7b0] hover:bg-[#f9e7b0]/20"
      >
        Download ZIP
      </a>
      <p className="mt-6 text-[12px] text-[#7a6a9a]">
        Also includes prompt-library.md and cards.json for regenerators.
      </p>
    </div>
  )
}
