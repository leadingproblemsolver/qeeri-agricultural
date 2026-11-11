# 4 — What has been established, and what hasn't

## Research findings — narrowly stated
- **Verified calculation, synthetic conditions:** 38.0°C dry bulb, 24.0°C wet bulb, effectiveness 0.85 → pad outlet **26.1°C**. This says nothing conclusive about crop-zone air temperature.
- **General engineering principle:** official UF/IFAS AE069 describes direct evaporative cooling and air warming/gradients after the pad. It is not local Qatar measured performance.
- **Source-checking examples:** greenhouse Test A documented three general-principle checks (C01/C02/C05). This is not a validated 11-subsystem feasibility report.
- **Retrieval/AI improvement:** no accepted, comparable evidence showing that the RAG prototype improves agricultural correctness over a fixed verified source packet.
- **Soil prediction:** no acceptable supervised field prediction from matched georeferenced lab measurements.
- **Field packet:** the AI-generated Al-Shahaniya design/telemetry JSON is quarantined as unverified, not a description of a confirmed operational facility.

## What the software does
The repository contains an earlier local Python `research_mvp` supporting evidence-linked candidate questions and decisions, and a newer branch `research/qeeri_rag_v0` with SQLite/FTS5 provenance, retrieval, receipt generation and negative tests. GitHub Actions showed software tests passing on dated runs. **These tests establish implemented behavior, not agricultural truth.** Do not conflate test totals from different branches or dates.

## What not to claim publicly
No verified 20%→100% accuracy jump, no crop-killing prognosis, no approved 28°C tomato physiological cutoff, no measured six-month Al-Shahaniya telemetry, no safety-certified greenhouse design, no current soil-model accuracy figure, no QEERI approval inferred from a draft.

**Next decision:** when reliable model comparison is produced, identify whether a fixed source packet improves the answer. Retrieval is an optional later intervention, not the research objective.

Open the [field-packet integrity assessment](../../research/greenhouse_llm_feasibility/RC04_FIELD_PACKET_INTEGRITY_2026-11-11.md), [research journey](../../research/greenhouse_llm_feasibility/JOURNEY_AND_STATUS_2026-11-10.md) and [existing research MVP](../../research_mvp/README.md).

[Technical continuation](technical/README.md)
