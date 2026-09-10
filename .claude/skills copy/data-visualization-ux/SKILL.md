---
name: data-visualization-ux
description: Design and implement data visualizations (charts, analytics UIs) for Khaos Machine using khaotik-ui's Svelte components. Covers chart type selection, the project's measured no-charting-dependency position, accessible table-based chart construction, and the catalog fixture every chart needs. Use when adding or changing a chart in khaotik-ui or khaos-app.
---

# Data Visualization in Khaos Machine

## The two rules that are specific to this project

Everything else in this skill is craft guidance. These two are decisions the
project already made, on evidence, and they are not yours to re-open casually.

### 1. Do not add a charting dependency

Charts here are hand-rolled. That was measured, not preferred. The same
`BarChart` was prototyped on LayerCake — the strongest of four candidates —
against the same real data and the same build:

```text
hand-rolled   70 lines   15,133 B gzipped
LayerCake     79 lines   32,599 B gzipped, +9 transitive d3 packages
```

The dependency produced *more* code, because LayerCake is headless: it hands
you scales and a measured container and you still draw every rectangle. The
full comparison, including why Unovis and LayerChart were ruled out, is on
khaotik-ui issue #28.

So: no Recharts, no D3, no LayerCake. If you believe a chart genuinely needs
one, the bar is a measurement on real data showing it pays for its bytes —
posted to the issue, not asserted in a PR description.

React is not used anywhere in this workspace and is an avoided technology per
`AGENTS.md`. Charts are Svelte.

### 2. A chart is a table first

`BarChart` renders a `<table>`, not an SVG. The data is tabular — labelled
categories with counts — so a screen reader gets the numbers with no extra
work, and it stays readable with no CSS at all. The bar is decoration over the
value beside it.

Reach for SVG only when the shape genuinely is not tabular (a continuous
series, a network). Then accessibility is your problem to solve explicitly.

## Where the code lives

| What | Path |
|------|------|
| Chart components | `khaotik-ui/components/svelte/` (`BarChart.svelte`, `PacingChart.svelte`) |
| Stories | `khaotik-ui/stories/charts/*.stories.svelte` |
| Tests | `khaotik-ui/apps/catalog/src/components/*.test.js` |
| Design tokens | `khaotik-ui/tokens/tokens.css` |
| Shared types | `khaotik-ui/components/svelte/lib/types.js` |

Read `BarChart.svelte` before writing a new chart. It is the worked example,
and its header comment carries the reasoning this skill summarizes.

## Conventions the existing components follow

- **Colour comes from `StatusTone`**, the seven-way scale in `lib/types.js`:
  `neutral | success | warning | danger | info | accent | skipped`. Do not
  introduce a parallel palette; use tokens from `tokens/tokens.css`.
- **Ordering is the caller's**, not the component's. Ranking is editorial —
  most-first, alphabetical, and the screenplay's own order are each correct
  somewhere. Take pre-ordered data.
- **Absence is not zero.** A non-finite value is *dropped*, not drawn as zero:
  an entity the engine did not measure is not an entity measured at zero.
  Provide an `emptyLabel` — a zeroed axis reads as *a measurement of nothing*
  rather than *an absence of measurement*.
- **Formatting belongs to the caller.** Default to counts; a percentage or a
  duration is passed in as a `format` function.

## The catalog

khaotik-ui retired Storybook in D61 — there are no `.stories.svelte` files, no
`@storybook/addon-svelte-csf`, and no `just storybook` recipe. The catalog is
the library's only component surface, and a chart reaches it through a fixture
in `khaotik-ui/apps/catalog/src/fixtures.js`. See the `BarChart` and
`PacingChart` entries there (`group: 'charts'`) as the reference.

The real-data rule outlived Storybook and is enforced in the same place. Use
**real measured data** in fixtures; the existing ones use distributions counted
from the committed scenes of BROKEN IN 4 PLACES — time-of-day is DAY 34 /
NIGHT 20, scene type is INT 41 / EXT 12 / INT-EXT 1. Invented data hides the
shape the component must survive: two bars, three bars, and a top-heavy
ranking of 27.

```bash
cd khaotik-ui && npm run check-coverage   # check-catalog fails if a chart has no fixture;
                                          # check-compile builds the catalog, which imports
                                          # every export — the job build-storybook used to do
```

## Choosing a chart type

`references/chart-selection-guide.md` is framework-agnostic guidance on picking
the right form for the data. For general chart-design craft — colour systems,
axes, legends, dashboards — prefer the `dataviz` skill, which is broader and
maintained outside this repo. This skill covers only what is specific to Khaos
Machine.

## Checklist

- [ ] No new charting dependency (or a measured case posted to the issue)
- [ ] Tabular data renders as a `<table>`
- [ ] Colour drawn from `StatusTone` and `tokens.css`, no parallel palette
- [ ] Non-finite values dropped, `emptyLabel` provided
- [ ] Caller supplies ordering and number formatting
- [ ] Fixture added to `khaotik-ui/apps/catalog/src/fixtures.js` using real measured data
- [ ] `cd khaotik-ui && npm run check-coverage` passes
