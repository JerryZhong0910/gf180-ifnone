#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
rev=5b9ce29b41d6af30e6ccb6e178d3ed2a71974e69
sha=9e4709f2299af169d6855cd013720545ec5032f6224901a25b12001b3d41f03b
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
