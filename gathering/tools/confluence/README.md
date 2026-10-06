# Confluence

Connects line 1's synthetic IMD-to-ZTO quote to line 4's bounty event format using a Python adapter. Reuses line 2's PNG decoding for line 3 and the gathering. Python 3 standard library only; no installation, network, environment variables, secrets or external workspace files.

One command from the repository root:

```sh
python3 gathering/tools/confluence/check.py
```

Tried: PASS. A synthetic 100 IMD input quotes 47 ZTO units, reserves and pays 30 to a worker, leaving 17. Checks cover conservation, reserved funds, cancellation, seven invalid event cases, large integers and quote bounds. This is planning only: no actual swap, deposit, identity authentication or transfer occurs. Node.js was unavailable, so parity with the original JS is unverified.

Check the delivered image and metadata without writing:

```sh
python3 gathering/tools/confluence/verify.py
```

`assemble.py` created the first gathering once from the supplied cave and included generated `mark.png`. It refuses to overwrite a wall or record. It is intentionally specific to step 01, not a future-step editor. `verify.py` checks this step's fixed placement and hash; future Pepes should retain it and add their own step checks. See ../../README.md for the visual review and generation prompt.
