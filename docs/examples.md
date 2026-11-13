# Run, inspect and adapt the examples

The supplied examples include every model, SDF, Liberty group, owner ledger, bench and expected event needed to reproduce their results. Start with the commands below; use [current scope](scope.md#check-your-input) before preparing another cell. The [case index](#source-files-and-complete-changes) links inputs to full diffs and results.

## Run and interpret the results

Use the [main checkout instructions](../README.md#run-and-see-the-result), then run from that checkout's root with the [build dependencies](#build-environment) installed:

```sh
make build
make check
make check-upstream
```

`make check` runs the 14 source regressions, original addf/mux4 simulations, mux2 source check, 36 edge-annotation comparisons, mixed mux2 and addf carry. It checks expected failures and reproduces the committed reference outputs. `make check-upstream` runs 23 selected condition and event regressions against the same fixed tool source.

| Run a selected check | Successful result |
|---|---|
| `make test` | Source structure, field bindings, ordinary-record handling and rejection controls pass. |
| `make check-mixed` | Six input records become eight; nine output events match; three dynamic corruptions reach and fail event checks. |
| `make check-carry` | Original carry COND preserved; nine carry paths checked; CO at 10,211/20,419 ps. |
| `make check-annotation` | 36 combinations of model, SDF record form/order and min/typ/max triplet selection match actual path readback and complete scored events. |

For source-only conversion and checking, no simulator is needed:

```sh
python3 -B tools/prepare.py runs/source-review
```

This prepares addf, mux4 and seven-track mux2 in separate subdirectories. To choose a fresh destination for the original addf/mux4 simulation and source checks:

```sh
python3 -B tools/run.py --prefix .build/install --out runs/review
```

Use a new destination each time. The runners otherwise print automatically created `runs/case-*`, `runs/annotation-*`, `runs/mixed-*` or `runs/carry-*` directories. A nonzero command status means a check failed. Expected negative controls are caught by the runner and reported as passing rejection checks.

### Read the outputs

| Files in the printed run directory | What to inspect |
|---|---|
| `<case>/changes.diff`, `model.v`, `helper.v`, `converted.sdf` | Complete change from the source inputs. Mixed and carry runners put these files under `converted/`. |
| `source-map.json` beside each generated model | Every source/generated path location, including collateral and untouched paths. |
| `record-map.json` beside each generated SDF | Every input occurrence, instance, processing action and output line. |
| `field-map.json` beside each generated SDF | Source occurrence, Liberty group/sense, input edge and output slot for each redistributed field. |
| Original case run: `capture.log`, `delivery.json` | Ordered annotation writes and source-to-pin chains, with expected/observed values and times. |
| Mixed/carry: `results.json`, `converted/capture.log`; annotation controls: `results.json` and each variant's `capture.log` | Actual path readback and complete scored events, checked against independent expectations. |
| Original case run: `invalid-annotation/capture.log` | Unknown second predicate rejected after the first write, before stimulus. |

Source-only success establishes model structure and field relationships. Simulation additionally checks actual annotated paths and the complete event lists in each bench's declared windows. The original examples expect S at 10,233 ps and Z at 50,511/70,617 ps. Their missing-owner control fails `MISSING_FIELD_OWNER`; the cold annotation control exits with status 1, retains the first readback and releases no input events.

## Inputs for another cell

The file-based command requires all five options together. The [mixed mux2 command](#convert-target-and-ordinary-records-together) is a complete example that can be copied and run.

| Option | Required content |
|---|---|
| `--model` | Original behavioral model for the exact track library and master, with the [supported path structure](scope.md#check-your-input). |
| `--helper` | The matching original functional model. Conversion adapts its module declaration name to the wrapper; the logic body stays intact. |
| `--liberty` | Liberty text for that master and the corner supplying the SDF fields. The fixture uses TT, 25°C, 5 V. |
| `--sdf` | Single-cell input in the accepted layout: target records plus any ordinary records to retain. |
| `--producer` | JSON profile declaring the master, target endpoint groups, declaration counts and source-to-Liberty field owners. See the [mixed profile](../examples/mixed-mux2/producer.json). |

The profile's `master` is the complete cell name and `groups` lists every paired-edge `ifnone` `[input, output]` pair in that master, including groups with no supplied SDF record. `original_declarations` and `generated_declarations` count the rewritten population, including collateral paths to the selected outputs. For each target record, `records` identifies its input line and authenticates the exact record text. `rise_group` and `fall_group` identify zero-based Liberty group ordinals; a shared `group_sha256` or per-field group hashes authenticate the raw group text. Only supplied fields need owners.

Acquire the record/arc correspondence when exporting the SDF, or assign it explicitly when constructing a synthetic fixture. The independent checker verifies the supplied endpoints, condition, timing sense and resulting edge/slot relation. Matching hashes authenticate the inputs; they do not recover a missing source relationship from record order or numeric values. Resolve missing or ambiguous owners at the producer.

Ordinary records require no field-owner entries: their source declaration matches determine retention and any condition rename. An edge-qualified target must agree with its owner-derived input edge. Numeric tokens, record order, instance context and empty-slot writes are preserved as described in [scope](scope.md#what-the-candidate-changes). The committed fixture inputs and expected events are authenticated by [inputs.json](inputs.json).

## Source files and complete changes

Each case keeps its SDF, owner ledger and references under `examples/`; original PDK model/helper/Liberty files live in `upstream/`. The complete diffs include all model edits, helper declaration-name adaptation and SDF changes. Source and generated locations are measured separately.

| Case | Source inputs | Full change and result |
|---|---|---|
| Seven-track mux2_2 | [Model](../upstream/gf180mcu_fd_sc_mcu7t5v0__mux2_2.behavioral.v), [Liberty](../upstream/gf180mcu_fd_sc_mcu7t5v0__mux2_2__tt_025C_5v00.lib), [SDF](../examples/mux2-7t/original.sdf), [owners](../examples/mux2-7t/producer.json) | [Diff](../examples/mux2-7t/reference/changes.diff), [model](../examples/mux2-7t/reference/model.v), [fields](../examples/mux2-7t/reference/field-map.json), [all paths](../examples/mux2-7t/reference/source-map.json) |
| Nine-track addf_1 | [Model](../upstream/gf180mcu_fd_sc_mcu9t5v0__addf_1.behavioral.v), [Liberty](../upstream/gf180mcu_fd_sc_mcu9t5v0__addf_1__tt_025C_5v00.lib), [SDF](../examples/addf/original.sdf), [owners](../examples/addf/producer.json) | [Diff](../examples/addf/reference/changes.diff), [model](../examples/addf/reference/model.v), [fields](../examples/addf/reference/field-map.json), [all paths](../examples/addf/reference/source-map.json) |
| Nine-track mux4_2 | [Model](../upstream/gf180mcu_fd_sc_mcu9t5v0__mux4_2.behavioral.v), [Liberty](../upstream/gf180mcu_fd_sc_mcu9t5v0__mux4_2__tt_025C_5v00.lib), [SDF](../examples/mux4/original.sdf), [owners](../examples/mux4/producer.json) | [Diff](../examples/mux4/reference/changes.diff), [model](../examples/mux4/reference/model.v), [fields](../examples/mux4/reference/field-map.json), [all paths](../examples/mux4/reference/source-map.json) |
| Seven-track mixed mux2_2 | Same mux2 model/Liberty; [SDF](../examples/mixed-mux2/original.sdf), [owners](../examples/mixed-mux2/producer.json) | [Diff](../examples/mixed-mux2/reference/changes.diff), [record map](../examples/mixed-mux2/reference/record-map.json), [result](../examples/mixed-mux2/reference/results.json) |
| Nine-track addf_1 carry | Same addf model/Liberty/profile; [SDF](../examples/addf-carry/original.sdf), [bench](../examples/addf-carry/bench.v) | [Diff](../examples/addf-carry/reference/changes.diff), [record map](../examples/addf-carry/reference/record-map.json), [result](../examples/addf-carry/reference/results.json) |
| Seven-track mux2 controls | Same mux2 helper; [model/SDF variants](#what-happens-if-the-select-path-becomes-simple), [bench](../examples/edge-annotation/bench.v) | [All path readbacks and events](../examples/edge-annotation/reference/results.json) |

## mux2: real fields with no select conditions

For seven-track `mux2_2`, S → Z contains a positive-edge and negative-edge `ifnone`, with no conditional member on that endpoint. Removing the fallback keyword yields the pair shown on the [home page](../README.md#what-changes-in-a-real-cell). The conditions on I0/I1 → Z belong to different endpoint groups and do not determine the S → Z fallback.

The source SDF's two bare S → Z records need distinct Liberty identities. The ledger binds record occurrence **and both output fields** to raw timing-group hashes, related pin, output pin and sense. Group ordinals are zero-based within the master; SDF line numbers are one-based. The source order is:

| Source SDF | Liberty owner | Output-rise field → input edge | Output-fall field → input edge |
|---|---|---|---|
| Line 7 | group 7, positive unate | 0.289752 ns → posedge S | 0.382399 ns → negedge S |
| Line 8 | group 6, negative unate | 0.445571 ns → negedge S | 0.428267 ns → posedge S |

The [converted SDF](../examples/mux2-7t/reference/converted.sdf) writes one field per child, in source-record order, rise child then fall child. The final pairs are `(0.289752, 0.428267)` ns for posedge S and `(0.445571, 0.382399)` ns for negedge S. The checker verifies all four fields against the original declarations and Liberty groups.

The [ledger](../examples/mux2-7t/producer.json) retains the original producer record identities and byte offsets for these real fields; the SDF wrapper contains just this cell. The source-only case checks their mapping, and the [mixed-record run](#convert-target-and-ordinary-records-together) measures select and data deliveries. [Original acquisition and circuit results](https://github.com/JerryZhong0910/gf180-ifnone/blob/98c39b18f0ecd4fa25080d35aa24cc2a6bca600a/docs/scope.md#historical-execution-and-current-examples).

The full diff also rewrites six I0/I1 → Z declarations because the candidate makes fallback membership explicit for every endpoint group feeding Z. Each data group's fallback depends on its own two conditions, alongside the unconditional S edge pair. The data paths keep their simple form, endpoints, defaults and one-to-one declaration relation; the helper's mux logic is unchanged. The independent checker verifies these predicate cones as well as the select pair. The [mixed example](#convert-target-and-ordinary-records-together) shows the corresponding ordinary SDF condition rename and measures data-path delivery; [implementation](implementation.md#what-the-python-tools-own) explains the representation choice.

## addf: four conditions including members after `ifnone`

For nine-track `addf_1`, the A → S source group appears in this order (comments and blank lines omitted):

```verilog
if(B===1'b0 && CI===1'b1) (A => S) = (1.0,1.0);
if(B===1'b1 && CI===1'b0) (A => S) = (1.0,1.0);
ifnone (posedge A => (S:A)) = (1.0,1.0);
ifnone (negedge A => (S:A)) = (1.0,1.0);
if(B===1'b0 && CI===1'b0) (A => S) = (1.0,1.0);
if(B===1'b1 && CI===1'b1) (A => S) = (1.0,1.0);
```

A scan that stops at `ifnone` would miss the last two members. The converter collects every declaration with the same master, input and output across the whole specify block. Each of the four conditions gets two edge children. The fallback pair uses the complement of membership in **all four** exact conditions.

For B=CI=0, the generated predicate and path children are:

```verilog
wand __gls_path_A_S_9f7c123088d11c7d;
assign __gls_path_A_S_9f7c123088d11c7d = (B === 1'b0);
assign __gls_path_A_S_9f7c123088d11c7d = (CI === 1'b0);
// Inside specify:
if (__gls_path_A_S_9f7c123088d11c7d) (posedge A => (S : A)) = (1.0,1.0);
if (__gls_path_A_S_9f7c123088d11c7d) (negedge A => (S : A)) = (1.0,1.0);
```

The four predicate nets drive a `wor` named `__gls_path_A_S_any`; a scalar comparison computes `__gls_path_A_S_fallback = (__gls_path_A_S_any === 1'b0)`. The full model contains these fallback paths:

```verilog
if (__gls_path_A_S_fallback) (posedge A => (S : A)) = (1.0,1.0);
if (__gls_path_A_S_fallback) (negedge A => (S : A)) = (1.0,1.0);
```

The input fixture supplies TT/25°C/5 V Liberty **group 12**, whose related pin is A, output is S, sense is positive-unate, and condition is B=CI=0. The fixture authenticates both that raw group and the source record. The SDF change is:

```diff
-(COND (B===1'b0 && CI===1'b0) (IOPATH A S (0.211:0.233:0.267) (0.319:0.347:0.383)))
+(COND __gls_path_A_S_9f7c123088d11c7d (IOPATH (posedge A) S (0.211:0.233:0.267) ()))
+(COND __gls_path_A_S_9f7c123088d11c7d (IOPATH (negedge A) S () (0.319:0.347:0.383)))
```

With typical selection, the first write yields a 233 ps rise slot and retains the 1,000 ps fall default. B=CI=0 makes the original sum helper follow A. A rises at 10,000 ps, so the frozen expectation is **S=1 at 10,233 ps**. The measured event matches. This exercises a conditional child; mux4 below exercises fallback delivery.

The addf view transforms A/B/CI → S, including the unannotated B and CI groups. Its carry-output declarations and original helper logic remain byte-identical. The [full diff](../examples/addf/reference/changes.diff) makes that distinction reviewable; the checker verifies it.

## addf carry: preserve the record and bind its condition

For nine-track `addf_1`, conversion leaves the carry declarations and their SDF records intact. `make check-carry` uses the public file-based converter with the [addf profile](../examples/addf/producer.json), [carry SDF](../examples/addf-carry/original.sdf) and [bench](../examples/addf-carry/bench.v). With B=0 and CI=1, A → CO uses the original `B===1'b0 && CI===1'b1` condition.

The upstream case-equality binding support from [Icarus PR #1771](https://github.com/steveicarus/iverilog/pull/1771), included in the fixed build, gives that path `(211,419)` ps. A changes at 10/20 ns produce CO at **10,211/20,419 ps**, matching the [independent expectation](../examples/addf-carry/expected.json). All nine carry paths are read back; the other eight retain 1 ns defaults. [Complete model/helper/SDF diff](../examples/addf-carry/reference/changes.diff) · [Record destinations](../examples/addf-carry/reference/record-map.json) · [Measured paths and events](../examples/addf-carry/reference/results.json)

The [original carry validation](https://github.com/JerryZhong0910/gf180-ifnone/blob/efb18976afa3dba64c5430dba0c662fa45a75300/docs/validation.md#carry-repair-and-fixedupstream-comparison) shows the old-tool control reaching the same event checks with 1 ns defaults. The runtime binding fix preserves the original model condition and the candidate's four-state policy.

## mux4: an unselected X and two fallback deliveries

For nine-track `mux4_2`, S0 → Z has sixteen conditional declarations. For example, the source tests all four data pins and S1:

```verilog
if(I0===1'b0 && I1===1'b1 && I2===1'b0 && I3===1'b0 && S1===1'b0)
```

Every member requires binary values for all four data pins. Each becomes two edge paths; the fallback predicate is the complement of their sixteen-member union. [The full diff](../examples/mux4/reference/changes.diff) shows the other members, both fallback edges, the parallel S1 group and the four collateral data-input groups. Those data paths keep their simple form and one-to-one mapping while their predicates become explicit.

At **30 ns**, the bench sets S1=0, I0=0, I1=1, I2=X, I3=0 and S0=0. S1=0 selects the I0/I1 pair, so the functional mux output is known despite I2=X. The exact binary comparisons still see I2, so all S0 → Z conditions are false and the fallback is enabled. S0 rises at **50 ns** and falls at **70 ns**.

Both source records say `(IOPATH S0 Z ...)`, with no `COND`. The writer fixture assigns the first to negative-unate Liberty group 44, and the second to positive-unate group 53. Their [actual SDF change](../examples/mux4/reference/changes.diff) produces:

```sdf
(COND __gls_path_S0_Z_fallback (IOPATH (negedge S0) Z (0.701:0.727:0.759) ()))
(COND __gls_path_S0_Z_fallback (IOPATH (posedge S0) Z () (0.811:0.839:0.877)))
(COND __gls_path_S0_Z_fallback (IOPATH (posedge S0) Z (0.503:0.511:0.557) ()))
(COND __gls_path_S0_Z_fallback (IOPATH (negedge S0) Z () (0.601:0.617:0.653)))
```

| Final fallback slots | Rise | Fall |
|---|---:|---:|
| posedge S0 | 511 ps, group 53 | 839 ps, group 44 |
| negedge S0 | 727 ps, group 44 | 617 ps, group 53 |

The readback checks all four slots, including preservation of the earlier field when the later record writes its companion. The output events exercise the positive-unate owner's 511 and 617 ps fields: **Z=1 at 50,511 ps**, then **Z=0 at 70,617 ps**.

The [bench](../examples/bench.v) retains initialization at 1 ns and the first mux cofactor/transition at 10 ns before the 30 ns setting. The scored windows are 9–80 ns for S and 40–80 ns for Z. The checker compares the entire ordered output list in each window, including population, values and times, with [independent frozen expectations](../examples/expected.json). The [trace](../examples/reference/trace.txt) groups passive channels for reading; each fresh `capture.log` retains simulator order. Settled predicate probes establish the enabled path at the source event.

## What happens if the select path becomes simple?

The control starts from the same seven-track `gf180mcu_fd_sc_mcu7t5v0__mux2_2`, S → Z, used above. It keeps the PDK helper and the data paths, and varies only the select declarations:

```diff
-(posedge S => (Z : S)) = (1.0,1.0);
-(negedge S => (Z : S)) = (1.0,1.0);
+(S => Z) = (1.0,1.0);
```

A second simple variant keeps two duplicate simple declarations, corresponding to removing the edge qualifiers without coalescing the pair. These **constructed GF180 simulator controls** are separate from the reported IHP model update. The measurements use the [fixed Icarus build](#build-environment). [Edge model / full diff](../examples/edge-annotation/reference/edge.diff) · [One simple path / full diff](../examples/edge-annotation/reference/simple.diff) · [Two simple paths / full diff](../examples/edge-annotation/reference/simple-pair.diff)

The two synthetic source records use different values in every slot and triplet position. In the [bare input](../examples/edge-annotation/reference/bare.sdf):

```sdf
(IOPATH S Z (0.101:0.211:0.311) (0.401:0.419:0.431))
(IOPATH S Z (0.503:0.521:0.541) (0.601:0.631:0.661))
```

The [qualified input](../examples/edge-annotation/reference/qualified.sdf) changes the first source to `(posedge S)` and the second to `(negedge S)`, preserving the output slots and all numeric tokens. Separate [bare-reversed](../examples/edge-annotation/reference/bare-reversed.sdf) and [qualified-reversed](../examples/edge-annotation/reference/qualified-reversed.sdf) inputs exchange the two records.

Input edge, output transition and triplet selection are independent dimensions. `(posedge S)` selects a compiled input-edge path. The first/second delay fields select output rise/fall. Within either field, `min:typ:max` is selected by `-Tmin`, `-Ttyp` or `-Tmax` before annotation; it does not select an input edge.

The [bench](../examples/edge-annotation/bench.v) annotates the first record alone and snapshots actual paths, then annotates the full ordered pair and snapshots again, all at time zero. Inputs start at 1 ns. S changes at 10/20 ns with I0=0, I1=1, then at 40/50 ns with I0=1, I1=0. Thus the four scored outputs are rise, fall, fall, rise. Cell time units/precision are 1 ns / 1 ps; all synthetic delays are exact integer picoseconds. The same stimulus, timescale and windows apply to every variant.

At typical selection, record A supplies `(211,419)` ps and record B `(521,631)` ps, ordered A then B:

| Model / SDF | Actual final path readback | Observed Z times for S↑, S↓, S↑, S↓ |
|---|---|---|
| Edge pair / bare A, B | Both edges: `(521,631)` ps | 10,521; 20,631; 40,631; 50,521 ps |
| Edge pair / posedge A, negedge B | Posedge: `(211,419)`; negedge: `(521,631)` ps | 10,211; 20,631; 40,419; 50,521 ps |
| Simple path / bare A, B | No input edge: `(521,631)` ps | 10,521; 20,631; 40,631; 50,521 ps |
| Simple path / posedge A, negedge B | No matches; `(1000,1000)` ps defaults | 11,000; 21,000; 41,000; 51,000 ps |

Reversing the bare records leaves A's values instead. Reversing the edge-qualified records leaves each edge's values unchanged. Two duplicate simple declarations behave the same way as one, with both path objects read back.

The [measurement record](../examples/edge-annotation/reference/results.json) includes first/final path edges and delays, expected/observed events, and unmatched-annotation counts for all 36 combinations. With simple paths and qualified SDF, the three annotation attempts (first-only, then the two-record file) report no matching ModPath; the same bench completes with the default delays shown above.

Run just this comparison with `make check-annotation`. Its fresh directory contains each complete model, model diff, SDF input, compile log and raw VPI/pin capture. The [frozen source-derived predictions](../examples/edge-annotation/expected.json) predate the first measurement.

## Convert target and ordinary records together

The [mixed fixture](../examples/mixed-mux2/original.sdf) uses the real S → Z records above and interleaves synthetic I0/I1 → Z records in the same mux2 cell. It names `(INSTANCE mux)`. The ordinary records keep simple paths; their fields need no producer/Liberty reassignment. One condition must follow the model's new scalar predicate name:

```diff
-(COND (I1===1'b0) (IOPATH I0 Z (0.101:0.211:0.311) (0.401:0.419:0.431)))
+(COND __gls_path_I0_Z_3235b9e3e2cc8771 (IOPATH I0 Z (0.101:0.211:0.311) (0.401:0.419:0.431)))
```

The bare `(IOPATH I1 Z ...)` record stays byte-identical and still matches all three simple I1 → Z paths. A later ordinary I0 record writes only fall, retaining the earlier rise value. A final `() ()` ordinary record writes neither field. [Complete model/helper/SDF diff](../examples/mixed-mux2/reference/changes.diff) · [Converted SDF](../examples/mixed-mux2/reference/converted.sdf) · [Every input record's destination](../examples/mixed-mux2/reference/record-map.json)

| Input occurrence | Processing | Output record count |
|---|---|---:|
| Line 7: positive-unate S → Z | Distribute two real fields using Liberty group 7 | 2 |
| Line 8: conditional I0 → Z | Rename condition; retain leaf and both triplets | 1 |
| Line 9: negative-unate S → Z | Distribute two real fields using Liberty group 6 | 2 |
| Line 10: bare I1 → Z | Keep the original record | 1 |
| Line 11: conditional I0 → Z, fall only | Rename condition; preserve the empty rise slot | 1 |
| Line 12: conditional I0 → Z, both empty | Rename condition; preserve both existing slots | 1 |

The [producer file](../examples/mixed-mux2/producer.json) supplies identities for lines 7 and 9. Ordinary records use the original model's match set, including bare-record fanout. Classification follows source path structure; omitting a required target owner still fails. The independent checker re-derives the mode, target declarations, raw Liberty condition/sense and edge/slot binding. An authentic group hash with the wrong condition is rejected by a separate regression.

The public conversion command takes files and a declared profile rather than a built-in case name:

```sh
python3 -B tools/prepare.py runs/mixed-source \
  --model upstream/gf180mcu_fd_sc_mcu7t5v0__mux2_2.behavioral.v \
  --helper upstream/gf180mcu_fd_sc_mcu7t5v0__mux2_2.functional.v \
  --liberty upstream/gf180mcu_fd_sc_mcu7t5v0__mux2_2__tt_025C_5v00.lib \
  --sdf examples/mixed-mux2/original.sdf \
  --producer examples/mixed-mux2/producer.json
make check-mixed
```

The mixed runner invokes that same file-based entry before compilation. It annotates relative to `bench`, resolving the preserved instance to `bench.mux`, and releases stimulus at 1 ns. The four real select-field deliveries are shown on the home page. The synthetic ordinary paths add these measured events:

| Input event | Expected delay / output | Expected / observed time |
|---|---|---|
| I0 falls at 60 ns; S=0, I1=0 | 617 ps, Z falls | 60,617 / 60,617 ps |
| I0 rises at 70 ns; S=0, I1=0 | 211 ps, Z rises | 70,211 / 70,211 ps |
| I0 falls at 80 ns; S=0, I1=0 | 617 ps, Z falls | 80,617 / 80,617 ps |
| I1 rises at 100 ns; S=1, I0=0 | 811 ps, Z rises | 100,811 / 100,811 ps |
| I1 falls at 110 ns; S=1, I0=0 | 877 ps, Z falls | 110,877 / 110,877 ps |

Actual path snapshots check all eight path objects. The named I0 path reads `(211,419)`, then `(211,617)`, then `(211,617)` ps after its successive writes. The real select fields round to `(290,428)` ps on posedge and `(446,382)` ps on negedge. [Measured results](../examples/mixed-mux2/reference/results.json) · [Frozen events and windows](../examples/mixed-mux2/expected.json)

Three dynamic negatives run the unchanged stimulus through ordinary `$sdf_annotate` to its final 120 ns, then fail `MIXED_PIN_EVENTS`: swapping input edges moves the first select event to 10,446 ps; dropping I1's record moves its first event to 101,000 ps; leaving I0's condition unsynchronized moves its first data fall to 61,000 ps. These runs compile successfully and reach the event checker. The positive uses `$sdf_annotate_initial`; the original strict-entry negative separately checks rejection before stimulus. Source tests also reject the wrong record/field relation before simulation.

## Build environment

Use Linux, a checkout path without spaces, a C/C++ compiler, make, autoconf, flex, bison, gperf, Python 3.9+, Git, patch, tar and coreutils. Python has no third-party dependencies. `make build` uses Icarus `5b9ce29` (the merge of PR #1771), fixed in [build.sh](../tools/build.sh), plus [initial-annotation.patch](../patches/initial-annotation.patch). `JOBS=8 make build` selects eight compiler jobs. To reuse a local clone or transfer inputs to an offline machine:

```sh
git -c tar.umask=0002 -C /path/to/iverilog archive --format=tar \
  5b9ce29b41d6af30e6ccb6e178d3ed2a71974e69 -o /tmp/icarus-source.tar
ICARUS_ARCHIVE=/tmp/icarus-source.tar make build
```

The build script verifies the archive against its stored checksum before extraction. Supply a `git archive` tar with the command above; a GitHub-generated tar.gz has different bytes. [Validation manifest](validation.json) records the source, patches and installed tool identities.

An existing Linux Docker image with the listed build tools can run the same commands without network access. Set `IMAGE` to that image's immutable ID and prepare the archive above:

```sh
docker run --rm --network none --pull never --user "$(id -u):$(id -g)" \
  --entrypoint /bin/sh -v "$PWD:/repo" -v /tmp/icarus-source.tar:/input/icarus-source.tar:ro \
  -w /repo "$IMAGE" -c 'ICARUS_ARCHIVE=/input/icarus-source.tar make build && make check && make check-upstream'
```

Keep using the same `/repo` mount when running that installed toolchain: Icarus embeds its installation prefix. [Current validation](validation.md) records the actual image and commands used here. The checkout, authenticated archive and ordinary build dependencies supply the run inputs.

## Updating derived references

`examples/*/reference/` and `examples/reference/` are the single committed reference set. Normal checks compare against them without writing. After an intentional implementation change, run the affected runner with `--refresh-references` (`run.py`, `run_annotation.py`, `run_mixed.py` or `run_carry.py`), review the diffs and record the validation. This regenerates the full diffs and location maps together; [expected.json](../examples/expected.json) remains an independent input.
