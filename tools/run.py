# SPDX-License-Identifier: Apache-2.0
"""Fresh conversion, simulation and independent pin-level assessment."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
from assess import assess
from prepare import ROOT, CASES, prepare, check_inputs
from checks import exact
from references import references


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix',type=Path,default=ROOT/'.build'/'install')
    parser.add_argument('--out',type=Path,help='new directory (default: new child of runs/)')
    parser.add_argument('--refresh-references',action='store_true',help='replace checked-in derived references after a successful run')
    args=parser.parse_args()
    if args.out:
        out=args.out.resolve()
        out.mkdir(parents=True,exist_ok=False)
    else:
        (ROOT/'runs').mkdir(exist_ok=True)
        out=Path(tempfile.mkdtemp(prefix='case-',dir=ROOT/'runs'))
    check_inputs()
    maps={case:prepare(case,out) for case in CASES}
    expected=json.loads((ROOT/'examples'/'expected.json').read_text())
    probes=[]
    for case,instance in [('addf','adder'),('mux4','mux')]:
        e=expected[case]['events'][0]
        f,=[f for f in maps[case] if (f['original_sdf_line'],f['slot'])==(e['source_line'],e['slot'])]
        probes.append(f'always @({instance}.{f["source"]}) $strobe("PRED {expected[case]["pin"]} %0d %b", $time, {instance}.{f["key"]});')
    (out/'predicate_probes.vh').write_text('\n'.join(probes)+'\n')
    tools=args.prefix.resolve()/'bin'
    def run(args,filename):
        p=subprocess.run(args,cwd=out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                         timeout=90,text=True,env={**os.environ,'LC_ALL':'C'})
        (out/filename).write_text(p.stdout)
        if p.returncode:
            raise SystemExit(f'{filename}: exit {p.returncode}\n'+p.stdout)
        return p.stdout
    compile_log=run([tools/'iverilog','-g2012','-gspecify','-Ttyp','-s','bench','-o','bench.vvp',
                     ROOT/'examples'/'design.v',ROOT/'examples'/'bench.v'],'compile.log')
    exact(compile_log,'','COMPILE_DIAGNOSTICS')
    log=run([tools/'vvp','bench.vvp','-sdf-verbose'],'capture.log')
    rows=assess(log,expected,maps)
    # Corrupt only the condition on the second valid child. Keep the compiled
    # design and the first write identical to the positive run.
    neg=out/'invalid-annotation'
    for label in ('addf','mux4'):
        (neg/label).mkdir(parents=True)
        sdf=(out/label/'converted.sdf').read_text()
        if label=='addf':
            second=maps[label][1]
            parts=sdf.splitlines(keepends=True)
            line=second['sdf_line']-1
            exact(parts[line].count(second['key']),1,'NEGATIVE_SOURCE_KEY')
            parts[line]=parts[line].replace(second['key'],'missing_test_predicate')
            sdf=''.join(parts)
        (neg/label/'converted.sdf').write_text(sdf)
    rejected=subprocess.run([tools/'vvp',out/'bench.vvp','-sdf-verbose'],cwd=neg,stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,text=True,timeout=90)
    (neg/'capture.log').write_text(rejected.stdout)
    exact(rejected.returncode,1,'INVALID_ANNOTATION_EXIT')
    rows_neg=rejected.stdout.splitlines()
    exact([x for x in rows_neg if x.startswith('SDF INITIAL ERROR:')],
          ['SDF INITIAL ERROR: expected exactly one named conditional path'],'INVALID_ANNOTATION_REASON')
    exact([x for x in rows_neg if x.startswith('SDF READBACK:')],
          [next(x for x in log.splitlines() if x.startswith('SDF READBACK:'))],'FIRST_WRITE_RETAINED')
    exact([x for x in rows_neg if x.startswith(('SOURCE ','PIN ','END '))],[],'FAIL_BEFORE_STIMULUS')
    print('PASS unknown compiled predicate rejected after the first write, before stimulus')

    (out/'delivery.json').write_text(json.dumps(rows,indent=2)+'\n')
    for row in rows:
        print(f"PASS {row['master']} {row['input_edge']} -> {row['slot']}: "
              f"source {row['input_ps']} ps, expected {row['expected_ps']} ps, observed {row['observed_ps']} ps")
    references(out,write=args.refresh_references)
    print(f'Field maps, raw output and delivery chains: {out}')

if __name__=='__main__':
    main()
