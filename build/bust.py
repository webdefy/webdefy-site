# Add ?v=<content hash> to CSS/JS links so browsers fetch new versions after each change
import os,re,hashlib
R=os.path.dirname(os.path.abspath(__file__)) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'assets')) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H={}
for f in ['tokens.css','components.css','site.css','forms.js']:
    p=os.path.join(R,'assets',f)
    if os.path.exists(p): H[f]=hashlib.sha1(open(p,'rb').read()).hexdigest()[:8]
for r,d,fs in os.walk(R):
    if '.git' in r: continue
    for x in fs:
        if not x.endswith('.html'): continue
        p=os.path.join(r,x); s=open(p).read()
        s2=re.sub(r'(assets/(tokens\.css|components\.css|site\.css|forms\.js))(\?v=[0-9a-f]+)?"', lambda m: f'{m.group(1)}?v={H[m.group(2)]}"', s)
        if s2!=s: open(p,'w').write(s2)
print(H)
