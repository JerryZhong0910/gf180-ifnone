# GF180 edge-sensitive ifnone

Some GF180 timing models put `ifnone` on an edge-sensitive path. Consider a mux: the same select input can make the output rise or fall, depending on the data. A usable rewrite has to express when the fallback applies **and** preserve which physical arc supplied each output-delay field.

This package implements the finite **GF180-ARC-PAIR-1** model/SDF representation. It includes the converter, an independent source checker, a small Icarus patch, two runnable nine-track examples and a seven-track real-producer field example. The original library authors' intended four-state semantics remain an open question. [Upstream model discussion](https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_sc_mcu9t5v0/issues/3) · [Icarus implementation discussion](https://github.com/steveicarus/iverilog/discussions/1696)

**RC1** preserves the source and tool baseline used for its clean-directory acceptance. As checked on 2026-11-06, the separate SDF escaped-name fix [#1694](https://github.com/steveicarus/iverilog/pull/1694) is merged upstream; the first-matching-edge fix [#1704](https://github.com/steveicarus/iverilog/pull/1704) remains open and unmerged. Neither is a required patch for these examples. [Release evidence and scope](docs/release.md)

## Run the examples

On Linux, install a C/C++ compiler, make, autoconf, flex, bison, gperf, Python 3.9+, patch, curl, tar, gzip, coreutils and the usual Icarus build dependencies. The Python tools use the standard library. Use a directory without spaces for the upstream build.

```sh
git clone --branch rc1 --depth 1 https://github.com/JerryZhong0910/gf180-ifnone.git
cd gf180-ifnone
make build
make check
```

The build fetches and authenticates the pinned official Icarus source and installs the patched binaries under `.build/install`. For an offline build, set `ICARUS_ARCHIVE` to an already downloaded copy of the [same public source tarball](https://codeload.github.com/steveicarus/iverilog/tar.gz/9f26050130988d661cec6ab11b43d45f7ef533f5). `JOBS=8 make build` selects eight build jobs. The example check takes a fresh output directory under `runs/`. Open its `delivery.json`, per-cell `field-map.json` and `capture.log` to examine the calculation and measurements.

| Nine-track pin | Input transition | Source delay | Expected time | Observed time |
|---|---:|---:|---:|---:|
| `addf_1.S` rises | A rises at 10,000 ps | 233 ps | 10,233 ps | 10,233 ps |
| `mux4_2.Z` rises | S0 rises at 50,000 ps | 511 ps | 50,511 ps | 50,511 ps |
| `mux4_2.Z` falls | S0 falls at 70,000 ps | 617 ps | 70,617 ps | 70,617 ps |

The cell models, Boolean helpers and TT/25°C/5 V Liberty groups come from the public PDK. The nine-track SDF **values** are asymmetric synthetic inputs. Each writer fixture specifies the Liberty identity when constructing the record. The seven-track example checks four fields from a historical routed mux; its present-day check is offline. [Worked examples](docs/examples.md) · [Seven- and nine-track scope](docs/scope.md)

The run also removes one producer identity, then corrupts a generated condition in a separate cold annotation. The checks require rejection at the missing field and the unknown compiled condition respectively. In the latter case the first write is observed and the simulation finishes before any test input transition. [Runtime and source origins](docs/implementation.md) · [Licensing](NOTICE.md)
