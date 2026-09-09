import { Link } from "wouter";
import { Button } from "@/components/ui/button";

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-background/80 backdrop-blur-xl">
      <div className="container h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <img 
            src="/manus-storage/logo_d35dd45c.png" 
            alt="TerAustralis Incognita" 
            className="h-10 w-10 object-contain group-hover:scale-110 transition-transform duration-300" 
          />
          <span className="font-serif text-xl font-bold tracking-tight text-primary">
            TerAustralis
          </span>
        </Link>
        
        <div className="hidden md:flex items-center gap-8">
          <Link href="/codex" className="font-mono text-sm uppercase tracking-widest hover:text-primary transition-colors">Codex</Link>
          <Link href="/starline" className="font-mono text-sm uppercase tracking-widest hover:text-primary transition-colors">Starline</Link>
          <Link href="/gallery" className="font-mono text-sm uppercase tracking-widest hover:text-primary transition-colors">Gallery</Link>
          <Link href="/archive" className="font-mono text-sm uppercase tracking-widest hover:text-primary transition-colors">Archive</Link>
        </div>

        <div className="flex items-center gap-4">
          <Button variant="outline" className="font-mono text-xs border-primary/50 text-primary hover:bg-primary/10 transition-all active:scale-95">
            BOOT OS
          </Button>
        </div>
      </div>
    </nav>
  );
}
