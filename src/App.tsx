import { NavLink, Route, Routes } from 'react-router-dom'
import GalleryPage from './pages/GalleryPage'
import CodexPage from './pages/CodexPage'
import PromptsPage from './pages/PromptsPage'
import DownloadPage from './pages/DownloadPage'

const link = ({ isActive }: { isActive: boolean }) =>
  `text-[11px] tracking-[0.22em] uppercase transition ${
    isActive ? 'text-[#f9e7b0]' : 'text-[#8a7ab0] hover:text-[#e8e0f0]'
  }`

export default function App() {
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-40 border-b border-[#2a2540]/80 bg-[#07060d]/85 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-4 py-4">
          <div>
            <div className="text-[10px] tracking-[0.35em] uppercase text-[#f9e7b0]/80">
              TerAustralis Incognita
            </div>
            <div className="font-serif text-lg text-[#fdf6e3]">Mythic Canon · 16</div>
          </div>
          <nav className="flex flex-wrap gap-5">
            <NavLink to="/" end className={link}>Gallery</NavLink>
            <NavLink to="/codex" className={link}>Lore Codex</NavLink>
            <NavLink to="/prompts" className={link}>Prompt Library</NavLink>
            <NavLink to="/download" className={link}>Download Pack</NavLink>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8 md:py-12">
        <Routes>
          <Route path="/" element={<GalleryPage />} />
          <Route path="/codex" element={<CodexPage />} />
          <Route path="/prompts" element={<PromptsPage />} />
          <Route path="/download" element={<DownloadPage />} />
        </Routes>
      </main>
      <footer className="border-t border-[#2a2540]/60 py-8 text-center text-[10px] tracking-[0.25em] uppercase text-[#5a4a7a]">
        Custom fan set · Not affiliated with Wizards of the Coast · CC BY-NC-ND 4.0 · Non Solus
      </footer>
    </div>
  )
}
