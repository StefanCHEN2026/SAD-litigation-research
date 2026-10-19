# -*- coding: utf-8 -*-
"""Out-of-sample validation for sad_abm_v2.

Calibrate capacity0/cap_growth on 2020-2023, then predict 2024-2025.
Prints CSV to stdout; shell-redirect to a file.
"""
import statistics
from sad_abm_v2 import World, P

ACTUAL = {2020: 626, 2021: 865, 2022: 1031, 2023: 1363, 2024: 2082, 2025: 3356}
YEARS = [2020, 2021, 2022, 2023, 2024, 2025]


def run(params, years, seed):
    p = dict(P)
    p.update(params)
    p["years"] = years
    w = World(p, seed=seed, seal=1, platform_adaptive=0)
    return [r["cases"] for r in w.run()]


def mape(pred, actual):
    return sum(abs(p - a) / a for p, a in zip(pred, actual)) / len(actual)


def one_row(tag, params, seeds=(1, 2, 3, 4, 5)):
    runs = [run(params, len(YEARS), s) for s in seeds]
    means = [statistics.mean(r[i] for r in runs) for i in range(len(YEARS))]
    sds = [statistics.pstdev(r[i] for r in runs) for i in range(len(YEARS))]
    fit = mape(means[:4], [ACTUAL[y] for y in YEARS[:4]])
    hold = mape(means[4:], [ACTUAL[y] for y in YEARS[4:]])
    cols = [tag, str(params.get("capacity0")), str(params.get("cap_growth"))]
    cols += ["%.0f" % x for x in means]
    cols += ["%.0f" % x for x in sds]
    cols += ["%.4f" % fit, "%.4f" % hold]
    print(",".join(cols))
    for y, p, a in zip(YEARS, means, [ACTUAL[y] for y in YEARS]):
        print("  detail,%s,%d,pred=%.0f,actual=%d,err=%+.1f%%" % (tag, y, p, a, 100 * (p - a) / a))


print("grid,capacity0,cap_growth,c2020,c2021,c2022,c2023,mape_2020_2023")
best = None
for c in range(30000, 60001, 5000):
    for g in [0.20, 0.25, 0.30, 0.35, 0.40, 0.45]:
        pred = run({"capacity0": c, "cap_growth": g}, 4, 1)
        err = mape(pred, [ACTUAL[y] for y in YEARS[:4]])
        print("grid,%d,%.2f,%s,%.4f" % (c, g, ",".join(str(x) for x in pred), err))
        if best is None or err < best[0]:
            best = (err, c, g, pred)
print()
print("best_calibration_2020_2023,%.4f,capacity0=%d,cap_growth=%.2f" % (best[0], best[1], best[2]))
print("benchmark_full_series,capacity0=40000,cap_growth=0.35")
print("tag,capacity0,cap_growth,c2020,c2021,c2022,c2023,c2024,c2025,sd2020,sd2021,sd2022,sd2023,sd2024,sd2025,mape_fit,mape_holdout")
one_row("OOS_best", {"capacity0": best[1], "cap_growth": best[2]})
one_row("benchmark", {"capacity0": 40000, "cap_growth": 0.35})
