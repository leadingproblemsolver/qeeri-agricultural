# Decision memo: greenhouse LLM feasibility pilot P0 (2026-11-05)

Case `QAT-ALSHAHANIYA-TOMATO-SEMICLOSED-P0`, protocol `PROTOCOL_V0.md`. Pilot n=1; nothing here is validation.

## Decision

**The research question is not answered.** No model could be called (no API credential in this environment), so Arm A (closed book) and Arm B (same model plus approved passages) are both `NOT_EXECUTED`. There is no measured A-vs-B result and none was substituted. Do not invest in RAG, calculators or fine-tuning on this evidence. The cheapest valid next step is to run the already-frozen pair, two API calls, and have it judged blind.

## What the evidence work established

| Finding | Detail |
|---|---|
| Ledger status | 10 claims. 5 `SOURCE_TEXT_READ` (FAO 2013, KAHRAMAA wiring code, Tsafaras 2021). 5 `UNVERIFIED_ABSTRACT_ONLY` (all three Qatar papers: Mahmood 2022, Ghani, Lahlou 2025). 0 human-verified. |
| Source not found | "Qatari Crop Performance Index" (Nexus 2026) could not be located. No claim extracted. |
| No blueprint | Of 12 prompt subsystems: 0 fully covered, 9 partial, 3 none (site intake, commissioning, operating checks). No source supplies a Qatar-applicable sizing for any subsystem. |
| Anchor unconfirmed | Al-Shahaniya, Venlo, tomato and 4-mm glass are **UNVERIFIED**: the accessible record for the anchor paper states none of them. |
| Transfer risk | Riyadh irrigation (about 1246 L/m2 per season) is 4.5-7x FAO's Mediterranean net tomato requirement (177-276 mm). Do not carry values between climates. |
| Source hygiene | The KAHRAMAA PDF named "2018" is the 2016 Issue 0; current edition unverified. One FAO ventilation figure is internally inconsistent (0.06 m3/s/m2 at 3 m is 72 ACH, not 60) and was excluded. |

Pass condition not met: the protocol asks for 20-30 person-verified claims; this has 10, none person-verified.

## Blockers

1. No model credential here (`ANTHROPIC_API_KEY`). Blocks both arms.
2. Full text of the three Qatar papers (publisher access). Blocks verifying L01-L05 and the anchor attributes.
3. A person must check the 10 excerpts and page numbers against the PDFs. Locators were relayed by a fetch tool, pages are +/-1.
4. Second human annotator, blind judging, and the current KAHRAMAA edition.

## Next experiment

With a key set: `python run_pilot.py execute`. It sends the frozen prompt (sha256 `84f0dac1...`) to the same model at the same settings with and without passages `L06-L10`, saves raw responses, and blinds the outputs as X/Y. Judge both against the ledger using `score_rubric.py`. Any fabricated source, electrical-safety error, unsafe cooling or materially wrong sizing is an automatic `NOT_INSTALLATION_READY`.

Scope: preliminary planning evaluation only. Not a construction design, bill of quantities, permit drawing or electrical authorisation.
