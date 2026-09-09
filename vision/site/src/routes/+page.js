// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

import { listDocs } from '$lib/docs.js';

export const prerender = true;

export function load() {
  return { docs: listDocs() };
}
