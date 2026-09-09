import { listDocs } from '$lib/docs.js';

export const prerender = true;

export function load() {
  return { docs: listDocs() };
}
