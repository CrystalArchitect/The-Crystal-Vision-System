// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

let publicLimiterInstance: Ratelimit | null = null;
let strictLimiterInstance: Ratelimit | null = null;

// Lazy initialization — env vars are injected at runtime by Vercel
function initLimiters() {
	if (publicLimiterInstance) return;

	const url = process.env.KV_REST_API_URL;
	const token = process.env.KV_REST_API_TOKEN;

	if (!url || !token) {
		console.warn(
			'Upstash credentials not found. Rate limiting will be disabled. ' +
				'Ensure KV_REST_API_URL and KV_REST_API_TOKEN are set in Vercel environment.'
		);
		return;
	}

	const redis = new Redis({ url, token });

	publicLimiterInstance = new Ratelimit({
		redis,
		limiter: Ratelimit.slidingWindow(60, '1 m'),
		analytics: true,
		prefix: 'ratelimit:public'
	});

	strictLimiterInstance = new Ratelimit({
		redis,
		limiter: Ratelimit.slidingWindow(10, '1 m'),
		analytics: true,
		prefix: 'ratelimit:strict'
	});
}

export async function checkPublicLimit(identifier: string) {
	initLimiters();
	if (!publicLimiterInstance) return { success: true, limit: 0, remaining: 0, reset: 0 };
	return publicLimiterInstance.limit(identifier);
}

export async function checkStrictLimit(identifier: string) {
	initLimiters();
	if (!strictLimiterInstance) return { success: true, limit: 0, remaining: 0, reset: 0 };
	return strictLimiterInstance.limit(identifier);
}

export function getIdentifier(request: Request): string {
	const forwarded = request.headers.get('x-forwarded-for');
	if (forwarded) {
		return forwarded.split(',')[0].trim();
	}
	return 'anonymous';
}
