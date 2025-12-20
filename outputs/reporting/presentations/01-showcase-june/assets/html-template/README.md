### Include assets

Here's how to include local files:

**File Structure:**

```
your-presentation/
├── slideshow.html
├── pics/
│   ├── slide1.svg
│   ├── slide2.svg
│   └── slide3.svg
└── gifs/
    ├── animation1.gif
    └── animation2.gif
```

**Format Recommendation:**
Use **SVG** for slides - it preserves your Inkscape vector graphics, gradients, and shadows perfectly while keeping file sizes small. PNG is your backup if SVG export has issues.

**Code Example:**

```html
<img
  src="gifs/animation2.gif"
  alt="Large GIF"
  class="slide-gif"
  style="bottom: 10%; left: 10%; max-width: 40%; max-height: 30%;"
/>

<div class="slide">
  <img
    src="gifs/grad-cut.gif"
    alt="grad decent"
    class="slide-gif"
    style="top: 20%; right: 10%;"
  />
</div>
```

**CSS Changes:**
Replace the placeholder gradient CSS with:

```css
.slide:nth-child(1) {
  background-image: url("pics/slide0.svg");
}

.slide:nth-child(1) {
  background-image: url("pics/slide1.svg");
}

.slide:nth-child(2) {
  background-image: url("pics/slide2.svg");
}

.slide:nth-child(3) {
  background-image: url("pics/slide3.svg");
}
```

**Inkscape Export Settings:**

- **For SVG**: File → Save As → Optimized SVG (removes unnecessary metadata)
- **For PNG**: File → Export → Set DPI to 300, ensure 4:3 aspect ratio

The CSS `background-size: cover` will handle scaling your images to fill the slide perfectly while maintaining aspect ratio.
