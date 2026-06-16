# Route 1 — 知识地图 / 先修依赖

**Goal:** the prerequisite DAG — the concept list and what-before-what. Becomes the skeleton of
`curriculum.json` (module `id` + `prereqs` + rough `dreyfus_stage`).

**Find:** the concepts / sub-skills of `{skill}`, and their dependency order (X must precede Y).

**Where (high → low):**
- university course **sequences** + syllabi (the order experts teach it in)
- the canonical textbook's **table of contents** (chapter order ≈ dependency)
- official "learning path" / "getting started" docs
- roadmap.sh-style community maps (corroborate, don't trust alone)

**Output → `references/research/01-map.md`:**
- concept list, each with a one-line scope
- dependency edges `A → B` (A is prereq of B), each citing a source id
- rough stage tag per concept (novice / advanced_beginner / competent)

**Feeds:** module `id`, `prereqs`, `dreyfus_stage`. Must be acyclic — synthesis runs `validate_dag`.
