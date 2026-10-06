# Gathering 01 result

Wall: `artifacts/gathering/wall.png`, **1254 × 1254, 8-bit RGB PNG**. Record: `dist/gathering/01.json`. Tool: **Confluence**.

No inherited gathering wall or record existed; the supplied bare cave was the base. Added one ochre/charcoal Pepe holding open his hands above four stones in a bowl. Exactly 156,000 pixels changed inside the 590×590 placement at (330,330); zero outside. Rock, cracks, illumination and framing outside pigment remain unchanged.

Visual review: inspected the final whole wall. Counted four fingers plus one thumb on each of two hands. Heavy-lidded eyes and broad mouth read as Pepe; earth pigments, worn lines and exposed rock are present. No letters, numbers, captions, logos, signatures, borders, political/hateful symbols or other figures observed. **Unmet visual requirements: none observed.** Visual judgment is not a mechanical guarantee.

Used the installed subscription image tool (not CLI/API-key mode) to generate a transparent pigment layer, then the inherited PNG compositing method to preserve rock pixels. Prompt: “A single prehistoric cave painting of Pepe seated behind four small stones in a shallow bowl; wide downturned mouth and large heavy-lidded eyes; simple uneven charcoal, worn red/yellow ochre and sparse chalk; transparent unpainted gaps; two separated open hands with exactly four fingers and one thumb each; Lascaux burnt-stick drawing; no text, numbers, symbols, signatures, logos, watermark, border, photography or 3D.” The tool used chroma-key extraction internally to return an RGBA layer.

Offline validation: `python3 gathering/tools/confluence/verify.py` checks decoded pixels, CRCs, dimensions, record schema/hash and unchanged surrounding rock. The integration demo is documented in tools/confluence/README.md. The final wall remains untracked for daemon upload.
