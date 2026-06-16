# Route 6 — 能力评估 / 里程碑 (rust)

行为化的「会了」标志（来源：社区对「junior Rust 能做什么」的共识 `T06-S001`、the book 项目章 `T06-S002`）：

- **novice**：能独立写、编译、运行一个用 struct + enum + match 的小程序。
- **advanced beginner**：能用 `Result`/`?` 处理错误、用泛型 + trait、把代码拆成模块、加外部 crate。
- **competent**（本课天花板）：能从零搭一个**带测试、带错误处理的 CLI**，并能解释每个 `unwrap`/`?`/借用的选择；惯用迭代器。

毕业证明：`capstone-cli`（grep 克隆，可 `cargo install`）。再往上（async/unsafe/宏/嵌入式）属精通区。
