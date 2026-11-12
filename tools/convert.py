# SPDX-License-Identifier: Apache-2.0
"""GF180-ARC-PAIR-1 model and SDF emitter, extracted from the accepted implementation."""
from pathlib import Path
import collections, hashlib, json, re
import checks as c
from checks import ref

def sha(data):return hashlib.sha256(data).hexdigest()

def condition(tree):
    if tree is None:return '',0
    if tree[0]!='&&':return tree[0]+tree[1]+tree[2],1
    a,n=condition(tree[1]);b,m=condition(tree[2]);return ('('+a+')' if n>1 else a)+'&&'+('('+b+')' if m>1 else b),n+m

def standard_model(parent, canonical, catalog, matrix, destination, *, profile_inventory):
    """Materialize the selected ordinary interface; never certify its mapping.

    The original source supplies structural membership. Producer field ownership
    is a separate SDF operation. Generated locators are measured after emission;
    the source and generated files have independent line numbers.
    Independent source and emitted-program checks must validate this view.
    """
    parent,canonical,destination=map(Path,(parent,canonical,destination))
    c.require(not destination.exists(),'FRESH_STANDARD_MODEL')
    original=canonical.read_bytes();original.decode('ascii');base=parent.read_text();text=base
    owned={(g['master'],g['input'],g['output']) for g in matrix['groups']}
    masters=sorted({key[0] for key in owned})
    c.exact(masters,profile_inventory['masters'],'STANDARD_PROFILE_MASTER_IDENTITIES')
    c.exact(sorted(owned),sorted(tuple(g) for g in profile_inventory['groups']),'STANDARD_PROFILE_GROUP_IDENTITIES')
    declarations={};proof=[];used_names={}
    def leaves(tree):
        if tree[0]=='&&':return leaves(tree[1])+leaves(tree[2])
        c.require(len(tree)==3 and tree[1]=='===' and tree[2] in ("1'b0","1'b1"),'STANDARD_BINARY_SOURCE_TERM')
        c.require(re.fullmatch(r'[A-Za-z_][A-Za-z_0-9$]*',tree[0]) is not None,'STANDARD_SCALAR_IDENTIFIER')
        return [(tree[0],tree[2])]
    def body_span(source,master):
        headers=list(re.finditer(r'(?m)^module\s+'+re.escape(master)+r'\s*\(',source))
        c.exact(len(headers),1,'EXPECTED_SINGLE_PUBLIC_MODULE')
        end=source.index('endmodule',headers[0].start())+len('endmodule')
        return headers[0].start(),end
    for master in masters:
        a,b=body_span(text,master);body=text[a:b]
        ca,cb=body_span(original.decode(),master)
        c.exact(body,original[ca:cb].decode(),'STANDARD_UNCHANGED_PARENT_COMBINATIONAL_MASTER')
        ds=catalog[master]
        tagged={d['destination'] for d in ds if d['kind']=='ifnone' and d['edge'] is not None}
        groups=collections.defaultdict(list)
        for d in ds:
            start,end=d['loc']['bytes']
            c.exact(original[start:end].decode(),d['text'],'STANDARD_AUTHENTIC_SOURCE_DECLARATION')
            if d['destination'] in tagged:groups[d['source'],d['destination']].append(d)
        nets=[];rewrites=[];expected=[];names=set()
        for (source,target),members in groups.items():
            c.require(all(re.fullmatch(r'[A-Za-z_][A-Za-z_0-9$]*',x) for x in (source,target)),'STANDARD_ENDPOINT_IDENTIFIERS')
            replacement=(master,source,target) in owned
            conditions=[d for d in members if d['kind']=='conditional']
            fallbacks=[d for d in members if d['kind']=='ifnone']
            c.exact(len(conditions)+len(fallbacks),len(members),'STANDARD_SUPPORTED_DESTINATION_STRUCTURE')
            c.exact([d['edge'] for d in fallbacks],['posedge','negedge'] if replacement else [None],'STANDARD_FALLBACK_SHAPE')
            prefix='__gls_path_'+source+'_'+target+'_'
            predicates={}
            for d in conditions:
                c.exact(d['edge'],None,'STANDARD_SOURCE_SIMPLE_CONDITION')
                terms=leaves(d['condition_tree']);c.require(1<=len(terms)<=5,'STANDARD_CONDITION_WIDTH')
                c.exact(len(set(k for k,v in terms)),len(terms),'STANDARD_UNIQUE_COFACTORS')
                signature=json.dumps(d['condition_tree'],separators=(',',':'))
                name=prefix+hashlib.sha256(signature.encode()).hexdigest()[:16]
                c.require(name not in names,'STANDARD_UNIQUE_PREDICATE_NAME');names.add(name)
                predicates[d['id']]=name
                nets.append('wand '+name+';')
                nets.extend('assign '+name+' = ('+pin+' === '+value+');' for pin,value in terms)
            fallback=None
            if conditions:
                any_name=prefix+'any';fallback=prefix+'fallback'
                c.require(any_name not in names and fallback not in names,'STANDARD_UNIQUE_FALLBACK_NAMES')
                names.update((any_name,fallback));nets.append('wor '+any_name+';')
                nets.extend('assign '+any_name+' = '+predicates[d['id']]+';' for d in conditions)
                nets.extend(('wire '+fallback+';','assign '+fallback+' = ('+any_name+" === 1'b0);"))
            for d in members:
                raw=d['text'];c.exact(body.count(raw),1,'STANDARD_UNIQUE_STRUCTURAL_DECLARATION')
                c.exact(d['initial_ps'],[1000,1000],'STANDARD_SOURCE_DEFAULT_PAIR')
                generated=[]
                role='producer_edge' if replacement else 'literal_preservation'
                if replacement:
                    edges=['posedge','negedge'] if d['kind']=='conditional' else [d['edge']]
                    predicate=predicates[d['id']] if d['kind']=='conditional' else fallback
                    for edge in edges:
                        statement=('if ('+predicate+') ' if predicate else '')+'('+edge+' '+source+' => ('+target+' : '+source+')) = (1.0,1.0);'
                        generated.append(dict(origin_declaration=d['id'],source=source,destination=target,edge=edge,
                            kind='conditional' if predicate else 'unconditional',key=predicate or '',
                            condition_tree=d['condition_tree'],condition_role='strict_conjunction' if d['kind']=='conditional' else 'endpoint_fallback',
                            role=role,statement=statement,initial_ps=list(d['initial_ps'])))
                else:
                    predicate=predicates[d['id']] if d['kind']=='conditional' else fallback
                    c.require(predicate is not None,'STANDARD_COLLATERAL_PREDICATE_REQUIRED')
                    opening=re.search(r'\(\s*'+re.escape(source)+r'\s*=>',raw)
                    c.require(opening is not None,'STANDARD_COLLATERAL_SIMPLE_PATH')
                    statement='if ('+predicate+') '+raw[opening.start():]
                    c.require('\n' not in statement,'STANDARD_COLLATERAL_SINGLE_PATH_LINE')
                    generated.append(dict(origin_declaration=d['id'],source=source,destination=target,edge=None,kind='conditional',key=predicate,
                        condition_tree=d['condition_tree'],condition_role='strict_conjunction' if d['kind']=='conditional' else 'endpoint_fallback',
                        role=role,statement=statement,initial_ps=list(d['initial_ps'])))
                replacement_text='\n\t'.join(p['statement'] for p in generated)
                start=body.index(raw);rewrites.append((start,start+len(raw),replacement_text))
                expected.extend(generated)
        for name in names:c.require(re.search(r'\b'+re.escape(name)+r'\b',body) is None,'STANDARD_NO_SOURCE_NAME_COLLISION')
        for start,end,replacement_text in sorted(rewrites,reverse=True):body=body[:start]+replacement_text+body[end:]
        anchor=list(re.finditer(r'(?m)^[ \t]*specify\b',body))
        c.exact(len(anchor),1,'STANDARD_SINGLE_SPECIFY_BLOCK')
        at=anchor[0].start()
        body=body[:at]+''.join('   '+net+'\n' for net in nets)+'\n'+body[at:]
        for p in expected:
            c.exact(body.count(p['statement']),1,'STANDARD_UNIQUE_GENERATED_STATEMENT')
            p['line']=text[:a].count('\n')+body[:body.index(p['statement'])].count('\n')+1
        # Record only attributable changes; all untouched declarations retain
        # their original source identities and caller-supplied parent locators.
        proof.append(dict(master=master,original_body_sha256=sha(text[a:b].encode()),generated_body_sha256=sha(body.encode()),
                          rewritten_original_declarations=len(rewrites),generated_declarations=len(expected),predicate_nets=len(names)))
        for d in ds:
            if d['destination'] in tagged:continue
            c.exact(body.count(d['text']),1,'STANDARD_UNCHANGED_OTHER_DECLARATION')
            key,_=condition(d['condition_tree'])
            line=text[:a].count('\n')+body[:body.index(d['text'])].count('\n')+1
            expected.append(dict(d,origin_declaration=d['id'],role='untouched',key=key,line=line))
        declarations[master]=expected;used_names[master]=sorted(names)
        text=text[:a]+body+text[b:]
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('x') as f:f.write(text)
    return dict(status='GENERATED_REQUIRES_INDEPENDENT_SOURCE_AND_PROGRAM_CHECKS',interface='GF180-ARC-PAIR-1',
                parent=ref(parent),canonical=ref(canonical),target=ref(destination),masters=proof,declarations=declarations,
                predicate_names=used_names,ownership_groups=len(owned),native_or_scientific_validation=False)

def standard_cell(records, declarations, accepted_join):
    """Export ordinary records from an authenticated prior producer join.

    The caller authenticates the raw ledger and prior join. The join is an
    acquisition-time producer fact, never loaded by the engineering consumer.
    An independent source assessor must check the emitted relation and bytes.
    """
    c.require(bool(records),'STANDARD_NONEMPTY_CELL')
    master=records[0]['master'];c.require(all(r['master']==master for r in records),'STANDARD_SINGLE_MASTER')
    c.exact(len(accepted_join['records']),len(records),'STANDARD_JOIN_RECORD_POPULATION')
    header='(DELAYFILE\n (SDFVERSION "3.0")\n (DIVIDER /)\n (TIMESCALE 1ns)\n (CELL\n (CELLTYPE "'+master+'")\n (INSTANCE'+(' '+records[0]['instance'] if records[0]['instance'] else '')+')\n (DELAY (ABSOLUTE\n'
    body=[header];mapping=[];local=header.count('\n')+1
    for row,receipt in zip(records,accepted_join['records']):
        prior=receipt['values'];source,target=[x['port'] for x in row['events']]
        c.exact(prior['canonical'],row['id'],'STANDARD_JOIN_CANONICAL_RECORD')
        c.exact(prior['source_sha256'],sha(row['source_text'].encode()),'STANDARD_JOIN_RAW_RECORD')
        c.exact(prior['tokens'],row['selected_typical'],'STANDARD_JOIN_LITERAL_VALUES')
        c.exact(row['arity'],2,'STANDARD_TWO_SLOT_CELL_DOMAIN')
        c.require(all(len(slot)==1 for slot in row['slots']),'STANDARD_SINGLE_TRIPLET_SLOTS')
        candidates=[d for d in declarations if (d['source'],d['destination'])==(source,target)]
        exports=[]
        if prior['mode']=='O':
            c.require(candidates and all(d['role']=='producer_edge' for d in candidates),'STANDARD_OWNED_GROUP_ROLE')
            for slot in (0,1):
                if not row['slots'][slot][0]:continue
                fields=[f['values'] for f in receipt['fields'] if f['values']['slot']==slot]
                c.exact(len(fields),1,'STANDARD_ONE_PRODUCER_SLOT_OWNER');field=fields[0]
                edge={13:'posedge',50:'negedge'}[int(field['input_edge'])]
                selected=[d for d in candidates if d['edge']==edge and
                          (d['condition_tree']==row['condition_tree'] and d['condition_role']=='strict_conjunction'
                           if row['condition_tree'] else d['condition_role']=='endpoint_fallback')]
                c.exact(len(selected),1,'STANDARD_ONE_EDGE_CONDITION_OWNER');owner=selected[0]
                slots=['',''];slots[slot]=row['slots'][slot][0]
                record='(IOPATH ('+edge+' '+source+') '+target+' '+' '.join('('+value+')' for value in slots)+')'
                if owner['key']:record='(COND '+owner['key']+' '+record+')'
                exports.append((record,dict(input_edge=edge,slot=slot,key=owner['key'],origin_declaration=owner['origin_declaration'],group=field['group'],group_sha256=field['group_sha256'])))
        else:
            c.exact(prior['mode'],'L','STANDARD_ORDINARY_RECORD_MODE')
            c.require(candidates and all(d['role'] in ('literal_preservation','untouched') for d in candidates),
                      'STANDARD_LITERAL_GROUP_ROLE')
            selected=[d for d in candidates if d['origin_declaration'] in row['original_matches']]
            c.exact(len(selected),len(row['original_matches']),'STANDARD_LITERAL_MATCH_POPULATION')
            record=row['source_text'];key=''
            if row['condition_tree'] and any(d['role']=='literal_preservation' for d in selected):
                c.exact(len(selected),1,'STANDARD_LITERAL_CONDITION_OWNER')
                key=selected[0]['key'];record='(COND '+key+' '+row['leaf_text']+')'
            elif row['condition_tree']:key=condition(row['condition_tree'])[0]
            exports.append((record,dict(input_edge=row['events'][0]['edge'],slot=None,key=key,
                                        origin_declarations=[d['origin_declaration'] for d in selected])))
        for child,(record,relation) in enumerate(exports):
            body.append(record+'\n')
            mapping.append(dict(canonical=row['id'],canonical_source=row['source_loc'],mode=prior['mode'],child=child,line=local,
                                source=source,destination=target,source_sha256=sha(row['source_text'].encode()),
                                generated_sha256=sha(record.encode()),**relation))
            local+=record.count('\n')+1
    body.append('))\n)\n)\n')
    return ''.join(body),mapping
