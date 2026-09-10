# Accessibility in Information Architecture

WCAG navigation requirements and inclusive IA design patterns.

---

## Why Accessibility Matters for IA

> "By leaving accessibility out of IA (and IA out of accessibility), we are building deeply inaccessible, exclusionary structures." - Sarah R. Barrett

Information Architecture decisions directly impact:
- Screen reader navigation
- Keyboard-only users
- Cognitive load for all users
- Legal compliance (ADA, EAA)

---

## WCAG 2.4: Navigable

The core WCAG guideline for Information Architecture.

### Success Criteria Reference

| Criterion | Level | Requirement | IA Impact |
|-----------|-------|-------------|-----------|
| **2.4.1 Bypass Blocks** | A | Skip navigation for repeated content | Skip links implementation |
| **2.4.2 Page Titled** | A | Descriptive page titles | Title strategy in sitemap |
| **2.4.3 Focus Order** | A | Logical, meaningful tab order | Navigation sequence |
| **2.4.4 Link Purpose** | A | Link text describes destination | Labeling system |
| **2.4.5 Multiple Ways** | AA | Multiple ways to locate pages | Navigation + search + sitemap |
| **2.4.6 Headings & Labels** | AA | Descriptive headings and labels | Heading hierarchy |
| **2.4.7 Focus Visible** | AA | Visible keyboard focus | Navigation styling |
| **3.2.3 Consistent Navigation** | AA | Same relative order | Global nav consistency |
| **3.2.4 Consistent Identification** | AA | Same functionality labeled same | Labeling consistency |

---

## Accessible Navigation Patterns

### Semantic Structure

```html
<!-- Correct navigation structure -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/products">Products</a></li>
    <li><a href="/services">Services</a></li>
    <li>
      <a href="/about" aria-expanded="false" aria-haspopup="true">About</a>
      <ul>
        <li><a href="/about/team">Our Team</a></li>
        <li><a href="/about/history">History</a></li>
      </ul>
    </li>
  </ul>
</nav>
```

### Required Elements

| Element | Purpose | Implementation |
|---------|---------|----------------|
| `<nav>` | Navigation landmark | Wrap all nav regions |
| `aria-label` | Distinguish nav regions | "Main", "Footer", "Breadcrumb" |
| `<ul>/<li>` | List structure | Screen readers announce count |
| `aria-current="page"` | Current page indicator | On active link |
| `aria-expanded` | Submenu state | On parent of dropdown |

### Skip Navigation

```html
<!-- First element in body -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<!-- CSS: visually hidden until focused -->
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  left: 10px;
  top: 10px;
}
```

---

## Heading Hierarchy

### Correct Structure

```
H1: Page Title (one per page)
├── H2: Main Section 1
│   ├── H3: Subsection 1.1
│   └── H3: Subsection 1.2
├── H2: Main Section 2
│   ├── H3: Subsection 2.1
│   │   └── H4: Detail 2.1.1
│   └── H3: Subsection 2.2
└── H2: Main Section 3
```

### Heading Rules

- [ ] Exactly one `<h1>` per page
- [ ] Don't skip levels (H1 -> H3)
- [ ] Headings reflect document outline
- [ ] Don't use headings for styling only
- [ ] Navigation sections get `<nav>`, not heading

---

## Link Text Guidelines

### Good vs. Bad Examples

| Bad | Good | Why |
|-----|------|-----|
| "Click here" | "Download the annual report (PDF)" | Describes destination |
| "Learn more" | "Learn more about our pricing plans" | Context included |
| "Read more" | "Read the full case study" | Specific content described |
| Image with no alt | Image with alt="Company logo, go to homepage" | Purpose clear |

### Link Text Checklist

- [ ] Link text makes sense out of context
- [ ] Avoid "click here", "read more", "learn more" alone
- [ ] Include file type for downloads (PDF, 2MB)
- [ ] Indicate external links (opens in new tab)
- [ ] Use aria-label for icon-only links

---

## Multiple Ways to Content (2.4.5)

Provide at least two ways to find any page:

| Method | Implementation | Best For |
|--------|----------------|----------|
| **Navigation** | Hierarchical menus | Browsing, exploration |
| **Search** | Site-wide search | Known-item finding |
| **Sitemap** | HTML sitemap page | Overview, edge content |
| **Related links** | Contextual navigation | Discovery |
| **Breadcrumbs** | Location indicator | Deep hierarchies |
| **A-Z Index** | Alphabetical listing | Large content sets |

### Minimum Requirement

For WCAG AA compliance, provide:
1. Primary navigation (global/local)
2. At least one of: search, sitemap, or site index

---

## Accessibility by Disability Type

### Visual Impairments (Blind)

**Barriers**:
- Complex navigation without structure
- Visual-only hierarchy cues
- Image-based navigation
- Missing alt text

**Solutions**:
- Semantic HTML (`<nav>`, `<ul>`, headings)
- ARIA landmarks and labels
- Skip links
- Descriptive link text
- Logical heading hierarchy

### Visual Impairments (Low Vision)

**Barriers**:
- Small click targets
- Poor color contrast
- Hover-only information

**Solutions**:
- Minimum 44x44px touch targets
- Focus indicators (visible)
- Information not conveyed by color alone
- Keyboard-accessible menus

### Motor Impairments

**Barriers**:
- Mouse-only navigation
- Complex gestures
- Timed interactions

**Solutions**:
- Full keyboard navigation
- Logical tab order
- Skip links
- Avoid keyboard traps
- No time limits on navigation

### Cognitive Impairments

**Barriers**:
- Complex hierarchies
- Inconsistent patterns
- Information overload
- Ambiguous labels

**Solutions**:
- Simple, shallow navigation
- Consistent layout across pages
- Clear, specific labels
- Progressive disclosure
- Familiar patterns

---

## ARIA Landmarks

```html
<body>
  <header role="banner">
    <nav role="navigation" aria-label="Main">...</nav>
  </header>

  <main role="main" id="main-content">
    <nav role="navigation" aria-label="Breadcrumb">...</nav>
    <article role="article">...</article>
  </main>

  <aside role="complementary">
    <nav role="navigation" aria-label="Related">...</nav>
  </aside>

  <footer role="contentinfo">
    <nav role="navigation" aria-label="Footer">...</nav>
  </footer>
</body>
```

### Landmark Summary

| Landmark | Element | Purpose |
|----------|---------|---------|
| `banner` | `<header>` | Site header (once per page) |
| `navigation` | `<nav>` | Navigation regions |
| `main` | `<main>` | Main content (once per page) |
| `complementary` | `<aside>` | Supporting content |
| `contentinfo` | `<footer>` | Site footer (once per page) |
| `search` | `<form role="search">` | Search functionality |

---

## Testing Checklist

### Automated Testing

- [ ] Run WAVE or axe on all page templates
- [ ] Check heading hierarchy tool
- [ ] Validate landmarks
- [ ] Test color contrast

### Manual Testing

- [ ] Navigate with keyboard only (Tab, Enter, Arrows)
- [ ] Test with screen reader (NVDA, VoiceOver)
- [ ] Check focus visibility
- [ ] Verify skip links work
- [ ] Test at 200% zoom

### User Testing

- [ ] Include users with disabilities
- [ ] Test task completion rates
- [ ] Gather qualitative feedback
- [ ] Iterate based on findings

---

## Implementation Checklist

### Navigation

- [ ] `<nav>` elements for all navigation regions
- [ ] Unique `aria-label` for each nav region
- [ ] `<ul>/<li>` structure for menu items
- [ ] `aria-current="page"` on current page link
- [ ] `aria-expanded` on parent items with submenus
- [ ] Keyboard accessible (Tab, Enter, Escape)

### Page Structure

- [ ] Skip link as first focusable element
- [ ] Single `<h1>` matching page title
- [ ] Logical heading hierarchy (no skipped levels)
- [ ] Landmarks for major page regions
- [ ] `<main>` with id for skip link target

### Links

- [ ] Descriptive link text (no "click here")
- [ ] Visible focus indicator
- [ ] File type/size for downloads
- [ ] New window indicated (`aria-label` or visual)

### Consistency

- [ ] Same navigation order across pages
- [ ] Same labels for same functions
- [ ] Predictable behavior patterns
- [ ] Consistent page title format

---

## Resources

- [W3C WCAG 2.4 Navigable](https://www.w3.org/WAI/WCAG22/Understanding/navigable.html)
- [W3C Web Accessibility Tutorials: Menus](https://www.w3.org/WAI/tutorials/menus/)
- [WebAIM: Skip Navigation Links](https://webaim.org/techniques/skipnav/)
- [Deque: Navigation Accessibility](https://www.deque.com/blog/accessible-navigation/)
