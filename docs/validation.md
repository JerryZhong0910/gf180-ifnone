# Follow-up validation — 2026-11-12

The current candidate measures how input-edge matching and ordered SDF writes behave, and connects ordinary-record preservation to the public converter. All original case outputs and scored events are unchanged. The [home page](../README.md) shows the real mux2 repair and four measured select deliveries; [examples](examples.md) supplies the controls, mixed-path inputs and commands.

## Candidate and environment

The starting HEAD was `3e24e835089bcd5c4334d484d3be7f213d5ef500`, with a clean working tree. [validation.json](validation.json) identifies this local candidate by distributed-file SHA256 hashes, its inputs, tools and final logs. The previous maintenance record remains available [at its actual commit](https://github.com/JerryZhong0910/gf180-ifnone/blob/3e24e835089bcd5c4334d484d3be7f213d5ef500/docs/validation.md).

| Component | Identity |
|---|---|
| Icarus source, unchanged | `beb32f3945f5be1f45cf5d898d440161e9c6f113` |
| Source `git archive` SHA256 | `4d6471d2a79b2dcbf1270b9f494c772fd4b35e9d844683b11552c724f8283407` |
| [initial-annotation.patch](../patches/initial-annotation.patch) SHA256 | `9096ec309018e69a752ff148c90b73d8f77eb1395e2f51767375f3e3cd5d062c` |
| Docker image | `cva6-sha3-ready:20261014`, immutable ID `sha256:9bf368f4b38f15350dec8a8a0283225bcebddf51a91793c800ca60475d37a210` |
| Execution | Ubuntu 24.04.4, uid 1000, network disabled; checkout at `/repo`, task evidence at `/evidence` |
| Installed tools | Icarus 14.0 development, `/repo/.build/install`; binary hashes in the manifest |

`make build` verified the unchanged source/patch stamp and reused the existing build. The previous round's fresh offline build supplies build evidence; this round reran the affected behavior on that build. The VPI observer was compiled with its `iverilog-vpi`. There was no toolchain change or new online fetch.

## Commands and observed results

The final combined run executed from `/repo` in the container:

```sh
make build
make check
make check-upstream
python3 -B tools/prepare.py /evidence/final-source-verified
```

The mixed runner also executes the documented five-input `tools/prepare.py` command. `make check-annotation` and `make check-mixed` provide separate public entries for the new measurements.

| Check on this candidate | Observed result |
|---|---|
| Source regression suite | 14/14 passed: six existing structural/field tests plus eight mixed-record, partial-field, owner-condition, input-edge and unsupported-record tests |
| Original three cases | addf: three groups/two fields; mux4: two groups/four fields plus collateral paths; mux2: one group/four real fields plus collateral paths |
| Original runtime | Six ordered writes and both effective slots after each write; complete event lists matched at 10,233, 50,511 and 70,617 ps |
| Existing negatives | Missing owner rejected; unknown compiled predicate exited 1 after retaining the first write and before releasing stimulus |
| Edge-annotation controls | 36/36 combinations: three path forms × four record forms/orders × three triplet selections; actual first/final path edges and both slots, four complete scored events per run |
| Mixed seven-track mux2 | Six source occurrences → eight ordered output records; instance preserved; all eight compiled path objects read back; all nine scored events matched |
| Mixed ordinary writes | Named I0 slots read `(211,419)`, `(211,617)`, `(211,617)` ps; bare I1 updates all three simple paths to `(811,877)` ps |
| Dynamic mixed negatives | Wrong select edges, missing ordinary record and unsynchronized condition each exited 0 at 120 ns, then failed `MIXED_PIN_EVENTS` |
| References | 23 original-case/reference files, 11 annotation-control files and eight mixed-case files reproduced |
| [Upstream condition regressions](../tests/upstream.list) | 15/15 passed, including input edges, partial writes, multiple matches and expression conditions |
| Source-only entry | Original three cases passed; mixed file-based entry passed before every mixed run |

The [annotation results](../examples/edge-annotation/reference/results.json) retain observed readbacks and events alongside predictions. Bare records match all endpoint-compatible paths; the last supplied `ABSOLUTE` slot wins. Qualified records match the corresponding edge paths and leave simple paths at their defaults. Reversing the records distinguishes overwrite from aggregation. The [mixed results](../examples/mixed-mux2/reference/results.json) show delivery of the four real select fields and the continued operation of ordinary data paths.

The new expected files and stimulus were frozen before their first measurement. The first annotation-control attempt exposed a VPI observer bug: multiple `vpi_get_str` calls reused one buffer, corrupting printed names. Printing each value before the next call repaired the observer; the original expectations did not change. The mixed case passed its first execution. Its non-integer source delays were independently rounded from the pinned VVP time conversion rule before execution.

## Review of the previous deletions

The audit compares `1ca8ea512fc21c921e7d8889f0968cb04bb79210` with `3e24e835089bcd5c4334d484d3be7f213d5ef500`, following callers and replacement responsibilities rather than example usage alone.

| Removed or replaced item | Caller/data flow and disposition |
|---|---|
| `convert.standard_cell` ordinary (`L`) branch and corresponding `verify.standard_cell` branch | Useful responsibility: retain ordinary records and synchronize renamed conditions. The old public `intake.writer_join` emitted only owned (`O`) rows, so neither old nor reduced public entry exposed that responsibility. Restored through source-based classification, the five-file CLI and independent verification; mixed mux data and untouched addf carry exercise both ordinary forms. |
| Physical line-count constraints in model generation/checking | Replaced by parsed source/generated locators, independently checked cones and unchanged spans. Single-line source and expanded-cone regressions still pass. No timing/path semantics depend on retaining physical line counts. |
| Duplicated compiler/VVP condition implementation in the old 17-file patch | Fixed upstream Icarus owns condition identity, scalar/expression matching and edge matching. The 15 upstream regressions pass with the remaining one-file initial-annotation patch. Initial-time supervision, strict named matching and effective readback remain in that patch. |
| Repeated `docs/reference` models/SDF and hand-maintained reference updates | One authoritative `examples/*/reference` set now comes from the runner after independent checks. All original outputs remain byte-identical this round; source maps and full diffs retain review/navigation duties. |
| Old archive/build entry | Fixed upstream source export and digest replace the older RC1 source/patch pair. The previous round's fresh offline build and archive-portability control remain recorded at the commit above; this round reuses its exact installed tools. |

Before implementing the mixed entry, an isolated copy of the baseline with one ordinary record added failed its supported `tools/prepare.py` command at `WRITER_RECORD_POPULATION` (two supplied owner entries versus three records). The old CLI also rejected the new file arguments. These failures establish the missing public data flow. An independent review of the deleted code confirmed that the earlier rationale for removing the ordinary branch was insufficient; the responsibility has been restored and connected rather than treated as obsolete. The new reader requires ownership only for fields actually redistributed, preserves the existing match relation for ordinary paths, and rejects unsupported records explicitly. Authentic hashes alone do not validate field ownership: a wrong-condition Liberty group with its correct hash is rejected independently.

The finite paired-edge profile remains separate from the historical scan and application profiles in [scope.md](scope.md). No fallback or four-state rule changed.

## Comparison, retained evidence and review

All 18 pre-existing input hashes match the baseline. Every original case's model, helper, SDF, full diff, source map and field map is byte-identical. The existing delivery JSON and ordered trace also match. New record maps account for all source occurrences. The new expected/stimulus hashes still match the pre-execution snapshots.

The prior [RC1 acceptance](release.md), source inventory and historical seven-/nine-track application results remain historical evidence. This round adds the explicitly listed controls and mixed-path run; it does not repeat SHA3 or physical implementation. The current candidate's complete execution record is retained in the local `gf180-ifnone-followup-20261112/` task directory, including `BASELINE.json`, `COMPARISON.json`, `logs/final-check.log`, `final-originals/`, `final-annotation/` and `final-mixed/`. Public reproducible results and complete diffs are beside each example.

The retained IHP classification authenticates `sg13g2_stdcell.v` as SHA256 `9c91c5311e0b10525b2e02bfd30910927d821c0928aff45cb7f34f3a6a3280f8`. The associated historical contracts describe an unchanged canonical model/UDP/raw SDF and a corresponding-edge compatibility policy. An authenticated before/after revision and matching SDF for the reported simple-path update were not obtained. The new GF180 controls therefore establish simulator matching behavior without attributing it to an executed IHP update.

Independent final reading covered the README, example inputs/commands, reader, checker, mixed runner and source regressions. It confirmed the ordinary-record responsibility and the event-failing negatives, and identified an untouched-carry condition boundary. A fresh fixed-tool probe reproduced it: conversion retains `(COND (B===1'b0 && CI===1'b1) (IOPATH A CO ...))`, while Icarus reports `COND not supported`, reads all carry paths at their 1 ns defaults, and observes CO at 11,000/21,000 ps for A events at 10/20 ns. The source regression now checks conditional as well as bare carry preservation; the input contract states this runtime boundary. No case-equality expression was weakened or fallback rule changed. Raw input, bench, converted output and observations are retained under `carry-boundary/` and `logs/carry-boundary.log`.

Local review checked 117 document links, 37 source-derived excerpts, 159 source/generated path locations, all 11 case input occurrences and the complete four-case diffs. The final commands reran after the carry-preservation test was extended.
