# SPDX-License-Identifier: Apache-2.0
"""Run the public mixed-record conversion, path readback and event controls."""
import argparse
from collections import Counter
import json
from pathlib import Path
import tempfile
from checks import exact, require, ContractError
from prepare import ROOT, check_inputs
from references import case_references
from run_annotation import execute, build_probe, snapshot, pin_events


def events(log, expected):
    exact(log.splitlines()[-1],'END '+str(expected['end_ps']),'MIXED_COMPLETE_STIMULUS')
    actual=pin_events(log,'Z',expected['windows'])
    exact(actual,[tuple(row) for row in expected['events']],'MIXED_PIN_EVENTS')
    return actual


def run(prefix, out, *, refresh=False):
    check_inputs()
    source=ROOT/'examples/mixed-mux2'
    master='gf180mcu_fd_sc_mcu7t5v0__mux2_2'
    # Use the same file-based CLI that an external producer uses.
    args=['python3','-B',ROOT/'tools/prepare.py',out/'converted',
        '--model',ROOT/'upstream'/(master+'.behavioral.v'),
        '--helper',ROOT/'upstream'/(master+'.functional.v'),
        '--liberty',ROOT/'upstream'/(master+'__tt_025C_5v00.lib'),
        '--sdf',source/'original.sdf','--producer',source/'producer.json']
    execute(args,out,'conversion.log')
    converted=out/'converted'
    build_probe(prefix,out)
    expected=json.loads((source/'expected.json').read_text())
    execute([prefix/'bin/iverilog','-g2012','-gspecify','-Ttyp','-s','bench','-o','bench.vvp',source/'bench.v'],converted,'compile.log')
    log=execute([prefix/'bin/vvp','-M'+str(out),'-mpath_snapshot','bench.vvp','-sdf-verbose'],converted,'capture.log')
    observed=events(log,expected)
    require(not any(x in log for x in ('WARNING:','ERROR:','FATAL:')),'MIXED_DIAGNOSTICS')
    lines=log.splitlines();barrier=lines.index('ANNOTATION_RETURNED 0')
    require(not any(x.startswith(('PIN ','SOURCE ')) for x in lines[:barrier]),'MIXED_COLD_ANNOTATION')
    for when,pin,value in expected['source_events']:
        exact(lines.count(f'SOURCE {pin} {when} {value}'),1,'MIXED_SOURCE_EVENTS')
    paths=snapshot(log,'final');exact(len(paths),8,'MIXED_PATH_POPULATION')
    exact(Counter((edge,rise,fall) for edge,src,dst,key,rise,fall in paths if src=='S'),
          Counter(tuple(row) for row in expected['select_readback_ps']),'MIXED_SELECT_SLOTS')
    key='__gls_path_I0_Z_3235b9e3e2cc8771'  # Original I1===0 predicate, checked from source.
    exact([(rise,fall) for edge,src,dst,k,rise,fall in paths if src=='I0' and k==key],
          [tuple(expected['i0_condition_zero_ps'])],'MIXED_PARTIAL_AND_EMPTY_SLOTS')
    exact(Counter((rise,fall) for edge,src,dst,k,rise,fall in paths if src=='I0' and k!=key),
          Counter({(1000,1000):2}),'MIXED_UNWRITTEN_DATA_PATHS')
    exact(Counter((rise,fall) for edge,src,dst,k,rise,fall in paths if src=='I1'),
          Counter({tuple(expected['i1_all_paths_ps']):3}),'MIXED_BARE_FANOUT')
    # Named ordinary writes: partial update changes only fall; no-op changes neither.
    reads=[x for x in lines if x.startswith('SDF READBACK:')]
    exact([x.split()[-2:] for x in reads],[['0.211','0.419'],['0.211','0.617'],['0.211','0.617']],
          'MIXED_ORDERED_ORDINARY_READBACK')
    sdf=(converted/'converted.sdf').read_text()
    corrupted={
        'swapped-input-edges':sdf.replace('(posedge S)','(TEMP S)').replace('(negedge S)','(posedge S)').replace('(TEMP S)','(negedge S)'),
        'dropped-ordinary-record':'\n'.join(x for x in sdf.splitlines() if not x.startswith('(IOPATH I1 Z'))+'\n',
        'unsynchronized-condition':sdf.replace('(COND '+key+' ',"(COND (I1===1'b0) ")}
    negatives=[]
    for name,bad in corrupted.items():
        folder=out/name;folder.mkdir();(folder/'converted.sdf').write_text(bad)
        # The exact same compiled design runs to its final stimulus time.
        bad_log=execute([prefix/'bin/vvp','-M'+str(out),'-mpath_snapshot',converted/'bench.vvp','-sdf-verbose'],folder,'capture.log')
        try:events(bad_log,expected)
        except ContractError as error:exact(error.code,'MIXED_PIN_EVENTS','MIXED_NEGATIVE_WRONG_FAILURE')
        else:raise ValueError('Undetected dynamic corruption: '+name)
        negatives.append(dict(name=name,exit=0,end_ps=expected['end_ps'],rejected_by='MIXED_PIN_EVENTS',
                              observed_events=pin_events(bad_log,'Z',expected['windows'])))
    report=dict(expected_events=expected['events'],observed_events=observed,
                source_records=6,output_records=8,paths=8,negative_controls=negatives,
                final_readback=[list(x[:4])+[str(x[4]),str(x[5])] for x in paths])
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    files={name:(converted/name).read_bytes() for name in ('model.v','helper.v','converted.sdf','changes.diff','source-map.json','record-map.json','field-map.json')}
    files['results.json']=(out/'results.json').read_bytes()
    case_references('mixed-mux2',files,write=refresh)
    print('PASS mixed mux2: 6 source records -> 8 output records; 9 pin events; 3 dynamic corruptions rejected at event checks')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prefix',type=Path,default=ROOT/'.build/install')
    p.add_argument('--out',type=Path)
    p.add_argument('--refresh-references',action='store_true')
    args=p.parse_args()
    if args.out:out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
    else:
        (ROOT/'runs').mkdir(exist_ok=True);out=Path(tempfile.mkdtemp(prefix='mixed-',dir=ROOT/'runs'))
    run(args.prefix.resolve(),out,refresh=args.refresh_references)
    print(out)
