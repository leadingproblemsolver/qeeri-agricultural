# Human verification checklist (nothing below has been done; every item is open)

A reviewer who is independent of the implementer should record outcomes in a review record (name, date, decision) — until then every claim stays `PENDING_REVIEW` and `human_verified` stays false.

**Source fidelity** (the index can only be as good as these)
- [ ] For L06–L10, open the original documents (Tsafaras 2021 Fig. 4A / §3.3 / §2.1.1; FAO 217 ch.4 pp. ~72–73 and Table 2; KAHRAMAA clauses 1.5, 1.7, 3.1) and confirm each chunk's statement, values, units and locator. Ledger page numbers are *inferred ±1*; the L06 values 5463/4435/72 % came from one extraction.
- [ ] Confirm FAO ledger copy (CORE) equals the FAO URL named in the protocol; confirm KAHRAMAA Issue 0 (2016) is the currently applicable edition (currency is unverified).
- [ ] Compare IFAS packet S01–S03 against AE069 itself (the packet is a paraphrase; only the 12-word excerpt is verbatim) and record the real publication date/version (currently `null`).

**Curator-assigned fields in `corpus/allowlist.json`**
- [ ] `reuse_status` per source (currently `LOCAL_ONLY` everywhere; confirm licence/permission before any `PERMITTED_EXPORT`).
- [ ] `jurisdiction`, `default_applicability`/`GENERAL_PRINCIPLE` for IFAS, `topics`, aliases.
- [ ] L07 vs L08 `quantity_key` pairing (Riyadh as-built per ground area vs FAO rule of thumb per greenhouse area): is "unresolved conflict" the right treatment, and is a priority rule needed?

**Behaviour**
- [ ] Re-label `eval/questions.json` independently (expected ANSWER/ABSTAIN and gold chunks), add held-out questions, re-run `evaluate`. The current set was written by the implementer and one guard was changed after it failed.
- [ ] Read the `evidence/DEMO_TRANSCRIPT.txt` answers and judge whether each cited chunk actually entails its question (the system only checks that citations resolve and numbers appear).
- [ ] Review `runs/review_queue.jsonl` entries after running the demo (every claim is queued).

**With credentials (not done here)**
- [ ] Run `evaluate` with `ANTHROPIC_API_KEY` in a clean session; score arm A/B/C claims blind (CORRECT / SUPPORTED / UNSUPPORTED / UNASSESSABLE); decide GO/NO-GO per the pilot's pre-RAG gate.
