# Quality Check — learning rubric (Phase 4)

Mechanical checks the generated `{skill}-learn` must pass. Mirrors master-skill's 16-check
spirit, learning-flavored. Run before delivery; feed `validation_gate`.

## Checks

1. **Source primary-ratio** ≥ target; **0** blacklisted sources; every claim cites a source id.
2. **DAG valid** — `validate_dag` returns `[]`; every prereq edge traces to a route-1/3 source.
3. **Every module has ≥1 assessable exercise** (not "read X").
4. **Competence checks behavioral** — "能独立做 X", not "理解 X". Grep milestone checks for
   "理解了 / 知道" → flag.
5. **Bloom progression** — objectives carry bloom levels and rise across stages; no module stuck
   at "understand" with no practice.
6. **Dreyfus ceiling honest** — `meta.dreyfus_ceiling` ≤ competent; no "become an expert" claim.
7. **Resources real + specific** — URLs to specific pages, not homepages / search results.
8. **Honest limits present** — ≥3 concrete limits incl. decay + (if non-cognitive) the
   upload/线下 handoff.
9. **learner-state wired** — the tutor `SKILL.md` reads learner-state + calls `learner_state.py`
   functions.
10. **Locale consistent** — zh-CN talks Chinese-internet idiom / en uses the field's English;
    resources match the locale.

## Gate (validation_gate)

Weighted **accept / conditional_accept / reject**. Critical failures (a blacklisted source, a
cyclic DAG, a module with no exercise, an "expert" overclaim) = one-vote **reject**. Output the
specific fixes.
