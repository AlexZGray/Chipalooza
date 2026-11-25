"""Output voltage and total supply current at one code (dc_op.sch). SI units."""
from typing import Any


def postprocess(results: dict[str, list], conditions: dict[str, Any]) -> dict[str, list]:
    return {
        'vout_en': list(results['vout']),
        'idd_total': [a + b for a, b in zip(results['idd'], results['istring'])],
    }
