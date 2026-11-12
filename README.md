# Agricultural AI research — start here

**One-sentence goal:** Test whether giving an AI checked agricultural information makes its answers more accurate and cautious.

**You can run the greenhouse demo without an AI account or API key.** The updated single-file runner requires `pip install pyyaml` and lives in [draft PR #4](https://github.com/leadingproblemsolver/qeeri-agricultural/pull/4), not yet in `main`.

**Scientific field guide:** [Climate data, greenhouse cooling, ET₀, source evidence and mentor-review decisions](https://github.com/leadingproblemsolver/qeeri-agricultural/blob/docs/simple-greenhouse-demo-2026-11-11/docs/SCIENTIFIC_RESEARCH_NAVIGATOR.md) (on draft PR #4; not yet merged).

## 1. Run your first demo

Install **Python 3.10+** and Git. Open Terminal, PowerShell or Command Prompt:

```bash
git clone https://github.com/leadingproblemsolver/qeeri-agricultural.git
cd qeeri-agricultural
git fetch origin pull/4/head:demo-start
git switch demo-start
python -m pip install pyyaml
python demo/greenhouse/run_demo.py
```

**No Git?** Visit [the demo branch](https://github.com/leadingproblemsolver/qeeri-agricultural/tree/docs/simple-greenhouse-demo-2026-11-11), click **Code → Download ZIP**, unzip, open a terminal inside that folder, and run `python -m pip install pyyaml`, then `python demo/greenhouse/run_demo.py`. On Windows, `py` may work instead of `python`.

**Expected result:** 10 actual check results (values, study limits, or abstentions). These check example math, source labels and safe refusals. They do **not** prove that the papers or a greenhouse are scientifically validated.

## 2. What the demo actually does

```text
Question + greenhouse inputs
            ↓
Check source, location, units and missing values
            ↓
Calculate what is possible; refuse what is not
            ↓
Show a result + evidence origin + limitations
```

**Example:** 38°C outside dry-bulb, 24°C wet-bulb, and 85% assumed pad effectiveness give **26.1°C at the cooling-pad outlet**. This does **not** tell us the temperature at plant height. These are illustrative values, not measured Qatar weather.

## 3. What should I open?

| If you want to… | Start here |
|---|---|
| Understand the demo and its data | [Plain-language overview](https://github.com/leadingproblemsolver/qeeri-agricultural/blob/docs/simple-greenhouse-demo-2026-11-11/demo/greenhouse/overview.md) |
| See examples and sources | [qeeri_evidence.yaml](https://github.com/leadingproblemsolver/qeeri-agricultural/blob/docs/simple-greenhouse-demo-2026-11-11/demo/greenhouse/qeeri_evidence.yaml) |
| Run the combined demo | `python demo/greenhouse/run_demo.py` |
| Explore the scientific questions | [Research in five steps](docs/README.md) |
| Use the older local evidence-search program | [research_mvp/README.md](research_mvp/README.md) |
| Explore the newer RAG code | [Draft PR #2](https://github.com/leadingproblemsolver/qeeri-agricultural/pull/2) |
| See what the research has actually shown | [Evidence and limits](docs/04_RESULTS_AND_SOFTWARE/README.md) |

**The source register and ten cases are consolidated** in `demo/greenhouse/qeeri_evidence.yaml`. The older separate files remain as historical fixtures; use the single-file `run_demo.py` for presentations.


## 4. Is RAG built?

**Yes, as a prototype.** RAG means **retrieval-augmented generation**: find relevant source passages first, then use them to produce a draft answer.

**Built:** local document ingestion, SQLite/FTS5 retrieval, source links, constrained answers, run receipts, automated software tests, and a queue for human review. The main branch also contains an older evidence-retrieval program in `research_mvp/`.

**Not yet proven:** RAG improves agricultural answers over a fixed verified source packet; independent agronomic validity; reliable greenhouse construction advice; or production readiness. The newer RAG is **in unmerged draft PR #2**, not `main`; its source exclusion rules also need reconciliation.

Try the prototype separately, without an API key:

```bash
git fetch origin pull/2/head:rag-prototype
git switch rag-prototype
cd research/qeeri_rag_v0
python -m unittest discover -s tests -v
python evidence/demo.py
python -m qeeri_rag health
```

Read [the RAG README](https://github.com/leadingproblemsolver/qeeri-agricultural/blob/claude/qeeri-rag-v0-18awxg/research/qeeri_rag_v0/README.md) for source restrictions and technical details. To return to the simpler demo from the repository root, use `git switch demo-start`. **Do not build another RAG system.**

## 5. What data are we collecting?

| Category | Main inputs |
|---|---|
| Weather | Dry/wet-bulb temperature, humidity, sun, wind, place and time |
| Greenhouse | Dimensions, cover, insulation, ventilation, pad/fan configuration |
| Crop | Species, growth stage, canopy conditions, water use |
| Water and soil | Moisture, salinity, water quality, lab data where available |
| Energy and money | Power, water, costs, prices, reported production |
| Evidence | Original source, exact passage, units, place, measured vs modeled, review |
| AI evaluation | Question, same-model prompts/settings, raw answers, reviewer scores |

Published regional examples can be used for a **demo**, but must retain their original locations and evidence types. An illustrative calculation is not a field observation.

## 6. What is missing?

- **Real soil ML:** matched laboratory soil samples and satellite/drone images.
- **Real greenhouse design:** site-specific measurements and expert verification.
- **AI benefit claim:** independently reviewed answer keys and matched, scored baseline-versus-evidence model runs.
- **Full 50-question benchmark:** verified reference answers and comparable four-model evaluation receipts.

**Next real research step:** verify one original source passage, freeze its answer key, then run a controlled comparison of AI answers with and without that source.

This repository is **public**. Do not commit private correspondence, restricted PDFs, participant data or unapproved field measurements. Keep the original research history intact in `docs/` and `research/`. Software PASS ≠ scientific validation.
