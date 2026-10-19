# -*- coding: utf-8 -*-
"""Behavioral sensitivity for sad_abm_v2.

Calibrate post_freeze_response so the baseline default rate matches
Goldman's 70%, then rerun the four scenarios.
Prints CSV to stdout; shell-redirect to a file.
"""
import statistics
from sad_abm_v2 import World, P

SCEN = {
    "base": dict(seal=1, platform_adaptive=0),
    "unseal": dict(seal=0, platform_adaptive=0),
    "resist": dict(seal=1, platform_adaptive=1),
    "both": dict(seal=0, platform_adaptive=1),
}


def run(params, years, seed, seal=1, adaptive=0):
    p = dict(P)
    p.update(params)
    p["years"] = years
    w = World(p, seed=seed, seal=seal, platform_adaptive=adaptive)
    rows = w.run()
    d = sum(r["default"] for r in rows)
    s = sum(r["settle"] for r in rows)
    f = sum(r["defend"] for r in rows)
    return {
        "cases": sum(r["cases"] for r in rows),
        "default_rate": d / max(1, d + s + f),
        "defend_rate": f / max(1, d + s + f),
        "coord_eff": statistics.mean(r["coord_effective"] for r in rows),
        "settle": s,
        "default": d,
        "defend": f,
    }


print("grid,post_freeze_response,scenario,cases_total,default_rate,defend_rate,coord_eff")
grid = []
for pfr in [0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30]:
    for name in ("base", "unseal"):
        r = run({"post_freeze_response": pfr}, 11, 1, seal=SCEN[name]["seal"])
        print("grid,%.2f,%s,%d,%.3f,%.3f,%.3f" % (
            pfr, name, r["cases"], r["default_rate"], r["defend_rate"], r["coord_eff"]))
        if name == "base":
            grid.append((abs(r["default_rate"] - 0.70), pfr, r["default_rate"]))

grid.sort()
best_pfr = grid[0][1]
print()
print("calibrated_post_freeze_response,%.2f,base_default_rate_at_seed1,%.3f" % (best_pfr, grid[0][2]))
print("scenario,seed,cases_total,default_rate,defend_rate,coord_eff")
summary = {}
for name, cfg in SCEN.items():
    vals = []
    for seed in (1, 2, 3, 4, 5):
        r = run({"post_freeze_response": best_pfr}, 11, seed, seal=cfg["seal"],
                adaptive=cfg["platform_adaptive"])
        vals.append(r)
        print("%s,%d,%d,%.3f,%.3f,%.3f" % (
            name, seed, r["cases"], r["default_rate"], r["defend_rate"], r["coord_eff"]))
    summary[name] = {
        "cases": statistics.mean(v["cases"] for v in vals),
        "default_rate": statistics.mean(v["default_rate"] for v in vals),
        "defend_rate": statistics.mean(v["defend_rate"] for v in vals),
        "coord_eff": statistics.mean(v["coord_eff"] for v in vals),
    }
print()
print("summary,scenario,mean_cases,mean_default_rate,mean_defend_rate,mean_coord_eff")
for name, v in summary.items():
    print("summary,%s,%.0f,%.3f,%.3f,%.3f" % (
        name, v["cases"], v["default_rate"], v["defend_rate"], v["coord_eff"]))
base = summary["base"]["cases"]
print()
print("effect_vs_base,scenario,case_change_pct,default_rate_change_pp")
for name in ("unseal", "resist", "both"):
    print("effect,%s,%+.1f%%,%+.1f" % (
        name, 100 * (summary[name]["cases"] / base - 1),
        100 * (summary[name]["default_rate"] - summary["base"]["default_rate"])))
