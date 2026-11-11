# QEERI Agricultural AI Research

**Question:** Does giving an AI verified agricultural evidence make its answers more accurate and safer?

We are testing this, not assuming the answer. Our first example is greenhouse cooling.

## Start here

1. **[Research overview](overview.md)** — objective, what data to collect, what the demo shows, and what remains unknown.
2. **[Run the 10 demo checks](demo/README.md)** — input → calculation / evidence check → output.
3. **[Evidence and limitations](docs/02_EVIDENCE_AND_DATA/README.md)** — which papers and data can be used, and what still needs review.
4. **[Study methods](docs/03_METHOD_AND_EXPERIMENTS/README.md)** — how to compare AI answers fairly.
5. **[Results and software](docs/04_RESULTS_AND_SOFTWARE/README.md)** — what passed technically, and what has *not* been shown scientifically.

For full records, see the [existing research documentation](docs/README.md). Existing code, historical files, audit notes and other research workstreams have **not** been moved or deleted.

## What the demo does

**Inputs → checks → output → source → limitations.**

You can provide greenhouse weather, cooling and study values. The demo checks a small set of known calculations and source-record rules, including when there is **not enough information to decide**. It does **not** design a greenhouse or certify that any crop will survive.

Try:
```bash
python demo/check_cases.py
```

## Current state

| Area | What exists | What is missing |
| --- | --- | --- |
| Greenhouse checks | General cooling equation; synthetic examples; published-study leads | Measured local performance and independent review |
| Agricultural AI test | Candidate questions, rubric and exploratory responses | Locked expert-reviewed answer keys and comparable model runs |
| Soil sensing | Research design and required data fields | Matched lab soil samples and imagery |
| Retrieval software | Existing local prototypes and tests | Evidence that retrieval actually improves AI answers |

**10 green demo checks do not mean 10 scientific trials.** A working calculation is not a field measurement; a citation is not necessarily scientific support; a passing software test is not a validated agricultural recommendation.

**Next research result to obtain:** freeze one independently checked greenhouse answer key, run the same AI model with and without a verified source packet, and record both original answers and the human assessment.

**Privacy:** This is a public GitHub repo. Do not commit private correspondence, restricted papers, field coordinates, raw participant data, passwords or institution-only archives.
