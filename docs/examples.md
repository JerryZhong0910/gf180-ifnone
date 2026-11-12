# Follow a source field through the repair

Each case keeps its SDF input, producer identity and generated reference together under `examples/`. Original PDK model, helper and Liberty bytes have one home in `upstream/`. The complete diffs below include every model edit, the helper module-name adaptation and every SDF change. `source-map.json` locates all paths; `field-map.json` locates the annotated fields. Original and generated line numbers are measured separately.

| Case | Source inputs | Full change and result |
|---|---|---|
| Seven-track mux2_2 | [Model](../upstream/gf180mcu_fd_sc_mcu7t5v0__mux2_2.behavioral.v), [Liberty](../upstream/gf180mcu_fd_sc_mcu7t5v0__mux2_2__tt_025C_5v00.lib), [SDF](../examples/mux2-7t/original.sdf), [owners](../examples/mux2-7t/producer.json) | [Diff](../examples/mux2-7t/reference/changes.diff), [model](../examples/mux2-7t/reference/model.v), [fields](../examples/mux2-7t/reference/field-map.json), [all paths](../examples/mux2-7t/reference/source-map.json) |
| Nine-track addf_1 | [Model](../upstream/gf180mcu_fd_sc_mcu9t5v0__addf_1.behavioral.v), [Liberty](../upstream/gf180mcu_fd_sc_mcu9t5v0__addf_1__tt_025C_5v00.lib), [SDF](../examples/addf/original.sdf), [owners](../examples/addf/producer.json) | [Diff](../examples/addf/reference/changes.diff), [model](../examples/addf/reference/model.v), [fields](../examples/addf/reference/field-map.json), [all paths](../examples/addf/reference/source-map.json) |
| Nine-track mux4_2 | [Model](../upstream/gf180mcu_fd_sc_mcu9t5v0__mux4_2.behavioral.v), [Liberty](../upstream/gf180mcu_fd_sc_mcu9t5v0__mux4_2__tt_025C_5v00.lib), [SDF](../examples/mux4/original.sdf), [owners](../examples/mux4/producer.json) | [Diff](../examples/mux4/reference/changes.diff), [model](../examples/mux4/reference/model.v), [fields](../examples/mux4/reference/field-map.json), [all paths](../examples/mux4/reference/source-map.json) |

## mux2: real fields with no select conditions

For seven-track `mux2_2`, S → Z contains a positive-edge and negative-edge `ifnone`, with no conditional member on that endpoint. Removing the fallback keyword yields the pair shown on the [home page](../README.md#what-changes-in-a-real-cell). The conditions on I0/I1 → Z belong to different endpoint groups and do not determine the S → Z fallback.

The source SDF's two bare S → Z records need distinct Liberty identities. The ledger binds record occurrence **and both output fields** to raw timing-group hashes, related pin, output pin and sense. Group ordinals are zero-based within the master; SDF line numbers are one-based. The source order is:

| Source SDF | Liberty owner | Output-rise field → input edge | Output-fall field → input edge |
|---|---|---|---|
| Line 7, historical record 6 | group 7, positive unate | 0.289752 ns → posedge S | 0.382399 ns → negedge S |
| Line 8, historical record 7 | group 6, negative unate | 0.445571 ns → negedge S | 0.428267 ns → posedge S |

The [converted SDF](../examples/mux2-7t/reference/converted.sdf) writes one field per child, in source-record order, rise child then fall child. The final pairs are `(0.289752, 0.428267)` ns for posedge S and `(0.445571, 0.382399)` ns for negedge S. The checker verifies all four fields against the original declarations and Liberty groups.

These records come from a historical routed minimal circuit. The reduced ledger retains source digests and original byte offsets; the SDF wrapper was rebuilt for this single-cell example. The supplying Liberty group text matches the historical group hashes. Current execution checks the mapping offline; the historical circuit simulation is listed separately in [scope](scope.md#historical-execution-and-current-examples).

The full diff also rewrites six I0/I1 → Z declarations to named conditions and explicit fallback. Their simple path form, endpoints and one-to-one multiplicity stay intact. The independent checker verifies these predicate cones as well as the select pair.

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

## Run and interpret the results

All supplied model, helper, Liberty, SDF, producer, bench and expected-event inputs are authenticated by [inputs.json](inputs.json). The converter accepts the pinned scalar source syntax, one-cell 1 ns SDF envelopes, explicit rise/fall triplets, and positive/negative-unate combinational Liberty owners. To prepare a different fixture, supply its exact endpoint inventory and declaration populations, and an acquisition-time owner identity for **each source record and output field**. A real producer with missing or ambiguous identities must be resolved at its source; the converter cannot infer those identities from the SDF numbers.

From the repository root:

```sh
make build
make check
# Source-only conversion and checking; no simulator needed:
python3 -B tools/prepare.py runs/source-review
# An explicit fresh destination and an already built tool prefix:
python3 -B tools/run.py --prefix .build/install --out runs/review
```

Use a new output directory for each command. A passing full run prints the three expected/observed times, missing-owner rejection, unknown-predicate rejection, and `PASS 20 derived references reproduced`. `make check` also runs the source regressions. Inspect:

| Output | What it establishes |
|---|---|
| `<case>/changes.diff`, `model.v`, `helper.v`, `converted.sdf` | Complete generated change from the shipped inputs |
| `<case>/source-map.json` | Source/generated locations for every path, including collateral and untouched paths |
| `<case>/field-map.json` | SDF occurrence, Liberty group/sense, edge, slot and generated location for each supplied field |
| `capture.log`, `delivery.json` | Ordered writes, observations and source-to-pin event chains |
| `invalid-annotation/capture.log` | Unknown second predicate rejected after the first write and before stimulus |

The missing-owner negative fails at `MISSING_FIELD_OWNER`. The annotation negative must return exit 1, report the unknown compiled condition, retain the first readback and release no input events. Source regressions additionally corrupt membership, collateral endpoints, carry text and unequal field bindings. A nonzero command status is a failed check; source-only success establishes structure and mapping, while the full run also establishes the declared pin events.

### Build environment

`make build` uses public Icarus commit `beb32f3945f5be1f45cf5d898d440161e9c6f113` plus [initial-annotation.patch](../patches/initial-annotation.patch). The tool requirements are listed on the home page. `JOBS=8 make build` selects eight compiler jobs. To reuse a local clone or transfer inputs to an offline machine:

```sh
git -c tar.umask=0002 -C /path/to/iverilog archive --format=tar \
  beb32f3945f5be1f45cf5d898d440161e9c6f113 -o /tmp/icarus-source.tar
ICARUS_ARCHIVE=/tmp/icarus-source.tar make build
```

The exported archive SHA256 is `4d6471d2a79b2dcbf1270b9f494c772fd4b35e9d844683b11552c724f8283407`. The script checks it before extracting. This is a `git archive` tar, not a GitHub-generated tar.gz.

An existing Linux Docker image with the listed build tools can run the same commands without network access. Set `IMAGE` to that image's immutable ID and prepare the archive above:

```sh
docker run --rm --network none --pull never --user "$(id -u):$(id -g)" \
  --entrypoint /bin/sh -v "$PWD:/repo" -v /tmp/icarus-source.tar:/input/icarus-source.tar:ro \
  -w /repo "$IMAGE" -c 'ICARUS_ARCHIVE=/input/icarus-source.tar make build && make check'
```

Keep using the same `/repo` mount when running that installed toolchain: Icarus embeds its installation prefix. [Current validation](validation.md) records the actual image and commands used here. Source and example execution need no historical container contents.

### Updating derived references

`examples/*/reference/` and `examples/reference/` are the single committed reference set. Normal checks compare against them without writing. After an intentional implementation change, run `python3 -B tools/run.py --refresh-references`, review the diffs and record the validation. This regenerates the full diffs and location maps together; [expected.json](../examples/expected.json) remains an independent input.
