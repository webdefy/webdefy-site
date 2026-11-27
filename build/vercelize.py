import os,re
R='/home/claude/site'
for r,d,f in os.walk(R):
  for x in f:
    if not x.endswith('.html'): continue
    p=os.path.join(r,x); s=open(p).read()
    if 'data-netlify' not in s: continue
    s=s.replace('data-netlify="true" netlify-honeypot="company"','data-mailto')
    s=re.sub(r'<input type="hidden" name="form-name"[^>]*>','',s)
    depth=os.path.relpath(p,R).count('/')
    s=s.replace('</body>',f'<script src="{"../"*depth}assets/forms.js" defer></script>\n</body>')
    open(p,'w').write(s)
