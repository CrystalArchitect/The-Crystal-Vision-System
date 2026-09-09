import raw from '../data/prompt-library.md?raw'

export default function PromptsPage() {
  return (
    <div className="max-w-3xl">
      <div className="text-[10px] tracking-[0.35em] uppercase text-[#f9e7b0]">Prompt Library</div>
      <h1 className="mt-2 font-serif text-4xl text-[#fdf6e3]">Regenerate every card</h1>
      <p className="mt-4 text-[#b9aecf]">
        Exact regeneration prompts for the locked 16 + tokens. Style anchors live in Drive
        folder TerAustralis_Complete_Canon.
      </p>
      <pre className="mt-8 overflow-x-auto whitespace-pre-wrap rounded-2xl border border-[#2a2540] bg-[#0c0a16] p-5 text-[12px] leading-relaxed text-[#cbbfe0]">
{raw}
      </pre>
    </div>
  )
}
