# -*- coding: utf-8 -*-
"""Shape validator for gen145_200_data_*.py"""
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

NAMES = [f"gen145_200_data_{c}" for c in "abcdefghij"]
DATA = {}
for n in NAMES:
    try:
        DATA.update(importlib.import_module(n).DATA)
    except ImportError:
        pass

problems = []
for key in sorted(DATA, key=int):
    d = DATA[key]
    for f in ("topic_en", "topic_vi", "mech_en", "mech_vi"):
        if not isinstance(d.get(f), str) or not d[f].strip():
            problems.append(f"{key}: missing {f}")
    for f, shape, n in (("vars", 3, 3), ("subs", 2, 4), ("errs", 2, 8)):
        v = d.get(f)
        if not isinstance(v, list) or len(v) != shape or any(len(x) != n for x in v):
            problems.append(f"{key}: {f} shape {[len(x) for x in v] if isinstance(v, list) else type(v)} expected {shape}x{n}")
    for f in ("steps", "drills"):
        v = d.get(f)
        ok = isinstance(v, list) and (
            (len(v) == 4 and all(len(x) == 2 for x in v)) or
            (len(v) == 2 and all(len(x) == 4 for x in v)))
        if not ok:
            problems.append(f"{key}: {f} shape {[len(x) for x in v] if isinstance(v, list) else type(v)}")

print(f"entries: {len(DATA)}  keys: {','.join(sorted(DATA, key=int)[:3])} ... {','.join(sorted(DATA, key=int)[-3:])}")
missing = [str(n) for n in range(145, 201) if str(n) not in DATA]
print(f"missing entries: {' '.join(missing) if missing else 'none'}")
if problems:
    print(f"PROBLEMS ({len(problems)}):")
    for p in problems:
        print("  " + p)
else:
    print("all shapes OK")
