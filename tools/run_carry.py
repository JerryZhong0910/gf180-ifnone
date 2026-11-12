# SPDX-License-Identifier: Apache-2.0
"""Regress the existing addf carry probe through the public converter."""
import argparse
from collections import Counter
import json
from pathlib import Path
import tempfile
from checks import exact, require
from prepare import ROOT, check_inputs
from references import case_references
from run_annotation import execute, build_probe, snapshot, pin_events


def run(prefix, out, *, refresh=False):
    check_inputs()
    source=ROOT/'examples/addf-carry'
    master='gf180mcu_fd_sc_mcu9t5v0__addf_1'
    converted=out/'converted'
    execute(['python3','-B',ROOT/'tools/prepare.py',converted,
        '--model',ROOT/'upstream'/(master+'.behavioral.v'),
        '--helper',ROOT/'upstream'/(master+'.functional.v'),
        '--liberty',ROOT/'upstream'/(master+'__tt_025C_5v00.lib'),
        '--sdf',source/'original.sdf','--producer',ROOT/'examples/addf/producer.json'],out,'conversion.log')
    build_probe(prefix,out)
    execute([prefix/'bin/iverilog','-g2012','-gspecify','-Ttyp','-s','bench','-o','bench.vvp',source/'bench.v'],converted,'compile.log')
    log=execute([prefix/'bin/vvp','-M'+str(out),'-mpath_snapshot','bench.vvp','-sdf-verbose'],converted,'capture.log')
    expected=json.loads((source/'expected.json').read_text())
    observed=pin_events(log,'CO',[expected['window_ps']]);paths=snapshot(log,'final')
    report=dict(expected_events=expected['events'],observed_events=observed,
        actual_paths=[list(x[:4])+[str(x[4]),str(x[5])] for x in paths])
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    exact(log.splitlines().count('END '+str(expected['end_ps'])),1,'CARRY_COMPLETE_STIMULUS')
    exact(observed,[tuple(row) for row in expected['events']],'CARRY_PIN_EVENTS')
    require(not any(x in log for x in ('WARNING:','ERROR:','FATAL:')),'CARRY_DIAGNOSTICS')
    exact(len(paths),expected['all_paths'],'CARRY_ALL_PATH_POPULATION')
    carry=[p for p in paths if p[2]=='CO']
    exact(len(carry),expected['carry_paths'],'CARRY_PATH_POPULATION')
    key='hex:'+expected['carry_key'].encode('ascii').hex()
    exact([p for p in carry if p[3]==key],[(0,'A','CO',key,*expected['carry_pair_ps'])],'CARRY_TARGET_READBACK')
    exact(Counter((p[0],p[4],p[5]) for p in carry if p[3]!=key),
          Counter({(0,*expected['other_carry_pair_ps']):expected['carry_paths']-1}),'CARRY_OTHER_READBACK')
    # The exact ordered SDF/source relation was checked by the public CLI.
    # Keep the ordinary COND intact; the fix belongs to simulator identity binding.
    record=(source/'original.sdf').read_text().splitlines()[7]
    require(record in (converted/'converted.sdf').read_text().splitlines(),'CARRY_ORIGINAL_RECORD_PRESERVED')
    files={name:(converted/name).read_bytes() for name in ('changes.diff','converted.sdf','record-map.json')}
    files['results.json']=(out/'results.json').read_bytes()
    case_references('addf-carry',files,write=refresh)
    print('PASS addf carry: original COND preserved; 9 carry paths read back; CO at 10211/20419 ps')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prefix',type=Path,default=ROOT/'.build/install')
    p.add_argument('--out',type=Path)
    p.add_argument('--refresh-references',action='store_true')
    args=p.parse_args()
    if args.out:out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
    else:
        (ROOT/'runs').mkdir(exist_ok=True);out=Path(tempfile.mkdtemp(prefix='carry-',dir=ROOT/'runs'))
    run(args.prefix.resolve(),out,refresh=args.refresh_references)
    print(out)
