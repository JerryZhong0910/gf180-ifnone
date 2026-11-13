# Fixed upstream upgrade validation — 2026-11-13

The fixed tool is now official Icarus merge [`5b9ce29`](https://github.com/steveicarus/iverilog/commit/5b9ce29b41d6af30e6ccb6e178d3ed2a71974e69), which merged [PR #1771](https://github.com/steveicarus/iverilog/pull/1771). Upstream supplies the `===` condition identity repair, so the duplicate local case-equality patch is removed. The original GF180 models, SDF inputs, owner relationships, independent event expectations and all 46 reference files are unchanged.

[Current scope](scope.md) describes accepted inputs and executed coverage. [Implementation](implementation.md#what-fixed-upstream-icarus-owns) separates upstream responsibilities from the remaining local initialization/readback facility.

## Build and patch identity

The merge's code tree is identical to the independently tested PR candidate. The new source was exported from the official merge, authenticated by the digest in [build.sh](../tools/build.sh), and freshly configured, built and installed in the same Linux Docker image used for the previous validation, with networking disabled. The compiler's own `make check` passed.

The remaining [initial-annotation patch](../patches/initial-annotation.patch) needed new context because upstream inserted an INTERCONNECT helper before `sdf_fname`. Its added/removed source lines are identical to the previous patch's applied delta; only context and hunk positions changed. It applies to the new source with zero fuzz and zero offsets. The fresh build uses this single patch, and its cache stamp binds the new commit and that patch's content.

[validation.json](validation.json) records the complete source, patch, installed binary and evidence hashes. The [input manifest](inputs.json) continues to authenticate the supplied PDK files, fixtures and independent expectations.

## Commands and results

From the repository root, using the [build environment](examples.md#build-environment):

```sh
make build
make check
make check-upstream
```

The build was fresh for this upgrade. The public checks ran against that installed tool without regenerating any reference or expected-event input.

| Check | Observed result |
|---|---|
| Source regressions | 14/14 passed, including source membership, field binding, ordinary-record retention and condition synchronization. |
| Original addf/mux4 examples | All six ordered writes and complete expected event lists reproduced: S at 10,233 ps; Z at 50,511/70,617 ps. |
| Strict initialization negative | Unknown second predicate rejected after preserving the first write and before stimulus. |
| Input-edge annotation controls | All 36 combinations of model, SDF record form/order and min/typ/max triplet selection passed actual path readback and four scored events each. |
| Mixed mux2 | Nine events and all eight path objects matched; each of three corruptions completed the stimulus and failed the independent event check. |
| Addf carry | Original carry COND retained; CO at 10,211/20,419 ps. All nine carry paths checked; eight retain their 1 ns defaults. |
| Committed references | All 46 reproduced unchanged, including the carry and mixed-record results. |
| Upstream native selection | 23/23 passed: 20 condition-binding tests and three existing event tests. This includes the merged case-equality test and four OR tests. |
| Upstream COND through vlog95 | 20 expected outcomes: eight simulations passed and 12 existing translation cases retained their expected compile errors. The new case-equality fixture checks all 32 events in both native and translated flows. |

The additional vlog95 check uses the same upstream tests and their existing expectations. With the fixed installation available at the path used to build it, run:

```sh
gf180_root=$PWD
icarus_source=$(cat .build/SOURCE)
sed -n '/^sdf_cond/p' tests/upstream.list > /tmp/gf180-cond.list
(cd "$icarus_source/ivtest" && PATH="$gf180_root/.build/install/bin:$PATH"   python3 -B vvp_reg.py --vlog95 /tmp/gf180-cond.list)
```

The case-equality regression uses standard `$sdf_annotate` without PDK inputs. Its fixture bytes match the original PR's frozen inputs. The existing operator-mismatch regressions remain effective; `===` and `==` retain different condition identities. The [public test list](../tests/upstream.list) makes these upstream checks part of the fixed tool's regression selection.

## Comparison with earlier evidence

The new execution replaces the fixed-tool identity for current use. It preserves the selected model/SDF strategy and independent predictions. The [preceding validation](https://github.com/JerryZhong0910/gf180-ifnone/blob/efb18976afa3dba64c5430dba0c662fa45a75300/docs/validation.md) retains the original carry failure, research handoff and independent PR baseline comparison under their original tool identities. [RC1 acceptance](release.md) and [historical family/application results](https://github.com/JerryZhong0910/gf180-ifnone/blob/98c39b18f0ecd4fa25080d35aa24cc2a6bca600a/docs/scope.md#historical-execution-and-current-examples) remain at their existing locations.

The local `gf180-ifnone-upstream-1771-20261113/` execution record contains the baseline, verified merge metadata, authenticated archive, patch-context comparison, fresh build log, native/vlog95 logs and document checks. Original PDK inputs, event expectations, references, `rc1` and historical releases remain unchanged.
