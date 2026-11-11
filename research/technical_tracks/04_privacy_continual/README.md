# 04 — Privacy, continual learning and test-time adaptation

**State:** NOT IMPLEMENTED / NOT REQUIRED for the present QEERI scientific experiment. Do not add speculative DP libraries, adapters or model-training infrastructure.

## When this becomes a real research need
- **Differential privacy:** only if an authorized sensitive dataset and specific privacy threat model exist. Identify unit of protection, adjacency, epsilon/delta budget, mechanisms and measured privacy–utility tradeoff; plain hashing/redaction is **not** differential privacy.
- **Continual learning:** only if changing, labeled observations and drift create a measured baseline failure. Compare frozen model to a defined update rule on time-ordered holdouts with rollback.
- **Test-time training/adaptation:** only if adaptation on an input distribution yields an independently measured improvement and information leakage is excluded; new retrieval/context is **not** test-time weight training.

## Reusable existing boundaries, not DP proof
- [Field-ingestion provenance gate](../../greenhouse_llm_feasibility/validate_field_packet.py) and [privacy rules in research MVP](../../../research_mvp/README.md) are useful *data handling precautions*, **not** privacy guarantees.
- [Research scope and data permissions](../../../docs/02_EVIDENCE_AND_DATA/README.md).

**Exit receipt if activated:** authorized data contract, exact update/privacy mechanism and threat model, controlled baseline, independent utility and failure metrics, reproducible code/seed/receipts, supervisor/ethics review. Otherwise explicitly `NOT_STARTED`.

**Industry signal today:** prudent governance and refusal to exaggerate. **Not supportable yet:** differential privacy or continually trained LLM expertise.
