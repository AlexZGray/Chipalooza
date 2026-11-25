"""DC gain, unity-gain frequency and phase margin of the buffer loop (ac_loop.sch).

lg_db and lg_ph are the magnitude (dB) and continuous phase (degrees) of the loop gain
T = -V(out)/V(inm) with the feedback broken at the inverting input.
"""
from typing import Any
import math


def postprocess(results: dict[str, list], conditions: dict[str, Any]) -> dict[str, list]:
    f = results['frequency']
    g = results['lg_db']
    p = results['lg_ph']
    ugf = pm = None
    for i in range(1, len(f)):
        if g[i - 1] >= 0 > g[i]:
            a = g[i - 1] / (g[i - 1] - g[i])
            lf = math.log10(f[i - 1]) + a * (math.log10(f[i]) - math.log10(f[i - 1]))
            ugf = 10 ** lf
            ph = p[i - 1] + a * (p[i] - p[i - 1])
            pm = 180 + (ph - 360 * round(p[0] / 360))
            break
    # gain margin: loop gain where the phase crosses -180 degrees
    gm = None
    p0 = 360 * round(p[0] / 360)
    for i in range(1, len(f)):
        if (p[i - 1] - p0) > -180 >= (p[i] - p0):
            a = (p[i - 1] - p0 + 180) / (p[i - 1] - p[i])
            gm = -(g[i - 1] + a * (g[i] - g[i - 1]))
            break
    return {
        'dc_gain': [g[0]],
        'ugf': [ugf if ugf else 0.0],                                       # Hz
        'phase_margin': [pm if pm is not None else 0.0],
        'gain_margin': [gm if gm is not None else 99.0],
        'loop_gain': g,
        'loop_phase': [x - p0 for x in p],
    }
