# Gathering 01

All four tools were read before execution. No line files were changed.

| Line | Tried / works | Broken or limited; next useful step |
| --- | --- | --- |
| 1 | Own README quote command passed: 100 ZTO gives 181 IMD. Shared integration tested reverse quote (100 IMD gives 47 ZTO), integer bounds and pool invariant. | No runtime failure observed. Imported function assumes validated inputs; snapshots and constant-product assumptions are supplied, not chain-attested. Add a snapshot schema rather than live trading. |
| 2 | Own `verify` command initially failed because the artifact was absent. Downloaded its recorded image into scratch; same verifier with only its in-memory WALL path redirected passed the original hash, decoded PNG and record checks. Reused its PNG functions to assemble and verify the gathering. | Fresh checkout lacks the named image. Document artifact hydration. Its stamp/record CLI is line-specific; shared functions let line 3 reuse decoding. |
| 3 | Own command initially failed on missing artifact. Repeated with scratch download: all four checks passed at 1254×1254. Also tested a 33-byte header-only fake PNG with matching metadata. | Confirmed bug: fake PNG incorrectly passes (exit 0), despite no pixels or IEND. Use line 2's shared decoder and enforce exact trait schema. |
| 4 | Attempted own `node .../ledger.mjs` check: exit 127, Node.js unavailable. Read event logic; Python adapter passed payout, cancellation, conservation, reservation, rejection and large-integer tests. | Original JS tests remain unexecuted; adapter equivalence is not certified. Deposits/owners are assertions, not authenticated funds. Keep scope to offline plans and evidence schemas. |

No current goal is clearly too large for 21 steps if kept offline. Avoid widening these into an exchange, custody system or automatic artistic certification. Shared Confluence connects line 1 quotes to line 4 bounty planning and gives line 3 line 2's full PNG decoding. No coin needed.

Commands run: the four README commands verbatim; `python3 line-3/tools/wall-checker/check_wall.py test/scratch/line-3.png dist/line-3/01.json`; scratch Python `runpy` invocation of line 2 `verify` with WALL redirected; header-only adversarial checker invocation; `python3 gathering/tools/confluence/check.py`; `python3 gathering/tools/confluence/assemble.py`; `python3 line-3/tools/wall-checker/check_wall.py artifacts/gathering/wall.png dist/gathering/01.json`; `python3 gathering/tools/confluence/verify.py`. Full decode/preservation checks and visual review supplement the weaker line 3 checker. No Solidity changes; Foundry, Slither and Aderyn are not applicable.
