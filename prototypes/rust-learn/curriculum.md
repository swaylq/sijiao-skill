# rust — 学习路径

## 阶段：novice

### 工具链与第一个程序  `(setup-toolchain)`
- 目标（apply）：用 rustup 装好工具链，能 cargo new / run / build
- 目标（understand）：说清 cargo 是包管理器 + 构建器 + 测试器
- 练习（drill）：cargo new hello，改 main 打印一句话，cargo run 跑通；再 cargo build --release 看 target 目录变化

### 基础语法：变量、类型、函数、控制流  `(syntax-basics)`
- 先修：setup-toolchain
- 目标（understand）：区分 let / let mut / const，说清不可变默认
- 目标（apply）：写带参数和返回值的函数 + if / loop / while / for
- 练习（drill）：做 Rustlings 的 variables + functions + if 三组，全部编译通过

### 所有权与 move 语义  `(ownership)`
- 先修：syntax-basics
- 目标（understand）：解释 move 后原变量失效、为何这样设计（无 GC 的内存安全）
- 目标（analyze）：判断一段代码哪里发生 move、哪里需要 clone
- 练习（drill）：做 Rustlings move_semantics 全组；对每个修复说出『为什么这里 move 了』

### 结构体、枚举与模式匹配  `(compound-types)`
- 先修：syntax-basics
- 目标（apply）：定义 struct / enum，用 match 穷尽处理每个变体
- 目标（create）：用 enum + match 建模一个状态机
- 练习（drill）：做 Rustlings structs + enums；用 enum 写一个交通灯状态机，match 返回下一个状态

### 借用与引用  `(borrowing-references)`
- 先修：ownership
- 目标（remember）：复述借用三原则（任意多个 & 或 唯一一个 &mut，不可同时）
- 目标（apply）：把一个 move-报错的函数改成借用，编译通过
- 练习（drill）：给定 5 个 borrow-checker 报错片段，逐个改对并解释报错
- 里程碑：写一个对 Vec<i32> 求和但不拿走所有权的函数 — 会了的标志：能独立写出借用版函数且 caller 之后还能用这个 Vec

## 阶段：advanced_beginner

### 模块系统与 crate 依赖  `(modules-crates)`
- 先修：syntax-basics
- 目标（apply）：用 mod / pub / use 组织代码
- 目标（apply）：从 crates.io 加一个依赖并在项目里用起来
- 练习（drill）：把单文件程序拆成 2-3 个模块；加 `anyhow` 依赖并用它简化错误处理

### 错误处理：Result / Option / ?  `(error-handling)`
- 先修：compound-types
- 目标（understand）：区分可恢复（Result）与不可恢复（panic!）错误
- 目标（apply）：用 ? 传播错误，避免到处 unwrap
- 练习（drill）：把一个满是 .unwrap() 的读文件函数改写成返回 Result<_, io::Error> 并用 ? 传播

### 集合与字符串：Vec / HashMap / String vs &str  `(collections-strings)`
- 先修：compound-types, borrowing-references
- 目标（understand）：讲清 String（拥有）vs &str（借用）的区别和何时用哪个
- 目标（apply）：用 Vec + HashMap 解决一个统计类问题
- 练习（project）：读一段文本，用 HashMap 统计词频，按出现次数排序打印 top 10

### 泛型与 trait  `(generics-traits)`
- 先修：compound-types, error-handling
- 目标（apply）：写泛型函数 + trait bound
- 目标（apply）：为自己的类型实现标准 trait（如 Display / From）
- 练习（drill）：做 Rustlings generics + traits；给一个 Temperature 类型实现 Display 和 From<f64>

### 生命周期标注  `(lifetimes)`
- 先修：borrowing-references, generics-traits
- 目标（understand）：读懂 'a 标注表达的是引用有效期关系
- 目标（apply）：给一个返回引用的函数加正确的生命周期标注
- 练习（drill）：做 Rustlings lifetimes 全组；写一个返回两个 &str 中较长者的函数

## 阶段：competent

### 测试与工程化工具：test / clippy / rustfmt  `(testing-tooling)`
- 先修：modules-crates, error-handling
- 目标（apply）：写单元测试 + 集成测试，cargo test 跑通
- 目标（apply）：用 clippy + rustfmt 让代码符合社区规范
- 练习（drill）：给词频统计模块写 3 个单元测试 + 1 个集成测试；跑 cargo clippy 清掉所有 warning

### 闭包与迭代器  `(closures-iterators)`
- 先修：generics-traits, collections-strings
- 目标（apply）：用 map / filter / collect / fold 替代手写 for 循环
- 目标（evaluate）：判断何时迭代器链比命令式循环更清晰/更慢
- 练习（drill）：把之前词频统计的循环版重写成迭代器链版，行为不变

### 智能指针与内部可变性：Box / Rc / RefCell  `(smart-pointers)`
- 先修：lifetimes, error-handling
- 目标（understand）：解释 Box / Rc / RefCell 各自解决什么问题
- 目标（create）：用 Rc<RefCell<T>> 实现一个共享可变的图/树节点
- 练习（project）：用 Box 实现一个递归链表；用 Rc<RefCell<>> 实现两个节点能互相引用的小图

### 并发：线程、channel、Arc/Mutex  `(concurrency)`
- 先修：smart-pointers, closures-iterators
- 目标（apply）：用 thread::spawn + channel 在线程间传消息
- 目标（analyze）：解释 Send/Sync 与 Arc<Mutex<T>> 为何能安全共享状态
- 练习（drill）：起 4 个线程并行算一个大 Vec 的和，用 Arc<Mutex<>> 或 channel 汇总，结果与单线程一致

### 毕业项目：完整 CLI 工具  `(capstone-cli)`
- 先修：testing-tooling, concurrency, closures-iterators
- 目标（create）：把所有权/错误处理/模块/测试整合进一个真实可用的 CLI
- 练习（project）：做一个 grep 克隆：读文件、按参数过滤行、错误用 Result 处理、带 clap 解析参数、写测试，发布到本地 cargo install
- 里程碑：一个能 cargo install 的 grep-clone CLI（参数解析 + 文件 IO + 错误处理 + 测试） — 会了的标志：能独立从零搭一个带测试和错误处理的 Rust CLI 并解释每个 unwrap/?/借用的选择
