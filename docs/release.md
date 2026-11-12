# Historical RC1 acceptance

This page records the **2026-11-04 acceptance and 2026-11-06 publication**. The current implementation and results are described in [validation.md](validation.md). Historical release/tag bytes remain available at [rc1](https://github.com/JerryZhong0910/gf180-ifnone/releases/tag/rc1).

The accepted candidate was extracted into an empty directory and executed in rootless Linux mount, PID and network namespaces. Only the extracted source, authenticated official Icarus archive and ordinary host compiler/OS dependencies were visible. HOME and temporary storage started empty; networking was disabled. `make build` and `make check` returned 0.

| Historical build input | Identity |
|---|---|
| Icarus source | `9f26050130988d661cec6ab11b43d45f7ef533f5` |
| Official tarball SHA256 | `7ab87bd7d524783ccdd26d23b1cfa9653311b9602608603d0cd150fe01ac38d2` |
| [RC1 condition patch](https://github.com/JerryZhong0910/gf180-ifnone/blob/rc1/patches/ordinary-sdf-condition.patch) SHA256 | `f4113dec40b35ab777e227f99752bfd162d049bb6d2412a3d124a11b9260ece1` |
| Publication commit | `1ca8ea512fc21c921e7d8889f0968cb04bb79210` |

RC1 measured S at 10,233 ps and Z at 50,511 / 70,617 ps on the synthetic nine-track fixtures. Six ordered conditional writes, companion slots, settled predicates, source vectors and complete scored output lists passed. Four seven-track real-producer fields were checked offline. Generated model/SDF/maps and delivery records matched the archived references.

Removing a writer identity produced `MISSING_FIELD_OWNER`. An unknown second addf condition returned exit 1, retained the first write and stopped before stimulus. The unmodified **RC1** public base, using ordinary `$sdf_annotate`, produced six unsupported-COND warnings, retained 1 ns defaults and delivered the three scored events at 11,000 / 51,000 / 71,000 ps. That control belongs to the old base; the current pinned upstream includes named-condition support.

The November 6 publication changed documentation and then-current upstream status, with no new simulation. The [scope table](scope.md) separately preserves the earlier seven-/nine-track application evidence. RC1 acceptance covered its declared fixtures and observation windows; it did not run a full upstream Icarus regression suite.

The release contains redistributable source, public per-cell PDK inputs, reduced fixture provenance, generated references and license texts. Terms and credits are in [NOTICE.md](../NOTICE.md). The current source layout keeps derived references beside each example; the release archive preserves the original layout.
