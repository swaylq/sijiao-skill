# rust-learn — 私教.skill 生成的 Rust 私教（参考样本）

sijiao-skill 的第一个端到端样本：把「学 Rust」蒸成一个**有状态私教** skill。

| 文件 | 层 | 说明 |
|------|----|------|
| `SKILL.md` | 教学层 | 私教 agent：读档 → 定位 → 教 → 批改 |
| `curriculum.json` → `curriculum.md` | 课程层 | 15 模块 novice→competent，由 `tools/curriculum_builder.py` 校验 + 渲染 |
| `learner-state.example.json` | 档案层 | 示例（真实 `learner-state.json` 私人、不进 git） |
| `references/research/01-08.md` | — | 8 路调研留痕，每条挂 source_id |
| `references/pedagogy.md` | — | Rust 特化教学法（报错驱动、卡点地图、间隔复习清单） |
| `meta.json` | — | 元数据：天花板 `competent`，诚实标注为 reference prototype |

装到 Claude Code：`python3 ../../tools/install.py install --host claude --source .`，或直接 `git clone`
到 host 的 skills 目录。

> 参考样本——课程从 Rust 正典（TRPL / Rustlings / Rust by Example）蒸出以演示管线端到端；
> 跑 `update 私教 rust` 做完整 8 路联网刷新 + 扩源。
