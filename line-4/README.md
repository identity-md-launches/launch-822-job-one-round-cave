# Pepe 01: The First Bounty Bowl

Line 4 starts with an offline ZTO bounty ledger. The new wall mark is Pepe holding a bowl of unmarked coin disks, painted in worn charcoal and ochre. Space remains for future Pepes.

## Result and review

- Wall: `artifacts/line-4/wall.png`, PNG, 1254 × 1254, square.
- Record: `dist/line-4/01.json`; exactly name, image and attributes. Image URL contains the SHA-256 of the saved PNG.
- Base cave SHA-256: `9cbb7bb2a41efa92e010921f287819c9ffb02c4375fa9496c8468701d8e00cc5`.
- No previous records or marks existed. Pixel comparison confirmed zero changed channels outside the new 470 × 470 pigment region at (365, 310). Rock, cracks, framing and light remain unchanged there.
- Visual review of the final PNG: recognizable wide-mouth, heavy-lidded Pepe; charcoal and earth ochres; no text, numerals, signatures, symbols, borders or handprints. Hands are fully hidden behind the bowl, so there are no visible digits to miscount.
- Unmet visual requirements: the supplied base cave has a photographic rock appearance, retained to satisfy the preservation requirement. The added figure is a painting, not a photo or 3D render. No other unmet requirements identified during review.
- Ledger demonstration and rejection checks passed. Run `node line-4/tools/zto-bounty-ledger/ledger.mjs`.

## Image method

The installed image generator created an isolated pigment figure with this prompt: a primitive worn charcoal/red-yellow ochre Pepe, wide mouth and heavy-lidded eyes, seated with hands hidden behind a bowl of three unmarked coins, white empty background, no text or symbols. The white background was removed by brightness-based blending, and the pigment was composited into the original cave without resizing the cave. Generation and compositing dependencies are not required by the delivered ledger.

Next useful steps: ledger schema validation, explicit funding evidence and authenticated bounty approvals. The present ledger models supplied events only and does not move funds.
