#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if ! test -f "$root/.build/SOURCE"; then
    echo 'Run make build first; the upstream checks use that exact source tree.' >&2
    exit 1
fi
source=$(cat "$root/.build/SOURCE")
export PATH="$root/.build/install/bin:$PATH"
cd "$source/ivtest"
python3 -B vvp_reg.py "$root/tests/upstream.list"
