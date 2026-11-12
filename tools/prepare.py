# SPDX-License-Identifier: Apache-2.0
"""Materialize one exact profile, then independently verify the generated files."""
import argparse
import copy
import difflib
import json
from pathlib import Path
import checks
import convert
import intake
import liberty
import verify

ROOT=Path(__file__).resolve().parents[1]
CASES=('addf','mux4','mux2-7t')


def check_inputs():
    for name,want in json.loads((ROOT/'docs'/'inputs.json').read_text())['sha256'].items():
        checks.exact(checks.sha(ROOT/name),want,'PINNED_INPUT_'+name)


def prepare(case, output):
    inputs=ROOT/'examples'/case
    profile=json.loads((inputs/'producer.json').read_text())
    master=profile['master']
    upstream=ROOT/'upstream'
    model=upstream/(master+'.behavioral.v')
    helper=upstream/(master+'.functional.v')
    lib=upstream/(master+'__tt_025C_5v00.lib')
    groups=liberty.liberty_groups(lib.read_text(),master)
    decls=intake.declarations(model)
    populated=[[master,*pins] for pins in profile['groups']]
    inventory=dict(masters=[master],groups=populated,original_declarations=profile['original_declarations'],
                   generated_declarations=profile['generated_declarations'])
    matrix=dict(groups=[dict(master=m,input=s,output=t) for m,s,t in populated])
    out=output/case
    out.mkdir(parents=True)
    transformed=out/'model.v'
    generated=convert.standard_model(model,model,{master:decls},matrix,transformed,profile_inventory=inventory)
    proven=verify.standard_model(model,model,{master:decls},matrix,transformed,profile_inventory=inventory)
    original=(inputs/'original.sdf').read_bytes()
    records=intake.records(original,master,decls)
    join=intake.writer_join(records,profile['records'],groups)
    sdf,mapping=convert.standard_cell(records,generated['declarations'][master],join)
    sdf_path=out/'converted.sdf'
    sdf_path.write_text(sdf)
    expected=verify.standard_cell(records,decls,proven['declarations'][master],join,groups,original,sdf_path.read_text())
    verify.standard_relation(mapping,expected)
    # Per-master functional views use the wrapper's module identifier. Only the
    # helper declaration name changes so that the vendor behavioural wrapper binds.
    h=helper.read_text()
    needle='module '+master+'('
    checks.exact(h.count(needle),1,'UNIQUE_HELPER_MODULE_NAME')
    (out/'helper.v').write_text(h.replace(needle,'module '+master+'_func('))
    # Keep the complete model/helper/SDF changes beside each case. These are
    # generated from the real inputs, including every collateral path edit.
    changes=[]
    for before,after in [(model,transformed),(helper,out/'helper.v'),(inputs/'original.sdf',sdf_path)]:
        changes.extend(difflib.unified_diff(before.read_text().splitlines(True),after.read_text().splitlines(True),
            fromfile=str(before.relative_to(ROOT)),tofile=f'examples/{case}/reference/{after.name}'))
    (out/'changes.diff').write_text(''.join(changes))
    source_map=[]
    for d in proven['declarations'][master]:
        orig=next(x for x in decls if x['id']==d.get('origin_declaration',d['id']))
        source_map.append(dict(source_line=orig['line'],generated_line=d['line'],
            input=d['source'],output=d['destination'],edge=d['edge'],
            role=d.get('role','untouched'),predicate=d['key']))
    (out/'source-map.json').write_text(json.dumps(source_map,indent=2)+'\n')
    # Source path and line references are relative to this release.
    audit=[]
    for row, record in zip(mapping,expected):
        d=record['targets'][0]; g=groups[record['producer_group']]
        orig=next(x for x in decls if x['id']==d['origin_declaration'])
        audit.append(dict(source=record['source'],destination=record['destination'],
                          original_declaration=orig['line'],original_sdf_line=row['canonical_source']['line'],
                          liberty_group=g['ordinal'],liberty_line=g['source_lines'][0],sense=g['timing_sense'],
                          condition=g['sdf_cond'],edge=record['edge'],key=record['key'],
                          slot=('rise','fall')[row['slot']],typical_ns=record['tokens'][row['slot']],
                          generated_model_line=d['line'],sdf_line=row['line']))
    (out/'field-map.json').write_text(json.dumps(audit,indent=2)+'\n')
    if case=='mux4':
        faulty=copy.deepcopy(profile['records'])
        del faulty[0]['rise_group']
        try:
            intake.writer_join(records,faulty,groups)
        except checks.ContractError as err:
            checks.exact(err.code,'MISSING_FIELD_OWNER','NEGATIVE_WRONG_GUARD')
            print(f'PASS missing ownership rejected: {err}')
        else:
            raise ValueError('Missing producer identity was accepted')
    print(f"PASS {case}: {len(populated)} owned groups; {len(audit)} checked output fields")
    return audit

def generate(output):
    check_inputs()
    for case in CASES: prepare(case,output)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('fresh_output',type=Path)
    generate(p.parse_args().fresh_output)
