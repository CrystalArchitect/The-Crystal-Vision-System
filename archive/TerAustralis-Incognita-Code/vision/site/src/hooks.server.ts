// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

import { sequence } from '@sveltejs/kit/hooks';
import type { Handle } from '@sveltejs/kit';
import { checkPublicLimit, getIdentifier } from '$lib/server/ratelimit';

/**
 * Request logging (observation-grade)
 * Records: method, path, status, duration
 * Never logs: bodies, cookies, headers, fingerprinting data
 */
const requestLog: Handle = async ({ event, resolve }) => {
	const start = Date.now();
	const { method } = event.request;
	const path = event.url.pathname;

	const response = await resolve(event);

	const duration = Date.now() - start;
	const status = response.status;

	// Structured, privacy-safe log
	// Can be shipped to Vercel logs or Sentry breadcrumbs in production
	console.info(
		JSON.stringify({
			type: 'request',
			method,
			path,
			status,
			duration_ms: duration,
			ts: new Date().toISOString()
		})
	);

	return response;
};

/**
 * Rate limiting (Upstash)
 * Skip static assets and common file types
 */
const rateLimit: Handle = async ({ event, resolve }) => {
	const path = event.url.pathname;

	// Expanded asset skip list
	if (
		path.startsWith('/_app') ||
		path.startsWith('/_svelte') ||
		path.startsWith('/favicon') ||
		path.startsWith('/robots') ||
		path.endsWith('.js') ||
		path.endsWith('.css') ||
		path.endsWith('.woff2') ||
		path.endsWith('.png') ||
		path.endsWith('.svg') ||
		path.endsWith('.ico')
	) {
		return resolve(event);
	}

	const identifier = getIdentifier(event.request);
	const { success, limit, remaining, reset } = await checkPublicLimit(identifier);

	if (!success) {
		return new Response('Too Many Requests', {
			status: 429,
			headers: {
				'Retry-After': Math.ceil((reset - Date.now()) / 1000).toString(),
				'X-RateLimit-Limit': limit.toString(),
				'X-RateLimit-Remaining': '0',
				'X-RateLimit-Reset': reset.toString()
			}
		});
	}

	const response = await resolve(event);
	response.headers.set('X-RateLimit-Limit', limit.toString());
	response.headers.set('X-RateLimit-Remaining', remaining.toString());
	response.headers.set('X-RateLimit-Reset', reset.toString());

	return response;
};

/**
 * Security & privacy headers
 * Complements headers from vercel.json
 */
const securityHeaders: Handle = async ({ event, resolve }) => {
	const response = await resolve(event);

	response.headers.set('X-Content-Type-Options', 'nosniff');
	response.headers.set('X-Frame-Options', 'DENY');
	response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
	response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');

	return response;
};

/**
 * Composed handle sequence
 * Order: log → rate-limit → security
 */
export const handle = sequence(requestLog, rateLimit, securityHeaders);
