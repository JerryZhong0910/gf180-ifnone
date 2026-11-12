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


def prepare_files(model, helper, lib, sdf_input, producer, out, *, case=None):
    """Public file-to-file conversion; profiles declare scope, not case names."""
    profile=json.loads(producer.read_text())
    master=profile['master']
    groups=liberty.liberty_groups(lib.read_text(),master)
    decls=intake.declarations(model)
    populated=[[master,*pins] for pins in profile['groups']]
    inventory=dict(masters=[master],groups=populated,original_declarations=profile['original_declarations'],
                   generated_declarations=profile['generated_declarations'])
    matrix=dict(groups=[dict(master=m,input=s,output=t) for m,s,t in populated])
    out.mkdir(parents=True)
    transformed=out/'model.v'
    generated=convert.standard_model(model,model,{master:decls},matrix,transformed,profile_inventory=inventory)
    proven=verify.standard_model(model,model,{master:decls},matrix,transformed,profile_inventory=inventory)
    original=sdf_input.read_bytes()
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
    for before,after in [(model,transformed),(helper,out/'helper.v'),(sdf_input,sdf_path)]:
        changes.extend(difflib.unified_diff(before.read_text().splitlines(True),after.read_text().splitlines(True),
            fromfile=str(before.relative_to(ROOT)) if before.is_relative_to(ROOT) else before.name,
            tofile=f'examples/{case}/reference/{after.name}' if case else after.name))
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
        if 'producer_group' not in record:continue
        d=record['targets'][0]; g=groups[record['producer_group']]
        orig=next(x for x in decls if x['id']==d['origin_declaration'])
        audit.append(dict(source=record['source'],destination=record['destination'],
                          original_declaration=orig['line'],original_sdf_line=row['canonical_source']['line'],
                          liberty_group=g['ordinal'],liberty_line=g['source_lines'][0],sense=g['timing_sense'],
                          condition=g['sdf_cond'],edge=record['edge'],key=record['key'],
                          slot=('rise','fall')[row['slot']],typical_ns=record['tokens'][row['slot']],
                          generated_model_line=d['line'],sdf_line=row['line']))
    (out/'field-map.json').write_text(json.dumps(audit,indent=2)+'\n')
    # One row per input occurrence, including records with no redistributed fields.
    record_map=[]
    for row,receipt in zip(records,join['records']):
        children=[m for m in mapping if m['canonical']==row['id']]
        c_mode=receipt['values']['mode']
        record_map.append(dict(source_line=row['source_loc']['line'],instance=row['instance'],
            action='edge-fields' if c_mode=='O' else ('condition-renamed' if row['condition_tree'] and any(m['key'].startswith('__gls_path_') for m in children) else 'preserved'),
            original_declarations=row['original_matches'],output_lines=[m['line'] for m in children]))
    (out/'record-map.json').write_text(json.dumps(record_map,indent=2)+'\n')
    (out/'inputs.json').write_text(json.dumps({str(p):checks.sha(p) for p in (model,helper,lib,sdf_input,producer)},indent=2)+'\n')
    print(f"PASS {case or master}: {len(populated)} owned groups; {len(audit)} checked output fields; {len(records)} source records accounted")
    return audit


def prepare(case, output):
    inputs=ROOT/'examples'/case
    producer=inputs/'producer.json'
    profile=json.loads(producer.read_text());master=profile['master']
    upstream=ROOT/'upstream'
    result=prepare_files(upstream/(master+'.behavioral.v'),upstream/(master+'.functional.v'),
        upstream/(master+'__tt_025C_5v00.lib'),inputs/'original.sdf',producer,output/case,case=case)
    if case=='mux4':
        records=intake.records((inputs/'original.sdf').read_bytes(),master,intake.declarations(upstream/(master+'.behavioral.v')))
        groups=liberty.liberty_groups((upstream/(master+'__tt_025C_5v00.lib')).read_text(),master)
        faulty=copy.deepcopy(profile['records']);del faulty[0]['rise_group']
        try:intake.writer_join(records,faulty,groups)
        except checks.ContractError as err:
            checks.exact(err.code,'MISSING_FIELD_OWNER','NEGATIVE_WRONG_GUARD')
            print(f'PASS missing ownership rejected: {err}')
        else:raise ValueError('Missing producer identity was accepted')
    return result


def generate(output):
    check_inputs()
    for case in CASES: prepare(case,output)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('fresh_output',type=Path)
    for name in ('model','helper','liberty','sdf','producer'):p.add_argument('--'+name,type=Path)
    args=p.parse_args()
    custom=[args.model,args.helper,args.liberty,args.sdf,args.producer]
    if any(custom):
        if not all(custom):p.error('--model, --helper, --liberty, --sdf and --producer are required together')
        prepare_files(*(x.resolve() for x in custom),args.fresh_output.resolve())
    else:generate(args.fresh_output)
