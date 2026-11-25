"""Supply rejection from VDDA to the output with the references held fixed (psrr.sch)."""
from typing import Any
import math


def at(f, y, f0):
    for i in range(1, len(f)):
        if f[i] >= f0:
            a = (math.log10(f0) - math.log10(f[i - 1])) / (math.log10(f[i]) - math.log10(f[i - 1]))
            return y[i - 1] + a * (y[i] - y[i - 1])
    return y[-1]


def postprocess(results: dict[str, list], conditions: dict[str, Any]) -> dict[str, list]:
    f, y = results['frequency'], results['psrr']
    return {
        'psrr_dc': [at(f, y, 10.0)],
        'psrr_10k': [at(f, y, 1e4)],
        'psrr_1m': [at(f, y, 1e6)],
    }
