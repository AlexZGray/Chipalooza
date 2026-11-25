"""Static transfer characteristics from the settled code staircase (static_staircase.sch).

The testbench steps the code 0, 1, ..., 63 and holds each code until the output has settled.
Each code is sampled at the last time point before the code changes (the end of the run for
code 63). The string runs from VREFL = 0 to VREFH = VDDA, so 1 LSB = VDDA / 64.
  error(k)  = (V(k) - k LSB) / LSB                          absolute error, ideal line
  inl(k)    = (V(k) - V(0) - k (V(63) - V(0)) / 63) / LSB    endpoint-fit INL
  dnl(k)    = (V(k+1) - V(k)) / LSB - 1                      for the step k -> k+1
  unsettled = largest output change over the last 2 us of any code (should be << 1 LSB)
CACE expects SI units (V, A); it scales them to the units in the datasheet.
"""
from typing import Any


def postprocess(results: dict[str, list], conditions: dict[str, Any]) -> dict[str, list]:
    vdd = float(conditions['Vvdd'])
    lsb = vdd / 64
    t, cv = results['time'], results['vcode']
    last = {}
    for i, c in enumerate(cv):                  # last sample at which each integer code is applied
        if abs(c - round(c)) < 1e-3:
            last[int(round(c))] = i
    code = sorted(last)
    idx = [last[k] for k in code]
    v = [results['vout'][i] for i in idx]
    tap = [results['vtap'][i] for i in idx]
    idd = [results['idd'][i] for i in idx]
    istring = [results['istring'][i] for i in idx]
    unsettled = []
    for i in idx:
        j = i
        while j > 0 and t[i] - t[j] < 2e-6:
            j -= 1
        unsettled.append(abs(results['vout'][i] - results['vout'][j]))
    n = len(v)
    v0, vn = v[0], v[-1]
    err = [(v[k] - code[k] * lsb) / lsb for k in range(n)]
    inl = [(v[k] - v0 - k * (vn - v0) / (n - 1)) / lsb for k in range(n)]
    dnl = [(v[k + 1] - v[k]) / lsb - 1 for k in range(n - 1)]
    return {
        'code': code,
        'vout_code': v,
        'error': err,
        'inl': inl,
        'code_lower': code[:-1],
        'dnl': dnl,
        'min_step': [min(v[k + 1] - v[k] for k in range(n - 1))],          # V
        'zero_error': [v0 / lsb],                                          # LSB
        'full_scale_error': [(vn - 63 * lsb) / lsb],                       # LSB
        'gain_error': [((vn - v0) - 63 * lsb) / lsb],                      # LSB
        'unsettled': [max(unsettled) / lsb],                             # LSB
        'buffer_offset': [a - b for a, b in zip(v, tap)],                  # V
        'iref': istring,                                                   # A, settled string current
        'idd_total': [a + b for a, b in zip(idd, istring)],  # A, VDDA + VREFH
    }
