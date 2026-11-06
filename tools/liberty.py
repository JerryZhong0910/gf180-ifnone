# SPDX-License-Identifier: Apache-2.0
"""Read timing group identities from the pinned per-cell Liberty files."""
import re
import checks as c

def block(text,start):
    at=text.index('{',start);depth=0;quote=False;escaped=False
    for i in range(at,len(text)):
        value=text[i]
        if escaped:escaped=False
        elif value=='\\' and quote:escaped=True
        elif value=='"':quote=not quote
        elif not quote:
            if value=='{':depth+=1
            elif value=='}':
                depth-=1
                if depth==0:return text[start:i+1],i+1
    raise ValueError('UNCLOSED_LIBERTY_BLOCK')

def liberty_groups(text,master):
    mark='cell('+master+')';c.exact(text.count(mark),1,'UNIQUE_LIBERTY_CELL')
    start=text.index(mark);cell,stop=block(text,start);rows=[]
    for pin in re.finditer(r'\bpin\(([^()]+)\)\s*\{',cell):
        part,end=block(text,start+pin.start())
        for match in re.finditer(r'\btiming\(\)\s*\{',part):
            a=start+pin.start()+match.start();raw,b=block(text,a);attrs={}
            for name in ('related_pin','timing_sense','timing_type','when','sdf_cond'):
                found=re.search(r'\b'+name+r'\s*:\s*([^;]+);',raw)
                attrs[name]=found.group(1).strip().strip('"') if found else None
            rows.append(dict(ordinal=len(rows),output=pin.group(1),source_bytes=[a,b],source_lines=[text.count('\n',0,a)+1,text.count('\n',0,b)+1],raw=raw,**attrs))
    return rows
