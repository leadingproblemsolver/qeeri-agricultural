# QEERI agricultural research — what works, what is missing

**Purpose:** Evaluate whether existing AI can make defensible agricultural statements relevant to Qatar, using sources, physical checks, independently scored answers and explicit uncertainty. Soil remote sensing and farm feasibility are related research aims, **not finished products**.

**Current scientific result: NONE independently established for the new greenhouse/RAG comparison.**

### Start here

| Need | Open |
|---|---|
| First reproducible example | [Cooling case: one equation, two synthetic inputs, tests and limitations](research/greenhouse_llm_feasibility/scientific_case_v0/README.md) |
| Source truth and dataset blockers | [Source and data reality](research/greenhouse_llm_feasibility/SOURCE_AND_DATA_REALITY.md) |
| Existing greenhouse research protocol | [Research protocol](research/greenhouse_llm_feasibility/PROTOCOL_V0_response.md) |
| Detailed source-coverage audit | [RAG branch audit](research/qeeri_rag_v0/RESEARCH_SOURCE_COVERAGE_AUDIT_2026-11-10.md) |
| Existing RAG software | [Prototype README](research/qeeri_rag_v0/README.md) |
| Original QEERI work-to-proof inventory | [Work mapping](02_QEERI_WORK_TO_PROOF_MAPPING.md) |

### The four research goals — current reality

| Goal | Reality | What has to happen |
|---|---|---|
| **Soil salinity and moisture** from UAV and Sentinel-2 | No verified paired Qatari lab ground-truth samples in this repository; real training/validation is blocked | Obtain authorized samples with dates/depths/location and matched imagery; spatial holdout before model comparison |
| **Agricultural LLM reliability** — 50 questions, 4 models | Existing materials describe 200 planned runs, but accepted comparable controlled results have not been established | Freeze actual question bank/reference answers, run isolated sessions, retain raw outputs and independent scoring |
| **Qatar greenhouse feasibility** | One Al-Shahaniya reference case and a small **synthetic** pad-exit calculator; no site measurements or approved design | Verify original papers, Qatar weather, physical assumptions, crop-zone variables, and an independent answer key |
| **Evidence-grounded assistance/RAG** | Local SQLite/FTS5 prototype and 75 passing RAG software tests from Nov 10; model A/B/C generation arms unexecuted | Show that the verified fixed-source packet actually improves an answer, then compare retrieval only if necessary |

### Exactly what the cooling example proves

Given **assumed** air temperature, wet-bulb temperature and pad effectiveness, a transparent equation yields pad-exit air temperature:

- 40°C / 20°C / 85% → **23.0°C**.
- 45°C / 31°C / 85% → **33.1°C**.

This **does not** establish crop-zone temperature, local Qatar summer weather, safe tomato pollination, equipment sizing or harvest outcomes. The uploaded November 9 QMD weather claim was *not* independently verified and was *not* used in calculations.

Run the example (Python stdlib only):

```bash
cd research/greenhouse_llm_feasibility/scientific_case_v0
python evaluate.py
python -m unittest discover -s . -p 'test_*.py' -v
```

The supplied example passed **5/5 local unit tests** on November 10, 2026. The existing RAG software passed **75/75 RAG unit tests** in [GitHub Actions](https://github.com/leadingproblemsolver/qeeri-agricultural/actions/runs/42787690162). In combined CI, **75 RAG tests plus 5 cooling tests passed** ([run 42802024430](https://github.com/leadingproblemsolver/qeeri-agricultural/actions/runs/42802024430)). Neither test count is scientific validation.

### Research integrity: claims currently **NOT proven**

A pasted analysis claims baseline AI scored 20%, sourced AI scored 100%, four models consistently made crop-killing recommendations, a universal 28°C crop threshold, and a verified Qatar summer wet-bulb range. **We do not have sufficient auditable raw responses, independent scores or measurements to support these as findings.** Do not cite those percentages as results.

A newly uploaded Mahmood source record labels its text verified, but the earlier repo ledger says abstract-only. Resolve that disagreement against the original document and store its exact source locators, not the YAML status label. FAO is listed as excluded in the new candidate corpus package, but the current RAG implementation still indexes FAO: **code-level exclusion is not yet done**.

AI can produce adversarial scientific questions; AI cannot grant itself an independent expert-review signature.

### What happens next (one actual research milestone)

**Lock one source-checked, physically falsifiable greenhouse question and its reference answer before re-running models.** Verify the primary article and enough weather/equipment inputs for *that question*. Preserve the A (no documents) and B (fixed verified passages) raw responses under identical model configuration. Independently score claim accuracy, appropriate abstention and source support. Do not build more retrieval infrastructure before comparing B against A.

**Current next external action:** obtain exact primary-paper passages or documented access denial and request technical review of the fixed case. If original data is missing, return **BLOCKED** and the specific acquisition requirement.

### Safety and publication scope

- This GitHub repository is currently **PUBLIC** according to the GitHub API (November 10, 2026). Older README text calling it private was stale. **Do not upload** restricted textbooks, unpublished QEERI information, private research correspondence, raw confidential model logs, lab data without rights, or UDST SCSC participant/IRB materials.
- Files committed in `scientific_case_v0/` contain only synthetic scenarios, source links, code and explicit unverified input labels.
- The uploaded `qeeri_rag_corpus_package.zip` was reviewed as **candidate** reference information, not merged into the RAG index. No source was newly marked human-verified or licensed for public redistribution.
- PR #2 is still a draft and was not merged.

### Historical background

An earlier, incomplete local evidence archive is described in the original README revision and [work mapping](02_QEERI_WORK_TO_PROOF_MAPPING.md). Claims about its contents should be confirmed against the actual archive, not reconstructed from branch summaries.
