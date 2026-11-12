# SPDX-License-Identifier: Apache-2.0
"""Reader for the public fixtures' small HDL/SDF language and declared writer IDs."""
import hashlib
import re
from checks import exact, require

PIN = r'[A-Za-z_]\w*'
TERM = re.compile(rf"({PIN})\s*===\s*(1'b[01])")
PATH = re.compile(rf'\(\s*(?:(posedge|negedge)\s+)?({PIN})\s*=>\s*(?:({PIN})|\(\s*({PIN})\s*:\s*({PIN})\s*\))\s*\)\s*=\s*\(1\.0,1\.0\);')
NUMBER = r'[0-9]+(?:\.[0-9]+)?'
VALUE = rf'(?:{NUMBER}(?::{NUMBER}:{NUMBER})?)?'
LEAF = re.compile(rf'\(IOPATH (?:({PIN})|\((posedge|negedge) ({PIN})\)) ({PIN}) \(({VALUE})\) \(({VALUE})\)\)')
def digest(s):
    return hashlib.sha256(s.encode('ascii')).hexdigest()

def terms(text):
    tree = None
    for term in text.split('&&'):
        m = TERM.fullmatch(term.strip())
        require(m, 'EXPECTED_BINARY_TERM', term)
        leaf = [m[1], '===', m[2]]
        tree = leaf if tree is None else ['&&', tree, leaf]
    return tree

def declarations(path):
    raw = path.read_text(encoding='ascii')
    start = raw.index('specify_block_begin') + len('specify_block_begin')
    end = raw.index('// specify_block_end', start)
    block = raw[start:end]
    rows = []
    # Remove comments for parsing while retaining original locations and bytes.
    stripped = re.sub(r'//[^\n]*', lambda m: ' ' * len(m[0]), block)
    offset = 0
    for line in stripped.split(';')[:-1]:
        a = offset + len(line) - len(line.lstrip())
        b = offset + len(line) + 1
        offset = b
        stmt = stripped[a:b]
        cond = re.match(r'if\s*\(([^()]*)\)\s*', stmt)
        fallback = re.match(r'ifnone\s*', stmt)
        prefix = cond or fallback
        require(prefix is not None, 'DECLARATION_KIND', stmt)
        m = PATH.fullmatch(stmt[prefix.end():])
        require(m is not None, 'DECLARATION_BODY', stmt)
        edge, source, simple, target, data = m.groups()
        if edge: exact(data, source, 'DESCRIPTIVE_SOURCE')
        line_number = raw.count('\n', 0, start+a)+1
        rows.append(dict(id=f'decl-{line_number}', kind='conditional' if cond else 'ifnone',
                         condition_tree=terms(cond[1]) if cond else None, edge=edge,
                         source=source, destination=target or simple, initial_ps=[1000,1000],
                         line=line_number, text=raw[start+a:start+b], loc={'bytes':[start+a,start+b]}))
    require(not stripped[offset:].strip(), 'UNPARSED_SPECIFY_TEXT')
    return rows

def records(data, master, decls):
    """Read the declared single-CELL ABSOLUTE language; reject every unknown row.

    Empty output slots preserve prior values. An input edge and an output slot
    are separate attributes. Keep the source leaf so ordinary paths can retain
    its exact spelling when only the surrounding condition needs a new name.
    """
    text = data.decode('ascii')
    prefix = f'(DELAYFILE\n (SDFVERSION "3.0")\n (DIVIDER /)\n (TIMESCALE 1ns)\n (CELL (CELLTYPE "{master}") (INSTANCE'
    require(text.startswith(prefix), 'EXPECTED_SINGLE_CELL_SDF')
    envelope = re.match(r'(?P<instance>(?: [A-Za-z_]\w*(?:[./][A-Za-z_]\w*)*)?)\)\n \(DELAY \(ABSOLUTE\n', text[len(prefix):])
    require(envelope is not None and text.endswith('\n))))\n'), 'EXPECTED_SINGLE_CELL_SDF')
    instance = envelope['instance'].strip()
    offset = len(prefix)+envelope.end()
    result = []
    for raw in text[offset:-6].splitlines():
        i = text.count('\n',0,offset)+1
        cond = None
        leaf = raw
        if raw.startswith('(COND '):
            m = re.fullmatch(r'\(COND \(([^()]+)\) (\(IOPATH .*)\)', raw)
            require(m is not None,'SOURCE_SDF_CONDITION_FORM',f'line {i}: {raw}')
            cond,leaf = m.groups()
        m = LEAF.fullmatch(leaf)
        require(m is not None,'SOURCE_IOPATH_FORM',f'line {i}: {raw}')
        plain,edge,edged,target,rise,fall = m.groups()
        source = plain or edged
        tree = terms(cond) if cond else None
        endpoint = [d for d in decls if (d['source'],d['destination'])==(source,target)]
        match = [d['id'] for d in endpoint if (tree is None or tree==d['condition_tree'])
                 and (edge is None or edge==d['edge'])]
        require(match,'SOURCE_DECLARATION_MISSING',raw)
        owned = any(d['kind']=='ifnone' and d['edge'] is not None for d in endpoint)
        require(not owned or rise or fall,'EMPTY_TARGET_RECORD',f'line {i}')
        def typical(value):return value.split(':')[1] if ':' in value else value
        result.append(dict(id=f'L{i}',master=master,instance=instance,
                           events=[dict(port=source,edge=edge),dict(port=target,edge=None)],
                           source_text=raw, source_loc=dict(line=i,bytes=[offset, offset+len(raw)]),
                           leaf_text=leaf,condition=cond,condition_tree=tree,arity=2,slots=[[rise],[fall]],
                           selected_typical=[typical(rise),typical(fall)],original_matches=match,
                           requires_ownership=owned))
        offset+=len(raw)+1
    require(result,'SOURCE_NONEMPTY_RECORDS')
    return result


def writer_join(records, authorities, groups):
    """Require producer owners only where conversion redistributes fields.

    Ordinary paths use the original model match set. Classification comes from
    the source path structure, never from whether an owner happens to be present.
    """
    owners = {a['line']:a for a in authorities}
    exact(len(owners),len(authorities),'WRITER_OCCURRENCE_IDENTITY')
    required = {r['source_loc']['line'] for r in records if r['requires_ownership']}
    require(set(owners)<=required,'UNUSED_FIELD_OWNER',sorted(set(owners)-required))
    joined=[]
    for r in records:
        n=r['source_loc']['line']; src,dst=[e['port'] for e in r['events']]
        values=dict(canonical=r['id'],source=src,destination=dst,tokens=r['selected_typical'],
                    source_sha256=digest(r['source_text']))
        if not r['requires_ownership']:
            joined.append(dict(values=dict(values,mode='L'),fields=[]));continue
        require(n in owners,'MISSING_WRITER_OCCURRENCE',n)
        a=owners[n]
        exact(a['record_sha256'],digest(r['source_text']),'WRITER_RECORD_HASH')
        fields=[]
        for i,name in enumerate(('rise_group','fall_group')):
            if not r['slots'][i][0]:continue
            require(name in a,'MISSING_FIELD_OWNER',f'line {n}, {name}')
            idx=a[name]
            require(type(idx) is int and 0<=idx<len(groups),'UNKNOWN_LIBERTY_GROUP',idx)
            g=groups[idx]
            group_hash=a.get(name+'_sha256',a.get('group_sha256'))
            exact(digest(g['raw']),group_hash,'WRITER_LIBERTY_HASH')
            exact((src,dst),(g['related_pin'],g['output']),'WRITER_LIBERTY_ENDPOINTS')
            require(g['timing_sense'] in ('positive_unate','negative_unate'),'WRITER_UNATE_SENSE')
            edge=13 if (i==0)==(g['timing_sense']=='positive_unate') else 50
            if r['events'][0]['edge']:
                exact(edge,{'posedge':13,'negedge':50}[r['events'][0]['edge']],'SOURCE_EDGE_CONFLICT')
            fields.append(dict(values=dict(slot=i,output_slot=i,input_edge=edge,group=str(idx),group_sha256=group_hash)))
        joined.append(dict(values=dict(values,mode='O'),fields=fields))
    return dict(records=joined)
