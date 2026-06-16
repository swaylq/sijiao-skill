# Rust 教学法笔记（rust-learn 特化）

基于 `../../../references/pedagogy-framework.md`，针对 Rust 的具体落地。

## 最该刻意练习的点

Rust 的难不在语法，在**所有权 / 借用 / 生命周期**这套心智模型。这三块用「报错驱动」练：
直接喂真实 borrow-checker 报错，让学习者改对并**解释为什么报错**——比读十遍文档有用。

## 卡点地图（route 5）

- **跟 borrow checker 打架** — novice→advanced beginner 最大平台期。解法不是绕过，是把报错当信号读懂。
- **String vs &str 混淆** — 在 `collections-strings` 模块集中讲清「拥有 vs 借用」。
- **到处 .unwrap()** — `error-handling` 模块用强制改写练习根治。
- **想用继承 / OOP 写 Rust** — 用 trait + 组合替代；`compound-types` + `generics-traits` 纠正。

## 间隔重复清单（进 spaced_queue）

借用三原则 · Copy vs move · `Result`/`Option` 的 `?` 传播 · `Send`/`Sync` 含义 · `Rc`/`RefCell` 各自场景。

## 教学节奏（route 8）

6 小时/周，到「胜任」约 **10-14 周**。所有权那几周最容易弃坑——用小而频繁的 drill 维持打卡，
别一上来就上大项目。`capstone-cli` 放最后，作为「能独立做」的毕业证明。
