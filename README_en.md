<div align="center">

# 🎓 learn-skill (学习.skill)

### Name any skill you want to learn — it distills a private tutor that takes you from 0 to competent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![tests](https://img.shields.io/badge/tests-35%20passing-brightgreen)](tests/)

<br>

[colleague-skill](https://github.com/titanwings/colleague-skill) distills **one person** into an AI.<br>
[nuwa-skill](https://github.com/alchaincyf/nuwa-skill) distills **anyone's way of thinking**.<br>
[master-skill](https://github.com/swaylq/master-skill) distills **a whole industry's judgment** — *gives you the fish*.<br>

learn-skill does the opposite of "do it for you":<br>
**it turns you into the person who can.** *Teaches you to fish.*

[🚀 Install](#-install) · [✨ What the tutor looks like](#-what-the-tutor-looks-like) · [中文 README](README.md)

</div>

---

> **v0.1** — meta-skill + tooling engine (35 tests green) + first end-to-end prototype
> `rust-learn` (15 modules, novice→competent). 4th in the colleague → nuwa → master family.

## ✨ What the tutor looks like

Not "give me a study plan" (ChatGPT does that in one shot). A tutor that **remembers you and drills you**:

```
You    ❯ continue learning rust

Tutor  ❯ State loaded: you're on "Borrowing & References" (mastery 0.55),
         last stuck on the &mut-vs-& conflict. First a due review, then that wall.

         [Retrieval · the borrowing rules] No peeking — recite:
         in one scope, either ___ &refs, or ___ &mut, never ___.

You    ❯ any number of &, or one &mut, not both at once

Tutor  ❯ ✅ Got it — next review in 6 days. Now today's wall. This won't compile:

           let mut v = vec![1,2,3];
           let first = &v[0];
           v.push(4);            // ← compiler errors here
           println!("{first}");

         Don't look it up: `first` holds a shared borrow of v, `push` needs &mut v —
         which rule you just recited does that break?
```

Four things a static plan can't do: **load state → surface due reviews (spaced repetition) →
hit your known weak spot → Socratic prompting**. Every session continues the last.

## 🧠 What it distills

Each generated `{skill}-learn` is a self-contained 3-layer directory:

- 📚 **Curriculum** (`curriculum.json` / `.md`) — prereq-ordered, Dreyfus-staged modules; each with
  Bloom-leveled objectives, canonical resources, an **assessable exercise**, a milestone, and a
  behavioral competence check.
- 🧑‍🏫 **Tutor** (`SKILL.md`) — reads state → places you → explain / worked-example / faded / independent → grade.
- 🗂️ **Learner state** (`learner-state.json`) — progress / weak spots / **SM-2 spaced repetition** / streak (private, gitignored).

Built on learning science: Dreyfus stages · Bloom · deliberate practice · spaced retrieval ·
desirable difficulty. See [`references/pedagogy-framework.md`](references/pedagogy-framework.md).

**Honest limits:** a tutor reaches ~**competent**; expertise needs years of real practice — it
says so. Skills needing real-world feedback get a curriculum but hand grading off to a human.

## ⚡ Install

```bash
git clone https://github.com/swaylq/learn-skill.git ~/.claude/skills/learn-skill
```

Other hosts: `python3 tools/install.py install --host <claude|openclaw|codex|hermit> --source <dir>`.

## 🚀 Usage

```
> learn rust            # not installed → distills a rust-learn
> continue learning rust
> quiz me on rust ownership
> update 学习 rust       # incremental refresh of decaying resources
```

## 📜 License

MIT © [swaylq](https://github.com/swaylq) · [中文 README](README.md)
