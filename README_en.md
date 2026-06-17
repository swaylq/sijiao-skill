<div align="center">

# 🎓 私教.skill &nbsp;(sijiao-skill)

### Name any skill you want to learn — it distills a **stateful private tutor** that takes you from 0 to competent

> *"Give a man a fish, or teach him to fish — master-skill makes your AI a master of the industry; 私教.skill trains YOU into a master of the field."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![tests](https://img.shields.io/badge/tests-35%20passing-brightgreen)](tests/)

<br>

[colleague-skill](https://github.com/titanwings/colleague-skill) distills **one person** into an AI.<br>
[master-skill](https://github.com/swaylq/master-skill) distills **a whole industry's judgment** — *gives you the fish*.<br>

But there's something more important than doing it for you —<br>
**turning you into the person who can.**

<br>

Tell it what you want to learn; it runs **8 research routes**, distills a learning-science path
from 0 to *competent*, and generates a tutor that **remembers where you are and adapts**.

<br>

> **The difference from "ChatGPT, give me a study plan":**<br>
> **that's a one-off sheet of paper; this is a tutor that remembers you, drills you, and knows where you're stuck.**

<br>

[🚀 Install](#-install) · [✨ What the tutor looks like](#-what-the-tutor-looks-like) · [🧠 What it distills](#-what-it-distills) · [⭐ Samples](#-distilled-samples) · [中文 README](README.md)

</div>

---

> 📊 &nbsp;**v0.1** — meta-skill + tooling engine (**35 tests green**, stdlib-only) + **4 end-to-end
> samples** (rust / linear-algebra / english-reading / weight-loss, **53 modules**). Every sample's prereq graph is
> topologically validated and its curriculum rendered by the engine.
>
> 🧬 &nbsp;**3rd in the family** — colleague → master → sijiao. Flips the meta-skill frame from
> *distill an expert* to *teach you to become one*.
>
> 🎯 &nbsp;**Ceiling honestly capped at "competent"** — a tutor gets you to "can do the normal task
> independently"; mastery takes years of real practice. A skill that hides its limits isn't trustworthy.

---

## ✨ What the tutor looks like

> Not a search engine, not a study plan. A tutor that *remembers you and drills you*, sitting next to you.

#### 🦀 Scenario 1 · Rust (load state → due review → hit the weak spot → Socratic)

```
You    ❯ continue learning rust

Tutor  ❯ State loaded: you're on "Borrowing & References" (mastery 0.55),
         last stuck on the &mut-vs-& conflict. First a due review, then that wall.

         [Retrieval · the borrowing rules] No peeking:
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

#### 📐 Scenario 2 · Linear algebra (diagnoses an intuition gap, not a prereq gap — builds the picture before computing)

```
You    ❯ learning linear algebra but eigenvalues just fog my brain

Tutor  ❯ State loaded: stuck on eigenvalues, but determinants & transforms are done
         (mastery 0.8+) — so it's not a prereq gap, it's a missing mental picture. Don't compute yet.

         One sentence: an eigenvector is a vector this matrix-as-transform leaves pointing
         the same way, only stretched; the eigenvalue is the stretch factor.

         Take [[2,0],[0,3]]: it stretches the x-axis 2× and the y-axis 3×.
         No computing — can you just name its two eigenvectors and eigenvalues?

You    ❯ (1,0) with 2, (0,1) with 3

Tutor  ❯ ✅ That's the geometric core. Now a non-diagonal matrix — reason from "direction unchanged"…
```

#### 📖 Scenario 3 · English reading (AI generates a level-matched sentence to drill the "translate word-by-word" habit)

```
You    ❯ continue practicing english reading

Tutor  ❯ State loaded: you're on "complex sentences" (mastery 0.45); old habit is
         word-by-word translation. Let's drill finding the main clause.

         [Generated · matched to your level] Find subject-verb-object, don't translate:
         "The startup that the investors had backed quietly
          collapsed after its only customer left."

You    ❯ main clause is "The startup collapsed"?

Tutor  ❯ ✅ Yes! "that…backed" is a relative clause modifying startup, "after…" is adverbial.
         You found the spine — exactly the skill. Here's one nested deeper…
```

**Four things a static study plan can't do:** load state → surface due spaced-repetition items →
hit your known weak spot → Socratic prompting. Every session continues the last.

---

## 🧠 What it distills

A **learning-science path**, not a pile of resources. Each generated `{skill}-learn` is a
self-contained 3-layer directory:

| Layer | File | What's in it |
|-------|------|--------------|
| 📚 **Curriculum** | `curriculum.json` / `.md` | prereq-ordered, Dreyfus-staged modules; each with Bloom-leveled objectives, canonical resources, an **assessable exercise**, a milestone, a behavioral competence check |
| 🧑‍🏫 **Tutor** | `SKILL.md` | reads state → places you → explain / worked-example / faded / independent → grade |
| 🗂️ **Learner state** | `learner-state.json` | progress / weak spots / **SM-2 spaced repetition** / streak (private, gitignored) |

Built on five learning-science principles ([`references/pedagogy-framework.md`](references/pedagogy-framework.md)):
Dreyfus stages · Bloom's taxonomy · deliberate practice (every module has an assessable exercise) ·
spaced retrieval · desirable difficulty (worked-example → faded guidance).

---

## 🔍 Why trust what it distills

Every generated skill passes a learning-specific quality rubric:

- ✅ **Prereq graph is acyclic and justified** — `validate_dag` returns empty; each "learn A before B" traces to a source
- ✅ **Every module has an assessable exercise** — not "read the book", but "a task that can be graded"
- ✅ **Competence checks are behavioral** — "can independently do X", not "understands X"
- ✅ **Primary sources** — canon recommended by ≥3 independent sources; SEO listicles / content farms rejected
- ✅ **Honest ceiling** — `dreyfus_ceiling ≤ competent`; never claims to make an expert

**Hard numbers in this repo:** 53 modules across 4 samples, all engine-validated; 35 tests over the tooling.

### Honest limits (family DNA)

- **Ceiling = competent**; mastery needs years of real practice — said plainly.
- What AI can't grade (craft / physical / social real-world feedback) is **flagged** and handed off to
  upload / a human (e.g. `english-reading` is explicitly reading-only — no listening/speaking).
- Resources/tools decay (3–6 mo); the prereq graph + pedagogy don't (`update 私教 X` refreshes).

---

## ⚡ Install

```bash
# Claude Code
git clone https://github.com/swaylq/sijiao-skill.git ~/.claude/skills/sijiao-skill
```

Other hosts: `~/.openclaw/skills/` · `~/.codex/skills/` · `~/.hermit/skills/`. Install a **generated**
`{skill}-learn` into a host:

```bash
python3 tools/install.py install --host <claude|openclaw|codex|hermit> --source ./prototypes/rust-learn
```

---

## 🚀 Usage

```
> learn rust            # not installed → distills a rust-learn
> continue learning rust # already there → loads state, picks up where you left off
> quiz me on rust ownership
> update 私教 rust       # incremental refresh of decaying resources
```

It confirms five things (skill, current level, goal, weekly hours, locale), then runs **8 parallel
research routes** → distills via learning science → generates the 3-layer tutor directory.

---

## ⭐ Distilled samples

| Skill | Type | Modules | Ceiling | Path |
|-------|------|---------|---------|------|
| **Rust** | hard-tech (cognitive sweet zone) | 15 | competent | [rust-learn/](prototypes/rust-learn/) |
| **Linear algebra** | cognitive / math | 13 | competent | [linear-algebra-learn/](prototypes/linear-algebra-learn/) |
| **English reading** | language · cognitive | 12 | competent | [english-reading-learn/](prototypes/english-reading-learn/) |
| **Weight loss** | physical · behavioral (honest degradation · ⚠️ not medical advice) | 13 | competent | [weight-loss-learn/](prototypes/weight-loss-learn/) |

> Sweet-zone first (cognitive/knowledge skills), mirroring how master-skill started with LLM-agent-infra
> then expanded. Want a skill not on the list? Install it and say "learn XXX".

---

## 🔬 How it works

```
0  Clarify skill      ← narrow over-broad skills + detect level / goal / time / skill-type
1  8 parallel routes  ← map / canon / paths / practice / pitfalls / assessment / feedback / motivation
   ─ research gate
2  Distill framework  ← build prereq DAG → Dreyfus stages → fill modules → three-fold validation
   ─ distillation gate
3  Write the skill    ← curriculum_builder validates + renders; emits tutor SKILL.md + state schema
4  Quality check      ← 10-item learning rubric + validation gate (one-vote reject on critical fails)
5  Two-agent refine   ← tighten "activate = start teaching" + verify state is actually used
```

See [SKILL.md](SKILL.md); methodology in [references/pedagogy-framework.md](references/pedagogy-framework.md).

---

## 🧬 The three-generation family

- **[colleague-skill](https://github.com/titanwings/colleague-skill)** — distills what **one specific person** does.
- **[master-skill](https://github.com/swaylq/master-skill)** — distills **a whole industry's** cognition + workflow + tools (*gives you the fish*).
- **🎓 私教.skill** — distills **a path for you to learn it yourself** (*teaches you to fish*). The first to flip the goal from "agent does it for you" to "you can do it yourself."

---

## 📂 Project structure

```
sijiao-skill/
├── SKILL.md       # meta-skill: 8-route research → distill curriculum → generate tutor
├── prompts/       # intake + 8 research routes + source policy + synthesis + quality_check
├── references/    # pedagogy-framework (learning-science core) + skill-template (output template)
├── tools/         # curriculum_builder · learner_state · install · self_test (stdlib only)
├── prototypes/    # 4 end-to-end samples: rust / linear-algebra / english-reading / weight-loss (53 modules)
└── tests/         # 35 tests
```

---

## 📄 Roadmap

| Version | Content | Status |
|---------|---------|--------|
| v0.1 | meta-skill + tooling engine + **3 sweet-zone samples** + packaging | ✅ |
| v1.x | quality-check automation (quality_check.py / validation_gate.py) + source_verifier + update_skill.py | 🔲 |
| v2.x | website (try-it-live) + "great-teacher" sub-skills + cli/ drills + PyPI | 🔲 |

---

## 📜 License

MIT © [swaylq](https://github.com/swaylq) · [中文 README](README.md)
