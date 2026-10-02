#!/usr/bin/env python3
"""Build a dependency-free reader from Markdown using locally installed Pandoc."""
from pathlib import Path
import subprocess,re,html,shutil,json,zipfile
import xml.etree.ElementTree as ET
from lab_templates import LABS,lab
ROOT=Path(__file__).resolve().parent
DOCS=ROOT/'docs';SOURCE=ROOT/'source';TITLE='Practical Data Analysis for Engineering Decisions'
PAGES=[]
SUMMARIES=['How to read evidence, examples, and the companion.','Turn a vague performance concern into a testable question.','Choose identifiers, endpoints, clocks, and units.','Make keys, joins, missingness, and provenance explicit.','Read distributions and check the mix beneath an average.','Preserve workload pairs and interpret uncertainty honestly.','Follow an observation through traces to a bounded explanation.','Design an intervention that can challenge your explanation.','Understand queues, censoring, drift, and time-ordered evaluation.','Separate task success, judge quality, cost, and safety.','Evaluate learning curves without leaking the test set.','Collect evidence with a schema and account for missing records.','Turn analysis into a reversible, well-supported next step.','Reproduce the results, try the labs, and use the checklist.']
for i,p in enumerate(sorted((SOURCE/'chapters').glob('*.md'))):
 raw=p.read_text();title=raw.splitlines()[0].removeprefix('# ');title='Start here' if p.name.startswith('00_') else title
 PAGES.append({'file':p,'slug':p.stem.replace('_','-'),'title':title,'raw':raw,'idx':i,'n':int(p.name[:2]),'summary':SUMMARIES[int(p.name[:2])] if int(p.name[:2])<len(SUMMARIES) else 'A worked mathematical perspective with reproducible examples.'})
shutil.copytree(SOURCE/'figures',DOCS/'assets/figures',dirs_exist_ok=True)
EMBEDS={4:['ecdf','cohort'],5:['paired'],9:['judge'],14:['vectors'],15:['pixels'],16:['gis'],17:['finance'],18:['workers']}
def a(s):return html.escape(str(s),quote=True)
def chapter_link(p,base=''):return base+'chapters/'+p['slug']+'.html'
def label(p):return 'Ref' if p['n']==90 else '—' if p['n']==0 else f"{p['n']:02}"
def nav(base='',current=None):
 return '<nav aria-label="Book chapters"><h2>In this book</h2><label><span class="eyebrow">Find a chapter</span><input class="tocsearch" type="search" placeholder="Filter chapters" aria-label="Filter chapters"></label>'+''.join(f'<a data-chapter href="{chapter_link(p,base)}"'+(' aria-current="page"' if current==p['slug'] else '')+f'><span class="navnum">{label(p)}</span> {a(re.sub(r"^\d+ ","",p["title"]))}</a>' for p in PAGES)+f'<hr><a href="{base}labs/index.html">Interactive labs</a><a href="{base}sources.html">Sources &amp; evidence</a><a href="{base}downloads.html">Download &amp; work offline</a></nav>'
def shell(title,body,base='',description='A practical interactive book for making better engineering decisions from data.'):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{a(description)}"><meta name="theme-color" content="#152f32"><title>{a(title)} · Practical Data Analysis</title><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/style.css"></head><body><a class="skip" href="#main">Skip to content</a><header class="topbar"><div class="topinner"><a class="brand" href="{base}index.html"><span aria-hidden="true">∑</span>Practical Data Analysis</a><nav class="topnav" aria-label="Primary"><a href="{base}chapters/{PAGES[0]['slug']}.html">Read</a><a href="{base}labs/index.html">Labs</a><a class="desktopnav" href="{base}downloads.html">Downloads</a><a class="desktopnav" href="https://github.com/MrScripty/practical-data-analysis">GitHub ↗</a></nav></div></header>{body}<footer class="sitefooter"><div class="wrap"><span>Practical Data Analysis for Engineering Decisions</span><span>Measured where stated. Synthetic where labeled. <a href="{base}sources.html">Evidence &amp; sources</a></span></div></footer><script src="{base}assets/math.js"></script><script src="{base}assets/data.js"></script><script src="{base}assets/expanded-data.js"></script><script src="{base}assets/expanded-math.js"></script><script src="{base}assets/labs.js"></script><script src="{base}assets/expanded-labs.js"></script><script src="{base}assets/site.js"></script></body></html>'''
def render_md(raw,depth=False):
 h=subprocess.run(['pandoc','--from=gfm','--to=html5','--no-highlight'],input=raw,text=True,check=True,capture_output=True).stdout
 h=re.sub(r'src="figures/([^\"]+)\.png"',lambda m:'src="'+('../' if depth else '')+'assets/figures/'+m[1]+'.svg"',h)
 def dimensions(m):
  tag=m[0];src=re.search(r'src="([^"]+)"',tag)[1]
  asset=DOCS/src.removeprefix('../')
  if asset.suffix=='.svg':
   root=ET.parse(asset).getroot();box=root.attrib.get('viewBox','').split()
   if len(box)==4:tag=tag.replace(' />',f' width="{float(box[2]):.3f}" height="{float(box[3]):.3f}" />')
  return tag
 h=re.sub(r'<img [^>]+>',dimensions,h)
 return h
for p in PAGES:
 h=render_md(p['raw'],True)
 if p['file'].name.startswith('00_'):h=h.replace('<h1>'+TITLE+'</h1>','<h1>Start here</h1>')
 # Insert each lab next to the concept it illustrates, retaining all manuscript text.
 patterns={'ecdf':'<h2 id="histograms-and-box-plots-have-jobs">','cohort':'<h2 id="outliers-are-questions">','paired':'<h2 id="uncertainty-is-not-a-decoration">','judge':'<h2 id="calibration-and-probability">'}
 for kind in EMBEDS.get(p['n'],[]):
  marker=patterns.get(kind,'')
  if marker and marker in h:h=h.replace(marker,lab(kind)+marker,1)
  else:h+=lab(kind)
 toc=''.join(f'<a href="#{id}">{re.sub("<[^>]*>","",title)}</a>' for id,title in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',h))
 prev=PAGES[p['idx']-1] if p['idx'] else None;nxt=PAGES[p['idx']+1] if p['idx']+1<len(PAGES) else None
 pager='<nav class="chapterpager" aria-label="Adjacent chapters">'+(f'<a href="{prev["slug"]}.html"><small>← Previous</small>{a(prev["title"])}</a>' if prev else '<span></span>')+(f'<a href="{nxt["slug"]}.html"><small>Next →</small>{a(nxt["title"])}</a>' if nxt else '<a href="../sources.html"><small>Next →</small>Sources &amp; evidence</a>')+'</nav>'
 body=f'<div class="reader"><aside class="sidebar">{nav("../",p["slug"])}</aside><main class="prose" id="main"><details class="mobilecontents"><summary>Browse chapters</summary>{nav("../",p["slug"])}</details><div class="chaptermeta"><span class="eyebrow">{"Reading guide" if p["n"]==0 else "Reference" if p["n"]==90 else "Chapter "+str(p["n"])}</span><span>{max(1,round(len(p["raw"].split())/220))} min read</span></div>{h}{pager}</main><aside class="sidebar onthispage"><h2>On this page</h2>{toc}</aside></div>'
 (DOCS/'chapters'/f'{p["slug"]}.html').write_text(shell(p['title'],body,'../'))
hero='''<div class="figurecard"><div class="figuretop"><strong>ONE QUESTION. THREE WORKLOADS.</strong><span>Matched comparison</span></div><svg viewBox="0 0 440 265" role="img" aria-label="Three matched workloads show that one policy can win one case and lose another"><g stroke="#e0e7e1"><path d="M70 35V205 M145 35V205 M220 35V205 M295 35V205 M370 35V205"/></g><g stroke="#99ada6" stroke-width="3"><path d="M108 73H142 M125 125H183 M138 177H332"/></g><g fill="#849594"><circle cx="142" cy="73" r="7"/><circle cx="125" cy="125" r="7"/><circle cx="138" cy="177" r="7"/></g><g fill="#12655f"><circle cx="108" cy="73" r="7"/><circle cx="183" cy="125" r="7"/><circle cx="332" cy="177" r="7"/></g><g font-family="system-ui,sans-serif" font-size="11" fill="#53686a"><text x="25" y="77">59</text><text x="25" y="129">83</text><text x="20" y="181">101</text><text x="70" y="231">Faster</text><text x="340" y="231">Slower</text><text x="169" y="253">Makespan →</text></g></svg><div class="figurecaption">The average cannot tell the whole story.<br>Residency <span style="color:#849594">●</span> &nbsp; Proposed <span style="color:#12655f">●</span> · Shape based on the randomized simulator case</div></div>'''
cards=''.join(f'<a class="chaptercard" href="{chapter_link(p)}"><span class="number">{label(p)}</span><div><h3>{a(re.sub(r"^\d+ ","",p["title"]))}</h3><p>{a(p["summary"])}</p></div></a>' for p in PAGES)
labcards=''.join(f'<a class="labcard" href="labs/{kind}.html"><span class="eyebrow">Lab {i+1:02}</span><h3>{v[0]}</h3><p>{v[1]}</p><span class="arrow">Explore the example →</span></a>' for i,(kind,v) in enumerate(LABS.items()))
body=f'''<main id="main"><div class="wrap"><section class="hero"><div><span class="eyebrow">An interactive field guide · Expanded edition</span><h1>Practical data analysis for <em>engineering decisions.</em></h1><p class="lede">From a surprising result to a better next experiment. Learn to measure, compare, explain, and decide, with a complete scheduler investigation you can reproduce.</p><div class="buttonrow"><a class="button" href="{chapter_link(PAGES[0])}">Start reading →</a><a class="button secondary" href="labs/index.html">Try an interactive lab</a></div></div><div class="covercard"><img src="assets/cover.png" alt="Puma front cover for Practical Data Analysis for Engineering Decisions" width="1102" height="1427"></div></section><div class="stats"><div class="stat"><strong>18 chapters</strong>A practical route from question to decision</div><div class="stat"><strong>{len(LABS)} live labs</strong>Change assumptions. See what changes.</div><div class="stat"><strong>Reproducible</strong>Download the data and Python companion</div></div><section class="section" id="contents"><div class="sectionhead"><div><span class="eyebrow">The book</span><h2>Build an evidence chain.</h2></div><p>Read in order for the full investigation, or jump to the question you are working on.</p></div><div class="chaptergrid">{cards}</div></section><section class="section"><div class="sectionhead"><div><span class="eyebrow">Learn by changing one thing</span><h2>Make the math tangible.</h2></div><p>Small, transparent experiments in your browser. No installation, accounts, or backend required.</p></div><div class="labgrid">{labcards}</div></section><section class="evidence"><div><h2>Know what the evidence is.</h2><p>The scheduler case uses measured Python-simulator reports and event traces. It is not a real-device benchmark. Agent and research examples are explicitly synthetic.</p></div><div><h2>Keep the work inspectable.</h2><p>Read the <a href="sources.html">sources and evidence notes</a>, inspect the input tables in each lab, or <a href="downloads.html">download the companion</a> to rerun the analysis yourself.</p></div></section></div></main>'''
(DOCS/'index.html').write_text(shell(TITLE,body))
(DOCS/'labs/index.html').write_text(shell('Interactive labs',f'<main class="wrap section" id="main"><span class="eyebrow">Hands-on learning</span><h1>Interactive labs</h1><p class="lede">The same examples are embedded in the relevant chapters. Try a change, inspect the result, and explain what the example cannot establish.</p><div class="labgrid">{labcards.replace("labs/","")}</div></main>','../'))
for kind,v in LABS.items():
 ch=next(p for p in PAGES if kind in EMBEDS.get(p['n'],[]))
 body=f'<main class="labpage" id="main"><span class="eyebrow">Interactive lab</span><h1>{v[0]}</h1><p><a href="../chapters/{ch["slug"]}.html#lab-{kind}">Read this example in chapter {ch["n"]} →</a></p>{lab(kind)}<p class="notice">Your changes stay in this page. Nothing is uploaded or saved. Reloading restores the original example.</p></main>'
 (DOCS/'labs'/f'{kind}.html').write_text(shell(v[0],body,'../'))
(DOCS/'sources.html').write_text(shell('Sources and evidence','<main id="main" class="labpage prose">'+render_md((SOURCE/'references.md').read_text())+'</main>'))
files=[('practical_data_analysis_for_engineering_decisions.pdf','Read the PDF','The complete 100-page expanded book, including its figures.'),('engineering_analytics_book_companion.zip','Get the reproducible companion','Markdown chapters, analysis code, input snapshot, figures, and integrity checks.'),('practical_data_analysis_for_engineering_decisions.md','Get the editable manuscript','Plain-text Markdown. Figures are included in the companion archive.'),('practical-data-analysis-offline.zip','Take the interactive site offline','Unzip and open index.html. All browser labs work locally. PDF/companion downloads and external references still need a connection.')]
body='<main id="main" class="labpage"><span class="eyebrow">Keep a copy</span><h1>Read, reproduce, and work offline.</h1><p class="lede">The PDF is self-contained. To rerun the Python analysis, extract the companion and follow its README. The interactive website needs only a browser.</p><div class="downloadlist">'+''.join(f'<a href="downloads/{f}" download><strong>{title} ↓</strong><span>{desc}</span></a>' for f,title,desc in files)+'</div><p class="notice">Companion: Python 3.12.14, NumPy 2.3.5, pandas 2.2.3, matplotlib 3.10.8 were used for the verified run. Create a separate environment rather than replacing unrelated project dependencies.</p></main>'
(DOCS/'downloads.html').write_text(shell('Downloads',body))
(DOCS/'404.html').write_text(shell('Page not found','<main id="main" class="labpage"><h1>This page isn’t here.</h1><p>Use the book navigation to find a chapter or lab.</p><a class="button" href="https://mrscripty.github.io/practical-data-analysis/">Go to the book</a></main>'))
(DOCS/'.nojekyll').touch()
(DOCS/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#152f32"/><text x="20" y="30" text-anchor="middle" font-size="31" fill="#faf8f2" font-family="serif">∑</text></svg>')
shutil.copytree(SOURCE/'figures',DOCS/'assets/figures',dirs_exist_ok=True)
# Statically rendered social metadata for crawlers that do not run JavaScript.
PUBLIC='https://mrscripty.github.io/practical-data-analysis/'
COVER=PUBLIC+'assets/cover.png'
DESC='An interactive book by Puma: 18 practical chapters, nine browser labs, and reproducible examples spanning engineering, vectors, images, GIS, finance, and uncertainty.'
ALT='Puma book cover for Practical Data Analysis for Engineering Decisions: mountain contours, a river, pixels, and analytical plots.'
for page in DOCS.rglob('*.html'):
 raw=page.read_text();rel=page.relative_to(DOCS).as_posix();canonical=PUBLIC+('' if rel=='index.html' else rel)
 page_title=html.unescape(re.search(r'<title>(.*?)</title>',raw)[1])
 share_title=TITLE if rel=='index.html' else page_title
 tags=[f'<link rel="canonical" href="{canonical}">',f'<meta property="og:type" content="website">',f'<meta property="og:site_name" content="{a(TITLE)}">',f'<meta property="og:title" content="{a(share_title)}">',f'<meta property="og:description" content="{a(DESC)}">',f'<meta property="og:url" content="{canonical}">',f'<meta property="og:image" content="{COVER}">',f'<meta property="og:image:secure_url" content="{COVER}">','<meta property="og:image:type" content="image/png">','<meta property="og:image:width" content="1102">','<meta property="og:image:height" content="1427">',f'<meta property="og:image:alt" content="{a(ALT)}">','<meta name="twitter:card" content="summary_large_image">',f'<meta name="twitter:title" content="{a(share_title)}">',f'<meta name="twitter:description" content="{a(DESC)}">',f'<meta name="twitter:image" content="{COVER}">',f'<meta name="twitter:image:alt" content="{a(ALT)}">']
 raw=raw.replace('</head>',''.join(tags)+'</head>');page.write_text(raw)

with zipfile.ZipFile(DOCS/'downloads/practical-data-analysis-offline.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in DOCS.rglob('*'):
  if not p.is_file() or p.suffix in ['.zip','.pdf']:continue
  if p.name=='downloads.html':
   offline=p.read_text().replace('href="downloads/','href="https://mrscripty.github.io/practical-data-analysis/downloads/')
   z.writestr('downloads.html',offline)
  else:z.write(p,p.relative_to(DOCS))
print(json.dumps({'chapters':len(PAGES),'labs':len(LABS),'html_pages':len(list(DOCS.rglob('*.html')))}))
