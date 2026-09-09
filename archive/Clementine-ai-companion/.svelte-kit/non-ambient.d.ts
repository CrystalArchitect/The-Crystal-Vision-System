
// this file is generated — do not edit it


declare module "svelte/elements" {
	export interface HTMLAttributes<T> {
		'data-sveltekit-keepfocus'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-noscroll'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-preload-code'?:
			| true
			| ''
			| 'eager'
			| 'viewport'
			| 'hover'
			| 'tap'
			| 'off'
			| undefined
			| null;
		'data-sveltekit-preload-data'?: true | '' | 'hover' | 'tap' | 'off' | undefined | null;
		'data-sveltekit-reload'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-replacestate'?: true | '' | 'off' | undefined | null;
	}
}

export {};


declare module "$app/types" {
	type MatcherParam<M> = M extends (param : string) => param is (infer U extends string) ? U : string;

	export interface AppTypes {
		RouteId(): "/" | "/apocryphon" | "/clementine" | "/codex" | "/docs" | "/docs/[slug]";
		RouteParams(): {
			"/docs/[slug]": { slug: string }
		};
		LayoutParams(): {
			"/": { slug?: string | undefined };
			"/apocryphon": Record<string, never>;
			"/clementine": Record<string, never>;
			"/codex": Record<string, never>;
			"/docs": { slug?: string | undefined };
			"/docs/[slug]": { slug: string }
		};
		Pathname(): "/" | "/apocryphon" | "/clementine" | "/codex" | "/docs" | `/docs/${string}` & {} | `/docs/${string}/` & {};
		ResolvedPathname(): `${"" | `/${string}`}${ReturnType<AppTypes['Pathname']>}`;
		Asset(): "/assets/codex-cover.jpeg" | "/favicon.svg" | string & {};
	}
}