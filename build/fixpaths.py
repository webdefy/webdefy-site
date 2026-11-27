import os,re
for r,d,f in os.walk('/home/claude/site'):
    for x in f:
        if not x.endswith('.html') or x=='404.html': continue
        p=os.path.join(r,x); rel=os.path.relpath(p,'/home/claude/site'); depth=rel.count('/')
        pre='../'*depth
        s=open(p).read()
        s=re.sub(r'(href|src)="/assets/', lambda m: f'{m.group(1)}="{pre}assets/', s)
        open(p,'w').write(s)
