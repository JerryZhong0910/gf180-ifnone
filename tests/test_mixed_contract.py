# SPDX-License-Identifier: Apache-2.0
"""Public-entry coverage for mixed records, partial fields and independent rejection."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import checks
import intake
import liberty
import verify
from prepare import ROOT


class MixedContract(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.profile=json.loads((ROOT/'examples/mixed-mux2/producer.json').read_text())
        self.sdf=(ROOT/'examples/mixed-mux2/original.sdf').read_text()

    def convert(self, successful=True):
        self.master=self.profile['master'];up=ROOT/'upstream'
        self.model=up/(self.master+'.behavioral.v');self.lib=up/(self.master+'__tt_025C_5v00.lib')
        (self.root/'input.sdf').write_text(self.sdf)
        (self.root/'producer.json').write_text(json.dumps(self.profile))
        self.output=self.root/'output'
        p=subprocess.run([sys.executable,'-B',str(ROOT/'tools/prepare.py'),str(self.output),
            '--model',str(self.model),'--helper',str(up/(self.master+'.functional.v')),'--liberty',str(self.lib),
            '--sdf',str(self.root/'input.sdf'),'--producer',str(self.root/'producer.json')],capture_output=True,text=True)
        if successful:self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        else:self.assertNotEqual(p.returncode,0)
        return p.stdout+p.stderr

    def verify_sdf(self, body):
        ds=intake.declarations(self.model)
        records=intake.records(self.sdf.encode(),self.master,ds)
        groups=liberty.liberty_groups(self.lib.read_text(),self.master)
        joined=intake.writer_join(records,self.profile['records'],groups)
        inventory=dict(self.profile,masters=[self.master],groups=[[self.master,*g] for g in self.profile['groups']])
        matrix=dict(groups=[dict(master=self.master,input=s,output=t) for s,t in self.profile['groups']])
        proven=verify.standard_model(self.model,self.model,{self.master:ds},matrix,self.output/'model.v',profile_inventory=inventory)
        return verify.standard_cell(records,ds,proven['declarations'][self.master],joined,groups,self.sdf.encode(),body)

    def test_public_mixed_context_order_and_empty_slots(self):
        self.convert();body=(self.output/'converted.sdf').read_text()
        self.assertIn('(INSTANCE mux)',body)
        self.assertIn('(IOPATH I1 Z (0.801:0.811:0.821) (0.861:0.877:0.899))',body)
        records=json.loads((self.output/'record-map.json').read_text())
        self.assertEqual([r['action'] for r in records],['edge-fields','condition-renamed','edge-fields','preserved','condition-renamed','condition-renamed'])
        self.assertEqual([r['output_lines'] for r in records],[[9,10],[11],[12,13],[14],[15],[16]])
        self.assertIn('(IOPATH I0 Z () (0.601:0.617:0.653))',body)
        self.assertIn('(IOPATH I0 Z () ())',body)
        self.verify_sdf(body)

    def test_missing_ordinary_record_and_unsynchronized_condition_rejected(self):
        self.convert();body=(self.output/'converted.sdf').read_text()
        bad=['\n'.join(line for line in body.splitlines() if not line.startswith('(IOPATH I1 Z'))+'\n',
             body.replace('(COND __gls_path_I0_Z_3235b9e3e2cc8771 ',"(COND (I1===1'b0) ")]
        for text in bad:
            with self.subTest(text=text),self.assertRaises(checks.ContractError) as err:self.verify_sdf(text)
            self.assertEqual(err.exception.code,'STANDARD_SOURCE_EXACT_ORDERED_RECORDS')

    def test_target_partial_requires_only_present_field_owner(self):
        self.sdf=self.sdf.replace('(0.382399:0.382399:0.382399)', '()',1)
        self.profile['records'][0]['record_sha256']=intake.digest(self.sdf.splitlines()[6])
        del self.profile['records'][0]['fall_group']
        self.convert();self.assertEqual(len(json.loads((self.output/'field-map.json').read_text())),3)
        self.verify_sdf((self.output/'converted.sdf').read_text())

    def test_edged_target_has_distinct_field_owners(self):
        lines=self.sdf.splitlines();lines[6]=lines[6].replace('IOPATH S','IOPATH (posedge S)')
        self.sdf='\n'.join(lines)+'\n'
        owner=self.profile['records'][0];other=self.profile['records'][1]
        owner['record_sha256']=intake.digest(lines[6]);owner['fall_group']=6
        owner['rise_group_sha256']=owner['group_sha256'];owner['fall_group_sha256']=other['group_sha256'];del owner['group_sha256']
        self.convert();body=(self.output/'converted.sdf').read_text()
        self.assertIn('(IOPATH (posedge S) Z () (0.382399:0.382399:0.382399))',body)
        self.verify_sdf(body)

    def test_input_edge_conflict_is_rejected(self):
        self.sdf=self.sdf.replace('IOPATH S','IOPATH (negedge S)',1)
        self.profile['records'][0]['record_sha256']=intake.digest(self.sdf.splitlines()[6])
        self.assertIn('SOURCE_EDGE_CONFLICT',self.convert(False))

    def test_valid_hash_does_not_prove_condition_binding(self):
        # A->S groups have the same endpoints but different conditions. Assign
        # another authentic group's ID/hash; independent condition checking rejects it.
        self.profile=json.loads((ROOT/'examples/addf/producer.json').read_text())
        self.sdf=(ROOT/'examples/addf/original.sdf').read_text()
        m=self.profile['master'];groups=liberty.liberty_groups((ROOT/'upstream'/(m+'__tt_025C_5v00.lib')).read_text(),m)
        wrong=next(g for g in groups if g['related_pin']=='A' and g['output']=='S' and g['timing_sense']=='positive_unate' and g['ordinal']!=12)
        record=self.profile['records'][0];record.update(rise_group=wrong['ordinal'],fall_group=wrong['ordinal'],group_sha256=intake.digest(wrong['raw']))
        self.assertIn('STANDARD_SOURCE_LIBERTY_CONDITION',self.convert(False))

    def test_untouched_addf_carry_records_need_no_owner(self):
        self.profile=json.loads((ROOT/'examples/addf/producer.json').read_text())
        ordinary='(IOPATH A CO (0.101:0.211:0.311) ())'
        conditional="(COND (B===1'b0 && CI===1'b1) (IOPATH A CO () (0.401:0.419:0.431)))"
        self.sdf=(ROOT/'examples/addf/original.sdf').read_text().replace('\n))))','\n'+ordinary+'\n'+conditional+'\n))))')
        self.convert();body=(self.output/'converted.sdf').read_text()
        self.assertIn(ordinary,body);self.assertIn(conditional,body)
        self.verify_sdf((self.output/'converted.sdf').read_text())

    def test_unknown_record_is_reported_not_dropped(self):
        self.sdf=self.sdf.replace('\n))))','\n(INTERCONNECT a b (0.1:0.2:0.3))\n))))')
        self.assertIn('SOURCE_IOPATH_FORM',self.convert(False))


if __name__=='__main__':unittest.main()
