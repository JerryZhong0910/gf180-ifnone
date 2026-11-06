# RC1 release evidence

RC1 connects original GF180 path declarations, producer-owned SDF fields and observed output delivery. Start with [the worked examples](examples.md). The converter, independent source verifier and necessary experimental Icarus patch are included as source.

## Accepted baseline

The local source candidate passed a fresh build and example run on 2026-11-04. It was extracted into an empty directory and executed in rootless Linux mount, PID and network namespaces. Only the extracted source package, the authenticated official Icarus archive and ordinary host OS/compiler dependencies were available. HOME and temporary storage started empty, and network access was disabled. `make build` followed by `make check` completed with exit status 0.

| Build input | Pinned identity |
|---|---|
| Official Icarus source | `9f26050130988d661cec6ab11b43d45f7ef533f5` |
| Official source tarball SHA256 | `7ab87bd7d524783ccdd26d23b1cfa9653311b9602608603d0cd150fe01ac38d2` |
| Bundled `ordinary-sdf-condition.patch` SHA256 | `f4113dec40b35ab777e227f99752bfd162d049bb6d2412a3d124a11b9260ece1` |

This publication adds documentation and upstream status updates. All converter, checker, patch, build, model, Liberty, stimulus, expectation and recorded-reference bytes remain identical to that accepted candidate. No build, control campaign or simulation was rerun for publication.

## Results available in this package

| Track and case | Evidence |
|---|---|
| Nine-track `addf_1` | A rises at 10,000 ps with a 233 ps source delay; S is observed at 10,233 ps. |
| Nine-track `mux4_2` | S0 rises at 50,000 ps and falls at 70,000 ps; Z is observed at 50,511 ps and 70,617 ps. The masked-X condition exercises the fallback. |
| Seven-track `mux2_2` | Four fields from two historical real-producer SDF records are checked offline against source declarations and authenticated Liberty owners. RC1 adds no seven-track simulation. |

The nine-track delays are synthetic, asymmetric SDF inputs. Six ordered conditional writes, their companion slots, settled predicates, source-pin vectors and complete output event lists within the declared windows were checked. Generated models, SDF records, field maps and delivery results matched the included references. [Delivery records](reference/delivery.json) · [Trace](reference/trace.txt) · [Input identities](inputs.json)

Two negative controls establish specific rejection paths. Removing a source-field owner reaches `MISSING_FIELD_OWNER`. Changing the second generated addf condition to an unknown name reaches the initial-annotation error with exit status 1, retains the first write, and stops before stimulus. On the unmodified public Icarus base, the standard annotation entry reported six unsupported-COND warnings and retained 1 ns defaults, giving the three scored output times 11,000 / 51,000 / 71,000 ps.

The [scope table](scope.md) separately preserves historical seven-track and nine-track results. Fresh RC1 measurements cover the declared fixtures and observation windows. They do not establish original-model equivalence, independent-simulator agreement, exhaustive waveform coverage or physical signoff. The extracted patch has not undergone a full upstream regression suite in this package's acceptance run.

## Distribution

The release contains source, public per-cell PDK files, reduced fixture provenance, generated reference files and license texts. It includes no internal chip design, PAD design, application capture, historical workspace, private binary or build output. The Icarus source is downloaded from its public pinned URL, or supplied through the digest-checked `ICARUS_ARCHIVE` option.

Project-owned files use Apache-2.0. PDK files and Icarus-derived changes retain their original terms as detailed in [NOTICE.md](../NOTICE.md). The published source archive and SHA256 checksum are attached to [release rc1](https://github.com/JerryZhong0910/gf180-ifnone/releases/tag/rc1).

The upstream status table in [implementation.md](implementation.md) records #1694 as merged and #1704 as open on 2026-11-06. The bundled experimental condition patch remains separate from both contributions.
