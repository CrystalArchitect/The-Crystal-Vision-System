import { error } from '@sveltejs/kit';
import { docs, getDoc, renderMarkdown } from '$lib/docs.js';

export const prerender = true;

export function entries() {
  return docs.map((doc) => ({ slug: doc.slug }));
}

/** @param {{ params: { slug: string } }} event */
export function load({ params }) {
  const doc = getDoc(params.slug);
  if (!doc) {
    throw error(404, 'Document not found');
  }
  return {
    slug: doc.slug,
    title: doc.title,
    description: doc.description,
    html: renderMarkdown(doc.raw)
  };
}
