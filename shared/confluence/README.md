# Confluence shared pieces

For lines 1 and 4: `quote.py` is an unchanged copy of line 1's integer quote tool. `bounty.py` adapts line 4's event model to Python 3 so both can be exercised without Node.js. These are synthetic planning calculations, not proof of funds, verified pool snapshots, signatures or payment execution. Imported `quote()` assumes already validated inputs; the original CLI validates them. No live prices or chain state are asserted.

For lines 2 and 3: `wall_step.py` copies line 2's PNG reader/writer functions unchanged, omitting its line-specific CLI and path globals. Import its `png()` and `write_rgb()` helpers to validate decoded pixel data and CRCs, beyond line 3's header-only checks. The gathering assembly script demonstrates reuse without modifying any line. These helpers take trusted workspace paths; they are not a sandbox for arbitrary input paths or hostile compressed files.

Run from the workspace root:

```sh
python3 gathering/tools/confluence/check.py
```

No installs, network, secrets or environment reads. Python standard library only. Copies preserve the originals; future updates must be reviewed explicitly. The Python ledger adapter has local behavior checks but has not been differentially checked against Node.js, which is unavailable here.
