#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
rev=9f26050130988d661cec6ab11b43d45f7ef533f5
sha=7ab87bd7d524783ccdd26d23b1cfa9653311b9602608603d0cd150fe01ac38d2
patchfile="$root/patches/ordinary-sdf-condition.patch"
dest="$root/.build"
jobs=${JOBS:-4}
mkdir -p "$dest"
patchsha=$(sha256sum "$patchfile" | cut -d' ' -f1)
if test -x "$dest/install/bin/vvp" && test -f "$dest/BUILT" && test "$(cat "$dest/BUILT")" = "$rev $patchsha"; then
    echo "Toolchain already built at $dest/install"
    exit 0
fi
archive=${ICARUS_ARCHIVE:-"$dest/icarus-$rev.tar.gz"}
if ! test -f "$archive"; then
    if test -n "${ICARUS_ARCHIVE:-}"; then echo "Missing requested Icarus archive: $archive" >&2; exit 1; fi
    curl -fLSs --retry 2 -o "$archive.part" "https://codeload.github.com/steveicarus/iverilog/tar.gz/$rev"
    mv "$archive.part" "$archive"
fi
printf '%s  %s\n' "$sha" "$archive" | sha256sum -c -
work=$(mktemp -d "$dest/build-XXXXXXXX")
mkdir "$work/src" "$work/obj"
tar xzf "$archive" --strip-components=1 -C "$work/src"
cd "$work/src"
# Use patch against this source archive even if an enclosing directory is a Git checkout.
patch --batch --fuzz=0 -p1 < "$patchfile"
sh autoconf.sh
cd "$work/obj"
"$work/src/configure" --prefix="$dest/install"
make -j"$jobs" CFLAGS="-O1 -g0" CXXFLAGS="-O1 -g0"
make install
printf '%s %s\n' "$rev" "$patchsha" > "$dest/BUILT"
