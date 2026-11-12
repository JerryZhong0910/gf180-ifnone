# GF180 edge-sensitive `ifnone`: from model repair to pin timing

Some GF180 cell models attach `ifnone` to an edge-sensitive timing path. Icarus warns that this form is unsupported and omits the declaration. Simulation can therefore produce the right logic value without the intended path delay. A repair must express the fallback condition **and** bind each SDF delay field to the right input edge and output transition.

This repository supplies a candidate model/SDF conversion, an independent source checker, a small Icarus annotation patch, and reproducible examples. It connects the proposed GF180 model repair to incremental Icarus support. The selected modeling rule uses exact binary condition membership and an endpoint-local fallback; its relationship to the original library authors' intended four-state behavior remains an open modeling question.

## What changes in a real cell?

Start with seven-track `mux2_2`, select input **S → Z**. Its source has no conditional declarations on that endpoint, so the fallback becomes an ordinary unconditional edge pair:

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

The empty companion slot keeps its previous value. The negative-unate record supplies the other two fields. **This example checks all four field bindings from real producer records.** Its [complete Verilog/helper/SDF diff](examples/mux2-7t/reference/changes.diff) also shows how the collateral I0/I1 data paths retain their simple path form while acquiring explicit predicates. [Original model](upstream/gf180mcu_fd_sc_mcu7t5v0__mux2_2.behavioral.v) · [Converted model](examples/mux2-7t/reference/model.v)

## Which case answers my question?

| Question | Read and inspect |
|---|---|
| How do two bare SDF records get different edge/slot owners? | [mux2: real seven-track fields](docs/examples.md#mux2-real-fields-with-no-select-conditions) |
| How are conditions after `ifnone` included in the fallback? | [addf: four conditions and a measured sum event](docs/examples.md#addf-four-conditions-including-members-after-ifnone) |
| Can an unselected X trigger fallback while the output stays known? | [mux4: sixteen conditions and two measured deliveries](docs/examples.md#mux4-an-unselected-x-and-two-fallback-deliveries) |
| Which families and endpoint structures are covered? | [Family, master and coverage tables](docs/scope.md) |
| What does the converter require, and how do I run it? | [Inputs and commands](docs/examples.md#run-and-interpret-the-results) |
| Which responsibilities remain in the Icarus patch? | [Implementation and upstream boundary](docs/implementation.md) |

## Run and see the result

Use Linux with a C/C++ compiler, make, autoconf, flex, bison, gperf, Python 3.9+, Git, patch, tar and coreutils. Python needs no third-party packages. Run from a checkout of this revision, in a directory without spaces:

```sh
make build
make check
```

The build fetches the [fixed public Icarus commit](https://github.com/steveicarus/iverilog/commit/beb32f3945f5be1f45cf5d898d440161e9c6f113), verifies its exported source digest, and installs under `.build/install`. [Offline and Docker instructions](docs/examples.md#build-environment) reuse the same source. `make check` runs source regressions, converts all three cases, simulates the two nine-track cases, checks negative controls, and reproduces the committed references. It prints a fresh `runs/case-…/` directory containing raw logs and field-to-pin chains.

| Nine-track fixture | Input event | Source delay | Expected / observed output time |
|---|---:|---:|---:|
| `addf_1`, A → S | A rises at 10,000 ps | 233 ps | S rises at **10,233 / 10,233 ps** |
| `mux4_2`, S0 → Z | S0 rises at 50,000 ps | 511 ps | Z rises at **50,511 / 50,511 ps** |
| `mux4_2`, S0 → Z | S0 falls at 70,000 ps | 617 ps | Z falls at **70,617 / 70,617 ps** |

These are measured public-fixture results with asymmetric synthetic nine-track SDF values and original PDK functional helpers. Seven-track mux2 is an offline field check. [Current validation](docs/validation.md) identifies the candidate, tools and commands; [RC1 evidence](docs/release.md) preserves the historical acceptance separately.

[GF180 model discussion](https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_sc_mcu9t5v0/issues/3) · [Icarus discussion](https://github.com/steveicarus/iverilog/discussions/1696) · [Input provenance](docs/inputs.json) · [Licenses and credits](NOTICE.md)
