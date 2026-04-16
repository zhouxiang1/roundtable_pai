# Candidate Selection

阶段 1 直接从全人物池按稀有度权重随机抽取 10 张候选卡。

## 数据来源

- 只从 `data/character_pool.json` 的 `characters` 字段获取人物列表（包含 display_name、character_id、rarity、fit_hint）
- 不读取 `candidate_index.json`（该文件含标签数据，阶段1不需要）
- 不读取 `references/personas/*.md`
- 按 `canonical` 角色去重，不展示 alias 重复人物

## 稀有度权重

- 史诗：权重 3（0~2）
- 传说：权重 15（3~17）
- 精英：权重 82（18~99）

## 抽卡步骤（必须用脚本执行）

> **重要**：阶段1的随机抽取必须通过 `scripts/roundtable_controller.py` 脚本执行，不能让 LLM 自行生成随机数。LLM 只负责展示脚本输出结果。

1. 运行 Bash 命令：`python3 scripts/roundtable_controller.py start "<问题>"`（其中问题由用户提供）
2. 脚本输出即为 10 位候选人物，按抽中顺序展示 1~10 序号
3. 脚本内部已完成：权重随机（0~2=史诗3%、3~17=传说15%、18~99=精英82%）、去重、不放回抽取

## 排序规则

- 按抽中顺序输出，保持 1~10 序号

## 展示格式

```text
1. 乔布斯（史诗 ★ 3%）：适合看差异化和产品判断。
2. 芒格（传说 ★ 15%）：适合拆风险和机会成本。
3. 雷军（精英 ★ 82%）：适合看落地和获客。
```

## 候选推荐提示模板

> **注意**：随机抽取必须用 `scripts/roundtable_controller.py` 脚本执行，以下模板只用于生成展示文案，不做随机。

```text
你现在为这个问题推荐 10 位候选人物。

任务：运行 `python3 scripts/roundtable_controller.py start "<问题>"`，将脚本输出作为候选池直接展示。

输出格式：
- display_name
- character_id
- rarity
- fit_reason（12~28字，只解释适配点）

要求：
- 候选只从 `character_pool.json` 的 `characters` 列表里抽取，禁止自行补充
- 人物稀有度和概率标注格式：`人物名（稀有度 ★ X%）`（史诗 3%、传说 15%、精英 82%）
```
