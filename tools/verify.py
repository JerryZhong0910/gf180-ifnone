# SPDX-License-Identifier: Apache-2.0
"""Verify the generated text and fields against the original declarations and Liberty groups."""
from pathlib import Path
from collections import Counter
import re, hashlib
import checks as c

def digest(raw):return hashlib.sha256(raw).hexdigest()

def expression(tree):
    # Preserve source association in the compiler's finite key serialization.
    if tree is None:return '',0
    if tree[0]=='&&':
        left,ln=expression(tree[1]);right,rn=expression(tree[2])
        return ('('+left+')' if ln>1 else left)+'&&'+('('+right+')' if rn>1 else right),ln+rn
    c.exact(tree[1],'===','SOURCE_CASE_EQUALITY');c.require(tree[2] in ("1'b0","1'b1"),'SOURCE_BINARY_TERM')
    return ''.join(tree),1

def standard_model(parent, canonical, catalog, matrix, generated, *, profile_inventory):
    """Independently verify the corrected source relation and predicate cones.

    No generator module or generated ownership map is read. Canonical endpoint
    and cofactor structure defines the obligations. Physical lines locate the
    attributable edit only; they never choose an arc owner.
    """
    original=Path(canonical).read_bytes();original.decode('ascii')
    before=Path(parent).read_text();after=Path(generated).read_text()
    ownership={(g['master'],g['input'],g['output']) for g in matrix['groups']}
    masters=sorted({m for m,s,d in ownership})
    c.exact(masters,profile_inventory['masters'],'STANDARD_SOURCE_PROFILE_MASTER_IDENTITIES')
    c.exact(sorted(ownership),sorted(tuple(g) for g in profile_inventory['groups']),'STANDARD_SOURCE_PROFILE_GROUP_IDENTITIES')
    result={};cones={};deltas=[];rest_before=before;rest_after=after
    ident=r'[A-Za-z_][A-Za-z_0-9$]*'
    path_pattern=re.compile(r'(?:if\s*\(('+ident+r')\)\s*)?\(\s*(?:(posedge|negedge)\s+)?('+ident+r')\s*=>\s*(?:('+ident+r')|\(('+ident+r')\s*:\s*('+ident+r')\))\s*\)\s*=\s*\(1\.0,1\.0\);')
    def body(source,master):
        start=source.index('module '+master+'(') if 'module '+master+'(' in source else re.search(r'(?m)^module\s+'+re.escape(master)+r'\s*\(',source).start()
        end=source.index('endmodule',start)+len('endmodule')
        return start,end,source[start:end]
    def operands(tree):
        if tree[0]=='&&':return operands(tree[1])+operands(tree[2])
        c.require(tree[1]=='===' and tree[2] in ("1'b0","1'b1"),'STANDARD_SOURCE_COFACTOR')
        return [(tree[0],tree[2])]
    for master in masters:
        a,b,old=body(before,master);na,nb,new=body(after,master)
        ca,cb,raw=body(original.decode(),master);c.exact(old,raw,'STANDARD_ORIGINAL_COMBINATIONAL_HELPER_SOURCE')
        # The source prefix and every inter-declaration byte remain intact.
        # Parse the inserted cone and path statements by syntax, not physical rows.
        old_spec=re.search(r'(?m)^[ \t]*specify\b',old)
        new_spec=re.search(r'(?m)^[ \t]*specify\b',new)
        c.require(old_spec and new_spec,'STANDARD_SPECIFY_BLOCK')
        prefix=old[:old_spec.start()]
        c.exact(new[:len(prefix)],prefix,'STANDARD_ORIGINAL_FUNCTIONAL_PREFIX')
        cone=new[len(prefix):new_spec.start()]
        old_at=old_spec.start();new_at=new_spec.start()
        ds=catalog[master];destinations={d['destination'] for d in ds if d['kind']=='ifnone' and d['edge']}
        selected=[d for d in ds if d['destination'] in destinations]
        expected=[];group_conditions={};group_fallbacks={}
        for d in selected:
            x,y=d['loc']['bytes'];c.exact(original[x:y].decode(),d['text'],'STANDARD_RAW_DECLARATION_IDENTITY')
            c.exact(old.count(d['text']),1,'STANDARD_ONE_ORIGINAL_DECLARATION')
            offset=old.index(d['text'])
            unchanged=old[old_at:offset]
            c.exact(new[new_at:new_at+len(unchanged)],unchanged,'STANDARD_UNCHANGED_BETWEEN_PATHS')
            new_at+=len(unchanged)
            source,target=d['source'],d['destination'];owned=(master,source,target) in ownership
            edges=['posedge','negedge'] if owned and d['kind']=='conditional' else [d['edge']]
            for j,edge in enumerate(edges):
                if j:
                    new_at+=len(new[new_at:])-len(new[new_at:].lstrip())
                match=path_pattern.match(new,new_at)
                c.require(match is not None,'STANDARD_EXACT_PATH_LANGUAGE',new[new_at:new_at+150])
                line=after[:na+new_at].count('\n')+1
                new_at=match.end()
                key,actual_edge,src,simple,output,data=match.groups();key=key or ''
                c.exact([actual_edge,src,output or simple],[edge,source,target],'STANDARD_SOURCE_ENDPOINT_EDGE')
                c.exact(data,source if edge else None,'STANDARD_DESCRIPTIVE_EDGE_DATA_SOURCE')
                if d['kind']=='conditional':
                    c.require(bool(key),'STANDARD_REQUIRED_PREDICATE')
                    group=group_conditions.setdefault((source,target),{});terms=operands(d['condition_tree'])
                    if d['id'] in group:c.exact(group[d['id']],(key,terms),'STANDARD_EDGE_CHILDREN_SHARE_SOURCE_PREDICATE')
                    group[d['id']]=(key,terms)
                    condition_role='strict_conjunction'
                else:
                    c.exact(d['kind'],'ifnone','STANDARD_SOURCE_FALLBACK_KIND')
                    group_fallbacks.setdefault((source,target),set()).add(key);condition_role='endpoint_fallback'
                expected.append(dict(id=str(d['id'])+(':'+edge if owned else ''),origin_declaration=d['id'],source=source,destination=target,
                    edge=edge,edge_mask={None:0,'posedge':13,'negedge':50}[edge],kind='conditional' if key else 'unconditional',key=key,
                    condition_tree=d['condition_tree'],condition_role=condition_role,role='producer_edge' if owned else 'literal_preservation',
                    line=line,file=str(generated),initial_ps=list(d['initial_ps']),omitted=False,source_sha256=digest(original[x:y])))
            old_at=offset+len(d['text'])
        c.exact(new[new_at:],old[old_at:],'STANDARD_ORIGINAL_FUNCTIONAL_AND_UNAFFECTED_TEXT')
        declarations={};drivers={}
        tokens=[token.strip() for token in cone.split(';')]
        c.exact(tokens.pop(),'','STANDARD_CONE_COMPLETE_TERMINATOR')
        for token in tokens:
            decl=re.fullmatch(r'(wand|wor|wire)\s+('+ident+r')',token)
            if decl:
                kind,name=decl.groups();c.require(name not in declarations,'STANDARD_UNIQUE_LOCAL_NET')
                c.require(re.search(r'\b'+re.escape(name)+r'\b',old) is None,'STANDARD_NO_ORIGINAL_NAME_COLLISION')
                declarations[name]=kind;continue
            assign=re.fullmatch(r'assign\s+('+ident+r')\s*=\s*(.*)',token)
            c.require(assign is not None,'STANDARD_ONLY_CONTINUOUS_CONE_DRIVERS')
            name,rhs=assign.groups();c.require(name in declarations,'STANDARD_DECLARED_DRIVER_TARGET')
            drivers.setdefault(name,[]).append(rhs)
        used=set();master_cones=[]
        for endpoint in sorted(group_fallbacks):
            conditions=group_conditions.get(endpoint,{})
            c.exact(len(group_fallbacks[endpoint]),1,'STANDARD_ONE_ENDPOINT_FALLBACK')
            fallback=next(iter(group_fallbacks[endpoint]))
            if not conditions:
                c.exact(fallback,'','STANDARD_EMPTY_UNCONDITIONAL_FALLBACK');continue
            c.require(bool(fallback),'STANDARD_NONEMPTY_EXPLICIT_FALLBACK')
            c.exact(declarations.get(fallback),'wire','STANDARD_FALLBACK_NET')
            c.exact(len(drivers.get(fallback,[])),1,'STANDARD_ONE_FALLBACK_DRIVER')
            match=re.fullmatch(r'\(('+ident+r") === 1'b0\)",drivers[fallback][0]);c.require(match is not None,'STANDARD_FALLBACK_EXACT_BINARY_COMPLEMENT')
            aggregate=match[1];c.exact(declarations.get(aggregate),'wor','STANDARD_MEMBERSHIP_WIRED_OR')
            predicates=[key for key,terms in conditions.values()]
            c.exact(Counter(drivers.get(aggregate,[])),Counter(predicates),'STANDARD_COMPLETE_MEMBERSHIP_DRIVERS')
            c.exact(len(set(predicates)),len(predicates),'STANDARD_DISTINCT_CONDITION_PREDICATES')
            for key,terms in conditions.values():
                c.exact(declarations.get(key),'wand','STANDARD_PREDICATE_WIRED_AND')
                c.exact(Counter(drivers.get(key,[])),Counter('('+pin+' === '+value+')' for pin,value in terms),'STANDARD_EXACT_ORIGINAL_COFACTORS')
                c.require(key not in used,'STANDARD_NO_SHARED_OWNERSHIP_PREDICATE');used.add(key)
                master_cones.append(dict(kind='strict_conjunction',net=key,terms=[list(x) for x in terms],source=endpoint[0],destination=endpoint[1]))
            c.require(fallback not in used and aggregate not in used,'STANDARD_DISTINCT_FALLBACK_CONE')
            used.update((fallback,aggregate));master_cones.append(dict(kind='endpoint_fallback',net=fallback,aggregate=aggregate,members=predicates,source=endpoint[0],destination=endpoint[1]))
        c.exact(used,set(declarations),'STANDARD_NO_UNCHECKED_CONE_NETS');c.exact(used,set(drivers),'STANDARD_NO_MISSING_OR_UNCHECKED_DRIVERS')
        # Add any genuinely untouched paths in these masters independently.
        for d in ds:
            if d in selected:continue
            c.exact(new.count(d['text']),1,'STANDARD_UNCHANGED_OTHER_PATH')
            line=after[:na+new.index(d['text'])].count('\n')+1
            key,_=expression(d['condition_tree'])
            expected.append(dict(d,key=key,edge_mask={None:0,'posedge':13,'negedge':50}[d['edge']],line=line,file=str(generated)))
        result[master]=expected;cones[master]=master_cones
        rest_before=rest_before.replace(old,'<verified '+master+'>',1);rest_after=rest_after.replace(new,'<verified '+master+'>',1)
        deltas.append(dict(master=master,original=len(selected),generated=sum('origin_declaration' in d for d in expected),total_paths=len(expected)))
    c.exact(rest_after,rest_before,'STANDARD_ALL_OTHER_MODEL_BYTES_UNCHANGED')
    c.exact(sum(r['original'] for r in deltas),profile_inventory['original_declarations'],'STANDARD_REWRITTEN_SOURCE_POPULATION')
    c.exact(sum(r['generated'] for r in deltas),profile_inventory['generated_declarations'],'STANDARD_GENERATED_SOURCE_POPULATION')
    return dict(status='PASS_SOURCE_RELATION_ONLY',declarations=result,predicate_cones=cones,masters=deltas,
                parent_sha256=c.sha(parent),canonical_sha256=c.sha(canonical),generated_sha256=c.sha(generated),
                generator_used_as_oracle=False,native_validation=False)

def standard_cell(records, original_declarations, declarations, accepted_join, liberty_groups, canonical_sdf, body):
    """Independent producer-to-ordinary-annotation relation for one CELL.

    Prior source-join identities must be authenticated by the caller. The prior
    join disambiguates producer groups that have identical bare SDF endpoints;
    numerical coincidences and generated target IDs never disambiguate them.
    The raw Liberty sense, source condition and corrected source declarations
    independently derive each exported edge/slot and literal fanout.
    """
    c.require(bool(records),'STANDARD_SOURCE_NONEMPTY_CELL')
    master=records[0]['master'];c.exact(len(accepted_join['records']),len(records),'STANDARD_SOURCE_JOIN_POPULATION')
    expected=[];pieces=[]
    instance_match=re.search(r'\(INSTANCE(?: ([A-Za-z_]\w*(?:[./][A-Za-z_]\w*)*))?\)',canonical_sdf.decode('ascii'))
    c.require(instance_match is not None,'STANDARD_SOURCE_INSTANCE')
    instance=instance_match[1] or ''
    c.require(all(row['instance']==instance for row in records),'STANDARD_INSTANCE_PRESERVATION')
    header='(DELAYFILE\n (SDFVERSION "3.0")\n (DIVIDER /)\n (TIMESCALE 1ns)\n (CELL\n (CELLTYPE "'+master+'")\n (INSTANCE'+(' '+instance if instance else '')+')\n (DELAY (ABSOLUTE\n'
    line=header.count('\n')+1
    for row,prior in zip(records,accepted_join['records']):
        a,b=row['source_loc']['bytes'];c.exact(canonical_sdf[a:b].decode(),row['source_text'],'STANDARD_SOURCE_RAW_SDF')
        v=prior['values'];source,destination=[e['port'] for e in row['events']]
        c.exact([v['canonical'],v['source'],v['destination'],v['tokens'],v['source_sha256']],
                [row['id'],source,destination,row['selected_typical'],digest(canonical_sdf[a:b])],'STANDARD_SOURCE_PRIOR_RECORD')
        c.exact(row['arity'],2,'STANDARD_SOURCE_TWO_FIELDS')
        original=[d for d in original_declarations if d['source']==source and d['destination']==destination
                  and (not row['condition_tree'] or d['condition_tree']==row['condition_tree'])
                  and (not row['events'][0]['edge'] or d['edge']==row['events'][0]['edge'])]
        c.exact([d['id'] for d in original],row['original_matches'],'STANDARD_SOURCE_LITERAL_TARGET_SET')
        endpoint=[d for d in original_declarations if (d['source'],d['destination'])==(source,destination)]
        needs_owners=any(d['kind']=='ifnone' and d['edge'] for d in endpoint)
        c.exact(v['mode'],'O' if needs_owners else 'L','STANDARD_SOURCE_RECORD_ROLE')
        if needs_owners:
            c.exact(len(prior['fields']),sum(bool(s[0]) for s in row['slots']),'STANDARD_SOURCE_FIELD_POPULATION')
            for slot in (0,1):
                if not row['slots'][slot][0]:continue
                fields=[f['values'] for f in prior['fields'] if f['values']['slot']==slot]
                c.exact(len(fields),1,'STANDARD_SOURCE_SINGLE_PRODUCER_FIELD');f=fields[0]
                group=liberty_groups[int(f['group'])]
                c.exact(digest(group['raw'].encode()),f['group_sha256'],'STANDARD_SOURCE_LIBERTY_IDENTITY')
                c.exact([group['related_pin'],group['output'],group['timing_type']],[source,destination,'combinational'],'STANDARD_SOURCE_LIBERTY_ENDPOINT_ROLE')
                c.exact(re.sub(r'\s+','',group['sdf_cond'] or ''),re.sub(r'\s+','',row['condition'] or ''),'STANDARD_SOURCE_LIBERTY_CONDITION')
                c.require(group['timing_sense'] in ('positive_unate','negative_unate'),'STANDARD_SOURCE_UNATE_ROLE')
                edge='posedge' if (slot==0)==(group['timing_sense']=='positive_unate') else 'negedge'
                c.exact(int(f['input_edge']),13 if edge=='posedge' else 50,'STANDARD_SOURCE_PRODUCER_EDGE')
                c.exact(f['output_slot'],slot,'STANDARD_SOURCE_PRODUCER_SLOT')
                if row['events'][0]['edge']:c.exact(edge,row['events'][0]['edge'],'STANDARD_SOURCE_INPUT_EDGE')
                owners=[d for d in original if d['kind']=='conditional'] if row['condition_tree'] else [d for d in original if d['kind']=='ifnone' and d['edge']==edge]
                c.exact(len(owners),1,'STANDARD_SOURCE_ORIGINAL_OWNER')
                target=[d for d in declarations if d.get('origin_declaration')==owners[0]['id'] and d['edge']==edge and d.get('role')=='producer_edge']
                c.exact(len(target),1,'STANDARD_SOURCE_REPLACEMENT_OWNER');d=target[0]
                raw_slots=['',''];raw_slots[slot]=row['slots'][slot][0]
                text='(IOPATH ('+edge+' '+source+') '+destination+' ('+raw_slots[0]+') ('+raw_slots[1]+'))'
                if d['kind']=='conditional':text='(COND '+d['key']+' '+text+')'
                else:c.exact(d['kind'],'unconditional','STANDARD_SOURCE_EMPTY_PATH_KIND')
                tokens=['',''];tokens[slot]=row['selected_typical'][slot]
                expected.append(dict(canonical=row['id'],source=source,destination=destination,edge=edge,key=d['key'],line=line,tokens=tokens,
                                     targets=target,mode='ordinary',producer_group=group['ordinal'],producer_output_slot=slot))
                pieces.append(text);line+=text.count('\n')+1
        else:
            c.exact(prior['fields'],[],'STANDARD_LITERAL_NO_REDISTRIBUTION')
            targets=[d for source_d in original for d in declarations
                     if d.get('origin_declaration',d['id'] if 'id' in d else None)==source_d['id']]
            c.exact(len(targets),len(original),'STANDARD_SOURCE_PRESERVED_LITERAL_FANOUT')
            c.require(bool(targets),'STANDARD_SOURCE_REQUIRED_LITERAL_TARGETS')
            c.require(all(d.get('role')!='producer_edge' for d in targets),'STANDARD_SOURCE_LITERAL_PATH_FORM')
            text=row['source_text'];key=''
            if row['condition_tree'] and any(d.get('role')=='literal_preservation' for d in targets):
                c.exact(len(targets),1,'STANDARD_SOURCE_ONE_LITERAL_CONDITION')
                key=targets[0]['key']
                # Locate the source IOPATH independently; the reader's leaf
                # metadata and the emitter's ownership map are not expectations.
                leaf=re.search(r'\(IOPATH .+\)\)$',row['source_text'])
                c.require(leaf is not None,'STANDARD_SOURCE_LITERAL_LEAF')
                text='(COND '+key+' '+leaf[0][:-1]+')'
            elif row['condition_tree']:key=expression(row['condition_tree'])[0]
            expected.append(dict(canonical=row['id'],source=source,destination=destination,
                edge=row['events'][0]['edge'],key=key,line=line,tokens=list(row['selected_typical']),targets=targets,mode='literal'))
            pieces.append(text);line+=text.count('\n')+1
    c.exact(body,header+'\n'.join(pieces)+'\n))\n)\n)\n','STANDARD_SOURCE_EXACT_ORDERED_RECORDS')
    return expected

def standard_relation(mapping,expected):
    """Verify audit metadata against the independently established relation."""
    c.exact(len(mapping),len(expected),'STANDARD_AUDIT_RECORD_POPULATION')
    for row,wanted in zip(mapping,expected):
        c.exact({k:row[k] for k in ('canonical','source','destination','line','key')},
                {k:wanted[k] for k in ('canonical','source','destination','line','key')},'STANDARD_AUDIT_RECORD_RELATION')
        c.exact(row['input_edge'],wanted['edge'],'STANDARD_AUDIT_INPUT_EDGE')
        owned='producer_output_slot' in wanted
        c.exact(row['slot'],wanted.get('producer_output_slot'),'STANDARD_AUDIT_OUTPUT_SLOT')
        c.exact(row['mode'],'O' if owned else 'L','STANDARD_AUDIT_SOURCE_MODE')
        if owned:
            c.exact(row['group'],str(wanted['producer_group']),'STANDARD_AUDIT_PRODUCER_GROUP')
            c.exact(row['origin_declaration'],wanted['targets'][0]['origin_declaration'],'STANDARD_AUDIT_ORIGINAL_OWNER')
        else:
            c.exact(row['origin_declarations'],[d.get('origin_declaration',d.get('id')) for d in wanted['targets']],
                    'STANDARD_AUDIT_LITERAL_TARGETS')
    return dict(status='PASS',records=len(expected),generator_decisions_used_as_expectations=False)
