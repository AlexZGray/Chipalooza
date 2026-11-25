"""Settling, slew and overshoot of a code step (tran_step.sch).

The code changes from b to 63 - b at t = 2 us. Settling time is measured from the step to
the last time the output is outside +-0.5 LSB of its final value (last sample).
CACE expects SI units (s, V/s, V); it scales them to the units in the datasheet.
"""
from typing import Any

T_STEP = 2e-6


def postprocess(results: dict[str, list], conditions: dict[str, Any]) -> dict[str, list]:
    vdd = float(conditions['Vvdd'])
    lsb = vdd / 64
    t = results['time']
    v = results['vout']
    i0 = next(i for i, x in enumerate(t) if x >= T_STEP)
    v_start = v[i0 - 1]
    v_end = v[-1]
    band = 0.5 * lsb
    last_out = None
    for i in range(i0, len(t)):
        if abs(v[i] - v_end) > band:
            last_out = i
    if last_out is None:
        settle = 0.0
    else:
        settle = t[min(last_out + 1, len(t) - 1)] - T_STEP
    # 10 % to 90 % slew rate, full-scale steps only (a one-LSB step has no slewing part)
    dv = v_end - v_start
    slew = []
    if abs(dv) > 4 * lsb:
        lo, hi = v_start + 0.1 * dv, v_start + 0.9 * dv
        t10 = next(t[i] for i in range(i0, len(t)) if (v[i] - lo) * dv >= 0)
        t90 = next(t[i] for i in range(i0, len(t)) if (v[i] - hi) * dv >= 0)
        slew = [abs(0.8 * dv) / max(t90 - t10, 1e-12)]               # V/s
    # Overshoot: largest excursion past the final value in the direction of the step
    sign = 1 if dv > 0 else -1
    over = max((x - v_end) * sign for x in v[i0:])
    return {
        'settling_time': [settle],
        'slew_rate': slew,
        'overshoot': [max(over, 0.0)],                                      # V
        'final_error': [(v_end - (63 - int(conditions['b'])) * lsb) / lsb],  # LSB
    }
