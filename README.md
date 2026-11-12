# GF180 edge-sensitive `ifnone`: model and SDF repair

Some GF180 cell models attach `ifnone` to an edge-sensitive timing path. Icarus warns that this form is unsupported and omits the declaration. The output can reach the right logic value without the intended path delay.

This repository delivers a candidate GF180 model/SDF repair, runnable examples and independent checks. It makes fallback conditions explicit and assigns each SDF field to its input edge and output transition. The Icarus increments provide the condition binding and annotation checks used by the examples.

[Check input suitability](docs/scope.md) · [Inspect a real change](#what-changes-in-a-real-cell) · [Run the examples](#run-and-see-the-result) · [Supply your own files](docs/examples.md#inputs-for-another-cell) · [Review the Icarus changes](docs/implementation.md#what-fixed-upstream-icarus-owns)

## What changes in a real cell?

Start with seven-track `mux2_2`, select input **S → Z**. Its source has no conditional declarations on that endpoint, so the candidate removes `ifnone` and keeps both input edges:

```diff
-ifnone
-// comb arc posedge S --> (Z:S)
- (posedge S => (Z:S)) = (1.0,1.0);
+(posedge S => (Z : S)) = (1.0,1.0);

-ifnone
-// comb arc negedge S --> (Z:S)
- (negedge S => (Z:S)) = (1.0,1.0);
+(negedge S => (Z : S)) = (1.0,1.0);
```

The two [source SDF records](examples/mux2-7t/original.sdf) both say `(IOPATH S Z ...)`. The [producer ledger](examples/mux2-7t/producer.json) identifies one as positive-unate Liberty group 7 and the other as negative-unate group 6. This information is an input to the conversion: endpoints, record order and delay magnitudes cannot recover it. For the positive-unate record, the actual SDF change is:

```diff
-(IOPATH S Z (0.289752:0.289752:0.289752) (0.382399:0.382399:0.382399))
+(IOPATH (posedge S) Z (0.289752:0.289752:0.289752) ())
+(IOPATH (negedge S) Z () (0.382399:0.382399:0.382399))
```

The empty companion slot keeps its previous value. The negative-unate record supplies the other two fields. **The independent checker verifies all four field bindings; `make check-mixed` measures their delivery.** Its [complete Verilog/helper/SDF diff](examples/mux2-7t/reference/changes.diff) also shows how the collateral I0/I1 data paths retain their simple path form while acquiring explicit predicates. [Original model](upstream/gf180mcu_fd_sc_mcu7t5v0__mux2_2.behavioral.v) · [Converted model](examples/mux2-7t/reference/model.v)

With the original mux2 helper and a 1 ns / 1 ps timebase, the mixed-record fixture measures both output transitions for each select edge. The SDF values below are the unchanged real seven-track fields; Icarus rounds each delay to 1 ps before scheduling:

| Input event and data | Output event | Source delay → effective delay | Expected / observed time |
|---|---|---|---|
| S rises at 10 ns; I0=0, I1=1 | Z rises | 0.289752 ns → 290 ps | 10,290 / 10,290 ps |
| S falls at 20 ns; I0=0, I1=1 | Z falls | 0.382399 ns → 382 ps | 20,382 / 20,382 ps |
| S rises at 40 ns; I0=1, I1=0 | Z falls | 0.428267 ns → 428 ps | 40,428 / 40,428 ps |
| S falls at 50 ns; I0=1, I1=0 | Z rises | 0.445571 ns → 446 ps | 50,446 / 50,446 ps |

[Measured mixed-path results](examples/mixed-mux2/reference/results.json) also include the ordinary I0/I1 paths. For conditions on addf/mux4 and the different clock-path structure of scan cells, see [current scope](docs/scope.md).

## Would simple paths preserve separate input-edge delays?

On the fixed Icarus build used here, repeated bare `ABSOLUTE IOPATH` records overwrite supplied output-rise/fall slots in source order. Edge-qualified SDF records do not match a simple model path. Keeping separate input-edge paths lets the two edges receive different values. [The measured comparison](docs/examples.md#what-happens-if-the-select-path-becomes-simple) shows actual path readback and output events for both record orders and all three triplet selections.

## Run and see the result

Use Linux with Python 3.9+ and the [build dependencies](docs/examples.md#build-environment). Run from the repository root in a path without spaces:

```sh
make build
make check
make check-upstream
```

`make build` verifies and builds the fixed Icarus source plus the two local patches under `.build/install`. [Offline and Docker instructions](docs/examples.md#build-environment) use the same source and checks. `make check` runs the source suite, supplied cell examples, edge-annotation comparisons and negative controls; `make check-upstream` adds the selected Icarus condition and event regressions.

Each example runner prints a fresh `runs/` directory containing its generated files and raw logs. Success requires source checks, actual path readback, complete expected output events and rejection of the intended corruptions. Normal runs also reproduce the committed references. [Commands and output guide](docs/examples.md#run-and-interpret-the-results)

| Inspect or run | What to look for |
|---|---|
| [Seven-track mixed mux2](docs/examples.md#convert-target-and-ordinary-records-together), `make check-mixed` | The four select events above plus five data-path events; ordinary records and partial writes remain effective. |
| [Nine-track addf sum](docs/examples.md#addf-four-conditions-including-members-after-ifnone), included in `make check` | Conditions after `ifnone` join the fallback membership; A → S delivers at 10,233 ps. |
| [Nine-track mux4](docs/examples.md#mux4-an-unselected-x-and-two-fallback-deliveries), included in `make check` | An unselected X enables fallback while the output stays known; Z delivers at 50,511 and 70,617 ps. |
| [Nine-track addf carry](docs/examples.md#addf-carry-preserve-the-record-and-bind-its-condition), `make check-carry` | The original carry condition stays intact; CO delivers at 10,211 and 20,419 ps. The binding fix is [Icarus PR #1771](https://github.com/steveicarus/iverilog/pull/1771). |
| [Input-edge annotation comparison](docs/examples.md#what-happens-if-the-select-path-becomes-simple), `make check-annotation` | 36 model/record/order/corner combinations compare actual paths and complete event lists. |

Nine-track delays and the ordinary mux2 data-path delays are asymmetric synthetic fixtures; the seven-track select fields above come from real producer records. [Scope](docs/scope.md#executed-coverage) separates model conversion, supplied-field checking and simulated events for each master. [Validation](docs/validation.md) records the tools, commands and results; [input identities](docs/inputs.json) and the [validation manifest](docs/validation.json) maintain the full checksums.

[GF180 model discussion](https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_sc_mcu9t5v0/issues/3) · [Icarus discussion](https://github.com/steveicarus/iverilog/discussions/1696) · [Earlier family and application results](https://github.com/JerryZhong0910/gf180-ifnone/blob/98c39b18f0ecd4fa25080d35aa24cc2a6bca600a/docs/scope.md#historical-execution-and-current-examples) · [RC1 release](https://github.com/JerryZhong0910/gf180-ifnone/releases/tag/rc1) · [Licenses and credits](NOTICE.md)
