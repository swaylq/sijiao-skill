# Route 5 — 常见卡点 / 误区 / 平台期 (rust)

来源：users.rust-lang.org 与 r/rust 高频初学者问题 `T05-S001`、社区「learning Rust mistakes」长文 `T05-S002`。

| 卡点 | 落在模块 | 解法 |
|------|---------|------|
| **跟 borrow checker 打架**（最大平台期，weeks 2-4） | borrowing-references | 报错当信号读懂，不绕过 |
| String vs &str 混淆 | collections-strings | 讲清「拥有 vs 借用」 |
| 到处 .unwrap() | error-handling | 强制改写成 `?` 传播 |
| 想用继承/OOP | compound-types / generics-traits | trait + 组合替代 |
| 生命周期标注恐慌 | lifetimes | 等编译器逼时再学，给范例撤支架 |

这些直接 seed 进 tutor 期望的 `weak_spots`。
