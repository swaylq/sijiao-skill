# Synthesis — build the curriculum (Phase 2)

Apply `references/pedagogy-framework.md` to the 8-route notes. Output: `curriculum.json` +
`pedagogy.md` + honest limits.

## Steps

1. **DAG skeleton** (route 1): turn concepts + edges into modules with `id` / `prereqs` /
   `dreyfus_stage`. Run `tools/curriculum_builder.py:validate_dag` — fix every error
   (cycles, unknown prereqs, dup ids).
2. **Stage segmentation**: assign each module a Dreyfus stage; the curriculum ceiling is
   **competent** (pedagogy §1). Anything past competent → point outward, don't fake.
3. **Fill each module**:
   - `objectives[]` with Bloom levels (rise remember → … → create across stages; §2)
   - `resources[]` from route 2 (canon, ≥3-recommended, real URLs)
   - `exercises[]` from route 4 — **≥1 assessable per module** (§3)
   - `milestone` from route 6 — behavioral competence check
   - `honest_limit` from intake `skill_type` + route 7 (null for cognitive sweet-zone)
4. **Weave pitfalls** (route 5): attach "前方有坑" to the module where each bites.
5. **Three-fold validation** (pedagogy): drop/downgrade any module failing prereq-justified /
   resource-backed / practice-assessable.
6. **Derive the teaching protocol** → `pedagogy.md`: per content type, the move
   (explain → worked-example → faded / drill / spaced retrieval); pacing from route 8.
7. **Render**: `topo_sort` → `segment_by_dreyfus` → `render_curriculum_md` → `curriculum.md`.
8. **Honest limits**: ceiling stage; fastest-decaying modules; upload/线下 parts; not a cert.

## Gate

Stop and let the user review the curriculum **skeleton** (modules + order) before filling
everything — don't pour effort into a wrong DAG.
