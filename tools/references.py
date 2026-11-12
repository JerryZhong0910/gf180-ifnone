# SPDX-License-Identifier: Apache-2.0
"""One authoritative, reproducible reference set beside each example."""
from pathlib import Path
from checks import exact

ROOT = Path(__file__).resolve().parents[1]


def references(output, *, write=False):
    files = {}
    for case in ('addf', 'mux4', 'mux2-7t'):
        for name in ('model.v', 'helper.v', 'converted.sdf', 'field-map.json', 'source-map.json', 'changes.diff'):
            files[ROOT/'examples'/case/'reference'/name] = (output/case/name).read_bytes()
    files[ROOT/'examples/reference/delivery.json'] = (output/'delivery.json').read_bytes()
    # Same-time passive observations have no order across channels. Preserve
    # ordered writes and each individual channel's event order in the reference.
    lines = (output/'capture.log').read_text().splitlines()
    trace = [x for x in lines if x.startswith(('SDF READBACK:', 'ANNOTATION_RETURNED'))]
    channels = sorted({tuple(x.split()[:2]) for x in lines if x.startswith(('PIN ', 'PRED ', 'SOURCE '))})
    for channel in channels:
        trace.extend(x for x in lines if tuple(x.split()[:2]) == channel)
    trace.extend(x for x in lines if x.startswith('END '))
    files[ROOT/'examples/reference/trace.txt'] = ('\n'.join(trace)+'\n').encode()
    for path, data in files.items():
        if write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        else:
            exact(path.read_bytes(), data, 'REFERENCE_DRIFT_'+str(path.relative_to(ROOT)))
    print(f'PASS {len(files)} derived references '+('refreshed' if write else 'reproduced'))
