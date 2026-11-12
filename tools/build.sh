#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
rev=beb32f3945f5be1f45cf5d898d440161e9c6f113
sha=4d6471d2a79b2dcbf1270b9f494c772fd4b35e9d844683b11552c724f8283407
patchfile="$root/patches/initial-annotation.patch"
dest="$root/.build"
jobs=${JOBS:-4}
mkdir -p "$dest"
patchsha=$(sha256sum "$patchfile" | cut -d' ' -f1)
if test -x "$dest/install/bin/iverilog" && test -x "$dest/install/bin/vvp" && test -f "$dest/SOURCE" && test -f "$dest/BUILT" && test "$(cat "$dest/BUILT")" = "$rev $patchsha"; then
    echo "Toolchain already built at $dest/install"
    exit 0
fi
archive=${ICARUS_ARCHIVE:-"$dest/icarus-$rev.tar"}
if ! test -f "$archive"; then
    if test -n "${ICARUS_ARCHIVE:-}"; then echo "Missing requested Icarus archive: $archive" >&2; exit 1; fi
    # Export the exact public commit, excluding any local working-tree edits.
    source="$dest/upstream"
    git init -q "$source"
    git -C "$source" fetch -q --depth=1 https://github.com/steveicarus/iverilog.git "$rev"
    git -c tar.umask=0002 -C "$source" archive --format=tar "$rev" > "$archive.part"
    mv "$archive.part" "$archive"
fi
printf '%s  %s\n' "$sha" "$archive" | sha256sum -c -
work=$(mktemp -d "$dest/build-XXXXXXXX")
mkdir "$work/src" "$work/obj"
tar xf "$archive" -C "$work/src"
cd "$work/src"
# Use patch against this source archive even if an enclosing directory is a Git checkout.
patch --batch --fuzz=0 -p1 < "$patchfile"
sh autoconf.sh
cd "$work/obj"
"$work/src/configure" --prefix="$dest/install"
make -j"$jobs" CFLAGS="-O1 -g0" CXXFLAGS="-O1 -g0"
make install
printf '%s\n' "$work/src" > "$dest/SOURCE"
printf '%s %s\n' "$rev" "$patchsha" > "$dest/BUILT"
