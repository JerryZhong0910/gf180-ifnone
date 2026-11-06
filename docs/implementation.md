# Sources, assumptions and runtime

The model and SDF emitters in `tools/convert.py` are extracted from the research implementation of `standard_model` and `standard_cell`. The source verifier in `tools/verify.py` separately reconstructs the predicate cone and checks original declaration membership, edges, slots, untouched text and ordered SDF records. Its expected ownership comes from the original model, the authenticated writer identity and the raw Liberty sense/condition. The generator's mapping is checked last. The two public fixtures use per-cell PDK source files, an explicit small inventory, and file-local line numbers. They need no chip netlist.

Each original conjunction is a local `wand` of scalar case equalities; a `wor` combines membership. `membership === 1'b0` enables the fallback. The compiler retains the named scalar condition alongside the actual module path. The SDF consumer matches scope, source, destination, edge and the compiled predicate key. A generic bare endpoint alone cannot distinguish two unqualified producer records with different Liberty senses. Writer IDs in the fixture are bound to original record and raw timing-group digests. Delay magnitudes do not select the owner.

**Dependencies.** Start from public Icarus commit `9f26050130988d661cec6ab11b43d45f7ef533f5` and apply [the source patch](../patches/ordinary-sdf-condition.patch). It carries the scalar predicate identity through the compiler/target/VVP interface, binds bare named SDF conditions, and reports effective slots after each write in verbose mode. A time-zero system task, `$sdf_annotate_initial`, checks the named target population and returns an error for a missing conditional path. Earlier writes remain visible on rejection. The demo bench performs both annotations while its inputs are still unknown and drives its first inputs at 1 ns. This finite entry does not implement the historical full-design supervisor or every form of SDF condition.

In a control run on the same public base without the patch, using its standard `$sdf_annotate` entry, the SDF parser emitted six unsupported-COND warnings and left the 1 ns path defaults active. The three pin events occurred at 11,000 / 51,000 / 71,000 ps. This distinguishes conditional field binding from correct functional output alone.

The larger research execution also checked genuine history at time zero and general event competition with a patched runtime and observer. The two release stimuli select paths after time has advanced and after the documented input settling step. The release uses pin and source observations, settled named predicates and per-write path readback. It does not require the independent [Icarus time-zero history PR #1704](https://github.com/steveicarus/iverilog/pull/1704) or inherit that PR's time-zero result. The [escaped-name PR #1694](https://github.com/steveicarus/iverilog/pull/1694) is independent as well.

Upstream status checked on **2026-11-06**:

| Contribution | Upstream status | Relationship to RC1 |
|---|---|---|
| [#1694 — escaped identifier boundaries](https://github.com/steveicarus/iverilog/pull/1694) | Merged as `3b5615f55eea381aa03aea019691c9cc5d03f280` | Separate parser repair; RC1 retains its accepted source pin and does not require this patch. |
| [#1704 — first matching edge](https://github.com/steveicarus/iverilog/pull/1704) | Open, unmerged | Separate scheduling repair; RC1's scored events occur after the documented settling step. |
| RC1 named-condition binding and cold annotation | Experimental patch distributed here | Required by the supplied `make build` / `make check` route; upstream adoption is not claimed. |

The build remains pinned to `9f26050130988d661cec6ab11b43d45f7ef533f5` with the bundled patch. Upstream status updates do not change the accepted executable or scientific inputs.

**Format limits.** The intake accepts the pinned scalar cell source syntax, a single-cell 1 ns SDF envelope, two explicit output triplets per source record, and positive/negative-unate combinational owners. It preserves all three supplied tokens but the simulation selects typical. Names and input files are pinned for these examples. Each zero-based writer group ordinal is checked against a raw group hash, the actual related pin, output and original condition. Source readback/derivation is independent of the net names produced by the generator.

Release provenance for the converter and checker: research revision `424bf08221c027a374271b8d173f100a472a9d6b`, functions in `prepare_owned_inputs.py`, `independent_owned.py` and `producer_formats.py`. The new standalone input reader, build route, scoped native port and testbench are release adaptations. The source build, distributions and operating-system requirements are part of this package's validation boundary.
