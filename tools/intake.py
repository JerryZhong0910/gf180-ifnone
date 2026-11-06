# SPDX-License-Identifier: Apache-2.0
"""Reader for the public fixtures' small HDL/SDF language and declared writer IDs."""
import hashlib
import re
from checks import exact, require

PIN = r'[A-Za-z_]\w*'
TERM = re.compile(rf"({PIN})\s*===\s*(1'b[01])")
PATH = re.compile(rf'\(\s*(?:(posedge|negedge)\s+)?({PIN})\s*=>\s*(?:({PIN})|\(\s*({PIN})\s*:\s*({PIN})\s*\))\s*\)\s*=\s*\(1\.0,1\.0\);')
TRIPLET = r'[0-9]+\.[0-9]+:[0-9]+\.[0-9]+:[0-9]+\.[0-9]+'
LEAF = re.compile(rf'\(IOPATH ({PIN}) ({PIN}) \(({TRIPLET})\) \(({TRIPLET})\)\)')
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
    text = data.decode('ascii')
    prefix = f'(DELAYFILE\n (SDFVERSION "3.0")\n (DIVIDER /)\n (TIMESCALE 1ns)\n (CELL (CELLTYPE "{master}") (INSTANCE)\n (DELAY (ABSOLUTE\n'
    require(text.startswith(prefix) and text.endswith('\n))))\n'), 'EXPECTED_SINGLE_CELL_SDF')
    offset = len(prefix)
    result = []
    for i, raw in enumerate(text[len(prefix):-6].splitlines(), 7):
        cond = None
        leaf = raw
        if raw.startswith('(COND '):
            m = re.fullmatch(r'\(COND \(([^()]+)\) (\(IOPATH .*)\)', raw)
            require(m is not None,'SOURCE_SDF_CONDITION_FORM',raw)
            cond,leaf = m.groups()
        m = LEAF.fullmatch(leaf)
        require(m is not None,'SOURCE_IOPATH_FORM',leaf)
        source,target,rise,fall = m.groups()
        tree = terms(cond) if cond else None
        match = [d['id'] for d in decls if (d['source'],d['destination'])==(source,target)
                 and (tree is None or tree==d['condition_tree'])]
        require(match,'SOURCE_DECLARATION_MISSING',raw)
        result.append(dict(id=f'L{i}',master=master,events=[dict(port=source,edge=None),dict(port=target,edge=None)],
                           source_text=raw, source_loc=dict(line=i,bytes=[offset, offset+len(raw)]),
                           condition=cond,condition_tree=tree,arity=2,slots=[[rise],[fall]],
                           selected_typical=[rise.split(':')[1],fall.split(':')[1]],original_matches=match))
        offset+=len(raw)+1
    return result

def writer_join(records, authorities, groups):
    """The fixture supplies an acquisition-time group ID for each original field."""
    exact(len(records),len(authorities),'WRITER_RECORD_POPULATION')
    owners = {a['line']:a for a in authorities}
    exact(len(owners),len(records),'WRITER_OCCURRENCE_IDENTITY')
    joined=[]
    for r in records:
        n=r['source_loc']['line']
        require(n in owners,'MISSING_WRITER_OCCURRENCE',n)
        a=owners[n]
        exact(a['record_sha256'],digest(r['source_text']),'WRITER_RECORD_HASH')
        src,dst=[e['port'] for e in r['events']]
        fields=[]
        for i,name in enumerate(('rise_group','fall_group')):
            require(name in a,'MISSING_FIELD_OWNER',f'line {n}, {name}')
            idx=a[name]
            require(type(idx) is int and 0<=idx<len(groups),'UNKNOWN_LIBERTY_GROUP',idx)
            g=groups[idx]
            exact(digest(g['raw']),a['group_sha256'],'WRITER_LIBERTY_HASH')
            exact((src,dst),(g['related_pin'],g['output']),'WRITER_LIBERTY_ENDPOINTS')
            require(g['timing_sense'] in ('positive_unate','negative_unate'),'WRITER_UNATE_SENSE')
            edge=13 if (i==0)==(g['timing_sense']=='positive_unate') else 50
            fields.append(dict(values=dict(slot=i,output_slot=i,input_edge=edge,group=str(idx),group_sha256=a['group_sha256'])))
        joined.append(dict(values=dict(canonical=r['id'],source=src,destination=dst,mode='O',tokens=r['selected_typical'],
                                       source_sha256=digest(r['source_text'])),fields=fields))
    return dict(records=joined)
