# @crystal-core/sdk

TypeScript client for the **local node agent** (`python -m node.agent.server`).

```ts
import { CrystalClient } from "@crystal-core/sdk";

const c = new CrystalClient({ baseUrl: "http://127.0.0.1:8787" });
console.log(await c.health());
```

Status: **v0.5 scaffold**. No npm publish. Mainnet **HOLD**.

See OpenAPI: `docs/openapi.yaml`
