# Find a family, then inspect its paths

A **family** is a logic type such as mux2. A **master** fixes the track library and drive strength, such as `gf180mcu_fd_sc_mcu7t5v0__mux2_2`. An **endpoint group** fixes that master, one input and one output. Conditional membership is collected across the entire specify block for that group, including declarations after `ifnone`.

## Family and endpoint structure

The table retains the eight combinational families from the historical nine-track route. Master names below omit `gf180mcu_fd_sc_mcu9t5v0__`. Conditional counts describe each listed replacement endpoint; the positive/negative fallback pair is additional.

| Family | Historical nine-track masters | Replacement endpoint groups | Conditions per group | Structural distinction and example |
|---|---|---|---:|---|
| addf | `addf_1` | A/B/CI → S (3) | 4 | Other two inputs define binary membership. CO paths stay unchanged. [Worked sum path](examples.md#addf-four-conditions-including-members-after-ifnone). |
| addh | `addh_1`, `addh_2`, `addh_4` | A/B → S (6) | 0 | Paired unconditional replacement; carry is a separate destination. |
| mux2 | `mux2_2` | S → Z (1) | 0 | Same output also has conditional simple data paths. [Seven-track field example](examples.md#mux2-real-fields-with-no-select-conditions) demonstrates this structure in its own library. |
| mux4 | `mux4_2` | S0/S1 → Z (2) | 16 | Four data pins plus the other select define membership. Unselected X can activate fallback. [Worked mux path](examples.md#mux4-an-unselected-x-and-two-fallback-deliveries). |
| xnor2 | `xnor2_2`, `xnor2_4` | A1/A2 → ZN (4) | 0 | Paired fallback; unateness still determines field ownership. |
| xnor3 | `xnor3_2`, `xnor3_4` | A1/A2/A3 → ZN (6) | 4 | Binary conditions on the other two inputs; inverted parity output. |
| xor2 | `xor2_2`, `xor2_4` | A1/A2 → Z (4) | 0 | Paired fallback on non-inverted parity output. |
| xor3 | `xor3_2` | A1/A2/A3 → Z (3) | 4 | Binary conditions on the other two inputs. |

This is **13 masters and 29 replacement groups**: 15 with zero, 12 with four, and two with sixteen conditions. Six additional mux data groups—mux2 I0/I1 → Z and mux4 I0/I1/I2/I3 → Z—retain simple paths with explicit predicates. Condition counts index the structures; the actual scalar comparisons, endpoints, edges and Liberty owners determine the conversion. [Historical inventory and directed results](https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_sc_mcu9t5v0/issues/3#issuecomment-6596739026)

For seven-track SHA3, the suffix inventory adds `mux2_4` S → Z and omits both `xor2_4` groups: **13 masters, 28 groups**. These are different library models even where suffixes match.

## Source inventory versus executed coverage

| Pinned public source scan | Masters | Any `ifnone` | Edge-sensitive `ifnone` masters | Edge-sensitive declarations |
|---|---:|---:|---:|---:|
| [Nine-track](https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_sc_mcu9t5v0/tree/02b7af3f8d88c0b014d9af3db6a17f02aa983305/cells) | 229 | 108 | 36 | 120 |
| [Seven-track](https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_sc_mcu7t5v0/tree/0ef8889a8df0acf959683fbe73013f342a2206a2/cells) | 229 | 108 | 36 | 120 |

Each source scan counts every `cells/<family>/*.behavioral.v` master once. The 36 target masters comprise the eight combinational families above and four scan families, each at strengths 1/2/4. The scan families `sdffq`, `sdffrnq`, `sdffrsnq`, `sdffsnq` have a **single rising-clock fallback**, with clock-to-Q conditions. Their separate finite scan-profile work is described in the [model discussion](https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_sc_mcu9t5v0/issues/3). The converter here expects a paired-edge combinational structure; the scan form needs its own profile.

A source inventory establishes where the syntax occurs. Structural checking establishes the generated path relation. Field checking establishes source-to-slot ownership. Readback observes annotated slots. Pin events establish timed delivery for the supplied stimuli. These evidence types have different populations:

## Historical execution and current examples

| Evidence | Structural / field coverage | Dynamic coverage |
|---|---|---|
| Historical nine-track combinational route | 13 masters, 29 replacement groups, six collateral mux data groups; structure, binding and readback | D1–D9 representative xnor2, mux4 and addf behavior; invalid annotation, ordered partial writes and genuine time-zero history |
| Historical seven-track minimal circuit | mux2_2 S → Z; complete circuit contained 20 IOPATH, 10 timing and 14 INTERCONNECT records | Retained-capture reassessment passed the selected observations and expected violations |
| Historical seven-track SHA3 | 13 masters, 28 propagation groups | C35 capture, C42 complete declared reassessment: scoped timed GLS **PASS_NON_SIGNOFF**, physical acceptance **FAIL**; representative independent waveforms |
| Current nine-track addf_1 | Three sum groups rewritten (18 → 30 paths); nine carry declarations unchanged; two supplied fields checked | One conditional A → S delivery |
| Current nine-track mux4_2 | Two select groups plus four collateral data groups (72 → 104 paths); four supplied fields checked and read back | Two fallback S0 → Z deliveries |
| Current seven-track mux2_2 | One select group plus two collateral data groups (8 → 8 paths); four real fields checked offline | Uses the historical minimal-circuit evidence above |

The current examples use the supplied original Boolean helpers. Nine-track SDF delays are synthetic and asymmetric; seven-track values and ownership are reconstructed from real producer records. The [current validation record](validation.md) separates reruns from reused historical evidence. Whole-library dynamic qualification, independent-simulator agreement and original-model equivalence require further evidence; the SHA3 physical failure remains part of its historical result.

Both historical seven-track profiles identify the installed aggregate model by SHA256 `9a21c5f98200acfe77d8ba52067164e0802284dc1c1e117f0e64fb6ac42eb64b`. The accepted SHA3 TT aggregate Liberty is `330aa9439255e3870ad7adfb987cd4d7bcfa7b6f9fb0cd0a712400e9bd80e38a`. These installation identities are distinct from the public per-cell source-scan pins. Today's individual inputs are authenticated by [inputs.json](inputs.json).
