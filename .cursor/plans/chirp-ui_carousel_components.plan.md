---
name: ""
overview: ""
todos: []
isProject: false
---

# chirp-ui Carousel Component Family

## Goal

Carousels for horizontal swipe/scroll content: compact (card strips, thumbnails) and page-size (hero slides). Zero-JS core using CSS scroll-snap; native touch swipe; anchor links for navigation.

---

## Approach: CSS Scroll-Snap

- `overflow-x: auto` + `scroll-snap-type: x mandatory` on track
- Each slide: `scroll-snap-align: start` (compact) or `center` (page)
- Touch swipe = native horizontal scroll (no JS)
- Dots: `<a href="#slide-N">` — zero-JS jump to slide
- Prev/next: Requires knowing "current" slide → needs minimal JS (see below)

---

## Components

### 1. carousel (main)

**File**: [chirpui/carousel.html](chirp-ui/src/chirp_ui/templates/chirpui/carousel.html) (new)

**API**:

```jinja
carousel(variant="compact|page", slide_count=0, show_dots=false, show_arrows=false, cls="")
```

**Params**:

- `variant`: `compact` — multiple slides visible, smaller; `page` — one slide per viewport, full-width
- `slide_count`: Required when `show_dots` or `show_arrows` true. Number of slides (ids 1..N).
- `show_dots`: Render dot links to #slide-1, #slide-2, etc. Zero-JS.
- `show_arrows`: Render prev/next. Zero-JS: arrows link to #slide-1 (prev) and #slide-{slide_count} (next) — not ideal. **Recommendation**: Phase 1 omit arrows; add in Phase 2 with optional script.

**Structure**:

```html
<div class="chirpui-carousel chirpui-carousel--{variant}">
  <div class="chirpui-carousel__track" role="region" aria-label="Carousel">
    {% slot %}  <!-- carousel_slide() calls -->
  </div>
  {% if show_dots and slide_count %}
  <nav class="chirpui-carousel__dots" aria-label="Slide navigation">
    {% for i in range(1, slide_count + 1) %}
    <a href="#slide-{{ i }}" class="chirpui-carousel__dot" aria-label="Slide {{ i }}"></a>
    {% end %}
  </nav>
  {% end %}
</div>
```

---

### 2. carousel_slide

**File**: Same [chirpui/carousel.html](chirp-ui/src/chirp_ui/templates/chirpui/carousel.html)

**API**:

```jinja
carousel_slide(id, cls="")
```

**Structure**:

```html
<div id="slide-{{ id }}" class="chirpui-carousel__slide" role="group" aria-roledescription="slide">
  {% slot %}
</div>
```

**id**: Required, unique. Use 1, 2, 3... for anchor targets. Must match `slide_count` ordering.

---

## Variant Styling

### compact

- Track: `display: flex`, `gap`, `overflow-x: auto`, `scroll-snap-type: x mandatory`
- Slide: `scroll-snap-align: start`, `scroll-snap-stop: always`, `flex: 0 0 X` (e.g. min-width: 280px or 50%)
- Multiple slides visible; horizontal scroll

### page

- Track: same scroll-snap
- Slide: `scroll-snap-align: center`, `flex: 0 0 100%` (full viewport width)
- One slide per viewport; hero-style

---

## CSS

```css
.chirpui-carousel__track {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

.chirpui-carousel__slide {
  scroll-snap-align: start;  /* or center for page */
  scroll-snap-stop: always;
  flex: 0 0 auto;
}

.chirpui-carousel--compact .chirpui-carousel__slide {
  min-width: 280px;  /* or similar */
}

.chirpui-carousel--page .chirpui-carousel__slide {
  min-width: 100%;
  scroll-snap-align: center;
}
```

---

## Prev/Next Arrows (Phase 2)

Zero-JS prev/next that "go to adjacent slide" requires knowing current slide. Options:

1. **Omit in Phase 1** — Dots + swipe sufficient. Document manual `<a href="#slide-2">Next</a>` if needed.
2. **Optional script** — Ship `chirpui-carousel.js` (~30 lines): IntersectionObserver detects visible slide, updates prev/next hrefs. Add `data-carousel-nav` to enable.
3. **Per-slide nav** — Each slide contains "Next →" linking to next slide. Zero-JS. Nav scrolls with slide. Works for page variant.

**Recommendation**: Phase 1 = track + dots. Phase 2 = per-slide "Next" link (user adds `carousel_slide(2)` with slot containing `<a href="#slide-3">Next</a>`) — or we add `carousel_next(target_id)` helper. Simpler: document the pattern; no built-in arrows in v1.

---

## Deliverables


| Item     | File                             |
| -------- | -------------------------------- |
| Template | chirpui/carousel.html            |
| CSS      | chirpui.css                      |
| Tests    | test_components.py               |
| Showcase | layout.html or new carousel.html |


---

## Showcase

- **Compact**: 4–5 card slides, show_dots=true
- **Page**: 3 hero-style slides (title + CTA), full-width

---

## Accessibility

- `role="region"` + `aria-label="Carousel"` on track
- `role="group"` + `aria-roledescription="slide"` on each slide
- Dots: `aria-label="Slide N"`
- `scroll-snap` can affect keyboard nav; ensure focus management if needed (Phase 2)

---

## Risks

- **scroll-behavior: smooth** — Not supported in all browsers; degrades to instant.
- **Dots "active" state** — Without JS, we can't highlight current slide. Use `:target` on slides: when URL is #slide-2, we could style the second dot. But :target applies to the slide, not the dot. We'd need `#slide-2:target` to affect a sibling dot — possible with `:has()` on parent: `.chirpui-carousel:has(#slide-2:target) .chirpui-carousel__dot:nth-child(2)` could get active style. The dot is not a child of the slide; we need the carousel to be the parent of both track and dots. So `.chirpui-carousel:has(#slide-2:target) .chirpui-carousel__dots a:nth-child(2)` — the second dot. When #slide-2 is :target, that selector matches. So we CAN do active dot with pure CSS! Add `.chirpui-carousel__dot:target` — no, the dot isn't the target, the slide is. So we need the carousel to have structure: track (with slides) + dots. When we navigate to #slide-2, the slide with id="slide-2" gets :target. The carousel is an ancestor. So `.chirpui-carousel:has(#slide-2:target) .chirpui-carousel__dot[href="#slide-2"]` — we can add a class to the dot when its href matches the current target. But we can't do that with CSS alone — we'd need the dot's href to match. The selector `a[href="#slide-2"]` matches the dot. And when the document has #slide-2 in the URL, we want that dot to be active. The issue: `:target` is on the element with that id. So `#slide-2:target` is true. The carousel contains #slide-2. So `.chirpui-carousel:has(#slide-2:target)` is true. And we want to style the dot with `href="#slide-2"`. So `.chirpui-carousel:has(#slide-2:target) .chirpui-carousel__dot[href="#slide-2"]` — that works! But we need one rule per slide. Or we could use a more generic approach... Actually we need N rules for N slides. That's fine — we can generate them or use a different approach. Simpler: don't style "active" dot in v1. Dots are for navigation; active state is nice-to-have.

