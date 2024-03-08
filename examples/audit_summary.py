"""New archive utility: check published aggregates, not unseen raw data."""
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path

def audit(summary):
    values={key:Decimal(str(summary[key])) for key in ['count','minimum','maximum','sum','mean','standard_deviation','nulls']}
    if any(not v.is_finite() for v in values.values()):
        raise ValueError('All numeric fields must be finite')
    n=values['count']; missing=values['nulls']; places=summary['mean_decimal_places']
    if n<=0 or n!=n.to_integral_value() or missing<0 or missing!=missing.to_integral_value():
        raise ValueError('Count must be a positive integer and null count a nonnegative integer')
    if type(places) is not int or not 0<=places<=6:
        raise ValueError('Mean decimal places must be an integer from zero to six')
    if values['minimum']>values['maximum'] or values['standard_deviation']<0:
        raise ValueError('Invalid range or negative standard deviation')
    quantum=Decimal(1).scaleb(-places)
    calculated=values['sum']/n
    return {'mean_matches_sum_and_count':calculated.quantize(quantum,rounding=ROUND_HALF_UP)==values['mean'].quantize(quantum,rounding=ROUND_HALF_UP),'reported_mean_within_range':values['minimum']<=values['mean']<=values['maximum'],'calculated_mean':str(calculated),'standard_deviation_verified':False,'raw_data_verified':False}

if __name__=='__main__':
    source=Path(__file__).resolve().parents[1]/'data/reported-summary.json'
    print(json.dumps(audit(json.loads(source.read_text())),indent=2))
