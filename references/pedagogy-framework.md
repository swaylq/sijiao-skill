# Pedagogy Framework — how 学习.skill distills a learning path

This is to 学习.skill what `extraction-framework.md` is to master-skill: the
methodology Phase 2 applies. master-skill distills *how an expert thinks*; this
distills *how a beginner becomes able*. Phase 2 must obey every rule here.

## The thesis

A good `{skill}-learn` is **not a curriculum dump** (a list of books + topics). It is a
**runnable path from 0 to competent**:

- ordered by real prerequisite dependency, not table-of-contents convenience;
- staged to how skill is actually acquired (Dreyfus), not by topic size;
- every step has a *thing you do* with feedback (deliberate practice), not just a *thing you read*;
- it knows where beginners get stuck, and routes around it;
- it is honest about what it cannot teach without a human.

The five research-to-pedagogy mappings below turn the 8-route research notes into that path.

## 1. Dreyfus model → stage segmentation

Five stages: **novice → advanced beginner → competent → proficient → expert**.

| Stage | What the learner needs | Tutor move |
|-------|------------------------|-----------|
| Novice | context-free rules + recipes; minimal choice | "Do exactly this." Worked examples. |
| Advanced beginner | rules + situational cues; can't yet prioritize | Heuristics; start naming what matters. |
| Competent | can plan, handle the normal case end-to-end | Projects; let them choose, then critique. |
| Proficient / expert | intuition, pattern recognition | Mostly built by years of real practice — **not** by a tutor. |

**Rule:** a `{skill}-learn` curriculum credibly takes a learner to **competent**. Past that it
points outward (route 7 feedback loops, route 8 sustained practice) and says so in 诚实边界.
Do not pretend a skill makes someone an expert.

## 2. Bloom's taxonomy → objective leveling

**remember → understand → apply → analyze → evaluate → create.**

- Every module objective is tagged with its Bloom level (`objectives[].bloom`).
- Novice / advanced-beginner objectives cluster at remember/understand/apply; competent at
  analyze/evaluate; **create** is the milestone project.
- A module whose objectives never leave *understand* has no practice — flag it (see §3).

## 3. Deliberate practice → every module DOES something

(Ericsson) Skill grows from practice at the edge of ability with immediate feedback, not from exposure.

- **Every module has ≥1 assessable exercise** — a task whose output can be judged
  right / wrong / partial. "Read TRPL ch.4" is not practice; "fix these 5 borrow-checker
  errors" is.
- Exercises are pitched just above current ability; the learner-state `mastery` score gates difficulty.
- Feedback: the AI grades what it can; route 7 (community / mentor) for what it can't.
  No feedback loop → not deliberate practice → flag.

## 4. Retrieval practice + spacing → the learner-state queue

(Testing effect; Bjork) Retrieving from memory beats re-reading; spacing beats massing.

- Key facts / sub-skills enter `spaced_queue`; `learner_state.schedule_review` (SM-2-lite)
  brings them back on expanding intervals.
- Each session opens with **due retrievals before new material**.
- This is *why the tutor is stateful*: spacing is impossible without memory across sessions.

## 5. Desirable difficulties → worked-example → faded guidance

(Bjork; Sweller cognitive-load theory) Easy ≠ effective; some difficulty improves retention —
but novices overload on pure problem-solving.

Teaching move per content type:

- **new concept** → explain → **worked example** → faded steps → independent problem;
- **skill** → drill with feedback;
- **retention** → spaced retrieval.

Interleave related sub-skills once basics are solid (don't block-practice forever). Match
scaffolding to stage: heavy for novice, removed by competent.

## 6. Cognitive load → sequencing

- One new hard idea at a time for novices; chunk prerequisites first.
- The prereq DAG (route 1) is the load-management tool — topological order keeps new load minimal.

## 7. Transfer → milestone projects

Exercises in isolation don't transfer to real use. Each stage ends with a **milestone project**:
a realistic, integrative task. Its competence check is **behavioral** ("能独立做 X"), the bridge
from drills to doing.

## Three-fold module validation (Phase 2 gate)

Every module must pass — mirrors master-skill's triple validation:

1. **Prereq-justified** — its position in the DAG traces to route 1/2 evidence, not arbitrary order.
2. **Resource-backed** — its canonical resource was independently recommended (≥2 sources, route 2/3).
3. **Practice-assessable** — it has an exercise whose output can be graded (route 4).

A module failing any of these is downgraded or cut. **Empty > padded.**

## Honest limits (every generated skill states them)

- A tutor reaches ~**competent**; proficiency/expertise need years + real feedback. Say so.
- Resources / courses / tools decay (refresh every 3-6 months); the prereq DAG + pedagogy do
  not (protected by `<!-- SLOW_UPDATE -->`).
- Skills needing physical / real-world feedback: curriculum yes, grading → upload or human
  (route 7). Mark the module's `honest_limit`.
- Placement is self-report + a short diagnostic, **not** a certification.
