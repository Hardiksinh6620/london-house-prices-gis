import unittest
from examples.audit_summary import audit

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.s=dict(count=33,minimum=180000,maximum=980000,sum=12088875,mean=366329.5,standard_deviation=163782.7,nulls=0,mean_decimal_places=1)
    def test_reported_summary(self):
        r=audit(self.s)
        self.assertTrue(r['mean_matches_sum_and_count'])
        self.assertTrue(r['reported_mean_within_range'])
        self.assertFalse(r['standard_deviation_verified'])
    def test_changed_total_detected(self):
        self.s['sum']=100
        self.assertFalse(audit(self.s)['mean_matches_sum_and_count'])
    def test_outside_range_detected(self):
        self.s['mean']=100
        self.assertFalse(audit(self.s)['reported_mean_within_range'])
    def test_invalid_counts_and_values(self):
        for field,value in [('count',0),('count',1.5),('nulls',-1),('sum',float('nan')),('standard_deviation',-1)]:
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):
                audit({**self.s,field:value})
    def test_explicit_decimal_rounding(self):
        r=audit(dict(count=2,minimum=0,maximum=3,sum=2.5,mean=1.3,standard_deviation=1,nulls=0,mean_decimal_places=1))
        self.assertTrue(r['mean_matches_sum_and_count'])
