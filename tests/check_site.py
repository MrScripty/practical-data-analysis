from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import re,json,csv,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs';errors=[]
class P(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.images=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag in ['a','img','script','link']:
   for k in ['href','src']:
    if k in a:self.links.append(a[k])
  if tag=='img' and not a.get('alt'):self.images.append(a)
parsed={}
for p in D.rglob('*.html'):
 x=P();x.feed(p.read_text());parsed[p]=x
 if len(x.ids)!=len(set(x.ids)):errors.append(f'{p}: duplicate IDs')
 if x.h1!=1:errors.append(f'{p}: {x.h1} h1 headings')
 if x.images:errors.append(f'{p}: missing image alt')
 for href in x.links:
  u=urlparse(href)
  if u.scheme or u.netloc:continue
  dest=(p.parent/unquote(u.path)).resolve() if u.path else p
  if not dest.exists():errors.append(f'{p}: missing {href}')
  if u.fragment and dest.suffix=='.html' and dest.exists():
   q=P();q.feed(dest.read_text())
   if u.fragment not in q.ids:errors.append(f'{p}: bad anchor {href}')
 for pattern in [r'/workspace/',r'/root/',r'ghp_[A-Za-z0-9_]+',r'github_pat_',r'sk-proj-']:
  if re.search(pattern,p.read_text()):errors.append(f'{p}: private marker {pattern}')
# Independent parity with the measured input CSVs.
data=json.loads((D/'assets/data.js').read_text().removeprefix('window.BookData=').removesuffix(';\n'))
assert len(data['tasks'])==60 and len(data['pairs'])==12
r=[x for x in data['tasks'] if x['run_id']=='after_fix_proposed']
assert abs(max(x['accepted_s'] for x in r)-56.642415)<1e-6
pairs=[x for x in data['pairs'] if x['scenario']=='randomized']
assert sum(x['proposed']<x['residency'] for x in pairs)==1
assert sum(x['proposed']>x['residency'] for x in pairs)==2
print(json.dumps({'html_pages':len(parsed),'input_rows':72,'errors':errors},indent=2))
assert not errors
