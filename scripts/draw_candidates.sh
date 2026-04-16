#!/bin/bash
# 阶段1随机抽卡脚本 - 真正的RNG，不依赖LLM"模拟"随机

POOL_JSON="/Users/ShownZHOU/Desktop/圆桌派skill/roundtable_pai/data/character_pool.json"

python3 - <<'PYEOF'
import json
import random

pool = json.load(open("/Users/ShownZHOU/Desktop/圆桌派skill/roundtable_pai/data/character_pool.json"))["characters"]

epic = [c for c in pool if c["rarity"] == "史诗"]
legendary = [c for c in pool if c["rarity"] == "传说"]
elite = [c for c in pool if c["rarity"] == "精英"]

result = []
attempts = 0
while len(result) < 10 and attempts < 1000:
    attempts += 1
    r = random.randint(0, 99)
    if r <= 2:
        group = epic
    elif r <= 17:
        group = legendary
    else:
        group = elite

    if group:
        c = random.choice(group)
        if c not in result:
            result.append(c)

for i, c in enumerate(result, 1):
    rarity_map = {"史诗": "3%", "传说": "15%", "精英": "82%"}
    pct = rarity_map.get(c["rarity"], "N/A")
    print(f"{i}. {c['display_name']}（{c['rarity']} ★ {pct}）：{c['fit_hint']}")
PYEOF
