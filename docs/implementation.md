# Conversion and runtime responsibilities

The [examples](examples.md) show the concrete changes. The selected representation is called **GF180-ARC-PAIR-1**: ordinary input-edge paths qualified by explicit scalar predicates, with each supplied output-delay field assigned through its producer/Liberty identity.

## What the Python tools own

| Component | Responsibility |
|---|---|
| [intake.py](../tools/intake.py), [liberty.py](../tools/liberty.py) | Read original declarations, every SDF occurrence and raw Liberty groups; classify target/ordinary paths and authenticate required writer identities |
| [convert.py](../tools/convert.py) | Emit predicate nets, edge paths and ordered one-field target children; preserve ordinary records and synchronize renamed conditions |
| [verify.py](../tools/verify.py) | Independently derive membership, cone structure, edge/slot ownership and unchanged text from source inputs; check emitted text before accepting generator metadata |
| [prepare.py](../tools/prepare.py) | Authenticate inputs, prepare each case, expose the file-based entry and generate complete diffs and source/record/field maps |
| [assess.py](../tools/assess.py), [run.py](../tools/run.py), [run_annotation.py](../tools/run_annotation.py), [run_mixed.py](../tools/run_mixed.py) | Compile, annotate, observe, compare independent expected events, and require effective negative controls |
| [references.py](../tools/references.py) | Compare the single committed reference set, or explicitly regenerate it after a passing run |

Each original conjunction becomes a `wand` driven by scalar `===` comparisons. A `wor` combines those exact binary matches; `membership === 1'b0` enables the endpoint fallback. Empty membership yields unconditional edge paths. The original helper evaluates the logic; the predicates affect timing paths only.

All declarations sharing a selected output are checked. On the owned paired-edge groups, each conditional declaration becomes two edge children. Collateral mux data groups keep one simple path per declaration and receive the same explicit predicate representation. This preserves the selected endpoint-local fallback policy without invoking destination-wide legacy `ifnone` selection. Addf carry paths and all functional helper bodies stay unchanged. Each helper's module declaration is renamed to match the behavioral wrapper, as shown in its case diff.

Generated nets occupy separate readable lines. The verifier reads syntax and unchanged byte spans, reconstructs every cone independently, and measures generated locations after parsing. Source line numbers identify the original statements; they do not dictate output formatting. The regression suite checks single-line source declarations, expanded cone formatting and rejected corruption of membership, collateral paths, untouched carry text and field bindings.

The public file-based reader classifies each occurrence from its source endpoint structure. A target record needs an authenticated Liberty identity for each supplied field; an ordinary record uses its original declaration match set. Ordinary conditions follow renamed collateral predicates, while the original IOPATH leaf, numeric tokens, empty slots and record order remain intact. Untouched addf carry records are emitted unchanged. A record map accounts for every input occurrence and its output lines. Unknown input forms fail explicitly.

The independent checker reconstructs the generated path relation from the source model, checks raw Liberty endpoints, condition, sense and timing type, and derives expected SDF text before checking emitter metadata. Hashes authenticate the inputs; condition and edge/slot checks establish their relationship. The mixed regression includes an authentic but wrong-condition Liberty owner, lost ordinary records, unsynchronized conditions and conflicting input edges. [Input contract and commands](examples.md#run-and-interpret-the-results) · [Deletion audit](validation.md#review-of-the-previous-deletions)

## What fixed upstream Icarus owns

The build pins official commit [`beb32f3945f5be1f45cf5d898d440161e9c6f113`](https://github.com/steveicarus/iverilog/commit/beb32f3945f5be1f45cf5d898d440161e9c6f113). It contains the following responsibilities formerly duplicated in the RC1 patch:

- [Local scalar COND binding, #1713](https://github.com/steveicarus/iverilog/pull/1713): carry condition identity through compiler and VVP, expose `_vpiModPathCondition`, and match scope, source, destination, input edge and condition during SDF annotation.
- [Comparison/conjunction support, #1718](https://github.com/steveicarus/iverilog/pull/1718): additional ordinary condition syntax. The GF180 exact-case predicate network remains necessary for the selected model representation.
- Existing `vpi_get_delays` / `vpi_put_delays` processing: preserve fields not specified by a partial SDF write.
- [First-matching-edge history, #1704](https://github.com/steveicarus/iverilog/pull/1704): included in this base. The current scored events occur after initialization and settling.

The [remaining patch](../patches/initial-annotation.patch) changes **one file**, `vpi/sys_sdf.c`, down from 17 in RC1. It supplies `$sdf_annotate_initial`, rejects calls after time zero, requires exactly one match for a named conditional path through that entry, and prints effective two-slot readback in verbose mode. Earlier writes remain observable if a later named path is missing. The ordinary `$sdf_annotate` entry retains upstream multiple-match and later-annotation behavior.

The demo calls the initial entry while inputs are unknown, then releases the first stimulus at 1 ns. The custom task's time check does not itself order other time-zero active events; the bench supplies that ordering. This small patch is an example harness facility. General SDF error supervision is outside its interface.

[Build instructions](examples.md#build-environment) pin and authenticate the source export. [Validation](validation.md) compares the old and new model structure, writes and events, and exercises upstream scalar-condition regressions against this reduced patch. Historical RC1's unmodified-base control is recorded in [release.md](release.md), separate from the new upstream base that already supports `COND`.

## Extraction provenance

The model and SDF emitters derive from `standard_model` and `standard_cell` in research revision `424bf08221c027a374271b8d173f100a472a9d6b` (`prepare_owned_inputs.py`, `independent_owned.py`, `producer_formats.py`). The standalone input reader, finite profile, bench and build route were extracted for RC1. This maintenance keeps that modeling policy and independent expected events while simplifying formatting, ownership of derived files and the runtime boundary. The larger historical research supervisor and application captures remain historical evidence, not runtime dependencies of these examples.
