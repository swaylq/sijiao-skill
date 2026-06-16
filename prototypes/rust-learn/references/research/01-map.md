# Route 1 — 知识地图 / 先修依赖 (rust)

依赖脊柱（来源：TRPL 章节顺序 = 官方公认教学序）：

```
setup → syntax-basics → ownership → borrowing-references
compound-types 早分叉；一切汇入 ownership/borrowing 后才进类型系统
(generics-traits → lifetimes)，再到 competent 段 (iterators / smart-pointers / concurrency) → capstone
```

- 关键洞察：**ownership/borrowing 是闸门** — 它没过，后面 lifetimes / smart-pointers / concurrency 全卡。所以放 novice 段、报错驱动练透。
- `compound-types`（struct/enum/match）不依赖 ownership，可与之并行，给学习者「能写出东西」的早期成就感。

来源：`T01-S001` TRPL 目录 https://doc.rust-lang.org/book/ · `T01-S002` Rustlings 练习目录顺序。
