# Source ID + Trust Policy

Shared across all 8 routes. Every source gets an id and a trust class; every claim in the
research notes cites ≥1 id.

## ID scheme

`T0N-S0kk` — `T` = route (track) number 01-08, `S` = source within that route.
e.g. `T02-S003` = route 2's third source. Stable across the skill's life.

## Trust classes (learning-specific)

- **primary** — official docs / the canonical book or course itself / a named practitioner's
  own long-form account of learning or teaching it / a university syllabus / the actual problem set.
- **secondary** — reputable third-party explainer, long-form media, a course review by a known practitioner.
- **reject** — SEO listicles ("10 ways to learn X fast"), content farms, auto-generated
  roadmaps, 百度百科, low-effort 知乎/CSDN/公众号 reposts (unless the author's original),
  affiliate "best course" pages.

## Cross-validation

- A resource enters the curriculum **canon** only with **≥3 independent** recommendations (route 2/3).
- A path claim ("learn A before B") needs **≥2** independent supports or it drops to a soft suggestion.

## Date stamping

Every source dated. Tools / courses / resources older than 18 months → flag for the decay table.
Foundational canon (math, a language's grammar) decays slowly; tooling / ecosystem decays fast.

## Thin coverage → deep mode

If a route returns < 5 usable primary sources, switch to deep mode: ask the user for insider
material + pull from adjacent authoritative sources (professional bodies, university courses,
official curricula). **Never pad with rejected sources.**
