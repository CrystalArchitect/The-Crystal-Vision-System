import { useEffect, useState } from "react";
import { useRoute, useLocation } from "wouter";
import Navbar from "@/components/Navbar";
import { getMythosById, getChapterById, MythosChapter } from "@/data/mythos";
import { motion } from "framer-motion";
import { ChevronLeft, ChevronRight, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Streamdown } from "streamdown";

export default function CodexReader() {
  const [match, params] = useRoute("/codex/:collection/:chapter");
  const [, setLocation] = useLocation();
  const [chapter, setChapter] = useState<MythosChapter | null>(null);
  const [collection, setCollection] = useState<any>(null);

  useEffect(() => {
    if (match && params) {
      const coll = getMythosById(params.collection);
      const chap = getChapterById(params.collection, params.chapter);
      setCollection(coll);
      setChapter(chap || null);
    }
  }, [match, params]);

  if (!chapter || !collection) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground font-mono">CHAPTER NOT FOUND</p>
        </div>
      </div>
    );
  }

  const currentIndex = collection.chapters.findIndex((c: MythosChapter) => c.id === chapter.id);
  const prevChapter = currentIndex > 0 ? collection.chapters[currentIndex - 1] : null;
  const nextChapter = currentIndex < collection.chapters.length - 1 ? collection.chapters[currentIndex + 1] : null;

  return (
    <div className="min-h-screen bg-background font-sans">
      <Navbar />
      
      {/* Reading Experience */}
      <div className="container pt-32 pb-20">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-16"
          >
            <div className="flex items-center gap-4 mb-6">
              <span className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary">
                {collection.name}
              </span>
              <div className="flex-1 h-px bg-gradient-to-r from-primary/50 to-transparent" />
            </div>
            
            <h1 className="font-serif text-5xl md:text-6xl font-bold mb-4 leading-tight">
              {chapter.title}
            </h1>
            
            {chapter.subtitle && (
              <p className="text-2xl text-primary font-serif italic mb-8">
                "{chapter.subtitle}"
              </p>
            )}

            <div className="flex items-center gap-6 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4" />
                <span className="font-mono">{chapter.readTime} MIN READ</span>
              </div>
              <div className="flex gap-2">
                {chapter.tags.map(tag => (
                  <span key={tag} className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] uppercase tracking-widest">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Divider */}
          <div className="h-px bg-gradient-to-r from-transparent via-primary/20 to-transparent mb-16" />

          {/* Content */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="prose prose-invert prose-primary max-w-none mb-20"
          >
            <Streamdown>{chapter.content}</Streamdown>
          </motion.div>

          {/* Divider */}
          <div className="h-px bg-gradient-to-r from-transparent via-primary/20 to-transparent mb-16" />

          {/* Navigation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="grid grid-cols-2 gap-8"
          >
            {prevChapter ? (
              <button
                onClick={() => setLocation(`/codex/${params?.collection}/${prevChapter.id}`)}
                className="group text-left p-6 rounded-xl border border-white/10 hover:border-primary/50 transition-all hover:bg-white/5"
              >
                <div className="flex items-center gap-2 mb-3 text-primary group-hover:translate-x-1 transition-transform">
                  <ChevronLeft className="h-4 w-4" />
                  <span className="font-mono text-[10px] uppercase tracking-widest">PREVIOUS</span>
                </div>
                <p className="font-serif text-lg font-bold group-hover:text-primary transition-colors">
                  {prevChapter.title}
                </p>
              </button>
            ) : (
              <div />
            )}

            {nextChapter ? (
              <button
                onClick={() => setLocation(`/codex/${params?.collection}/${nextChapter.id}`)}
                className="group text-right p-6 rounded-xl border border-white/10 hover:border-primary/50 transition-all hover:bg-white/5"
              >
                <div className="flex items-center justify-end gap-2 mb-3 text-primary group-hover:-translate-x-1 transition-transform">
                  <span className="font-mono text-[10px] uppercase tracking-widest">NEXT</span>
                  <ChevronRight className="h-4 w-4" />
                </div>
                <p className="font-serif text-lg font-bold group-hover:text-primary transition-colors">
                  {nextChapter.title}
                </p>
              </button>
            ) : (
              <div />
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
