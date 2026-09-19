import { Button } from "@/components/ui/button";
import Navbar from "@/components/Navbar";
import { motion } from "framer-motion";
import { ChevronRight, Database, Globe, Zap } from "lucide-react";
import { Link } from "wouter";

export default function Home() {
  return (
    <div className="min-h-screen bg-background font-sans overflow-x-hidden">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center pt-16">
        <div className="absolute inset-0 z-0">
          <img 
            src="/manus-storage/hero-bg_0d7db17d.png" 
            alt="Space Background" 
            className="w-full h-full object-cover opacity-60"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-background/0 via-background/40 to-background" />
        </div>

        <div className="container relative z-10">
          <div className="max-w-4xl">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: [0.23, 1, 0.32, 1] }}
            >
              <span className="font-mono text-primary text-sm tracking-[0.3em] uppercase mb-4 block">
                Incognita Lattice v2.0
              </span>
              <h1 className="font-serif text-6xl md:text-8xl font-bold leading-tight mb-8">
                The Red Dust <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-accent to-primary bg-[length:200%_auto] animate-gradient">Remembers the Stars</span>
              </h1>
              <p className="text-muted-foreground text-xl md:text-2xl max-w-2xl mb-12 leading-relaxed">
                TerAustralis Incognita is a sovereign mythos for the space age. 
                Bridging ancient Songlines with the reach for the deep black.
              </p>
              
              <div className="flex flex-wrap gap-6">
                <Link href="/crystalcore-os">
                  <Button size="lg" className="h-14 px-8 text-lg font-mono tracking-wide bg-primary text-primary-foreground hover:bg-primary/90 active:scale-95 transition-all">
                    INITIALIZE BOOT
                    <ChevronRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <Link href="/codex">
                  <a className="inline-flex items-center justify-center h-14 px-8 text-lg font-mono tracking-wide border border-white/20 hover:bg-white/5 active:scale-95 transition-all rounded-md">
                    EXPLORE CODEX
                  </a>
                </Link>
              </div>
            </motion.div>
          </div>
        </div>
        
        {/* Floating Starline Indicator */}
        <div className="absolute bottom-12 left-1/2 -translate-x-1/2 flex flex-col items-center gap-4 animate-bounce opacity-50">
          <span className="font-mono text-[10px] uppercase tracking-widest">Descent Protocol</span>
          <div className="w-px h-12 bg-gradient-to-b from-primary to-transparent" />
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-32 relative">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<Globe className="h-8 w-8 text-primary" />}
              title="Sovereign Earth"
              description="The red heart of the continent serves as the primary terrestrial hub for the Incognita Lattice."
            />
            <FeatureCard 
              icon={<Zap className="h-8 w-8 text-accent" />}
              title="Starline Protocol"
              description="P2P decentralized communication using Noise IK handshakes for secure, unbought interaction."
            />
            <FeatureCard 
              icon={<Database className="h-8 w-8 text-emerald-400" />}
              title="Emotion Warehouse"
              description="Local-first active learning models that prioritize human emotional intelligence and data sovereignty."
            />
          </div>
        </div>
      </section>

      {/* Narrative Section */}
      <section className="py-32 bg-secondary/30 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-white/10 to-transparent" />
        <div className="container relative z-10">
          <div className="flex flex-col md:flex-row items-center gap-20">
            <div className="flex-1">
              <img 
                src="/manus-storage/terminal-view_e65fbd0c.png" 
                alt="CrystalCore Terminal" 
                className="rounded-xl border border-white/10 shadow-2xl shadow-primary/10"
              />
            </div>
            <div className="flex-1">
              <h2 className="font-serif text-4xl md:text-5xl font-bold mb-8">CrystalCore.OS</h2>
              <p className="text-muted-foreground text-lg leading-relaxed mb-8">
                More than just a terminal—CrystalCore.OS is your window into the Starline. 
                Collect the Five Keys, synchronize your signature, and unlock the First Gate. 
                Experience the mythos through an interactive command-line interface designed 
                for the sovereign researcher.
              </p>
              <Link href="/crystalcore-os">
                <Button variant="link" className="text-primary p-0 h-auto text-lg font-mono hover:no-underline group">
                  LAUNCH TERMINAL 
                  <ChevronRight className="ml-1 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-20 border-t border-white/5 bg-background">
        <div className="container">
          <div className="flex flex-col md:flex-row justify-between items-start gap-12">
            <div className="max-w-sm">
              <div className="flex items-center gap-3 mb-6">
                <img src="/manus-storage/logo_d35dd45c.png" alt="Logo" className="h-8 w-8" />
                <span className="font-serif text-xl font-bold">TerAustralis</span>
              </div>
              <p className="text-muted-foreground text-sm leading-relaxed">
                A speculative futures project by Crystal Arena-Turner. 
                Non Solus — Not Alone.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-20">
              <FooterColumn 
                title="Lattice" 
                links={["Codex", "Starline", "Gallery", "Archive"]} 
              />
              <FooterColumn 
                title="Sovereign" 
                links={["Clementine", "Protocol", "GitHub", "X / Twitter"]} 
              />
            </div>
          </div>
          <div className="mt-20 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between gap-4">
            <p className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
              © 2026 CrystalCore.OS // ALL DATA SOVEREIGN
            </p>
            <p className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
              Synchronized via Incognita Lattice v2.0
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <div className="p-8 rounded-2xl border border-white/5 bg-white/[0.02] backdrop-blur-sm hover:border-primary/30 transition-all group">
      <div className="mb-6 p-3 rounded-xl bg-white/5 w-fit group-hover:scale-110 transition-transform">
        {icon}
      </div>
      <h3 className="font-serif text-2xl font-bold mb-4">{title}</h3>
      <p className="text-muted-foreground leading-relaxed text-sm">
        {description}
      </p>
    </div>
  );
}

function FooterColumn({ title, links }: { title: string, links: string[] }) {
  return (
    <div>
      <h4 className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary mb-6">{title}</h4>
      <ul className="space-y-4">
        {links.map(link => (
          <li key={link}>
            <a href="#" className="text-sm text-muted-foreground hover:text-white transition-colors">{link}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}
