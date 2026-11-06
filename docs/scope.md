# What the library scan and runs cover

The PDK inventory counts each `cells/<family>/*.behavioral.v` master once. An endpoint group is a specific master, input and output. A source declaration, a field binding and an observed output transition are different units of evidence.

| Pinned official library | Masters scanned | Masters with any ifnone | Masters with edge-sensitive ifnone | Edge-sensitive declarations |
|---|---:|---:|---:|---:|
| [Nine-track source](https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_sc_mcu9t5v0/tree/02b7af3f8d88c0b014d9af3db6a17f02aa983305/cells) | 229 | 108 | 36 | 120 |
| [Seven-track source](https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_sc_mcu7t5v0/tree/0ef8889a8df0acf959683fbe73013f342a2206a2/cells) | 229 | 108 | 36 | 120 |

On each track the 36 comprise eight combinational families (addf, addh, mux2, mux4, xnor2, xnor3, xor2, xor3) and four scan families (sdffq, sdffrnq, sdffrsnq, sdffsnq), each at strengths 1/2/4. The scan cells have a single rising-clock fallback with conditions on the clock-to-Q path. They have separate finite research coverage under a scan profile. The converter shipped here expects paired edges on the selected combinational endpoints. The PDK scan pins identify the public files used for this release; they do not establish that every historical installation was built from those exact commits.

| Evidence | Model/SDF scope | Execution scope |
|---|---|---|
| Historical nine-track combinational route | 13 masters in eight families; 29 producer-owned endpoint groups and six additional preserved mux data groups | All 13 covered by structure, binding and readback. D1–D9 exercised representative xnor2, mux4 and addf behavior, including invalid annotation, ordered partial writes and genuine time-zero history. |
| Historical seven-track/11K minimal real-SDF circuit | One mux2_2 select group. The full circuit had 20 IOPATH records, 10 timing records and 14 INTERCONNECT records. | Complete retained-capture reassessment passed for the selected observations and expected violations. |
| Historical seven-track/11K SHA3 | 13 masters; 28 propagation groups. Relative to the nine-track suffix list, seven-track includes mux2_4 S→Z and omits both xor2_4 groups. The cell models belong to different libraries. | C35 simulation plus C42 reassessment: scoped timed GLS PASS_NON_SIGNOFF; physical acceptance FAIL. Representative waveform checks. |
| This source package | Nine-track addf_1 and mux4_2 views. One conditional source SDF record and two bare source SDF records, yielding six checked conditional-field writes. Seven-track mux2_2 has four real field writes checked offline. | Three timed pin deliveries scored on nine-track, using a synthetic writer fixture and original library cells. |

Nine-track `Original conditional declarations per group` counts only original `if (...)` declarations on that endpoint. In the historical 29 groups, 15 had zero such declarations, 12 had four, and two had sixteen. The paired fallback statements are counted separately. The membership rule collects all declarations for the endpoint, including those after `ifnone`. The nine-track 13-master list and D1–D9 are available in the [upstream comment](https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_sc_mcu9t5v0/issues/3#issuecomment-6596739026).

Both historical seven-track profiles identify the installed aggregate Verilog model by SHA256 `9a21c5f98200acfe77d8ba52067164e0802284dc1c1e117f0e64fb6ac42eb64b`. The accepted SHA3 profile identifies its TT aggregate Liberty by `330aa9439255e3870ad7adfb987cd4d7bcfa7b6f9fb0cd0a712400e9bd80e38a`. Per-cell model, helper and Liberty identities for today's source checks are in [inputs.json](inputs.json).

The binary cofactor membership and endpoint-local fallback are selected modeling policies. Original model equivalence, portable execution on other simulators, exhaustive dynamic waveform coverage and physical signoff remain open. The historical scope above does not enlarge the three events measured here.
