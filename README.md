# The Business Plan Navigator

A static teaching site for EU Business School Munich students taking the **Master's capstone
as a business plan** (Level 7). It covers the full arc of that route in three parts:

| Part | Content | Page |
|---|---|---|
| **I** | The Proposal — EUBS Business Plan Proposal / Registration Form, section by section | `part1.html` |
| **II** | The Final Business Plan — seven rubric chapters with weights, frameworks and KPI inventories | `part2.html` |
| **III** | The Jury Defense — thumbnail storyboard (Meier) and message strategy (Bostelaar) | `part3.html` |

Supporting galleries: `frameworks.html` (58 frameworks, filterable, click-through detail),
`authors.html` (43 thinkers with anchor references), `references.html` (57 Harvard entries).

House style, palette and typography match
[MARTI301](https://drhaas-eubs.github.io/marti301/).

**Scope.** Every word count, rubric weight and checklist item on these pages applies to the
Master's business plan route alone. The Master's final project route, the MBA dissertation
and the Bachelor dissertation are separate awards with their own criteria, and the site says
so explicitly on the landing page and in the footer of every page. The framework, author and
reference galleries are level-neutral and can be reused across all routes unchanged.

---

## Deploying to GitHub Pages

1. Create a new repository under the `drhaas-eubs` account — for example `business-plan-navigator`.
2. Upload the contents of this folder to the repository root (drag and drop works in the
   GitHub web interface; `index.html` must sit at the top level, not inside a subfolder).
3. Go to **Settings → Pages**, set **Source** to *Deploy from a branch*, branch `main`,
   folder `/ (root)`, and save.
4. The site appears at `https://drhaas-eubs.github.io/business-plan-navigator/` within about a minute.

To publish it as a section of the existing MARTI301 site instead, copy the seven HTML files
and the `assets/` folder into a `business-plan/` subfolder of that repository. All internal links
are relative, so nothing needs to change.

---

## Editing the content

All content lives in `build/data.py`. The HTML is generated, so edits made directly to the
`.html` files will be overwritten on the next build.

```bash
python3 build/build.py
```

- **`REFERENCES`** — Harvard entries, keyed. Every framework and KPI points at a key here,
  so the reference list, the framework modals and the author cards all stay in sync
  automatically.
- **`FRAMEWORKS`** — each entry has `part` (`P1`/`P2`/`P3`), `chap`, `name`, `author`,
  `use` (why it is required) and `how` (how to apply it correctly).
- **`AUTHORS`** — name, dates, contribution, associated frameworks, reference key.
- **`KPIS`** — indicator, unit of measure, direction (`up`/`down`/`eq`), definition.

The chapter narratives, the thumbnail storyboard (`THUMBS`) and the question anticipation
matrix (`QA`) live in `build/build.py`.

The build prints a warning for any framework named in a chapter that has no matching entry
in `FRAMEWORKS`, which catches typos before they reach students.

---

## Content protection

Selection, copying, right-click, drag, print and the common developer-tool shortcuts are
disabled across all seven pages. An attempted copy shows a short notice rather than failing
silently, and printing produces a copyright notice instead of the content.

Implementation: `assets/js/protect.js` plus the protection block at the foot of
`assets/css/site.css`. Search boxes remain fully interactive, so the galleries still filter
normally.

**What this does and does not achieve.** It is a deterrent against casual copy-and-paste,
which is the realistic student behaviour. It is not — and no browser-side measure can be —
genuine protection. Anyone who disables JavaScript, opens the page source, uses browser
reader mode, or photographs the screen will still obtain the text. Treat it as a clear
signal of expectation rather than as a technical guarantee, and keep the copyright notice in
the footer, since that is what carries any actual weight.

**Optional exception.** If reference entries should remain copyable so that students can
paste Harvard citations into their own reference lists, add this rule to the end of
`assets/css/site.css`:

```css
.ref-item{-webkit-user-select:text!important;user-select:text!important}
.ref-item::selection{background:#00B388;color:#fff}
```

and add `if (e.target.closest(".ref-item")) return;` as the first line of the `copy` and
`cut` handlers in `assets/js/protect.js`.

---

## Notes on sources

Rubric weightings, word counts, slide requirements and checklist items are drawn from the
EUBS *Master Programme Capstone Guidelines*, the *Capstone Style Guide*, the *Checklist for
Proposal Forms* and the *BP/FP Defense Guidelines*. Students should confirm the applicable
academic year with their promoter, since weightings and word limits are revised between
cycles.

J.D. Meier's *Thumbnail Thinking* and Kurt Bostelaar's message-design work are practitioner
methods rather than peer-reviewed frameworks. They are cited as such, and the underlying
presentation principles are additionally anchored to Alley (2013), Duarte (2010),
Mayer (2009) and Minto (2009) so that the Use of References criterion is satisfied by
academic sources.

---

© 2026 Prof. Dr. Hildegard Haas · EU Business School Munich
