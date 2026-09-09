// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

import { atlasPlates } from '$lib/atlas';

export const prerender = true;

export function load() {
  return { plates: atlasPlates };
}
