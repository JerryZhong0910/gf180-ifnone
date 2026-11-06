# Follow a field to a pin

The row numbers below are one-based file line numbers; the Liberty group IDs are zero-based ordinals within each master. Every example uses the original helper gates. The checker reads original declarations and Liberty blocks separately, examines the generated HDL and ordered SDF children, and compares their effective slots with VPI readback. An empty companion slot keeps its prior value. The independent [expected pin events](../examples/expected.json) were frozen before simulation.

## Four conditions on addf_1, A → S

In the [original model](../upstream/gf180mcu_fd_sc_mcu9t5v0__addf_1.behavioral.v), the four `if` declarations for A → S test the binary combinations of B and CI. Two appear after the edge-sensitive fallback pair. Grouping by master and both endpoints finds all four. Each gets an input-rise and input-fall child; the two fallback declarations keep their respective edge. The converter verifies the original declarations for CO remain byte-identical in their module context.

With B=CI=0, the original line 90 condition applies and the sum follows A. The generated model uses scalar comparisons and wired conjunction/union to compute membership. For this condition its key is `__gls_path_A_S_9f7c123088d11c7d`. The generated declaration at line 90 reads:

```verilog
if (__gls_path_A_S_9f7c123088d11c7d) (posedge A => (S : A)) = (1.0,1.0);
```

[Original SDF line 7](../examples/addf/original.sdf) supplies both triplets. The [writer identity](../examples/addf/producer.json) points to TT Liberty group 12 at line 1559, positive unate with B=CI=0. Thus source output-rise maps to input posedge. [Generated SDF line 9](reference/addf/converted.sdf) writes the rise triplet `0.211:0.233:0.267`; its fall slot is empty. The compiler uses typical selection. Readback gives 0.233 ns rise and the 1 ns default fall. A rises at 10,000 ps, the predicate reads 1, and S rises at **10,233 ps**. This is the binary A-rise part of the historical D3 stimulus. The present invocation measures the enabled conditional child. [Generated model](reference/addf/model.v) · [Field map](reference/addf/field-map.json)

## Sixteen conditions on mux4_2, S0 → Z

The original S0 → Z group has sixteen conditions checking the data pins and the other select. Each condition gets its two edge children. The fallback predicate is the binary complement of the union of the sixteen exact matches. The generated posedge and negedge fallback statements occupy lines 214 and 218. Four other mux data-input groups keep their original simple path form and one-to-one declaration mapping; the independent checker verifies their predicate cones. [Original mux model](../upstream/gf180mcu_fd_sc_mcu9t5v0__mux4_2.behavioral.v) · [Generated mux model](reference/mux4/model.v)

[Original lines 7 and 8](../examples/mux4/original.sdf) are both bare `(IOPATH S0 Z ...)`. Their owner identities are explicit in the [writer fixture](../examples/mux4/producer.json). The first belongs to negative-unate group 44 (Liberty line 7751), the second to positive-unate group 53 (line 8361). Readback after each write checks the companion slot. Under typical selection the resulting fallback pairs in ps are:

| Input edge | Output-rise slot | Output-fall slot |
|---|---:|---:|
| posedge S0 | 511, group 53 | 839, group 44 |
| negedge S0 | 727, group 44 | 617, group 53 |

At 30 ns the D2-derived stimulus sets S1=0, I0=0, I1=1, I2=X, I3=0 and S0=0. I2 is unselected by the Boolean mux yet its X prevents the binary cofactors from matching. S0 rises at 50 ns and falls at 70 ns. The receiving-pin observations and settled fallback predicate agree with this setting. Positive-unate output rise and fall are delivered at **50,511 ps** and **70,617 ps**, respectively. All four slot values were read back; these two events exercise the 511 and 617 ps fields. [Generated SDF](reference/mux4/converted.sdf) · [Field map](reference/mux4/field-map.json)

## Read the evidence

`make check` also exercises the initialization and the first mux cofactor before the second setting. The scored windows are 9–80 ns for the sum and 40–80 ns for the mux. Within each window the checker compares the complete ordered output event list, including value, time and population. Predicate probes sample the settled input slot; they do not claim independent observation of every internal delta cycle. [Recorded pin deliveries](reference/delivery.json) · [Pin observations and ordered readbacks](reference/trace.txt)

For a source-only inspection run `python3 -B tools/prepare.py NEW_DIRECTORY`. This regenerates the three views, their SDF files and field maps and checks the source relation. The [runtime check](../tools/run.py) additionally compiles and simulates the two nine-track masters.

## Seven-track real SDF fields

The two mux2_2 S → Z records in [the seven-track excerpt](../examples/mux2-7t/original.sdf) were reconstructed from original producer record IDs 6 and 7 for the research minimal circuit. The [reduced ledger](../examples/mux2-7t/producer.json) includes the original byte offsets, source digests and the verified Liberty group hashes. Each supplying TT group matches the historical group text byte-for-byte. The SDF envelope was rebuilt for this example.

| Input edge | Output rise (ns) | Output fall (ns) |
|---|---:|---:|
| posedge S | 0.289752 (group 7) | 0.428267 (group 6) |
| negedge S | 0.445571 (group 6) | 0.382399 (group 7) |

The seven-track checker verifies both source declarations, all collateral mux data declarations and all four generated field writes offline. The historical minimal circuit also had a clocked cell and six delay cells. Its own simulation and reassessment provide the seven-track dynamic evidence. [Converted real fields](reference/mux2-7t/converted.sdf) · [Field map](reference/mux2-7t/field-map.json)
