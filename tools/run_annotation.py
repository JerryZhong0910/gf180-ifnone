# SPDX-License-Identifier: Apache-2.0
"""Measure bare/edge-qualified SDF against real mux2-derived simple/edge paths."""
import argparse
from collections import Counter
from decimal import Decimal
import difflib
import json
from pathlib import Path
import subprocess
import tempfile
from checks import exact
from prepare import ROOT, prepare, check_inputs
from references import case_references


def execute(argv, cwd, name):
    p = subprocess.run([str(x) for x in argv], cwd=cwd, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
    (cwd/name).write_text(p.stdout)
    exact(p.returncode, 0, 'COMMAND_EXIT_'+name)
    return p.stdout


def build_probe(prefix, output):
    execute([prefix/'bin/iverilog-vpi', ROOT/'tests/path_snapshot.c'], output, 'probe-build.log')
    return output/'path_snapshot.vpi'


def snapshot(log, label, source=None):
    rows=[]
    for line in log.splitlines():
        if not line.startswith('PATH '+label+' '): continue
        _,_,scope,edge,src,dst,key,rise,fall=line.split()
        if source is None or src==source:
            rows.append((int(edge),src,dst,key,Decimal(rise)*1000,Decimal(fall)*1000))
    return rows


def pin_events(log, pin, windows):
    return [(int(t),v) for line in log.splitlines() if line.startswith('PIN '+pin+' ')
            for _,_,t,v in [line.split()] if any(lo<=int(t)<=hi for lo,hi in windows)]


def run(prefix, out, *, refresh=False):
    check_inputs()
    prepare('mux2-7t',out)
    build_probe(prefix,out)
    spec=json.loads((ROOT/'examples/edge-annotation/expected.json').read_text())
    model=(out/'mux2-7t/model.v').read_text()
    master='gf180mcu_fd_sc_mcu7t5v0__mux2_2'
    pos='(posedge S => (Z : S)) = (1.0,1.0);'
    neg='(negedge S => (Z : S)) = (1.0,1.0);'
    exact(model.count(pos),1,'SELECT_POSEDGE');exact(model.count(neg),1,'SELECT_NEGEDGE')
    reports=[];review={}
    for variant,edges in spec['variants'].items():
        changed=model if variant=='edge' else model.replace(pos,'(S => Z) = (1.0,1.0);').replace(neg,'' if variant=='simple' else '(S => Z) = (1.0,1.0);')
        review[variant+'.v']=changed.encode()
        raw=(ROOT/'upstream'/(master+'.behavioral.v')).read_text()
        review[variant+'.diff']=''.join(difflib.unified_diff(raw.splitlines(True),changed.splitlines(True),
            fromfile='upstream/'+master+'.behavioral.v',tofile=variant+'.v')).encode()
        for style,order in spec['annotations'].items():
            for corner,select in enumerate(('min','typ','max')):
                folder=out/f'{variant}-{style}-{select}';folder.mkdir()
                (folder/'model.v').write_text(changed)
                (folder/'helper.v').write_bytes((out/'mux2-7t/helper.v').read_bytes())
                (folder/'model.diff').write_text(''.join(difflib.unified_diff(model.splitlines(True),changed.splitlines(True),fromfile='corrected-edge-model.v',tofile='model.v')))
                records=[]
                for identity in order:
                    values=spec['records'][identity]
                    port=('(posedge S)' if identity=='a' else '(negedge S)') if style.startswith('qualified') else 'S'
                    triplets=[':'.join(f'{v/1000:.3f}' for v in slot) for slot in values]
                    records.append(f'(IOPATH {port} Z ({triplets[0]}) ({triplets[1]}))')
                def sdf(rows):return f'(DELAYFILE (SDFVERSION "3.0") (TIMESCALE 1ns) (CELL (CELLTYPE "{master}") (INSTANCE) (DELAY (ABSOLUTE\n'+'\n'.join(rows)+'\n))))\n'
                (folder/'first.sdf').write_text(sdf(records[:1]));(folder/'records.sdf').write_text(sdf(records))
                review[style+'.sdf']=sdf(records).encode()
                execute([prefix/'bin/iverilog','-g2012','-gspecify','-T'+select,'-s','bench','-o','bench.vvp',ROOT/'examples/edge-annotation/bench.v'],folder,'compile.log')
                log=execute([prefix/'bin/vvp','-M'+str(out),'-mpath_snapshot','bench.vvp'],folder,'capture.log')
                states=[]
                for identities in (order[:1],order):
                    state=[[1000,1000] for _ in edges]
                    for identity in identities:
                        for n,edge in enumerate(edges):
                            if not style.startswith('qualified') or edge==spec['qualified_edge'][identity]:
                                state[n]=[slot[corner] for slot in spec['records'][identity]]
                    states.append(state)
                for label,state in zip(('first','final'),states):
                    exact(Counter(snapshot(log,label,'S')),Counter((edge,'S','Z','-',*slots) for edge,slots in zip(edges,state)), 'ACTUAL_PATH_EDGE_AND_SLOTS')
                    exact(len(snapshot(log,label)),6+len(edges),'ALL_PATH_POPULATION')
                predicted=[]
                for when,edge,old,value in spec['source_events']:
                    paths=[slots for e,slots in zip(edges,states[-1]) if e in (0,edge)]
                    delay=min(slots[0 if value==1 else 1] for slots in paths)
                    predicted.append((when+delay,str(value)))
                observed=pin_events(log,'Z',spec['windows'])
                exact(observed,predicted,'ANNOTATION_PIN_EVENTS')
                exact(log.splitlines()[-1],'END '+str(spec['end_ps']),'ANNOTATION_COMPLETE_STIMULUS')
                unmatched=3 if variant!='edge' and style.startswith('qualified') else 0
                exact(sum('Unable to match ModPath' in line for line in log.splitlines()),unmatched,'UNMATCHED_RECORDS')
                reports.append(dict(model=variant,sdf=style,selection=select,path_edges=edges,
                    first_readback_ps=states[0],final_readback_ps=states[1],unmatched_annotations=unmatched,
                    actual_readback_ps={label:[[edge,int(rise),int(fall)] for edge,src,dst,key,rise,fall in snapshot(log,label,'S')] for label in ('first','final')},
                    expected_events=predicted,observed_events=observed))
    (out/'results.json').write_text(json.dumps(reports,indent=2)+'\n')
    review['results.json']=(out/'results.json').read_bytes()
    case_references('edge-annotation',review,write=refresh)
    print(f'PASS edge annotation: {len(reports)} model/record/corner combinations; actual paths and complete scored events')
    return reports


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prefix',type=Path,default=ROOT/'.build/install')
    p.add_argument('--out',type=Path)
    p.add_argument('--refresh-references',action='store_true')
    args=p.parse_args()
    if args.out:out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
    else:
        (ROOT/'runs').mkdir(exist_ok=True)
        out=Path(tempfile.mkdtemp(prefix='annotation-',dir=ROOT/'runs'))
    run(args.prefix.resolve(),out,refresh=args.refresh_references)
    print(out)
