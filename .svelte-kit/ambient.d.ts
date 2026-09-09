
// this file is generated — do not edit it


/// <reference types="@sveltejs/kit" />

/**
 * This module provides access to environment variables that are injected _statically_ into your bundle at build time and are limited to _private_ access.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Static environment variables are [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env` at build time and then statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * **_Private_ access:**
 * 
 * - This module cannot be imported into client-side code
 * - This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured)
 * 
 * For example, given the following build time environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { ENVIRONMENT, PUBLIC_BASE_URL } from '$env/static/private';
 * 
 * console.log(ENVIRONMENT); // => "production"
 * console.log(PUBLIC_BASE_URL); // => throws error during build
 * ```
 * 
 * The above values will be the same _even if_ different values for `ENVIRONMENT` or `PUBLIC_BASE_URL` are set at runtime, as they are statically replaced in your code with their build time values.
 */
declare module '$env/static/private' {
	export const CLAUDE_CODE_CONTAINER_ID: string;
	export const CLAUDE_CODE_BASE_REF: string;
	export const GITHUB_TOKEN: string;
	export const GRPC_DEFAULT_SSL_ROOTS_FILE_PATH: string;
	export const GLOBAL_AGENT_HTTPS_PROXY: string;
	export const CLAUDE_CODE_REMOTE_HERMETIC_MODE: string;
	export const CURL_CA_BUNDLE: string;
	export const HTTPS_PROXY: string;
	export const CLAUDE_CODE_POST_FOR_SESSION_INGRESS_V2: string;
	export const UV_NATIVE_TLS: string;
	export const CCR_AGENT_PROXY_ENABLED: string;
	export const no_proxy: string;
	export const AI_AGENT: string;
	export const NODE_EXTRA_CA_CERTS: string;
	export const CLOUDSDK_AUTH_ACCESS_TOKEN: string;
	export const CLAUDE_CODE_ENTRYPOINT: string;
	export const CLAUDE_CODE_REMOTE_SEND_KEEPALIVES: string;
	export const RUST_BACKTRACE: string;
	export const npm_config_user_agent: string;
	export const CCR_ENABLE_TRACING: string;
	export const JAVA_TOOL_OPTIONS: string;
	export const GIT_EDITOR: string;
	export const GH_TOKEN: string;
	export const ANT_IMAGE_TAG: string;
	export const GIT_ASKPASS: string;
	export const BUN_INSTALL: string;
	export const DOCKER_HTTPS_PROXY: string;
	export const npm_node_execpath: string;
	export const GIT_SSL_CAINFO: string;
	export const SHLVL: string;
	export const npm_config_noproxy: string;
	export const HOME: string;
	export const GIT_CONFIG_COUNT: string;
	export const CLAUDE_CODE_SYNC_SKILLS: string;
	export const RBENV_ROOT: string;
	export const OLDPWD: string;
	export const NO_PROXY: string;
	export const npm_package_json: string;
	export const PYTHONUNBUFFERED: string;
	export const NODE_OPTIONS: string;
	export const CCR_EGRESS_GATEWAY_ENABLED: string;
	export const CLAUDE_CODE_CHILD_SESSION: string;
	export const CLAUDE_CODE_WEBSOCKET_AUTH_FILE_DESCRIPTOR: string;
	export const CCR_SPAWN_TIMESTAMP_MS: string;
	export const SSL_CERT_FILE: string;
	export const HEX_CACERTS_PATH: string;
	export const npm_config_userconfig: string;
	export const npm_config_local_prefix: string;
	export const DOCUMENTS_MCP_SCRATCH_ROOT: string;
	export const AWS_CA_BUNDLE: string;
	export const USE_BUILTIN_RIPGREP: string;
	export const COLOR: string;
	export const CLAUDE_ADDITIONAL_DIRECTORIES: string;
	export const npm_config_https_proxy: string;
	export const https_proxy: string;
	export const GCM_INTERACTIVE: string;
	export const CLAUDE_CODE_TEE_SDK_STDOUT: string;
	export const CLAUDE_SESSION_INGRESS_TOKEN_FILE: string;
	export const CCR_SETTINGS_JSON_OVERLAY: string;
	export const FSSPEC_GCS: string;
	export const _: string;
	export const npm_config_prefix: string;
	export const npm_config_npm_version: string;
	export const CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE: string;
	export const CLAUDE_CODE_REMOTE: string;
	export const ANTHROPIC_BASE_URL: string;
	export const TERM: string;
	export const npm_config_cache: string;
	export const CLAUDE_CODE_USER_EMAIL: string;
	export const MCP_TOOL_TIMEOUT: string;
	export const RUSTUP_HOME: string;
	export const YARN_HTTPS_PROXY: string;
	export const CLAUDE_CODE_ACCOUNT_UUID: string;
	export const SKIP_PLUGIN_MARKETPLACE: string;
	export const CLAUDE_AFTER_LAST_COMPACT: string;
	export const CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE: string;
	export const GIT_CONFIG_VALUE_0: string;
	export const MCP_CONNECTION_NONBLOCKING: string;
	export const npm_config_node_gyp: string;
	export const PATH: string;
	export const DENO_TLS_CA_STORE: string;
	export const GIT_CONFIG_VALUE_1: string;
	export const REQUESTS_CA_BUNDLE: string;
	export const NODE: string;
	export const npm_package_name: string;
	export const COREPACK_ENABLE_AUTO_PIN: string;
	export const PLAYWRIGHT_BROWSERS_PATH: string;
	export const GIT_CONFIG_VALUE_2: string;
	export const CLAUDE_CODE_ORGANIZATION_UUID: string;
	export const ENVRUNNER_SKIP_ACK: string;
	export const CLAUDE_EFFORT: string;
	export const CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST: string;
	export const CLAUDE_CODE_PROXY_RESOLVES_HOSTS: string;
	export const CLAUDE_CODE_DIAGNOSTICS_FILE: string;
	export const CLAUDE_PID: string;
	export const NoDefaultCurrentDirectoryInExePath: string;
	export const TRACEPARENT: string;
	export const CLAUDE_CODE_DISABLE_BUILTIN_ANTMCP: string;
	export const CLAUDE_CODE_USE_CCR_V2: string;
	export const DENO_CERT: string;
	export const CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD: string;
	export const CLAUDE_CODE_WORKER_EPOCH: string;
	export const BUN_OPTIONS: string;
	export const CLAUDE_CODE_ENVIRONMENT_RUNNER_VERSION: string;
	export const ELECTRON_GET_USE_PROXY: string;
	export const npm_lifecycle_script: string;
	export const CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: string;
	export const CCR_UPSTREAM_PROXY_ENABLED: string;
	export const CCR_TEST_GITPROXY: string;
	export const CLAUDE_ENABLE_STREAM_WATCHDOG: string;
	export const HTTPLIB2_CA_CERTS: string;
	export const DEBIAN_FRONTEND: string;
	export const SHELL: string;
	export const GLOBAL_AGENT_NO_PROXY: string;
	export const GIT_TERMINAL_PROMPT: string;
	export const npm_package_version: string;
	export const npm_lifecycle_event: string;
	export const CLAUDE_AUTO_BACKGROUND_TASKS: string;
	export const AWS_ACCESS_KEY_ID: string;
	export const GIT_CONFIG_KEY_0: string;
	export const CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR: string;
	export const CLAUDE_CODE_SESSION_ID: string;
	export const CLOUDSDK_PROXY_TYPE: string;
	export const AWS_SECRET_ACCESS_KEY: string;
	export const CLAUDE_CODE_VERSION: string;
	export const GIT_CONFIG_KEY_1: string;
	export const CLAUDECODE: string;
	export const NIX_SSL_CERT_FILE: string;
	export const CLOUDSDK_PROXY_ADDRESS: string;
	export const GIT_CONFIG_KEY_2: string;
	export const CLOUDSDK_PROXY_PORT: string;
	export const npm_config_globalconfig: string;
	export const npm_config_init_module: string;
	export const MAX_THINKING_TOKENS: string;
	export const CLAUDE_CODE_DEBUG: string;
	export const JAVA_HOME: string;
	export const PWD: string;
	export const npm_execpath: string;
	export const CLAUDE_CODE_EXECPATH: string;
	export const npm_config_global_prefix: string;
	export const IS_SANDBOX: string;
	export const ENV_MANAGER_ENABLE_DIAG_LOGS: string;
	export const USE_SHTTP_MCP: string;
	export const CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH: string;
	export const npm_command: string;
	export const CLAUDE_CODE_MESSAGING_SOCKET: string;
	export const ANT_IMAGE_REPOSITORY: string;
	export const CLAUDE_CODE_REMOTE_SESSION_ID: string;
	export const CARGO_HTTP_CAINFO: string;
	export const PIP_CERT: string;
	export const INIT_CWD: string;
	export const EDITOR: string;
	export const NODE_ENV: string;
}

/**
 * This module provides access to environment variables that are injected _statically_ into your bundle at build time and are _publicly_ accessible.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Static environment variables are [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env` at build time and then statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * **_Public_ access:**
 * 
 * - This module _can_ be imported into client-side code
 * - **Only** variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`) are included
 * 
 * For example, given the following build time environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { ENVIRONMENT, PUBLIC_BASE_URL } from '$env/static/public';
 * 
 * console.log(ENVIRONMENT); // => throws error during build
 * console.log(PUBLIC_BASE_URL); // => "http://site.com"
 * ```
 * 
 * The above values will be the same _even if_ different values for `ENVIRONMENT` or `PUBLIC_BASE_URL` are set at runtime, as they are statically replaced in your code with their build time values.
 */
declare module '$env/static/public' {
	
}

/**
 * This module provides access to environment variables set _dynamically_ at runtime and that are limited to _private_ access.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Dynamic environment variables are defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`.
 * 
 * **_Private_ access:**
 * 
 * - This module cannot be imported into client-side code
 * - This module includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured)
 * 
 * > [!NOTE] In `dev`, `$env/dynamic` includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 * 
 * > [!NOTE] To get correct types, environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * >
 * > ```env
 * > MY_FEATURE_FLAG=
 * > ```
 * >
 * > You can override `.env` values from the command line like so:
 * >
 * > ```sh
 * > MY_FEATURE_FLAG="enabled" npm run dev
 * > ```
 * 
 * For example, given the following runtime environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://site.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { env } from '$env/dynamic/private';
 * 
 * console.log(env.ENVIRONMENT); // => "production"
 * console.log(env.PUBLIC_BASE_URL); // => undefined
 * ```
 */
declare module '$env/dynamic/private' {
	export const env: {
		CLAUDE_CODE_CONTAINER_ID: string;
		CLAUDE_CODE_BASE_REF: string;
		GITHUB_TOKEN: string;
		GRPC_DEFAULT_SSL_ROOTS_FILE_PATH: string;
		GLOBAL_AGENT_HTTPS_PROXY: string;
		CLAUDE_CODE_REMOTE_HERMETIC_MODE: string;
		CURL_CA_BUNDLE: string;
		HTTPS_PROXY: string;
		CLAUDE_CODE_POST_FOR_SESSION_INGRESS_V2: string;
		UV_NATIVE_TLS: string;
		CCR_AGENT_PROXY_ENABLED: string;
		no_proxy: string;
		AI_AGENT: string;
		NODE_EXTRA_CA_CERTS: string;
		CLOUDSDK_AUTH_ACCESS_TOKEN: string;
		CLAUDE_CODE_ENTRYPOINT: string;
		CLAUDE_CODE_REMOTE_SEND_KEEPALIVES: string;
		RUST_BACKTRACE: string;
		npm_config_user_agent: string;
		CCR_ENABLE_TRACING: string;
		JAVA_TOOL_OPTIONS: string;
		GIT_EDITOR: string;
		GH_TOKEN: string;
		ANT_IMAGE_TAG: string;
		GIT_ASKPASS: string;
		BUN_INSTALL: string;
		DOCKER_HTTPS_PROXY: string;
		npm_node_execpath: string;
		GIT_SSL_CAINFO: string;
		SHLVL: string;
		npm_config_noproxy: string;
		HOME: string;
		GIT_CONFIG_COUNT: string;
		CLAUDE_CODE_SYNC_SKILLS: string;
		RBENV_ROOT: string;
		OLDPWD: string;
		NO_PROXY: string;
		npm_package_json: string;
		PYTHONUNBUFFERED: string;
		NODE_OPTIONS: string;
		CCR_EGRESS_GATEWAY_ENABLED: string;
		CLAUDE_CODE_CHILD_SESSION: string;
		CLAUDE_CODE_WEBSOCKET_AUTH_FILE_DESCRIPTOR: string;
		CCR_SPAWN_TIMESTAMP_MS: string;
		SSL_CERT_FILE: string;
		HEX_CACERTS_PATH: string;
		npm_config_userconfig: string;
		npm_config_local_prefix: string;
		DOCUMENTS_MCP_SCRATCH_ROOT: string;
		AWS_CA_BUNDLE: string;
		USE_BUILTIN_RIPGREP: string;
		COLOR: string;
		CLAUDE_ADDITIONAL_DIRECTORIES: string;
		npm_config_https_proxy: string;
		https_proxy: string;
		GCM_INTERACTIVE: string;
		CLAUDE_CODE_TEE_SDK_STDOUT: string;
		CLAUDE_SESSION_INGRESS_TOKEN_FILE: string;
		CCR_SETTINGS_JSON_OVERLAY: string;
		FSSPEC_GCS: string;
		_: string;
		npm_config_prefix: string;
		npm_config_npm_version: string;
		CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE: string;
		CLAUDE_CODE_REMOTE: string;
		ANTHROPIC_BASE_URL: string;
		TERM: string;
		npm_config_cache: string;
		CLAUDE_CODE_USER_EMAIL: string;
		MCP_TOOL_TIMEOUT: string;
		RUSTUP_HOME: string;
		YARN_HTTPS_PROXY: string;
		CLAUDE_CODE_ACCOUNT_UUID: string;
		SKIP_PLUGIN_MARKETPLACE: string;
		CLAUDE_AFTER_LAST_COMPACT: string;
		CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE: string;
		GIT_CONFIG_VALUE_0: string;
		MCP_CONNECTION_NONBLOCKING: string;
		npm_config_node_gyp: string;
		PATH: string;
		DENO_TLS_CA_STORE: string;
		GIT_CONFIG_VALUE_1: string;
		REQUESTS_CA_BUNDLE: string;
		NODE: string;
		npm_package_name: string;
		COREPACK_ENABLE_AUTO_PIN: string;
		PLAYWRIGHT_BROWSERS_PATH: string;
		GIT_CONFIG_VALUE_2: string;
		CLAUDE_CODE_ORGANIZATION_UUID: string;
		ENVRUNNER_SKIP_ACK: string;
		CLAUDE_EFFORT: string;
		CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST: string;
		CLAUDE_CODE_PROXY_RESOLVES_HOSTS: string;
		CLAUDE_CODE_DIAGNOSTICS_FILE: string;
		CLAUDE_PID: string;
		NoDefaultCurrentDirectoryInExePath: string;
		TRACEPARENT: string;
		CLAUDE_CODE_DISABLE_BUILTIN_ANTMCP: string;
		CLAUDE_CODE_USE_CCR_V2: string;
		DENO_CERT: string;
		CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD: string;
		CLAUDE_CODE_WORKER_EPOCH: string;
		BUN_OPTIONS: string;
		CLAUDE_CODE_ENVIRONMENT_RUNNER_VERSION: string;
		ELECTRON_GET_USE_PROXY: string;
		npm_lifecycle_script: string;
		CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: string;
		CCR_UPSTREAM_PROXY_ENABLED: string;
		CCR_TEST_GITPROXY: string;
		CLAUDE_ENABLE_STREAM_WATCHDOG: string;
		HTTPLIB2_CA_CERTS: string;
		DEBIAN_FRONTEND: string;
		SHELL: string;
		GLOBAL_AGENT_NO_PROXY: string;
		GIT_TERMINAL_PROMPT: string;
		npm_package_version: string;
		npm_lifecycle_event: string;
		CLAUDE_AUTO_BACKGROUND_TASKS: string;
		AWS_ACCESS_KEY_ID: string;
		GIT_CONFIG_KEY_0: string;
		CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR: string;
		CLAUDE_CODE_SESSION_ID: string;
		CLOUDSDK_PROXY_TYPE: string;
		AWS_SECRET_ACCESS_KEY: string;
		CLAUDE_CODE_VERSION: string;
		GIT_CONFIG_KEY_1: string;
		CLAUDECODE: string;
		NIX_SSL_CERT_FILE: string;
		CLOUDSDK_PROXY_ADDRESS: string;
		GIT_CONFIG_KEY_2: string;
		CLOUDSDK_PROXY_PORT: string;
		npm_config_globalconfig: string;
		npm_config_init_module: string;
		MAX_THINKING_TOKENS: string;
		CLAUDE_CODE_DEBUG: string;
		JAVA_HOME: string;
		PWD: string;
		npm_execpath: string;
		CLAUDE_CODE_EXECPATH: string;
		npm_config_global_prefix: string;
		IS_SANDBOX: string;
		ENV_MANAGER_ENABLE_DIAG_LOGS: string;
		USE_SHTTP_MCP: string;
		CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH: string;
		npm_command: string;
		CLAUDE_CODE_MESSAGING_SOCKET: string;
		ANT_IMAGE_REPOSITORY: string;
		CLAUDE_CODE_REMOTE_SESSION_ID: string;
		CARGO_HTTP_CAINFO: string;
		PIP_CERT: string;
		INIT_CWD: string;
		EDITOR: string;
		NODE_ENV: string;
		[key: `PUBLIC_${string}`]: undefined;
		[key: `${string}`]: string | undefined;
	}
}

/**
 * This module provides access to environment variables set _dynamically_ at runtime and that are _publicly_ accessible.
 * 
 * |         | Runtime                                                                    | Build time                                                               |
 * | ------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
 * | Private | [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private) | [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private) |
 * | Public  | [`$env/dynamic/public`](https://svelte.dev/docs/kit/$env-dynamic-public)   | [`$env/static/public`](https://svelte.dev/docs/kit/$env-static-public)   |
 * 
 * Dynamic environment variables are defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`.
 * 
 * **_Public_ access:**
 * 
 * - This module _can_ be imported into client-side code
 * - **Only** variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`) are included
 * 
 * > [!NOTE] In `dev`, `$env/dynamic` includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 * 
 * > [!NOTE] To get correct types, environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * >
 * > ```env
 * > MY_FEATURE_FLAG=
 * > ```
 * >
 * > You can override `.env` values from the command line like so:
 * >
 * > ```sh
 * > MY_FEATURE_FLAG="enabled" npm run dev
 * > ```
 * 
 * For example, given the following runtime environment:
 * 
 * ```env
 * ENVIRONMENT=production
 * PUBLIC_BASE_URL=http://example.com
 * ```
 * 
 * With the default `publicPrefix` and `privatePrefix`:
 * 
 * ```ts
 * import { env } from '$env/dynamic/public';
 * console.log(env.ENVIRONMENT); // => undefined, not public
 * console.log(env.PUBLIC_BASE_URL); // => "http://example.com"
 * ```
 * 
 * ```
 * 
 * ```
 */
declare module '$env/dynamic/public' {
	export const env: {
		[key: `PUBLIC_${string}`]: string | undefined;
	}
}
