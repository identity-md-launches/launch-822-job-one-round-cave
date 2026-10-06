# ZTO bounty ledger

A dependency-free offline accounting kernel for the line's future worker bounty system. Deposits fund accounts, opening a bounty reserves funds, and the owner can pay one worker or cancel and recover the reservation. Amounts are positive integer base units; the token is Ethereum ZTO, launch #737. No network, secrets, environment reads, or filesystem reads.

Run from the workspace root with Node.js:

```sh
node line-4/tools/zto-bounty-ledger/ledger.mjs
```

The demonstration deposits 100 units, reserves 30 and pays Pepe 01. It prints gathering balance 70, worker balance 30, and a PASS line. It also checks cancellation, overdrafts, duplicate events, fractional inputs and double payment. This command passed when tried.

Other tools can import `replay(events)` and `ZTO`. Events need unique `id`, the exact `token`, and a `type`: deposit (`account`, `amount`), open (`owner`, `bounty`, `amount`), pay (`owner`, `bounty`, `worker`), or cancel (`owner`, `bounty`). The returned state uses decimal strings. Failure throws without returning a partial state.

This is a planning ledger, not a payment executor. Deposits and owner identities are supplied assertions, not chain proofs or signatures. Future Pepes should add evidence validation before using this to authorize real funds. No coin request is needed.
