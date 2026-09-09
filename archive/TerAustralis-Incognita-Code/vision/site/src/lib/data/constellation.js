// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

// Single source of truth for the homepage constellation — accepted from
// the Phase I architecture plan ("data-driven, not hard-coded").
// Seven lights, seven real doors: every node here must be a route that
// actually opens. Dreamed destinations get no star until something
// exists behind them (the Incognita Rule).

/**
 * @typedef {Object} ConstellationNode
 * @property {number} x - viewBox x (0–800)
 * @property {number} y - viewBox y (0–400)
 * @property {number} r - star radius
 * @property {string} color - CSS custom property from the site palette
 * @property {string} label - display name
 * @property {string} sub - one-breath description
 * @property {string} href - a live route
 */

/** @type {ConstellationNode[]} */
export const constellationNodes = [
  { x: 130, y: 300, r: 9,  color: 'var(--gold)',   label: 'The Codex',      sub: 'the story',      href: '/codex' },
  { x: 255, y: 180, r: 10, color: 'var(--purple)', label: 'CrystalCore.OS', sub: 'fly the mythos', href: '/crystalcore-os' },
  { x: 400, y: 250, r: 12, color: 'var(--green)',  label: 'Clementine',     sub: 'the companion',  href: '/clementine' },
  { x: 395, y: 95,  r: 8,  color: 'var(--blue)',   label: 'Starline',       sub: 'the protocol',   href: '/starline' },
  { x: 545, y: 165, r: 9,  color: 'var(--silver)', label: 'The Archive',    sub: 'every document', href: '/docs' },
  { x: 585, y: 320, r: 8,  color: 'var(--pink)',   label: 'The Gallery',    sub: 'the art',        href: '/gallery' },
  { x: 700, y: 235, r: 9,  color: 'var(--gold)',   label: 'Join',           sub: 'walk with us',   href: '/join' }
];

// The asterism: which lights are drawn joined (index pairs).
export const constellationLines = [
  [0, 1], [1, 2], [1, 3], [3, 4], [2, 4], [4, 5], [4, 6], [5, 6]
];
