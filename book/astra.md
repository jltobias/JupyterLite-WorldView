# GPT-6 Astra for geospatial work

This project uses the documented `gpt-6-astra` model identifier. Official [model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra) describes reasoning, coding, image input, function calling, and structured outputs. This curriculum applies those general capabilities to GIS tasks; it does not assume a dedicated geospatial API or guaranteed spatial accuracy. Documentation was checked on **2026-10-02**.

| Capability | Application in the labs | Evidence to verify |
|---|---|---|
| Reasoning and coding | Critique a denominator, graph, or validation function | Executed code and edge cases |
| Image input | Describe a map, curve, or raster-change figure | Legend, units, source table, computed values |
| Structured outputs | Return a concise briefing with evidence IDs | Schema plus citation and factual review |
| Function calling | Request a narrow distance calculation | Allowlisted function and validated arguments |
| Research and synthesis | Compare methods and explain limitations | Primary references and source dates |
| Multilingual drafting | Adapt a reviewed handoff for another audience | Domain and language review |

Exact measurement belongs in GIS code. The [vision documentation](https://developers.openai.com/api/docs/guides/images-vision) explicitly describes limitations in precise spatial localization and visual interpretation. A picture alone cannot establish a CRS, calibrated scale, unseen population denominator, or causal relationship.

## Three levels of use

**No account required:** run Lab 08 to assemble an evidence bundle, construct the actual Responses API request, and test an authored brief against the validator. The fixture is labeled as authored, never as an Astra-generated result.

**Interactive assistance:** give Astra the exported figure, definitions, and evidence JSON in your available interface. Ask for alternative explanations, code review, uncertainty analysis, or a plain-language handoff. Keep citations attached. Product access and features depend on your account.

**Optional API integration:** run `tools/astra_brief.py` on a local computer or managed server. It reads `OPENAI_API_KEY` only from that process's environment, sends a single request to the Responses API, and writes a structured brief and audit metadata. `--dry-run` makes no network request. `--image` adds a reviewed PNG or JPEG. The teaching runner accepts only evidence labeled `SYNTHETIC EXERCISE`.

```bash
python tools/astra_brief.py --evidence astra-evidence.json --output artifacts/request.json --dry-run
python tools/astra_brief.py --evidence astra-evidence.json --output artifacts/brief.json
python tools/astra_brief.py --evidence raster-evidence.json --image raster-change.png --output artifacts/raster-brief.json
```

The first command is free of API activity. The other commands require account access and incur applicable API usage. No API call runs in the static dashboard, notebook default, or deployment workflow. Never embed an OpenAI secret in a browser bundle, notebook, URL, or `VITE_*` variable. `store: false` is included in the request; it is not a promise about all provider retention or organizational policy.

## The evidence contract

Each evidence record has a stable ID, a metric, units, and computed values. The response schema requires `summary`, `evidence_ids`, `limitations`, `review_questions`, and `requires_human_review: true`. The runner checks completion status, handles refusals, validates fields and evidence IDs, and records the evidence/image hashes, response ID, model, and usage. It never executes model-produced code or dispatches resources.

[Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) helps constrain shape, not factual correctness. A valid response can still misinterpret a statistic. The reviewer must check the narrative against the numbers, look for invented causes, and judge whether the questions are useful. API behavior is covered by mocked tests; a live model response is not required for this repository's build.

The Lab 08 dispatcher is a local teaching example, not an implemented autonomous agent loop. To extend it into one, follow the [function-calling guide](https://developers.openai.com/api/docs/guides/function-calling), keep a small allowlist, validate arguments, return measured results, and evaluate the complete workflow before enabling consequential actions.
