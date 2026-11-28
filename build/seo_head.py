# Adds icons, share image and PNG logo to every page. Safe to run repeatedly.
import os,re
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGS='''<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/icons/icon-96.png" type="image/png" sizes="96x96">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<meta property="og:image" content="https://webdefy.com/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Webdefy: we grew up on the web. Now we rewind it.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://webdefy.com/assets/img/og-image.png">'''
n=0
for r,d,fs in os.walk(R):
    if '.git' in r or '/build' in r: continue
    for x in fs:
        if not x.endswith('.html'): continue
        p=os.path.join(r,x); s=open(p).read()
        s=re.sub(r'<link rel="(icon|apple-touch-icon)"[^>]*>\n?','',s)
        s=re.sub(r'<meta (property="og:image[^"]*"|name="twitter:(card|image)")[^>]*>\n?','',s)
        s=s.replace('</head>',TAGS+'\n</head>',1)
        s=s.replace('"logo": "https://webdefy.com/assets/favicon.svg"','"logo": "https://webdefy.com/assets/icons/logo-512.png"')
        open(p,'w').write(s); n+=1
print(n,'pages')
