# Data Visualization Principles & Best Practices

## Core Principles

### 1. Clarity Over Aesthetics
- Choose clarity and accuracy first, beauty second
- Remove chart junk (unnecessary decorations, 3D effects, gridlines)
- Use the simplest chart type that accurately represents the data

### 2. Choose the Right Chart Type
- Bar charts for comparisons across categories
- Line charts for trends over time
- Pie/donut charts **sparingly** (humans are poor at comparing angles)
- Scatter plots for relationships and distribution
- Heatmaps for large matrices of data
- See chart-selection-guide.md for comprehensive decision tree

### 3. Data Ink Ratio
- Maximize the ratio of data ink to total ink in the visualization
- Remove redundant labels, decorations, backgrounds
- Every pixel should represent data

### 4. Hierarchy & Focus
- Draw attention to the most important insights first
- Use color, size, and position to guide the eye
- Secondary data should fade into the background
- Enable progressive disclosure for complex dashboards

### 5. Consistency
- Use consistent scales across related visualizations
- Apply consistent color coding (red = bad/error, green = good/success)
- Maintain consistent typography and spacing from the khaotik-ui design system

## Accessibility in Data Visualization

### Color Considerations
- **Never** rely on color alone to convey information (8% of males, 0.5% of females are colorblind)
- Use patterns, textures, or labels in addition to color
- Provide sufficient contrast (WCAG AA: 4.5:1 for text, 3:1 for graphics)
- Test with colorblind simulators (Sim Daltonism, Color Oracle)

### Interactive Elements
- All interactive elements must be keyboard accessible (Tab, Enter, Arrow keys)
- Provide ARIA labels for screen readers
- Ensure focus indicators are visible
- Support all standard gestures for touch devices

### Responsive Design
- Charts must work on mobile, tablet, and desktop
- Consider legend placement on small screens
- Use simplified views for mobile (fewer data points, larger fonts)
- Test with actual devices, not just browser resize

### Readability
- Font size minimum 12px on desktop, 14px on mobile
- Use sans-serif fonts (khaotik-ui default)
- Adequate line height (1.5x minimum) for labels
- High contrast between text and background

## Performance Considerations

### Data Limits
- **Limit DOM nodes**: Render max 500-1000 data points in DOM (virtualize beyond)
- **Aggregate before reaching for Canvas**: this project has no charting or
  rendering dependency by measured decision (khaotik-ui #28). At Khaos Machine
  data volumes — scene counts, character appearances — summarising beats
  rendering 10k points. Adding Canvas or WebGL needs the same evidence bar as
  adding a charting library.
- **Aggregate data**: Show summary statistics when data volume is high
- **Pagination or filtering**: Large datasets should offer ways to scope the view

### Rendering Strategy
- **SVG**: Best for <1000 interactive data points, good accessibility
- **Canvas**: Best for 1000+ points, limited interactivity
- **WebGL**: Best for massive datasets (100k+) with performance needs

### Lazy Loading
- Defer chart rendering until visible (Intersection Observer)
- Avoid rendering charts in hidden tabs or collapsed sections
- Load data incrementally as user scrolls

## Dashboard Patterns

### Layout
- **Grid-based**: Use consistent grid (khaotik-ui spacing tokens)
- **Visual hierarchy**: Most important chart top-left (Z-pattern)
- **Whitespace**: Adequate breathing room (24px minimum gutters)
- **Responsive grid**: 1 column mobile, 2-3 desktop

### Interactions
- **Brushing & linking**: Selecting data in one chart filters related charts
- **Tooltips**: Show detailed data on hover (not on click for desktop)
- **Drill-down**: Click to explore deeper levels of data
- **Filters**: Always show what filters are applied
- **Zoom/pan**: For large temporal or spatial data

### Updates & Animations
- Animate transitions when data changes (smooth, purposeful)
- Duration: 250-500ms for most animations
- Use easing functions (ease-out preferred)
- Disable animations option for motion sensitivity

## Khaos Machine Specifics

### Design System Integration
- Use colour from the seven-way `StatusTone` scale in
  `khaotik-ui/components/svelte/lib/types.js`, and tokens from
  `khaotik-ui/tokens/tokens.css` — do not introduce a parallel palette
- Apply typography, spacing and radius tokens from the same source

### Component Architecture
- Hand-roll the chart in Svelte; do not wrap a third-party charting library
  (see SKILL.md — this was measured, not preferred)
- Render tabular data as a `<table>`, so screen readers get the numbers for
  free and the chart survives with no CSS
- Support light/dark via tokens, not per-component colour logic
- Document in the component's own header comment and its catalog fixture

## Common Pitfalls to Avoid

❌ **Misleading axis scaling** - Always start at zero (except for specialized cases)
❌ **Too many colors** - Limit palette to 5-7 colors per chart
❌ **Animated entries** - Use sparingly; can distract from data
❌ **Dual-axis charts** - Hard to compare; use faceted charts instead
❌ **3D effects** - Distorts perception; avoid unless specifically needed
❌ **Missing context** - Always label axes, include units, add data source
❌ **Inconsistent sorting** - Sort meaningfully (by value, time, or alphabetical)
❌ **Truncated axes** - Can exaggerate differences; use full range

## Resources

- Edward Tufte - *The Visual Display of Quantitative Information*
- Storytelling with Data - Cole Nussbaumer Knaflic
- WCAG 2.1 Guidelines - https://www.w3.org/WAI/WCAG21/quickref/
- Colorblind Web Design - https://www.colorblindwebdesign.com/
