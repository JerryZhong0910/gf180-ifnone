# Current conversion scope

The public [file-based command](examples.md#convert-target-and-ordinary-records-together) converts one declared GF180 combinational master at a time. Its profile lists every paired-edge target group in that master; the rules below determine whether the model and SDF fit. The supplied executable fixtures use seven-track `mux2_2` and nine-track `addf_1`/`mux4_2`.

A **family** names a logic type, such as mux2. A **master** fixes the track library and drive strength, such as `gf180mcu_fd_sc_mcu7t5v0__mux2_2`. An **endpoint group** fixes that master, one input and one output. A different track library or drive strength needs its own model, Liberty and profile.

## Check your input

| Input | Accepted structure |
|---|---|
| Behavioral model | GF180 specify-block markers and scalar paths in the form used by the [shipped sources](../upstream/). Each selected group has a posedge/negedge `ifnone` pair, in that order, with `(1.0,1.0)` defaults. Conditional members use simple paths. |
| Conditions | One to five distinct scalar pins compared with `=== 1'b0` or `=== 1'b1`, joined by `&&`. Membership includes all declarations for the endpoint, even those after `ifnone`. |
| Other paths to a selected output | Conditional simple paths with a simple `ifnone` member. Their path form and multiplicity stay intact while conditions become named predicates. Paths to other outputs retain their original declarations. |
| SDF | One CELL, `ABSOLUTE` IOPATH records and a 1 ns timescale, using the exact envelope and record layout of the [mixed fixture](../examples/mixed-mux2/original.sdf). The instance may be empty, scalar or hierarchical. |
| Delay fields | Two output slots: rise and fall. Each accepts a non-negative decimal scalar, complete `min:typ:max` triplet or empty slot. A target record needs at least one supplied field; ordinary records may have both slots empty. |
| Liberty and producer data | A combinational positive- or negative-unate Liberty owner for each supplied field that changes input-edge placement, tied to its source SDF occurrence. Ordinary records use the original model match set. [Required files and profile fields](examples.md#inputs-for-another-cell). |

The reader reports unsupported records and source forms explicitly. Multi-cell SDF, timing-check records and INTERCONNECT require another input route. Use the fixture as the format example when preparing a per-cell input.

## Family and endpoint structure

These families share the paired-edge conversion rules. The table classifies path structure; the [execution table below](#executed-coverage) identifies the masters, fields and stimuli actually checked by the public commands. Condition counts help locate a structure; the actual terms and Liberty owners determine the change.

| Family | Target endpoints | Conditional members per target group | Other paths and example |
|---|---|---:|---|
| addf | A/B/CI → S | 4 | The other two inputs define membership. CO declarations stay unchanged. [Sum](examples.md#addf-four-conditions-including-members-after-ifnone) and [carry](examples.md#addf-carry-preserve-the-record-and-bind-its-condition). |
| addh | A/B → S | 0 | Unconditional replacement edge pair; carry is a separate destination. |
| mux2 | S → Z | 0 | I0/I1 → Z keep simple paths with explicit predicates. [Seven-track example](examples.md#mux2-real-fields-with-no-select-conditions). |
| mux4 | S0/S1 → Z | 16 | Four data pins and the other select define membership. I0/I1/I2/I3 → Z keep simple paths. [Fallback example](examples.md#mux4-an-unselected-x-and-two-fallback-deliveries). |
| xnor2 | A1/A2 → ZN | 0 | Unconditional replacement edge pair; field owners determine unateness. |
| xnor3 | A1/A2/A3 → ZN | 4 | Binary conditions on the other two inputs; inverted parity output. |
| xor2 | A1/A2 → Z | 0 | Unconditional replacement edge pair on the non-inverted output. |
| xor3 | A1/A2/A3 → Z | 4 | Binary conditions on the other two inputs. |

The command accepts a supplied profile rather than a fixed list of case names. To use another master in these families, supply its exact files, endpoint inventory, declaration counts and field owners, then check its generated relation and expected events. The [input manifest](inputs.json) links the seven- and nine-track PDK sources used here.

The scan families `sdffq`, `sdffrnq`, `sdffrsnq` and `sdffsnq` instead have a single rising-clock fallback with clock-to-Q conditions. That structure needs a separate scan profile; it does not satisfy the paired-edge rule above.

## What the candidate changes

Each conditional member becomes a named predicate of exact binary comparisons. Members on a selected endpoint receive separate posedge/negedge paths. A fallback predicate is true when none of that endpoint's conditions matches; an endpoint with no conditions gets an unconditional edge pair. This preserves the repository's selected endpoint-local policy. X/Z in a tested condition pin prevents that binary match; the [mux4 example](examples.md#mux4-an-unselected-x-and-two-fallback-deliveries) measures a fallback event with an unselected X and a known output. The candidate's agreement with the library authors' intended four-state semantics remains a modeling question.

For each supplied target SDF field, the producer/Liberty relationship determines input edge and output slot. The converter preserves triplet tokens and emits one-field writes in source order. Ordinary records keep their leaf text, instance, order and empty slots; a condition is renamed when its model declaration receives a named predicate. Untouched addf carry records remain unchanged. The [mixed example](examples.md#convert-target-and-ordinary-records-together) accounts for every input record and measures both target and ordinary paths.

The independent checker derives the expected path and field relations from the source model, Liberty and supplied owner ledger. Input hashes authenticate bytes; the relationship checks establish endpoint, condition, sense and edge/slot agreement. The producer ledger must come from the SDF export or an explicitly constructed fixture. Missing ownership cannot be inferred from delay values.

## Executed coverage

Conversion checks the full declared model structure. Field checks cover the SDF fields supplied by each fixture; path readback and pin events cover the listed runs. All examples use the original PDK functional helpers. Nine-track delays, mixed ordinary delays and annotation-control delays are synthetic; the seven-track select fields are real producer values.

| Library / master or control | Structural and field checks | Observed result and public entry |
|---|---|---|
| Nine-track `addf_1`, sum | Three sum groups: 18 → 30 declarations; nine carry declarations unchanged; two supplied A → S fields | A → S at 10,233 ps, with ordered write readback. `make check`; [result](../examples/reference/delivery.json). |
| Nine-track `addf_1`, carry | A → CO record retains its original condition; all nine carry paths read back | CO at 10,211/20,419 ps; eight other carry paths keep defaults. `make check-carry`; [result](../examples/addf-carry/reference/results.json). |
| Nine-track `mux4_2` | Two select groups plus four data groups: 72 → 104 declarations; four supplied S0 → Z fields | Two fallback deliveries at 50,511/70,617 ps; four annotated slots read back. `make check`; [result](../examples/reference/delivery.json). |
| Seven-track `mux2_2`, source case | One select and two data groups: eight paths retained; four supplied select fields | Source-only structure and field check. `python3 -B tools/prepare.py runs/source-review`; [field map](../examples/mux2-7t/reference/field-map.json). |
| Seven-track `mux2_2`, mixed records | Six input records become eight; target ownership, ordinary fanout, condition renaming and partial/empty writes | Nine output events and all eight path objects; three corruptions fail event checks. `make check-mixed`; [result](../examples/mixed-mux2/reference/results.json). |
| Seven-track mux2 annotation controls | Edge pair, one simple path and two simple paths; bare/qualified records, both orders, min/typ/max | 36 combinations check first/final path edges, delays and four output events each. `make check-annotation`; [result](../examples/edge-annotation/reference/results.json). |

`make check` includes every cell/control run in the table and the 14 source regressions. `make test` runs those source regressions alone: membership, source locations, collateral and untouched paths, field assignment, ordinary-record loss, condition synchronization and unsupported-record rejection. [Source tests](../tests/test_source_contract.py) · [Mixed-record tests](../tests/test_mixed_contract.py)

`make check-upstream` runs 15 condition-binding regressions plus existing tests for the first valid time-zero edge, pending asymmetric pulses and four-state/zero-delay output transitions. The [selection](../tests/upstream.list) names those tests. These event checks and the per-cell pin checks have explicit stimuli and expectations; application-wide causal-history analysis and producer-process acquisition need their own interfaces and validation.

[Validation and tool identity](validation.md) · [Commands, outputs and independent expectations](examples.md#run-and-interpret-the-results)
