# Delivery handoff validation — 2026-11-12

This candidate completes the existing addf carry probe's public conversion/annotation route and connects existing upstream event tests. It preserves the modeling policy, official PDK inputs, earlier independent expectations and all previously accepted references. [Current scope](scope.md) describes accepted inputs and executed coverage. The [recorded handoff](https://github.com/JerryZhong0910/gf180-ifnone/blob/98c39b18f0ecd4fa25080d35aa24cc2a6bca600a/docs/scope.md#handoff-from-research-to-the-current-combinational-delivery) retains the research comparison and responsibility decisions.

## Compared revisions and call chains

The starting HEAD was `a565911fc8068211d7970fe90cf75d2dbc81500e`, with a clean working tree. The audit read source at research `424bf08221c027a374271b8d173f100a472a9d6b`, first public package `1ca8ea512fc21c921e7d8889f0968cb04bb79210` and the current implementation. The research files read were checked byte-for-byte against that commit. Its matrix contains 13 masters and 29 replacement groups; six collateral mux endpoints follow the same-output rule.

The actual research source path is `materialize_finite.standard` → `prepare_owned_inputs.standard_cell`, independently checked by `finite_source_oracle.standard_assess` → `independent_owned.standard_model/standard_cell/standard_relation`. Application annotation uses the same source verifier. RC1 extracted those transformation/checking functions, but its `intake.writer_join` produced only O rows. The current file-based `prepare_files` entry carries both target and ordinary records through source classification, conversion, independent text checking and record/field maps. Existing source and mixed tests exercise that responsibility; this round did not duplicate them.

The producer's earlier source relationship was also traced: `producer.adapter` → `source_oracle.assess_transcript` → `source_join.when_identity`, using `producer_formats` for strict transcript decoding and exact binary32 writer arithmetic. This verifies graph/Liberty transition identity, source conditions/WHEN, labelled min/max analysis points and before/after export state. The public owner ledger is the input boundary for that relationship; current hashes and field checks do not recreate a producer capture or prove a newly supplied acquisition ledger. No OpenSTA or full-chip producer process was rerun.

The event assessor was traced through `finite_runtime.assess` → `path_assessment.predict_causal/compare_causal/compare_outputs` → `semantic_oracle`. Its receiving/pre-path history and object-identity interfaces require adaptation to replace the research observer. Current pin observations and the selected upstream events retain their specific scope. Scan, chip INTERCONNECT/timing checks and physical execution remain independent extensions. These distinctions are recorded as handoff outcomes, not as inherited full-population PASS claims.

## Carry repair and fixed/upstream comparison

The [existing probe input](../examples/addf-carry/original.sdf) and [bench](../examples/addf-carry/bench.v) were copied byte-for-byte from the preceding `carry-boundary/` execution. Its independent expectation was frozen before the new public entry's first run: B=0, CI=1 makes CO follow A, and the source SDF's typical fields are 211/419 ps.

| Same probe and expectation | Actual target readback | Observed CO events after A at 10/20 ns | Result |
|---|---|---|---|
| Previous pinned tool plus initial-annotation patch | 1,000/1,000 ps; no condition identity | 11,000/21,000 ps | Public runner failed `CARRY_PIN_EVENTS`; full stimulus completed |
| Same source version plus case-equality binding increment | 211/419 ps, exact source-condition identity | 10,211/20,419 ps | Both events match; all nine carry paths checked, eight defaults retained |

Both fixed source `beb32f3945f5be1f45cf5d898d440161e9c6f113` and inspected official HEAD [`af170a0b5adf0dc35c71f9d7f813b3dfd61b7d33`](https://github.com/steveicarus/iverilog/commit/af170a0b5adf0dc35c71f9d7f813b3dfd61b7d33) omit case-equality condition keys in the compiler and SDF reader. The latter adds ordered logical OR and unrelated changes, so advancing the pin alone would not repair the carry binding. The [increment](../patches/case-equality-condition.patch) adds distinct case-equality identity without changing HDL evaluation, model declarations, SDF conditions, fallback or four-state policy. It applies to the inspected upstream source with zero fuzz; the runtime measurements here use the fixed base.

The existing upstream rejection test still rejects `===` SDF against a `==` HDL path and the converse, with its original input, delay and event expectations. One diagnostic gold line changes from unsupported syntax to an unmatched parsed condition. That is the observable parser-support change, not a changed timing expectation.

A first full regression exposed the same distinction in the existing unsynchronized-mux-condition negative: the newly parsed condition now triggers the strict initial-entry mismatch guard, so that run exits before the event oracle. The negative harness now uses ordinary `$sdf_annotate` for its three corrupted SDF files, sharing one compiled design and the unchanged stimulus/expected events. They all finish at 120 ns and fail `MIXED_PIN_EVENTS`. The positive retains `$sdf_annotate_initial`, and the original strict cold-rejection test remains effective.

## Tools, commands and results

| Tool/input | Identity |
|---|---|
| Icarus base | `beb32f3945f5be1f45cf5d898d440161e9c6f113` |
| Source `git archive` SHA256 | `4d6471d2a79b2dcbf1270b9f494c772fd4b35e9d844683b11552c724f8283407` |
| Initial-annotation patch | Unchanged SHA256 `9096ec309018e69a752ff148c90b73d8f77eb1395e2f51767375f3e3cd5d062c` |
| Case-equality increment and installed binaries | Exact hashes in [validation.json](validation.json) |
| Docker image | `cva6-sha3-ready:20261014`, immutable ID `sha256:9bf368f4b38f15350dec8a8a0283225bcebddf51a91793c800ca60475d37a210` |
| Execution environment | Ubuntu 24.04.4, uid 1000, network disabled; `/repo`, `/evidence`, source archive mounted read-only at `/input/icarus-source.tar` |

The tool change received a fresh configure/build/install from the authenticated source archive in Docker. Both patches applied without fuzz. The build cache now authenticates the ordered pair of patch contents. The original runtime build remains identified by the saved baseline record.

```sh
# Existing tool: the new carry entry first failed its unchanged event oracle.
python3 -B tools/run_carry.py --out /evidence/carry-before
# Rebuild with the incremental fix, then generate the carry reference.
ICARUS_ARCHIVE=/input/icarus-source.tar JOBS=4 make build
python3 -B tools/run_carry.py --refresh-references --out /evidence/carry-after
# Final candidate, after preserving event-based negative checks:
make check
make check-upstream
make check-carry
```

| Final check | Observed result |
|---|---|
| Existing source suite | 14/14 passed, including authentic-but-wrong Liberty condition, partial owners, wrong edge/slot, ordinary loss/condition synchronization and untouched carry |
| Original case simulations | All six ordered writes and original complete event lists reproduced; S at 10,233 ps, Z at 50,511/70,617 ps |
| Original cold negative | Missing named predicate rejected after preserving the first write and before stimulus |
| Edge-annotation controls | 36/36 combinations; first/final actual edge/slot readback and all scored output events matched |
| Mixed mux2 | Nine events, all eight path objects and ordinary partial/empty writes passed; all three corruptions reached and failed the event oracle |
| Public carry entry | Source conversion preserved both records; original carry COND unchanged; nine carry paths read back and CO at 10,211/20,419 ps |
| References | All 42 pre-existing reference files reproduced unchanged; four carry references reproduced |
| Existing upstream COND regressions | 15/15 passed; rejection still distinguishes logical and case equality |
| Newly connected existing upstream event tests | 3/3 passed: first valid time-zero edge, asymmetric pending-pulse histories, four-state/zero-delay values |

No new duplicate source/event tests were created for responsibilities already checked. The carry probe is the new public regression; the three added upstream entries use the tests shipped by the fixed source. [Original follow-up validation](https://github.com/JerryZhong0910/gf180-ifnone/blob/a565911fc8068211d7970fe90cf75d2dbc81500e/docs/validation.md), [RC1 acceptance](release.md) and historical family/application results retain their original execution identities.

## Comparison and retained execution evidence

All pre-existing input-manifest entries, including PDK sources and independent expected files, match the starting HEAD. The carry input and bench also match the preceding probe; the carry expectation matches its pre-execution freeze. Model/SDF converter and independent source-checker behavior are unchanged. The source relation, compiled readback and pin delivery connect the completed carry duty without changing the selected model representation.

The local `gf180-ifnone-handoff-20261112/` record contains `BASELINE.json`, `HANDOFF.json`, `UPSTREAM_COMPARISON.json`, the before/after carry captures, new build log, first regression failure and final successful log. [validation.json](validation.json) binds the distributed candidate, input manifest, tool binaries and execution evidence by SHA256. Public measured results and complete changes remain beside the cases. That local handoff made no remote writes. The subsequent independent Icarus submission is recorded below; the GF180 patch, inputs, event expectations and release/tag refs remain unchanged.


## Independent Icarus submission

[Icarus PR #1771](https://github.com/steveicarus/iverilog/pull/1771) submits candidate [`8528dfb2b86120c411bbbc021ce615028d914f3e`](https://github.com/steveicarus/iverilog/commit/8528dfb2b86120c411bbbc021ce615028d914f3e) directly against official `af170a0b5adf0dc35c71f9d7f813b3dfd61b7d33`. Its two-file production delta is identical to the retained [fixed increment](../patches/case-equality-condition.patch). The standalone regression uses standard `$sdf_annotate`, four buffer paths and hand-authored SDF; it has no PDK or initial-annotation patch dependency.

The new regression checks 32 output events for `=== 0/1`, mixed `&&`/`||` conditions and 0/1/X/Z control values. Both the unmodified parent and candidate were freshly built in the same Docker image recorded above, with networking disabled. Both builds and `make check` passed.

| Flow | Unmodified official parent | Independent candidate |
|---|---|---|
| Native | Compiled; event check failed at 131 ps instead of 103 ps | All 32 new events passed; 20/20 COND regressions passed |
| Vlog95 | Translated and compiled; same 131-versus-103 ps event failure | All 32 new events passed; 8 simulations passed and 12 existing expected compile rejections remained effective |

The existing comparison and OR rejection tests retain their models, SDF delays and event expectations. Two diagnostic gold lines now identify an unmatched parsed condition. The fixed GF180 base predates OR support and needs only its original one-line diagnostic update.

The local `icarus-case-equality-20261112/` record contains the committed candidate, `FROZEN_INPUTS.json`, `VALIDATION.json`, build and per-test logs, and `PR.json`. The PR includes commands for reproducing the COND selection through the upstream test runner. These are new upstream execution results; the GF180 results above are reused unchanged. The source pin, both local patches, all original PDK files, independent event expectations and `rc1` remain byte-for-byte or ref-identical to the handoff. The separate PR association changes documentation only. Publication of this GF180 handoff reuses the exact validated implementation and fixed tools above; `rc1` and historical release assets remain unchanged.
