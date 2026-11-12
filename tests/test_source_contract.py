# SPDX-License-Identifier: Apache-2.0
"""Regressions for layout-independent source checking and collateral edits."""
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import checks
import convert
import intake
import liberty
import verify
from prepare import ROOT


class SourceContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name)

    def model(self, case, compact=False):
        self.profile = json.loads((ROOT/'examples'/case/'producer.json').read_text())
        self.master = self.profile['master']
        original = ROOT/'upstream'/(self.master+'.behavioral.v')
        self.source = self.out/'original.v'
        raw = original.read_text()
        if compact:
            # Same original declarations on single physical lines. The source
            # conditions after ifnone still belong to their endpoint group.
            for d in reversed(intake.declarations(original)):
                a,b = d['loc']['bytes']
                statement = re.sub(r'//[^\n]*', '', d['text'])
                raw = raw[:a]+' '.join(statement.split())+raw[b:]
        self.source.write_text(raw)
        self.decls = intake.declarations(self.source)
        groups = [[self.master,*pins] for pins in self.profile['groups']]
        self.inventory = dict(self.profile, masters=[self.master], groups=groups)
        self.matrix = dict(groups=[dict(master=m,input=s,output=t) for m,s,t in groups])
        self.generated = self.out/'model.v'
        convert.standard_model(self.source,self.source,{self.master:self.decls},self.matrix,self.generated,
                               profile_inventory=self.inventory)
        return self.check()

    def check(self):
        return verify.standard_model(self.source,self.source,{self.master:self.decls},self.matrix,self.generated,
                                     profile_inventory=self.inventory)

    def test_single_line_source_and_generated_locators(self):
        result = self.model('addf', compact=True)
        rows = [d for d in result['declarations'][self.master] if (d['source'],d['destination'])==('A','S')]
        # Four source conditions each have two edges, plus the fallback pair.
        self.assertEqual(len(rows), 10)
        self.assertEqual(sum(d['condition_role']=='strict_conjunction' for d in rows), 8)
        lines = self.generated.read_text().splitlines()
        for row in rows:
            self.assertIn(row['edge']+' A', lines[row['line']-1])
        self.assertNotEqual(len(lines), len(self.source.read_text().splitlines()))

    def test_multiline_cone_keeps_measured_locations(self):
        self.model('mux4')
        raw = self.generated.read_text().replace(';\n   assign', ';\n\n   assign')
        self.generated.write_text(raw)
        result = self.check()
        for d in result['declarations'][self.master]:
            self.assertIn(d['key'], raw.splitlines()[d['line']-1])

    def test_missing_member_after_ifnone_is_rejected(self):
        self.model('addf')
        # B=CI=0 appears after both source fallbacks; omitting it from the
        # union must fail even though the compiled path itself still exists.
        key = '__gls_path_A_S_9f7c123088d11c7d'
        raw = self.generated.read_text().replace('   assign __gls_path_A_S_any = '+key+';\n', '')
        self.generated.write_text(raw)
        with self.assertRaises(checks.ContractError) as error: self.check()
        self.assertEqual(error.exception.code, 'STANDARD_COMPLETE_MEMBERSHIP_DRIVERS')

    def test_collateral_mux_endpoint_change_is_rejected(self):
        self.model('mux2-7t')
        raw = self.generated.read_text().replace('(I0 => Z)', '(I1 => Z)', 1)
        self.generated.write_text(raw)
        with self.assertRaises(checks.ContractError) as error: self.check()
        self.assertEqual(error.exception.code, 'STANDARD_SOURCE_ENDPOINT_EDGE')

    def test_untouched_carry_change_is_rejected(self):
        self.model('addf')
        raw = self.generated.read_text().replace('(A => CO)', '(B => CO)', 1)
        self.generated.write_text(raw)
        with self.assertRaises(checks.ContractError): self.check()

    def test_swapped_unequal_fields_are_rejected(self):
        proven = self.model('mux4')
        original = (ROOT/'examples/mux4/original.sdf').read_bytes()
        records = intake.records(original, self.master, self.decls)
        groups = liberty.liberty_groups((ROOT/'upstream'/(self.master+'__tt_025C_5v00.lib')).read_text(), self.master)
        joined = intake.writer_join(records, self.profile['records'], groups)
        declarations = proven['declarations'][self.master]
        body,_ = convert.standard_cell(records, declarations, joined)
        # An input-edge swap preserves record count and all numeric tokens.
        broken = body.replace('(negedge S0)', '(SWAP S0)', 1).replace('(posedge S0)', '(negedge S0)', 1).replace('(SWAP S0)', '(posedge S0)', 1)
        with self.assertRaises(checks.ContractError) as error:
            verify.standard_cell(records,self.decls,declarations,joined,groups,original,broken)
        self.assertEqual(error.exception.code, 'STANDARD_SOURCE_EXACT_ORDERED_RECORDS')


if __name__ == '__main__': unittest.main()
