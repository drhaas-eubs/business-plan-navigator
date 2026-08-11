# -*- coding: utf-8 -*-
"""EUBS Capstone Navigator — static site generator."""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import REFERENCES, FRAMEWORKS, AUTHORS, KPIS

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PART_COLOR = {"P1": "var(--p1)", "P2": "var(--p2)", "P3": "var(--p3)"}
PART_NAME = {"P1": "Part I · Proposal", "P2": "Part II · Business Plan", "P3": "Part III · Defense"}
ARROW = {"up": '<span class="arrow-up">▲</span>', "down": '<span class="arrow-dn">▼</span>',
         "eq": '<span class="arrow-eq">◆</span>'}

# ───────────────────────── shared chrome ─────────────────────────
NAV = [("index.html", "Overview"), ("part1.html", "Part I · Proposal"),
       ("part2.html", "Part II · Business Plan"), ("part3.html", "Part III · Defense"),
       ("frameworks.html", "Framework Gallery"), ("authors.html", "Authors Gallery"),
       ("references.html", "Reference List")]


def head(title, sub):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{html.escape(sub)}">
<title>{html.escape(title)}</title>
<meta name="robots" content="noarchive, nosnippet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body oncontextmenu="return false" ondragstart="return false">
"""


def topnav(active):
    links = "".join(
        f'<a href="{h}" class="{"active" if h == active else ""}">{html.escape(t)}</a>'
        for h, t in NAV)
    return f'<nav class="topnav"><div class="topnav-in">{links}</div></nav>\n'


def hero(pre, h1, sub, stats=None):
    s = ""
    if stats:
        s = '<div class="stats">' + "".join(
            f'<div class="stat"><div class="n">{n}</div><div class="l">{html.escape(l)}</div></div>'
            for n, l in stats) + "</div>"
    return (f'<header class="hero"><div class="hero-pre">{html.escape(pre)}</div>'
            f'<h1>{h1}</h1><div class="sub">{html.escape(sub)}</div>'
            f'<div class="copy">© 2026 Prof. Dr. Hildegard Haas · EU Business School Munich</div>{s}</header>\n')


FOOT = """<footer>
<strong>The Business Plan Navigator</strong> · EU Business School Munich<br>
Master's Level 7 · Business Plan Route · Part I Proposal · Part II Business Plan · Part III Jury Defense<br>
<span style="color:#94A3B8">Does not apply to the Master's final project route, the MBA dissertation or the Bachelor dissertation.</span><br>
© 2026 Prof. Dr. Hildegard Haas · EU Business School Munich<br>
Structured with J.D. Meier's <strong>Thumbnail Thinking</strong> (2025) and Kurt Bostelaar's <strong>Message Strategy</strong> (2023)<br>
Companion site: <a href="https://drhaas-eubs.github.io/marti301/">MARTI301 — AI in Investment &amp; Competitiveness</a><br>
<span style="display:inline-block;margin-top:.7rem;font-size:.7rem;color:#475569">Protected teaching material. Selection, copying, printing and download are disabled.<br>
Students are expected to work from the frameworks and cite the sources given, not to reproduce this page.</span>
</footer>
<script src="assets/js/protect.js"></script>
</body>
</html>"""

MODAL = """
<div class="modal" id="mdl" onclick="if(event.target.id==='mdl')closeM()">
  <div class="modal-in">
    <span class="modal-close" onclick="closeM()">×</span>
    <h3 id="m-name"></h3>
    <div class="m-auth" id="m-auth"></div>
    <div class="m-lab">Why it is required</div><p id="m-use"></p>
    <div class="m-lab">How to apply it correctly</div><p id="m-how"></p>
    <div class="m-lab">Where it belongs</div><p id="m-where"></p>
    <div class="m-lab">Harvard reference</div><p id="m-ref" style="font-size:.78rem"></p>
  </div>
</div>
<script>
const FW = %s;
function openM(i){const f=FW[i];
 document.getElementById('m-name').textContent=f.name;
 document.getElementById('m-auth').textContent=f.author;
 document.getElementById('m-use').textContent=f.use;
 document.getElementById('m-how').textContent=f.how;
 document.getElementById('m-where').textContent=f.partname+'  ·  '+f.chap;
 document.getElementById('m-ref').innerHTML=f.ref;
 document.getElementById('mdl').classList.add('on');}
function closeM(){document.getElementById('mdl').classList.remove('on');}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeM();});
</script>
"""


def fw_json():
    out = []
    for f in FRAMEWORKS:
        out.append(dict(name=f["name"], author=f["author"], use=f["use"], how=f["how"],
                        chap=f["chap"], part=f["part"], partname=PART_NAME[f["part"]],
                        ref=REFERENCES.get(f["ref"], "")))
    return json.dumps(out, ensure_ascii=False)


def fw_index(name):
    for i, f in enumerate(FRAMEWORKS):
        if f["name"] == name:
            return i
    return -1


def pills(names):
    out = []
    missing = []
    for n in names:
        raw = n.replace("&amp;", "&").replace("&nbsp;", " ")
        i = fw_index(raw)
        disp = html.escape(raw)
        if i >= 0:
            out.append(f'<span class="pill" onclick="openM({i})">{disp}</span>')
        else:
            missing.append(raw)
            out.append(f'<span class="pill">{disp}</span>')
    if missing:
        print("    ! unlinked pills:", missing)
    return '<div class="pill-row">' + "".join(out) + "</div>"


def kpi_table(key):
    rows = ""
    for name, unit, direc, note, ref in KPIS[key]:
        rows += (f"<tr><td><strong>{html.escape(name)}</strong></td>"
                 f"<td>{html.escape(unit)}</td><td>{ARROW[direc]}</td>"
                 f"<td>{html.escape(note)}</td></tr>")
    return ('<table class="kpi-table"><thead><tr><th>Indicator</th><th>Unit of measure</th>'
            '<th>Direction</th><th>Definition and rubric note</th></tr></thead><tbody>'
            + rows + "</tbody></table>")


def chapter(num, title, weight, lede, fw_names, kpi_key=None, refs=None, extra=""):
    h = f'<div class="chapter" id="ch{num}"><h3>{num}. {html.escape(title)}</h3>'
    if weight:
        h += f'<div class="weight">{weight}</div>'
    h += f'<p class="lede">{lede}</p>'
    if fw_names:
        h += '<div class="subhead">Required frameworks, tools and models</div>' + pills(fw_names)
    if kpi_key:
        h += '<div class="subhead">Key performance indicators</div>' + kpi_table(kpi_key)
    h += extra
    if refs:
        cites = " ".join(REFERENCES[r] for r in refs)
        h += f'<div class="subhead">Anchor sources (Harvard)</div><div class="cite">{cites}</div>'
    return h + "</div>"


# ═════════════════════════════ INDEX ═════════════════════════════
def build_index():
    n_fw, n_au, n_kpi = len(FRAMEWORKS), len(AUTHORS), sum(len(v) for v in KPIS.values())
    parts = [
        ("P1", "I", "The Proposal", "EUBS Registration Form · 1,500–2,000 words · min. 10 citations",
         [("part1.html", "Proposal Navigator", "Section-by-section requirements, frameworks, KPIs, Harvard sources", "GUIDE"),
          ("frameworks.html#P1", "Proposal Frameworks", "The 16 tools that must appear before promoter sign-off", "GALLERY"),
          ("references.html", "Harvard Reference List", "Every source used across the three parts, alphabetical", "REFS")]),
        ("P2", "II", "The Final Business Plan", "10,000–12,000 words · 75% written content · 25% written communication",
         [("part2.html", "Business Plan Navigator", "Seven rubric chapters with weights, frameworks and KPI inventories", "GUIDE"),
          ("part2.html#chain", "The Logical Chain", "PESTEL → Competitors → SWOT → TOWS → Strategy → Mix → Operations → Financials", "LOGIC"),
          ("frameworks.html#P2", "Business Plan Frameworks", "The analytical apparatus expected at Master's level", "GALLERY")]),
        ("P3", "III", "The Jury Defense", "15–20 minutes · 20% of the final grade · one slide per capstone section",
         [("part3.html", "Defense Navigator", "Thumbnail storyboard, message strategy and slide-by-slide build", "GUIDE"),
          ("part3.html#board", "Thumbnail Storyboard", "The full deck sketched as frames before software is opened", "BOARD"),
          ("part3.html#qa", "Question Anticipation Matrix", "Responses to questions carry 30% of the presentation mark", "Q&A")]),
    ]
    units = ""
    for pid, roman, title, fmt, links in parts:
        lc = ""
        for href, t, d, tag in links:
            lc += (f'<a class="link-card" href="{href}">'
                   f'<div class="link-badge" style="background:{PART_COLOR[pid]}">{tag[:2]}</div>'
                   f'<div class="link-body"><div class="link-title">{html.escape(t)}</div>'
                   f'<div class="link-desc">{html.escape(d)}</div></div>'
                   f'<div class="link-tag">{html.escape(tag)}</div></a>')
        units += (f'<div class="unit open" data-part="{pid}"><div class="unit-header" onclick="toggle(this)">'
                  f'<div class="unit-num" style="background:{PART_COLOR[pid]}">{roman}</div>'
                  f'<div class="unit-info"><div class="unit-title">{html.escape(title)}</div>'
                  f'<div class="unit-format">{html.escape(fmt)}</div></div>'
                  f'<div class="unit-toggle">▾</div></div>'
                  f'<div class="unit-body"><div class="unit-links">{lc}</div></div></div>')

    body = f"""{hero("EU Business School Munich · Master's Level 7 · Business Plan Route",
                     "The Business Plan Navigator",
                     "Proposal → Business Plan → Jury Defense: one structure, end to end",
                     [(3, "Parts"), (n_fw, "Frameworks"), (n_au, "Authors"), (n_kpi, "KPIs")])}
{topnav("index.html")}
<div class="search-wrap"><div class="search-box"><span class="search-icon">⌕</span>
<input type="text" id="q" placeholder="Search frameworks, chapters, KPIs…" oninput="filt()"></div></div>

<div class="section-title">Who this site is for</div>
<div class="wrap">
<div class="callout must" style="font-size:.83rem">
<strong>Scope.</strong> This site covers one route only: the <strong>Master's capstone taken as a business plan</strong>, at Level&nbsp;7. Every word count, rubric weight, structural requirement and checklist item on these pages is drawn from the Master's business plan guidelines and applies to that route alone.
</div>
<div class="callout note" style="font-size:.83rem">
<strong>Other routes have different criteria.</strong> The Master's capstone taken as a <em>final project</em> follows a different chapter structure and a different rubric. The <em>MBA dissertation</em> and the <em>Bachelor dissertation</em> are separate awards at different levels, with their own word counts, assessment criteria and defence arrangements. Students on those routes should not work from these pages without confirming each requirement with their own promoter. The framework and author galleries, by contrast, are level-neutral: Porter, Weihrich and Doran apply wherever the analysis is done.
</div>
</div>
<div class="section-title">How to use this site</div>
<div class="section-note">The three parts of the Master's capstone are not three documents. They are one argument told three times at increasing resolution: the proposal commits to it, the business plan evidences it, and the defense delivers it. Every framework introduced in Part&nbsp;I reappears in Part&nbsp;II carrying evidence, and reappears again in Part&nbsp;III as a single thumbnail. Students who treat the three parts as separate assignments lose marks under Organisation &amp; Logic and under Analytical Thinking, which together account for a substantial share of the final grade.</div>

<div class="section-title">The Three Parts</div>
<div class="units" id="uc">{units}</div>

<div class="section-title">Galleries</div>
<div class="gallery-link">
  <a href="frameworks.html">■ <span>{n_fw} Frameworks</span> — Complete Gallery Wall, filterable by part and chapter</a>
  <a href="authors.html">■ <span>{n_au} Authors</span> — The Thinkers Behind the Frameworks</a>
  <a href="references.html">■ <span>{len(REFERENCES)} Harvard References</span> — Consolidated, alphabetical, copy-ready</a>
</div>

<div class="section-title">Grade architecture</div>
<div class="wrap">
<table class="kpi-table">
<thead><tr><th>Component</th><th>Weight</th><th>Criteria</th><th>Where it is earned</th></tr></thead>
<tbody>
<tr><td><strong>Written content</strong></td><td>75% of the reading grade</td><td>Executive Summary 10 · Business Identity &amp; Objectives 10 · Marketing Plan 20 · Production &amp; Operations 20 · Organization Plan 10 · Economic, Financial, Legal &amp; Taxation 15 · Analytical Thinking 15</td><td>Part II</td></tr>
<tr><td><strong>Written communication</strong></td><td>25% of the reading grade</td><td>Organisation &amp; Logic 25 · Style &amp; Tone 25 · Use of References 25 · Writing Skills 25</td><td>Parts I and II</td></tr>
<tr><td><strong>Oral defense</strong></td><td>20% of the final grade</td><td>Subject Knowledge &amp; Content 30 · Organisation 10 · Visuals &amp; Speaking 20 · Use of References 10 · Quality of Responses 30</td><td>Part III</td></tr>
</tbody></table>
<div class="callout note">Weightings are taken from the EUBS Master programme capstone guidelines. Students should confirm the applicable academic year with their promoter before relying on any figure.</div>
</div>

<script>
function toggle(el){{el.parentElement.classList.toggle('open');}}
function filt(){{const q=document.getElementById('q').value.toLowerCase();
 document.querySelectorAll('#uc .unit').forEach(u=>{{
   u.classList.toggle('search-hidden', q!=='' && !u.textContent.toLowerCase().includes(q));}});}}
</script>
{FOOT}"""
    write("index.html", head("The Business Plan Navigator — EUBS Master's Level 7",
                             "Structure, frameworks, KPIs and Harvard sources for the EU Business School Munich Master's business plan route") + body)


# ═════════════════════════════ PART I ═════════════════════════════
def build_part1():
    ch = ""
    ch += chapter("A", "Registration Information", "Section A · not graded",
        "Name, email, Master programme and promoter. The promoter signature on this form is the formal gate: no student proceeds to the full business plan without it. The form must be submitted to the Promoter Approval link before the Academic Research Coordinator will review it.",
        [], None, ["eubs2026"])
    ch += chapter("B.I", "Background of the Business Plan", "Section B · part of the graded proposal",
        "A brief history of the company or venture idea and its current status. This is the only genuinely descriptive section of the proposal, and it should still be evidenced. Where the venture does not yet exist, the background describes the market conditions and the founder's route to the idea, not a fictional company history.",
        ["Jobs to Be Done", "Lean Startup / MVP"], None, ["christensen2016", "ries2011"])
    ch += chapter("B.II.1", "Product or Service Concept", "Purpose &amp; Objectives",
        "A clear description of what will be sold. The concept must be specific enough that a reader can picture the transaction: what the customer receives, in what form, at what moment. Vagueness here propagates through every later section, because the marketing mix, the operations plan and the revenue model all depend on the unit being defined.",
        ["Value Proposition Canvas", "Jobs to Be Done", "Business Model Canvas"], None,
        ["osterwalder2014", "osterwalder2010"])
    ch += chapter("B.II.2", "Market and Target Customer", "Purpose &amp; Objectives",
        "A description of the market in which the product will operate, together with the target customer and that customer's profile. Market size must be built bottom-up and every input cited. Top-down claims of the form 'the global market is worth €40&nbsp;billion and the venture will capture 0.1%' are treated as unevidenced under the rubric. The competitive set belongs here too: the proposal should name at least three real competitors with their full legal form, since a market described without its incumbents cannot support a credible SWOT.",
        ["TAM / SAM / SOM", "STP — Segmentation, Targeting, Positioning", "Competitor Analysis Framework",
         "Strategic Group Mapping", "Diffusion of Innovations"], None,
        ["blankdorf2012", "kotler2016", "porter1980ch3", "hunt1972"])
    ch += chapter("B.II.3", "PESTEL Analysis", "Recommended in the form · expected in practice",
        "The macro-environmental test of feasibility. Although the registration form marks PESTEL as recommended, a proposal that omits it will struggle to evidence Analytical Thinking later, because the SWOT has nothing external to draw on. Six factors, minimum two evidenced points each, every point cited and dated, and a closing ranking of the three forces that matter most.",
        ["PESTEL Analysis", "Porter's Five Forces"], None, ["aguilar1967", "johnson2020", "porter2008"])
    ch += chapter("B.II.4", "SWOT Analysis", "Purpose &amp; Objectives",
        "Strengths that will support success, weaknesses to be overcome, threats that could put the business at risk, and opportunities that could boost it. Every cell must trace back to a PESTEL factor, a Five Forces finding or a documented internal capability. A SWOT whose cells cannot be traced upstream is the single most common weakness in capstone proposals.",
        ["SWOT Analysis", "TOWS Matrix", "VRIO Framework"], None, ["learned1969", "weihrich1982", "barney1991"],
        extra='<div class="callout tip"><strong>Promoter note.</strong> The proposal is the right place to add the TOWS step even though the form does not name it. Converting the SWOT into SO, WO, ST and WT strategies is what turns a list into an argument, and it is the move that most reliably lifts the Analytical Thinking mark in Part&nbsp;II.</div>')
    ch += chapter("B.II.5", "Marketing and Sales", "Purpose &amp; Objectives · SMART required",
        "A description of the main objectives using the SMART method, accompanied by the KPIs and the tools that will be used to measure achievement. Marketing and sales may be treated together or separately depending on the characteristics of the business.",
        ["SMART Objectives", "STP — Segmentation, Targeting, Positioning", "Marketing Mix — 4Ps / 7Ps",
         "AARRR Pirate Metrics", "CLV / CAC Ratio"], "Marketing Plan", ["doran1981", "kotler2016", "gupta2006"])
    ch += chapter("B.II.6", "Operations and Production", "Purpose &amp; Objectives · SMART required",
        "The plan for running the business effectively: main requirements in facilities, assets and machinery, and a brief description of the processes to be used. SMART objectives are required here as well, and the capacity implied must be consistent with the sales volumes claimed in the previous section.",
        ["Value Chain Analysis", "Capacity &amp; Bottleneck Planning", "Service Blueprint", "SMART Objectives"],
        "Operations Plan", ["porter1985", "slack2019", "shostack1984"])
    ch += chapter("B.II.7", "Human Resources", "Purpose &amp; Objectives · SMART required",
        "How many people are needed, how they will be organised, and what skills are required. SMART objectives apply here too. The headcount stated must reconcile to the personnel cost line in the five-year profit and loss account.",
        ["Mintzberg's Organisational Configurations", "RACI Matrix", "Belbin Team Roles", "SMART Objectives"],
        "Organization Plan", ["mintzberg1979", "belbin2010"])
    ch += chapter("B.II.8", "Technology", "Purpose &amp; Objectives · stand-alone chapter where material",
        "Where the venture requires substantial technology investment, this becomes a chapter in its own right. A brief description of the required technology and the related effort is expected, together with the capital expenditure it implies.",
        ["Lean Startup / MVP", "Value Chain Analysis", "Risk Register (ISO 31000)"], None, ["ries2011", "iso31000"])
    ch += chapter("B.II.9", "Finance", "Purpose &amp; Objectives · <strong>compulsory</strong>",
        "The crucial section. Where funding will come from, the sales results expressed in units or hours, the prices, the associated costs and the investments. <strong>A five-year profit and loss account and a balance sheet are compulsory at proposal stage.</strong> Parameters may change as the plan deepens, but the figures must already exist and must already reconcile.",
        ["Five-Year P&amp;L, Balance Sheet &amp; Cash Flow", "Break-Even / CVP Analysis",
         "NPV, IRR &amp; Payback", "WACC &amp; Capital Structure"], "Financial Plan",
        ["brealey2020", "mm1958"],
        extra='<div class="callout must"><strong>Blocking check.</strong> Assets must equal liabilities plus equity in every one of the five years. Any stated NPV or IRR must be reproducible from the student\'s own cash flows. A figure that cannot be recalculated from the model presented is treated as a blocking finding at review, not as a rounding issue.</div>')
    ch += chapter("B.III", "Phases and Deadlines", "Section B · Gantt chart mandatory",
        "The timeline that will be used to achieve the objectives and deliver on time. A Gantt chart or an equivalent scheduling system is required, with start and end dates included for every phase. Promoter meetings and submission gates should appear as milestones.",
        ["Gantt Chart", "Risk Register (ISO 31000)"], None, ["gantt1919", "iso31000"])
    ch += chapter("C", "Approval", "Section C · signatures",
        "Signature blocks for the promoter, the Research Coordinator and the Academic Department. The promoter's signature constitutes approval and is obtained through the Promoter Approval submission link.",
        [], None, ["eubs2026"])

    checklist = """
<div class="wrap" id="checklist">
<div class="chapter" style="border-left-color:var(--stop)">
<h3>Pre-submission checklist</h3>
<div class="weight" style="background:#FEE2E2;color:#991B1B">Every box must be ticked before the promoter will sign</div>
<table class="kpi-table"><thead><tr><th>#</th><th>Requirement</th><th>Standard</th></tr></thead><tbody>
<tr><td>1</td><td>Correct official form used</td><td>Business Plan Proposal / Registration Form for the current academic year</td></tr>
<tr><td>2</td><td>All sections completed in full</td><td>No section left blank, including Technology where not applicable — state why</td></tr>
<tr><td>3</td><td>Word count</td><td>Approximately 1,500–2,000 words</td></tr>
<tr><td>4</td><td>In-text citations supporting all sections</td><td>Minimum of ten, distributed across sections rather than clustered</td></tr>
<tr><td>5</td><td>Reference list</td><td>Every in-text citation present; every entry traceable to the body</td></tr>
<tr><td>6</td><td>Harvard referencing</td><td>EU Harvard Referencing Guide for the current academic year</td></tr>
<tr><td>7</td><td>Third-person academic register</td><td>No first or second person, no contractions, British spelling throughout</td></tr>
<tr><td>8</td><td>Gantt chart</td><td>Start and end dates shown for every phase</td></tr>
<tr><td>9</td><td>Similarity and AI check with the promoter</td><td>20% or higher, or a concentrated area, requires rewriting in the student's own words</td></tr>
<tr><td>10</td><td>AI usage annex</td><td>Mandatory; declared in line with the Student Good Practice Manual in AI Literacy</td></tr>
<tr><td>11</td><td>Five-year P&amp;L and balance sheet</td><td>Compulsory; balance sheet identity holds in every year</td></tr>
<tr><td>12</td><td>Promoter signature</td><td>Obtained via the Promoter Approval submission link</td></tr>
</tbody></table>
</div></div>"""

    body = f"""{hero("Part I · Master's Level 7 · Business Plan Route", "The Proposal", "EUBS Business Plan Proposal and Registration Form",
                     [(len([f for f in FRAMEWORKS if f['part'] == 'P1']), "Frameworks"), (10, "Min. citations"), ("1.5–2k", "Words"), (12, "Checks")])}
{topnav("part1.html")}
<div class="section-title">What the proposal is for</div>
<div class="section-note">The proposal is a contract, not a draft. It commits the student to a venture, a market, a set of objectives and a delivery schedule, and it commits the promoter to supervising that commitment. Everything the proposal asserts will be tested at business plan stage, which is why the financial statements are compulsory this early: a venture whose numbers do not reconcile at 2,000 words will not reconcile at 12,000. Approval is granted when the argument is coherent and evidenced, not when the writing is polished.</div>
<div class="section-title">Section-by-section requirements</div>
<div class="wrap">{ch}</div>
{checklist}
{MODAL % fw_json()}
{FOOT}"""
    write("part1.html", head("Part I · The Proposal — The Business Plan Navigator",
                             "Section-by-section requirements, frameworks, KPIs and Harvard sources for the EUBS Business Plan Proposal") + body)


# ═════════════════════════════ PART II ════════════════════════════
def build_part2():
    ch = ""
    ch += chapter("0", "Front Matter", "Not counted in the word limit",
        "Cover page in the official EUBS template, declaration of authorship, table of contents, list of tables, list of figures and the AI usage annex. Every figure and table obeys the three-location rule: it is introduced in the body text, it carries a caption, and it appears in the corresponding list. Figures created by the student are attributed with the exact formula <em>(Created by the author, 2026)</em>.",
        ["Harvard Referencing"], None, ["eubsstyle2026", "eubs2026"])
    ch += chapter("1", "Executive Summary", "10% of written content",
        "A thorough summary covering business identity, objectives, markets, operations, organisation, legal and taxation, and economics and finance. The standard for the top band is explicit: a reader who reads <em>only</em> the executive summary must walk away with a solid understanding of the purpose, scope, methods and findings. No longer than two pages. Written last, read first.",
        ["Pyramid Principle", "Message Strategy — one clear message"], None, ["minto2009", "bostelaar2023"],
        extra='<div class="callout tip"><strong>Structural test.</strong> Cover the rest of the document and hand the summary alone to a reader who has never seen the venture. If they cannot state what is sold, to whom, at what price, and whether it makes money, the summary has not met the rubric standard regardless of how well it is written.</div>')
    ch += chapter("2", "Business Identity and Business Objectives", "10% of written content",
        "The introduction to the business identity and its core values, plus the business objectives. The top band requires relevant background data, an identified information gap, and a clear explanation of why that gap needs filling. This chapter also carries the strategic analysis: PESTEL, Porter's Five Forces, <strong>competitor analysis</strong>, SWOT and TOWS belong here, under strategy, not under the marketing plan. Competitor analysis sits between the Five Forces and the SWOT — the Five Forces establish that rivalry exists, competitor analysis establishes who the rivals are and how they will respond, and only then can the SWOT be populated with something other than assertion.",
        ["Golden Circle", "Vision, Mission &amp; Core Values", "PESTEL Analysis", "Porter's Five Forces",
         "Competitor Analysis Framework", "Strategic Group Mapping", "Competitive Profile Matrix",
         "SWOT Analysis", "TOWS Matrix", "VRIO Framework", "Generic Competitive Strategies",
         "Ansoff Growth Matrix", "Blue Ocean / Strategy Canvas", "Balanced Scorecard", "SMART Objectives", "OKR"],
        None, ["collins1996", "sinek2009", "porter2008", "porter1980ch3", "hunt1972", "david2017", "weihrich1982", "barney1991", "kim2005"])
    ch += chapter("3", "Marketing Plan", "20% of written content",
        "The largest single content weight alongside operations. Segmentation, targeting and positioning, the marketing mix, the customer journey, the acquisition funnel and the pricing logic. Every element must follow from the strategy selected in Chapter&nbsp;2 and must reconcile numerically with the revenue model in Chapter&nbsp;6. A price stated here that differs from the price used in the financial model is an internal inconsistency the jury will find.",
        ["STP — Segmentation, Targeting, Positioning", "Positioning Statement", "Marketing Mix — 4Ps / 7Ps",
         "Customer Journey Mapping", "AIDA Funnel", "AARRR Pirate Metrics", "CLV / CAC Ratio",
         "Value-Based Pricing", "Diffusion of Innovations", "Value Proposition Canvas", "Perceptual Mapping"],
        "Marketing Plan", ["kotler2016", "booms1981", "riestrout2001", "nagle2018", "gupta2006", "lemon2016", "fleisher2015"])
    ch += chapter("4", "Production and Operations Plan", "20% of written content",
        "The what, why, where and when of production and operations: how the business will be managed day to day in terms of essential processes, resources needed, technology applied and quality management. The top band requires very detailed description <em>and justification</em>, thoroughly supported by academic literature. Capacity must exceed the sales forecast in every year or the plan contradicts itself.",
        ["Value Chain Analysis", "Service Blueprint", "Lean Thinking / Waste Elimination",
         "Capacity &amp; Bottleneck Planning", "SCOR Model", "Quality Management (ISO 9001)",
         "Risk Register (ISO 31000)", "Benchmarking", "Business Model Canvas"],
        "Operations Plan", ["porter1985", "shostack1984", "womack2003", "slack2019", "iso9001", "scor2017", "camp1989"])
    ch += chapter("5", "Organization Plan", "10% of written content",
        "The structure of the organisation and the human resources planning behind it. An organigram alone does not meet the criterion: the structure must be justified against the venture's stage and environment, and the headcount must reconcile to the personnel costs in Chapter&nbsp;6.",
        ["Mintzberg's Organisational Configurations", "RACI Matrix", "Belbin Team Roles",
         "Tuckman Group Development", "Schein's Levels of Culture"],
        "Organization Plan", ["mintzberg1979", "belbin2010", "tuckman1965", "schein2017"])
    ch += chapter("6", "Economic, Financial, Legal and Taxation Plan", "15% of written content",
        "Five-year profit and loss account, balance sheet and cash flow statement, break-even analysis, investment appraisal, funding structure, legal form and the tax position. Assumptions belong in an appendix, headline outputs in the body. The legal form of the venture and of every named competitor and supplier must be stated in full on first mention.",
        ["Five-Year P&amp;L, Balance Sheet &amp; Cash Flow", "Break-Even / CVP Analysis", "NPV, IRR &amp; Payback",
         "WACC &amp; Capital Structure", "Sensitivity &amp; Scenario Analysis", "Legal Form &amp; Statutory Reserve"],
        "Financial Plan", ["brealey2020", "mm1958", "gmbhg"],
        extra='<div class="callout must"><strong>Three non-negotiable checks.</strong> First, assets equal liabilities plus equity in every year. Second, the cash line in the balance sheet equals the closing cash in the cash flow statement. Third, the stated NPV and IRR are reproducible from the cash flows printed in the document, at the discount rate stated. Promoters recalculate these independently before feedback is issued.</div>')
    ch += chapter("7", "Analytical Thinking", "15% of written content · assessed across the whole document",
        "Not a chapter but a quality assessed throughout. It rewards the traceability of the argument: whether the strategy follows from the analysis, whether the marketing mix follows from the strategy, whether operations can deliver the mix, and whether the financials express the operations. Most marks are lost here not through wrong answers but through missing warrants — the sentence that explains why the evidence supports the claim.",
        ["The Logical Chain", "Toulmin Model of Argument", "TOWS Matrix"], None, ["toulmin2003", "eubs2026"])
    ch += chapter("8", "References and Appendices", "25% written communication · Use of References",
        "Harvard throughout, alphabetical, with every in-text citation present in the list and every list entry traceable to the body. Sources should generally be no more than five years old unless they are the seminal statement of a framework. Appendices are curated, labelled, titled and referenced from the body — never a dumping ground.",
        ["Harvard Referencing"], None, ["eubsstyle2026"])

    chain = """
<div class="section-title" id="chain">The logical chain</div>
<div class="section-note">This is the single strongest predictor of a high mark under Analytical Thinking and under Organisation &amp; Logic. Each stage consumes the output of the stage before it. Where a link is broken — a marketing decision with no strategic parent, a financial figure with no operational driver — the chapter may still read well and will still lose marks.</div>
<div class="wrap">
<svg viewBox="0 0 1075 200" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;background:#fff;border:1px solid var(--border);border-radius:10px;padding:8px">
  <defs><marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
    <path d="M0,0 L8,4 L0,8 z" fill="#00B388"/></marker></defs>
  <g font-family="Arial" font-size="11" text-anchor="middle">
""" + "".join(
        f'<rect x="{10 + i*133}" y="70" width="118" height="46" rx="7" fill="{c}" opacity="0.12" stroke="{c}"/>'
        f'<text x="{69 + i*133}" y="90" fill="#1B2A4A" font-weight="bold">{t1}</text>'
        f'<text x="{69 + i*133}" y="105" fill="#6B7280" font-size="9.5">{t2}</text>'
        + (f'<line x1="{128 + i*133}" y1="93" x2="{140 + i*133}" y2="93" stroke="#00B388" stroke-width="2" marker-end="url(#ar)"/>' if i < 7 else "")
        for i, (t1, t2, c) in enumerate([
            ("PESTEL", "external forces", "#1E40AF"),
            ("Competitors", "who + how they react", "#1E40AF"),
            ("SWOT", "internal vs external", "#1E40AF"),
            ("TOWS", "four strategy families", "#2563EB"),
            ("Strategy", "generic + growth", "#2563EB"),
            ("Marketing Mix", "4Ps / 7Ps", "#2563EB"),
            ("Operations", "capacity + quality", "#B45309"),
            ("Financials", "P&amp;L · BS · CF", "#B45309")])) + """
  <text x="537" y="40" font-size="12.5" font-weight="bold" fill="#1B2A4A">Every downstream decision must be traceable to an upstream finding</text>
  <text x="537" y="150" font-size="10.5" fill="#6B7280">Read backwards to test it: for any number in the financial model, name the operational driver;</text>
  <text x="537" y="165" font-size="10.5" fill="#6B7280">for that driver, name the marketing decision; for that decision, name the strategy; for that strategy, name the TOWS cell.</text>
  <text x="537" y="185" font-size="9" fill="#94A3B8" font-style="italic">(Created by the author, 2026)</text>
  </g>
</svg>
</div>"""

    body = f"""{hero("Part II · Master's Level 7 · Business Plan Route", "The Final Business Plan", "EUBS Master's business plan · 10,000–12,000 words",
                     [(7, "Rubric chapters"), (len([f for f in FRAMEWORKS if f['part'] == 'P2']), "Frameworks"),
                      (sum(len(KPIS[k]) for k in ["Marketing Plan", "Operations Plan", "Organization Plan", "Financial Plan"]), "KPIs"), ("75/25", "Content/Comms")])}
{topnav("part2.html")}
<div class="section-title">What changes between Part I and Part II</div>
<div class="section-note">Nothing in the argument changes. The resolution changes. Each proposal section becomes a chapter carrying evidence, each assertion acquires a citation, each figure acquires a source and an assumption, and each framework that was named in the proposal is now applied and interpreted rather than merely displayed. A business plan that introduces a new strategic direction not present in the approved proposal creates a problem for the jury, because the promoter signed something else.</div>
<div class="section-title">Chapter-by-chapter requirements</div>
<div class="wrap">{ch}</div>
{chain}
{MODAL % fw_json()}
{FOOT}"""
    write("part2.html", head("Part II · The Final Business Plan — The Business Plan Navigator",
                             "Rubric-weighted chapter requirements, frameworks, KPI inventories and Harvard sources") + body)


# ═════════════════════════════ PART III ═══════════════════════════
THUMBS = [
    ("01", "Title &amp; the one message", "Venture name, student, programme, promoter. Speak the governing message aloud within the first twenty seconds.", "Message Strategy (Bostelaar)", "0:00–0:30"),
    ("02", "Introduction from the founder", "Who is doing this and why they are credible. One photograph, three facts, no career history.", "Golden Circle (Sinek)", "0:30–1:15"),
    ("03", "Reasons why", "Personal interest, the wish to realise one's own idea, job creation. Kept short — the jury is testing sincerity, not length.", "Golden Circle (Sinek)", "1:15–1:45"),
    ("04", "The problem or gap", "One statistic, one image, one sentence. This is the tension the whole defense resolves.", "Sparkline (Duarte)", "1:45–2:45"),
    ("05", "The product or service", "What is actually sold. Show it — a mock-up, a screen, a photograph — rather than describing it.", "Value Proposition Canvas", "2:45–3:45"),
    ("06", "The unique selling point", "Why this and not the alternative. One comparison visual against named competitors.", "Competitor Analysis (Porter) · Positioning", "3:45–4:45"),
    ("07", "Business identity &amp; objectives", "Vision, mission, values in three lines, then the SMART objectives as a single table.", "SMART (Doran)", "4:45–6:00"),
    ("08", "Market &amp; strategic analysis", "TAM/SAM/SOM and the three PESTEL forces that matter. Never show a full six-column PESTEL on a slide.", "TAM/SAM/SOM · PESTEL", "6:00–7:30"),
    ("09", "Strategic choice", "The TOWS cell selected and the generic strategy it implies. One matrix, one highlighted quadrant.", "TOWS (Weihrich)", "7:30–8:45"),
    ("10", "Marketing plan", "Positioning statement, the mix in one visual, and the funnel with real conversion numbers.", "STP · 7Ps · AARRR", "8:45–10:30"),
    ("11", "Production &amp; operations", "The process from order to delivery as one flow diagram, with the bottleneck marked.", "Value Chain · Capacity", "10:30–12:00"),
    ("12", "Organization plan", "Organigram at launch and at year three, with the roles that carry key-person risk highlighted.", "Mintzberg · RACI", "12:00–13:00"),
    ("13", "Economic &amp; financial plan", "Revenue and EBITDA curve, break-even point, and the funding requirement. One chart, three numbers.", "P&amp;L · Break-even", "13:00–15:00"),
    ("14", "Investment appraisal", "NPV, IRR, payback and the discount rate, with the sensitivity range beside them.", "NPV/IRR · WACC", "15:00–16:00"),
    ("15", "Legal form &amp; taxation", "Legal form with full designation, statutory obligations, and the tax position in one table.", "GmbHG § 5a", "16:00–16:45"),
    ("16", "Risks &amp; mitigation", "The three risks that could end the venture, each with a trigger and a response.", "ISO 31000", "16:45–17:30"),
    ("17", "The ask &amp; next steps", "What happens on the Monday after the defense. Return to the governing message.", "Sparkline (Duarte)", "17:30–18:30"),
    ("18", "Reference list", "Mandatory graded slide. Harvard, corresponding to the citations used in the deck.", "EUBS Defense Guidelines", "18:30–19:00"),
]

QA = [
    ("Financial model", "Where exactly does the year-three revenue figure come from?", "Name the volume driver, the price and the conversion assumption, then point to the appendix slide showing the build-up."),
    ("Financial model", "Why is your discount rate what it is?", "State the cost of equity, the cost of debt, the weights and the tax shield. An unjustified rate invalidates the NPV."),
    ("Financial model", "Your NPV is negative — why should this proceed?", "Do not apologise. Explain the horizon, the terminal value treatment, or the strategic option being bought, and state what would have to change for the NPV to turn."),
    ("Market", "How did you size the market, and can you defend the SOM percentage?", "Bottom-up build, cited inputs, and a comparator venture that achieved a similar capture rate in a similar time."),
    ("Competition", "Who is your closest competitor and why will they not simply copy you?", "Name them with full legal form, place them on the strategic group map, then answer with Porter's response profile — their goals, strategy, assumptions and capabilities — and close with VRIO on what is rare and hard to imitate."),
    ("Operations", "Can you actually deliver the year-three volume?", "Give design capacity, effective capacity and the binding bottleneck, then show the headroom."),
    ("Organisation", "What happens if you are unavailable for three months?", "Key-person risk. Name the successor or the mitigation; do not answer that it will not happen."),
    ("Strategy", "Which of your assumptions is most likely to be wrong?", "Answer honestly and immediately. Name it, state the sensitivity, and state the trigger that would tell you early."),
    ("Legal", "Why this legal form rather than the alternative?", "Liability, capital requirement, statutory reserve obligation and tax treatment — four reasons, thirty seconds."),
    ("Method", "How did you use AI in preparing this work?", "Refer to the AI usage annex and state the specific tasks and the verification applied. This must match what the annex says."),
]


def build_part3():
    thumbs = "".join(
        f'<div class="thumb"><div class="tno">{n}<span>THUMBNAIL</span></div>'
        f'<div class="tbody"><div class="tmsg">{m}</div><div class="tvis">{v}</div>'
        f'<div class="tfw">{f}</div></div><div class="ttime">{t}</div></div>'
        for n, m, v, f, t in THUMBS)

    qa_rows = "".join(
        f"<tr><td><strong>{html.escape(a)}</strong></td><td>{html.escape(q)}</td><td>{html.escape(r)}</td></tr>"
        for a, q, r in QA)

    ch = ""
    ch += chapter("1", "Fix the message before the slides", "Bostelaar · Message Strategy",
        "The deck is not built first. The message is. Write, in one sentence, what the jury should be able to repeat to a colleague an hour after the defense ends. That sentence governs everything: any slide that does not advance it is deleted or demoted to the appendix. The discipline is to make a complex proposition simple, visual and practical without making it shallow — the jury must feel that depth is available behind every simplification, and the appendix is where that depth waits.",
        ["Message Strategy — one clear message", "Pyramid Principle for Speaking"], None,
        ["bostelaar2023", "bostelaar2016", "minto2009"],
        extra='<div class="callout tip"><strong>The one-sentence test.</strong> Write the governing message on a card before opening any software. If it takes more than one sentence, the venture is not yet understood well enough to defend. Read it aloud at thumbnail 01 and again at thumbnail 17.</div>')
    ch += chapter("2", "Sketch the deck as thumbnails", "Meier · Thumbnail Thinking",
        "Before any slide is built, the whole deck is drawn as small frames — postcard size, by hand, one idea per frame. The constraint is the point: an idea that does not fit inside a thumbnail is two ideas and must be split. Laid out together, the thumbnails expose problems that are invisible inside presentation software: a missing transition, three consecutive frames making the same point, a chapter with no visual, an argument that resolves too early. Cutting happens here, where cutting is cheap.",
        ["Thumbnail Thinking", "Sparkline / What Is — What Could Be"], None, ["meier2025", "duarte2010"])
    ch += chapter("3", "Build each slide assertion-first", "Alley · Mayer",
        "The headline is a complete sentence stating the message of the slide, not a topic label. The body is a visual that supports that sentence — a chart, a diagram, a photograph — rather than a list of the words about to be spoken. This single change does more for the Visuals and Speaking Skills criterion than any amount of template polish, and it is supported by the multimedia learning evidence: the redundancy effect means that reading a slide aloud actively reduces what the audience retains.",
        ["Assertion–Evidence Structure", "Multimedia &amp; Cognitive Load Principles"], None,
        ["alley2013", "mayer2009"])
    ch += chapter("4", "Meet the EUBS structural requirements", "EUBS Defense Guidelines",
        "One slide is required for each capstone section: the founder introduction, the product or service and its unique selling point, the reasons why, the problem or gap, business identity and objectives, the marketing plan, production and operations, the organization plan, and the economic, financial, legal and taxation plan. The reference list is a mandatory graded component. The whole defense must fit within fifteen to twenty minutes so that time remains for jury questions.",
        ["EUBS Defense Slide Requirements"], "Defense", ["eubsdef2026"])
    ch += chapter("5", "Prepare for the questions", "30% of the presentation mark",
        "Quality of responses to questions carries the highest single weight in the presentation rubric — equal to subject knowledge and content, and greater than visuals and organisation combined. Preparation means writing a thirty-second answer to each of the ten most likely challenges and building one appendix slide behind each answer, numbered so it can be retrieved instantly. The strongest signal a candidate can send is to answer a hard question by saying which appendix slide addresses it.",
        ["Question Anticipation Matrix"], None, ["eubsdef2026"])

    body = f"""{hero("Part III · Master's Level 7 · Business Plan Route", "The Jury Defense", "15–20 minutes · 20% of the final grade",
                     [(len(THUMBS), "Thumbnails"), (len(QA), "Anticipated questions"), ("30%", "Q&amp;A weight"), ("20%", "Of final grade")])}
{topnav("part3.html")}
<div class="section-title">Two authors govern this part</div>
<div class="section-note">J.D. Meier's <strong>thumbnail thinking</strong> settles the structure: the deck is sketched as small hand-drawn frames, one idea each, and edited on a wall before a single slide is built. Kurt Bostelaar's <strong>message strategy</strong> settles the content: one governing message, expressed simply, visually and practically, with every frame tested against it. Structure without message produces a well-organised deck that says nothing memorable. Message without structure produces a memorable sentence attached to nineteen minutes of drift. The two are applied together, in that order.</div>
<div class="section-title">The method</div>
<div class="wrap">{ch}</div>

<div class="section-title" id="board">The thumbnail storyboard</div>
<div class="section-note">Eighteen frames covering every mandatory EUBS section within the twenty-minute limit. Timings are indicative and should be adjusted after the first timed rehearsal. Each frame carries one idea and names the framework it renders — students should sketch these by hand before building anything.</div>
<div class="board">{thumbs}</div>

<div class="section-title" id="qa">Question anticipation matrix</div>
<div class="section-note">Ten questions that recur across defenses, with the shape of a strong answer. One appendix slide should sit behind each, numbered and retrievable. Students should rehearse the retrieval, not only the answer.</div>
<div class="wrap"><table class="kpi-table">
<thead><tr><th>Area</th><th>Likely question</th><th>Shape of a strong answer</th></tr></thead>
<tbody>{qa_rows}</tbody></table>
<div class="callout must"><strong>Never do these three things.</strong> Do not read a slide aloud. Do not answer a question you were not asked because you prepared that answer. Do not defend a number you cannot reconstruct — say what you would need to check and offer to follow up, which costs far less than a fabricated derivation.</div>
</div>
{MODAL % fw_json()}
{FOOT}"""
    write("part3.html", head("Part III · The Jury Defense — The Business Plan Navigator",
                             "Thumbnail storyboard, message strategy, slide requirements and question anticipation for the EUBS oral defense") + body)


# ═══════════════════════ FRAMEWORK GALLERY ════════════════════════
def build_frameworks():
    chaps = sorted({f["chap"] for f in FRAMEWORKS})
    filt = ('<div class="filters"><span class="filt on" data-f="all" onclick="setF(this)">All ' + str(len(FRAMEWORKS)) + '</span>')
    for p in ["P1", "P2", "P3"]:
        n = len([f for f in FRAMEWORKS if f["part"] == p])
        filt += f'<span class="filt" data-f="{p}" onclick="setF(this)">{html.escape(PART_NAME[p])} · {n}</span>'
    filt += "</div>"

    cards = ""
    for i, f in enumerate(FRAMEWORKS):
        cards += (f'<div class="fw" data-part="{f["part"]}" data-txt="{html.escape((f["name"]+" "+f["author"]+" "+f["chap"]+" "+f["use"]).lower())}" onclick="openM({i})">'
                  f'<span class="tag" style="background:{PART_COLOR[f["part"]]}">{html.escape(PART_NAME[f["part"]])}</span>'
                  f'<h4>{html.escape(f["name"])}</h4><div class="auth">{html.escape(f["author"])}</div>'
                  f'<div class="use">{html.escape(f["use"])}</div>'
                  f'<div class="where">▸ {html.escape(f["chap"])}</div></div>')

    body = f"""{hero("Framework Gallery · Level-neutral", "The Analytical Apparatus", "Every tool, framework and model required across the three parts",
                     [(len(FRAMEWORKS), "Frameworks"), (len(chaps), "Chapters"), (len(AUTHORS), "Authors"), (3, "Parts")])}
{topnav("frameworks.html")}
<div class="search-wrap"><div class="search-box"><span class="search-icon">⌕</span>
<input type="text" id="q" placeholder="Search by framework, author, chapter or purpose…" oninput="run()"></div></div>
{filt}
<div class="gal" id="gal">{cards}</div>
<script>
let cur='all';
function setF(el){{document.querySelectorAll('.filt').forEach(x=>x.classList.remove('on'));
 el.classList.add('on');cur=el.dataset.f;run();}}
function run(){{const q=(document.getElementById('q').value||'').toLowerCase();
 document.querySelectorAll('.fw').forEach(c=>{{
  const okP = cur==='all'||c.dataset.part===cur;
  const okQ = q===''||c.dataset.txt.includes(q);
  c.classList.toggle('hide', !(okP&&okQ));}});}}
if(location.hash){{const h=location.hash.slice(1);
 const b=document.querySelector('.filt[data-f="'+h+'"]'); if(b)setF(b);}}
</script>
{MODAL % fw_json()}
{FOOT}"""
    write("frameworks.html", head("Framework Gallery — The Business Plan Navigator",
                                  "All frameworks, tools and models required across the EUBS capstone, with Harvard references") + body)


# ═══════════════════════ AUTHOR GALLERY ═══════════════════════════
def build_authors():
    cards = ""
    for name, yrs, contrib, fws, ref in sorted(AUTHORS, key=lambda a: a[0].split()[-1]):
        init = "".join(w[0] for w in name.replace("&", "").split() if w[0].isupper())[:3]
        cards += (f'<div class="auth-card" data-txt="{html.escape((name+" "+contrib+" "+fws).lower())}">'
                  f'<div class="init">{html.escape(init)}</div>'
                  f'<h4>{html.escape(name)}</h4><div class="yrs">{html.escape(yrs)}</div>'
                  f'<div class="contrib">{html.escape(contrib)}</div>'
                  f'<div class="ref"><strong>{html.escape(fws)}</strong><br>{REFERENCES[ref]}</div></div>')

    body = f"""{hero("Authors Gallery · Level-neutral", "The Thinkers Behind the Frameworks", "Attribution is not decoration — it is the Use of References criterion",
                     [(len(AUTHORS), "Authors"), (len(FRAMEWORKS), "Frameworks"), (len(REFERENCES), "References")])}
{topnav("authors.html")}
<div class="section-note" style="margin-top:1.5rem">A framework used without attribution is an unevidenced assertion, and the rubric treats it as one. Students should cite the originating author on first use of every model — Weihrich for TOWS, Doran for SMART, Barney for VRIO — and reserve secondary textbook citations for the teaching form of a framework rather than its origin. The gallery below gives the anchor reference for each.</div>
<div class="search-wrap"><div class="search-box"><span class="search-icon">⌕</span>
<input type="text" id="q" placeholder="Search authors, frameworks, contributions…" oninput="run()"></div></div>
<div class="gal" id="gal">{cards}</div>
<script>
function run(){{const q=(document.getElementById('q').value||'').toLowerCase();
 document.querySelectorAll('.auth-card').forEach(c=>{{
  c.style.display=(q===''||c.dataset.txt.includes(q))?'':'none';}});}}
</script>
{FOOT}"""
    write("authors.html", head("Authors Gallery — The Business Plan Navigator",
                               "The thinkers behind every framework required in the EUBS capstone, with Harvard references") + body)


# ═══════════════════════ REFERENCE LIST ═══════════════════════════
def build_references():
    items = sorted(REFERENCES.values(), key=lambda s: s.lower())
    rows = "".join(f'<div class="ref-item" data-txt="{html.escape(i.lower())}">{i}</div>' for i in items)
    body = f"""{hero("Reference List · Level-neutral", "Consolidated Harvard References", "Alphabetical · EU Business School Harvard style",
                     [(len(REFERENCES), "References"), (len(AUTHORS), "Authors"), (len(FRAMEWORKS), "Frameworks")])}
{topnav("references.html")}
<div class="section-note" style="margin-top:1.5rem">These are the anchor sources for the frameworks used across the three parts. They are a starting point, not a substitute for the student's own reading: a capstone reference list built only from this page will read as generic and will lose marks under Use of References. Students should add sector-specific, geographically relevant and recent sources, and should check every entry against the EU Harvard Referencing Guide for the current academic year before submission. Where a source predates the five-year currency expectation, it should be the seminal statement of the framework rather than a convenience citation.</div>
<div class="search-wrap"><div class="search-box"><span class="search-icon">⌕</span>
<input type="text" id="q" placeholder="Filter references…" oninput="run()"></div></div>
<div class="refs">{rows}</div>
<script>
function run(){{const q=(document.getElementById('q').value||'').toLowerCase();
 document.querySelectorAll('.ref-item').forEach(c=>{{
  c.classList.toggle('hide', q!=='' && !c.dataset.txt.includes(q));}});}}
</script>
{FOOT}"""
    write("references.html", head("Reference List — The Business Plan Navigator",
                                  "Consolidated Harvard reference list for every framework used across the EUBS capstone") + body)


def write(fn, content):
    p = os.path.join(OUT, fn)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  ✓ {fn}  ({len(content):,} bytes)")


if __name__ == "__main__":
    print("Building The Business Plan Navigator…")
    build_index(); build_part1(); build_part2(); build_part3()
    build_frameworks(); build_authors(); build_references()
    print(f"\nDone. {len(FRAMEWORKS)} frameworks · {len(AUTHORS)} authors · "
          f"{len(REFERENCES)} references · {sum(len(v) for v in KPIS.values())} KPIs")
