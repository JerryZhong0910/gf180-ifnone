# SPDX-License-Identifier: Apache-2.0
"""Check cold writes, settled cofactors and externally visible timed transitions."""
from decimal import Decimal
from checks import exact, require


def ps(ns):
    value=Decimal(ns)*1000
    exact(value,value.to_integral_value(),'FIXTURE_INTEGER_PS')
    return int(value)


def assess(run, expected, maps):
    lines=run.splitlines()
    require(not any('WARNING:' in x or 'ERROR:' in x or 'FATAL:' in x for x in lines),
            'UNEXPECTED_SIMULATOR_DIAGNOSTIC')
    exact(lines.count('ANNOTATION_RETURNED 0'),1,'COLD_ANNOTATION_RETURN')
    exact(lines[-1],'END 80000','COMPLETE_BENCH')
    barrier=lines.index('ANNOTATION_RETURNED 0')
    require(all(not x.startswith(('PIN ','SOURCE ','PRED ')) for x in lines[:barrier]),'ANNOTATE_BEFORE_ACTIVITY')
    require(all(not x.startswith('SDF READBACK:') for x in lines[barrier:]),'NO_LATE_WRITES')
    reads=[x.split()[2:] for x in lines[:barrier] if x.startswith('SDF READBACK:')]
    desired=[]
    for label,instance in [('addf','adder'),('mux4','mux')]:
        state={}
        for field in maps[label]:
            key=field['key']; edge=field['edge']
            identity=(key,edge,field['source'],field['destination'])
            slots=state.setdefault(identity,[1000,1000])
            slots[('rise','fall').index(field['slot'])]=ps(field['typical_ns'])
            desired.append((['bench.'+instance,*identity],list(slots)))
    exact(len(reads),len(desired),'READBACK_POPULATION')
    for read,(ids,slots) in zip(reads,desired):
        exact(read[:5],ids,'READBACK_COMPILED_OWNER')
        exact([ps(x) for x in read[5:]],slots,'READBACK_BOTH_EFFECTIVE_SLOTS')
    result=[]
    for name in ['addf','mux4']:
        case=expected[name]; pin=case['pin']
        lo,hi=case['window']
        events=[(int(t),int(v)) if v in ['0','1'] else (int(t),v)
                for t,v in [x.split()[2:] for x in lines if x.startswith('PIN '+pin+' ')] if lo<=int(t)<=hi]
        exact(events,[(e['due_ps'],e['value']) for e in case['events']],'PIN_EVENTS_'+pin)
        for (observed_time, observed_value), e in zip(events, case['events']):
            f,=[f for f in maps[name] if f['original_sdf_line']==e['source_line'] and f['slot']==e['slot']]
            exact(f['sense'],e['sense'],'FROZEN_OWNER_SENSE')
            exact(ps(f['typical_ns']),e['delay_ps'],'FROZEN_SOURCE_DELAY')
            exact(e['input_ps']+e['delay_ps'],e['due_ps'],'SOURCE_DUE_TIME')
            exact(lines.count(f"SOURCE {f['source']} {e['input_ps']} {e['expected_source']}"),1,'PASSIVE_SOURCE_VECTOR')
            exact(lines.count(f"PRED {pin} {e['input_ps']} 1"),1,'SELECTED_PREDICATE_ENABLED')
            result.append(dict(case=name, master=('addf_1' if name=='addf' else 'mux4_2'),
                               source_model_line=f['original_declaration'],source_sdf_line=f['original_sdf_line'],
                               liberty_group=f['liberty_group'],liberty_line=f['liberty_line'],
                               slot=e['slot'],predicate=f['key'],input_edge=f['edge'],
                               generated_model_line=f['generated_model_line'],generated_sdf_line=f['sdf_line'],
                               input_ps=e['input_ps'],value=e['value'],expected_ps=e['due_ps'],
                               observed_ps=observed_time,observed_value=observed_value))
    return result
