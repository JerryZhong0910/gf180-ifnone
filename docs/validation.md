# Maintenance validation — 2026-11-12

The current conversion and reduced runtime reproduce the three scored deliveries and all ordered readbacks from the pre-change baseline. The source/field checks pass for all three cases. Original PDK inputs, producer fixtures, stimulus and independent expected events remain unchanged.

## Candidate and environment

The starting repository HEAD was `1ca8ea512fc21c921e7d8889f0968cb04bb79210`, with a clean working tree; the remote default HEAD matched. This record describes the local maintenance candidate on that base. [validation.json](validation.json) binds the implementation, input manifest, references and tool binaries to SHA256 identities.

| Component | Identity |
|---|---|
| Current Icarus source | `beb32f3945f5be1f45cf5d898d440161e9c6f113` |
| `git archive` source tar SHA256 | `4d6471d2a79b2dcbf1270b9f494c772fd4b35e9d844683b11552c724f8283407` |
| Current [initial-annotation.patch](../patches/initial-annotation.patch) SHA256 | `9096ec309018e69a752ff148c90b73d8f77eb1395e2f51767375f3e3cd5d062c` |
| Docker image used | `cva6-sha3-ready:20261014`, image ID `sha256:9bf368f4b38f15350dec8a8a0283225bcebddf51a91793c800ca60475d37a210` |
| Execution environment | Ubuntu 24.04.4, uid 1000, network disabled; repository at `/repo`, task evidence at `/evidence` |
| Installed tools | Icarus 14.0 development, built from the source and patch above under `/repo/.build/install` |

The fixed public commit was exported from an existing clean local upstream clone. The source archive was authenticated before a fresh container build. Subsequent example/regression runs reused that build. A final source-only export, with no Git history or prior build/run directories, then passed a second fresh offline Docker build and the documented commands. The online fetch path was not executed; the documented offline build path was executed. The container image supplies build tools, while the declared source archive supplies Icarus.

## Commands and observed results

Inside that container, from `/repo`:

```sh
ICARUS_ARCHIVE=/evidence/icarus-source.tar JOBS=4 make build
python3 -B tools/run.py --refresh-references --out /evidence/current
make check
make check-upstream
python3 -B tools/prepare.py /evidence/source-only
```

| Check | Observed result |
|---|---|
| Fresh fixed-source build | Exit 0; patch applied without fuzz; later `make build` reused the matching source/patch stamp |
| Source regression suite | 6/6 passed: compressed source declarations, expanded generated cone, missing after-ifnone member, wrong collateral endpoint, altered carry path, swapped field bindings |
| addf source/field relation | Three replacement groups, two supplied fields passed |
| mux4 source/field relation | Two replacement groups, four supplied fields passed; four collateral simple-path groups checked |
| mux2 seven-track relation | One replacement group, four real fields passed offline; two collateral groups checked |
| Ordered runtime writes | Six writes and both effective slots after each write matched |
| Scored output events | S rise 10,233 ps; Z rise 50,511 ps; Z fall 70,617 ps; complete scored event lists matched |
| Producer negative | Missing rise owner rejected at `MISSING_FIELD_OWNER` |
| Runtime negative | Unknown second condition: exit 1, expected diagnostic, first write retained, no released input events |
| Derived references | All 20 files reproduced; full diffs and measured source locations included |
| [Existing upstream COND tests](../tests/upstream.list) | 15/15 passed, including edges, partial updates, multiple matches, unknown conditions and expression conditions |
| Source-only public command | All three cases passed without simulator execution |

The upstream tests specifically protect ordinary `$sdf_annotate` behavior while the custom initial entry retains stricter checks. `make check-upstream` uses the exact extracted upstream test sources recorded by `make build`; it is a focused regression selection.

## Comparison with the pre-change baseline

Before editing, the original runner was executed with its accepted RC1 toolchain. After the changes:

- Generated model tokens match after removing comments and formatting whitespace. Predicate structure and path multiplicity are unchanged.
- All three generated SDF files and helper files are byte-identical to the baseline.
- Field bindings and deliveries match after excluding relocated generated-model line numbers.
- Ordered readbacks and each passive pin/source/predicate channel match, including initialization events.
- All original input-manifest hashes still match. The independent expected-event file was not regenerated.

The complete [case diffs](examples.md) are regenerated directly from the original model/helper/SDF inputs. Source regressions prove that the checker accepts changed physical layout while still rejecting semantic corruption. This supports a formatting and maintenance refactor of the selected modeling policy.

## Reused evidence and review

The [RC1 clean acceptance](release.md) and earlier seven-/nine-track application results in [scope.md](scope.md) remain historical evidence. Existing records were inspected both in the host extraction workspace and in the retained `cva6-sha3-proc` container. Its original representation document confirms the collateral mux simple-path obligations; its C42 report preserves scoped timed GLS PASS_NON_SIGNOFF and physical acceptance FAIL. No SHA3 or physical run was repeated.

Both public PDK source archives were rescanned: each contains 229 masters, 108 with any `ifnone`, 36 with the target edge-sensitive form and 120 edge-sensitive declarations. Those counts are inventory results, separate from timed coverage.

Independent maintenance review passed local navigation, code/SDF excerpts, complete diffs, all 151 source locators and the first-reader/run-command paths. It found an archive reproducibility issue: user Git `tar.umask` configuration changed the archive digest. Both export commands now fix `tar.umask=0002`; a conflicting-configuration control reproduced the expected digest. Raw task logs, baseline comparison, candidate file hashes and the final review receipt are retained with the local execution record; the reproducible public event and field evidence is beside each example.
