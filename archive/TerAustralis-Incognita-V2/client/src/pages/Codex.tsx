import Navbar from "@/components/Navbar";
import { motion } from "framer-motion";
import { MYTHOS_DATA } from "@/data/mythos";
import { Link } from "wouter";
import { ChevronRight, Clock } from "lucide-react";

export default function Codex() {
  return (
    <div className="min-h-screen bg-background font-sans">
      <Navbar />
      <div className="container pt-32 pb-20">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-16"
          >
            <h1 className="font-serif text-5xl md:text-6xl font-bold mb-6">The Archive</h1>
            <p className="text-xl text-muted-foreground leading-relaxed max-w-2xl">
              The collected mythos of TerAustralis Incognita. Navigate the deep knowledge, transmissions, and stories that define the sovereign vision.
            </p>
          </motion.div>

          {/* Collections Grid */}
          <div className="grid gap-12">
            {MYTHOS_DATA.map((collection, idx) => (
              <motion.div
                key={collection.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: idx * 0.1 }}
              >
                <div className="mb-8">
                  <h2 className="font-serif text-3xl font-bold mb-2">{collection.name}</h2>
                  <p className="text-muted-foreground">{collection.description}</p>
                </div>

                <div className="space-y-4">
                  {collection.chapters.map((chapter) => (
                    <Link key={chapter.id} href={`/codex/${collection.id}/${chapter.id}`}>
                      <a className="group block p-6 rounded-xl border border-white/10 hover:border-primary/50 transition-all hover:bg-white/5 cursor-pointer">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h3 className="font-serif text-xl font-bold mb-2 group-hover:text-primary transition-colors">
                              {chapter.title}
                            </h3>
                            {chapter.subtitle && (
                              <p className="text-muted-foreground italic mb-3">
                                "{chapter.subtitle}"
                              </p>
                            )}
                            <div className="flex items-center gap-4 text-sm text-muted-foreground">
                              <div className="flex items-center gap-2">
                                <Clock className="h-4 w-4" />
                                <span className="font-mono text-[10px] uppercase tracking-widest">
                                  {chapter.readTime} MIN
                                </span>
                              </div>
                              <div className="flex gap-2">
                                {chapter.tags.map(tag => (
                                  <span key={tag} className="px-2 py-1 rounded bg-white/5 text-[10px] uppercase tracking-widest">
                                    {tag}
                                  </span>
                                ))}
                              </div>
                            </div>
                          </div>
                          <ChevronRight className="h-5 w-5 text-primary mt-1 group-hover:translate-x-1 transition-transform" />
                        </div>
                      </a>
                    </Link>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
