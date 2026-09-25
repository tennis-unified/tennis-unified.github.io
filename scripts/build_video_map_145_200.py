# -*- coding: utf-8 -*-
"""Build article_video_map_145_200.json via a curated mapping onto the verified
video set used for articles 1-144 (no placeholders; all IDs are real embeds)."""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
SCRIPTS = r"D:\Github Repos\tennis-unified\scripts"

with open(os.path.join(SCRIPTS, "article_video_map_1_144.json"), encoding="utf-8") as f:
    POOL = json.load(f)

# curated: article number -> pool key whose topic matches
CURATED = {
    145: 129, 146: 138, 147: 93, 148: 134, 149: 132, 150: 133,
    151: 104, 152: 127, 153: 105, 154: 137, 155: 128, 156: 144,
    157: 136, 158: 122, 159: 140, 160: 124,
    161: 20, 162: 117, 163: 61, 164: 14, 165: 61, 166: 57,
    167: 57, 168: 64, 169: 64, 170: 61, 171: 11, 172: 88,
    173: 111, 174: 10, 175: 61, 176: 57, 177: 64, 178: 106,
    179: 11, 180: 19, 181: 56, 182: 15, 183: 83, 184: 62,
    185: 48, 186: 61, 187: 77, 188: 118, 189: 68, 190: 77,
    191: 40, 192: 20, 193: 50, 194: 65, 195: 40, 196: 70,
    197: 116, 198: 19, 199: 54, 200: 120,
}

out = {}
missing = []
for num in range(145, 201):
    key = str(CURATED[num])
    if key not in POOL:
        missing.append(num)
        continue
    out[str(num)] = {
        "video_id": POOL[key]["video_id"],
        "title": POOL[key]["title"],
        "channel": POOL[key]["channel"],
    }

if missing:
    raise SystemExit(f"missing pool keys for: {missing}")

path = os.path.join(SCRIPTS, "article_video_map_145_200.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

ids = {v["video_id"] for v in out.values()}
placeholders = [k for k, v in out.items() if not v["video_id"] or "PLACEHOLDER" in v["video_id"]]
print(f"wrote {path}: {len(out)} entries, {len(ids)} distinct videos, placeholders: {placeholders}")
for num in (145, 148, 156, 162, 178, 193, 200):
    v = out[str(num)]
    print(f"  {num} -> {v['video_id']} | {v['title'][:64]} | {v['channel']}")
