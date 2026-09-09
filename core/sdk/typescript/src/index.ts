// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

/**
 * Crystal Core TypeScript SDK — Phase 1 client for local node agent.
 * Mainnet HOLD. Auth (DID challenge + capability macaroon) planned.
 */

export type Health = {
  ok: boolean;
  did?: string;
  region?: string;
  authority?: string;
  [key: string]: unknown;
};

export type ServiceReceipt = {
  id: string;
  class: string;
  qty: string | number;
  status: "pending" | "confirmed" | string;
  credit_currency?: string;
  credit_debit?: string | number;
};

export type CrystalClientOptions = {
  /** Local agent default: http://127.0.0.1:8787 */
  baseUrl?: string;
  fetchImpl?: typeof fetch;
};

export class CrystalClient {
  readonly baseUrl: string;
  private readonly fetchImpl: typeof fetch;

  constructor(opts: CrystalClientOptions = {}) {
    this.baseUrl = (opts.baseUrl ?? "http://127.0.0.1:8787").replace(/\/$/, "");
    this.fetchImpl = opts.fetchImpl ?? fetch.bind(globalThis);
  }

  private async json<T>(path: string, init?: RequestInit): Promise<T> {
    const res = await this.fetchImpl(`${this.baseUrl}${path}`, {
      ...init,
      headers: {
        Accept: "application/json",
        ...(init?.body ? { "Content-Type": "application/json" } : {}),
        ...(init?.headers ?? {}),
      },
    });
    if (!res.ok) {
      const text = await res.text().catch(() => "");
      throw new Error(`CrystalClient ${path} → ${res.status} ${text}`);
    }
    return (await res.json()) as T;
  }

  health(): Promise<Health> {
    return this.json<Health>("/health");
  }

  manifest(): Promise<Record<string, unknown>> {
    return this.json("/manifest");
  }

  listReceipts(): Promise<ServiceReceipt[] | { receipts: ServiceReceipt[] }> {
    return this.json("/receipts");
  }

  createPendingReceipt(body: {
    class: string;
    qty: string | number;
    credit_currency?: string;
  }): Promise<ServiceReceipt> {
    return this.json("/receipts/pending", {
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  confirmReceipt(id: string): Promise<ServiceReceipt> {
    return this.json(`/receipts/${encodeURIComponent(id)}/confirm`, {
      method: "POST",
      body: JSON.stringify({}),
    });
  }

  twinEvents(): Promise<unknown> {
    return this.json("/twin/events");
  }

  layers(): Promise<unknown> {
    return this.json("/layers");
  }
}

/** Demo helper: Vision-shaped credit spend (client-side only until region API). */
export function previewCreditSpend(credits: number, cost: number): {
  ok: boolean;
  remaining: number;
} {
  if (cost > credits) return { ok: false, remaining: credits };
  return { ok: true, remaining: Math.round((credits - cost) * 1000) / 1000 };
}

export const VERSION = "0.5.0";
