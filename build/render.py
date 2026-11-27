# Render the Webdefy .dc.html designs to plain static HTML pages.
import json, os, re, subprocess, sys, html
from bs4 import BeautifulSoup, NavigableString, Tag

SRC = "/home/claude/rewind/canvas/project"
OUT = "/home/claude/site"

PAGES = {  # design file -> output path, canonical path
    "Home": ("index.html", "/"),
    "Story": ("story/index.html", "/story"),
    "Work": ("work/index.html", "/work"),
    "WorkWithUs": ("work-with-us/index.html", "/work-with-us"),
    "Contact": ("contact/index.html", "/contact"),
}
LINKMAP = {"Home.dc.html": "/", "Story.dc.html": "/story", "Work.dc.html": "/work", "WorkWithUs.dc.html": "/work-with-us",
           "Contact.dc.html": "/contact", "RewindProto.dc.html": "/rewind", "RewindYear.dc.html": "https://rewind.webdefy.com/2004"}

LEAF = "M50,0 H100 V50 A50,50 0 0 1 50,100 H0 V50 A50,50 0 0 1 50,0 Z"
W_PATH = re.search(r'var W_PATH = "([^"]+)"', open("/tmp/bundle.js").read()).group(1)

def mark(brand="webdefy", size=40, wordmark=False):
    size = int(size)
    if brand == "rewind":
        cx0, cy, w, hh = 48, 50, 50, 40; half = w / 2; x0 = cx0 - w / 2
        glyph = "".join(f'<polygon points="{a},{cy} {a+half},{cy-hh/2} {a+half},{cy+hh/2}" style="fill: var(--mark-glyph); stroke: var(--mark-glyph)" stroke-width="7" stroke-linejoin="round"></polygon>' for a in (x0, x0 + half))
    else:
        glyph = f'<path d="{W_PATH}" style="fill: var(--mark-glyph)"></path>'
    if size < 28: glyph = ""
    aria = 'aria-hidden="true"' if wordmark else f'role="img" aria-label="{brand}"'
    svg = (f'<svg width="{size}" height="{size}" viewBox="0 0 116 116" {aria} style="display: block; flex-shrink: 0">'
           f'<path d="{LEAF}" transform="translate(0 16)" style="fill: var(--mark-edge)"></path>'
           f'<path d="{LEAF}" transform="translate(16 0)" style="fill: var(--mark-leaf)"></path>'
           f'<g transform="translate(16 0)">{glyph}</g></svg>')
    if not wordmark: return svg
    return f'<span class="wd-mark" role="img" aria-label="{brand}">{svg}<span class="wd-mark__word" style="font-size: {round(size*0.98)}px">{brand}</span></span>'

def ev(expr, scope):
    e = expr.strip()
    if e in ("true", "false"): return e == "true"
    if re.fullmatch(r"-?\d+(\.\d+)?", e): return float(e) if "." in e else int(e)
    if re.fullmatch(r"'[^']*'|\"[^\"]*\"", e): return e[1:-1]
    cur = scope
    for part in e.split("."):
        if isinstance(cur, dict) and part in cur: cur = cur[part]
        else: return None
    return cur

def subst(s, scope):
    m = re.fullmatch(r"\s*\{\{(.+?)\}\}\s*", s)
    if m: return ev(m.group(1), scope)
    return re.sub(r"\{\{(.+?)\}\}", lambda mm: "" if ev(mm.group(1), scope) is None else str(ev(mm.group(1), scope)), s)

def fix_href(v):
    if not isinstance(v, str): return v
    base, _, frag = v.partition("#")
    if base in LINKMAP:
        t = LINKMAP[base]
        return t + ("#" + frag if frag else "")
    return v

def render_children(node, scope, soup):
    out = []
    for ch in list(node.children):
        out.extend(render(ch, scope, soup))
    return out

def render(node, scope, soup):
    if isinstance(node, NavigableString):
        if node.__class__.__name__ in ("Comment",): return []
        t = str(node)
        return [NavigableString(subst(t, scope) if "{{" in t else t)] if "{{" not in t or subst(t, scope) is not None else []
    if not isinstance(node, Tag): return []
    name = node.name
    if name == "sc-if":
        v = subst(node.get("value", ""), scope)
        return render_children(node, scope, soup) if v else []
    if name == "sc-for":
        lst = subst(node.get("list", ""), scope) or []
        asn = node.get("as", "item"); out = []
        for it in lst:
            sc = dict(scope); sc[asn] = it
            out.extend(render_children(node, sc, soup))
        return out
    if name == "dc-import":
        return [BeautifulSoup(PHONE, "html.parser")]
    if name == "x-import":
        comp = node.get("component-from-global-scope", "").split(".")[-1]
        a = {k: subst(v, scope) if isinstance(v, str) else v for k, v in node.attrs.items()}
        inner = "".join(str(x) for x in render_children(node, scope, soup))
        cls = a.get("class-name") or ""
        if comp == "Mark":
            return [BeautifulSoup(mark(a.get("brand", "webdefy"), a.get("size") or 40, bool(a.get("wordmark"))), "html.parser")]
        if comp == "Button":
            v = a.get("variant", "cta"); c = f'wd-btn wd-btn--{v}' + (" wd-btn--sm" if a.get("size") == "sm" else "") + (" " + cls if cls else "")
            href = fix_href(a.get("href"))
            if not href and "on-click" in node.attrs: href = "mailto:hello@webdefy.com?subject=Talk%20to%20Webdefy"
            st = f' style="{a["style"]}"' if a.get("style") else ""
            if href: return [BeautifulSoup(f'<a class="{c}" href="{href}"{st}>{inner}</a>', "html.parser")]
            return [BeautifulSoup(f'<button type="button" class="{c}"{st}>{inner}</button>', "html.parser")]
        if comp == "LeafPanel":
            tone = a.get("tone", "sub-a"); tag = a.get("as") or "section"
            title = a.get("title"); eb = a.get("eyebrow")
            ht = "h1" if tone == "hero" else "h2"
            s = f'<{tag} class="wd-leaf wd-leaf--{tone}{(" " + cls) if cls else ""}"' + (f' style="{a["style"]}"' if a.get("style") else "") + ">"
            if eb: s += f'<span class="wd-leaf__eyebrow">{html.escape(eb)}</span>'
            if title: s += f'<{ht} class="wd-leaf__title">{html.escape(title)}</{ht}>'
            if inner.strip(): s += f'<div class="wd-leaf__body">{inner}</div>'
            s += f"</{tag}>"
            return [BeautifulSoup(s, "html.parser")]
        if comp == "SiteFooter":
            links = a.get("links") or []; legal = a.get("legal") or []
            line = html.escape(a.get("line") or "We started young & creative.\nWe choose to stay the same.")
            meta = html.escape(a.get("meta") or "Since 2012 · remote, worldwide")
            ln = "".join(f'<a href="{fix_href(l.get("href"))}">{html.escape(l.get("label",""))}</a>' for l in links)
            lg = "".join(f'<a href="{fix_href(l.get("href"))}">{html.escape(l.get("label",""))}</a>' for l in legal)
            return [BeautifulSoup(f'<footer class="wd-footer" data-theme="webdefy-dark"><div class="wd-footer__top"><img class="wd-footer__faces" src="/assets/img/faces.svg" alt=""><div><p class="wd-footer__line">{line}</p><div class="wd-footer__meta">{meta}</div></div></div><div class="wd-footer__links"><nav aria-label="Footer">{ln}</nav><nav aria-label="Legal">{lg}</nav></div></footer>', "html.parser")]
        if comp == "StoryCard":
            return [BeautifulSoup(story_card(a.get("date", ""), a.get("event", ""), a.get("category")), "html.parser")]
        return render_children(node, scope, soup)
    # ordinary element
    new = soup.new_tag(name)
    for k, v in node.attrs.items():
        if k.startswith("on") or k.startswith("hint-"): continue
        if isinstance(v, list): v = " ".join(v)
        val = subst(v, scope) if isinstance(v, str) and "{{" in v else v
        if val is None or val is False: continue
        if val is True: val = "true"
        if k == "href": val = fix_href(val)
        if k == "classname": k = "class"
        new[k] = str(val)
    for x in render_children(node, scope, soup): new.append(x)
    return [new]

def story_card(date, event, cat):
    return (f'<article class="wd-story"><div class="wd-story__top"><span class="wd-story__date">{html.escape(date)}</span>'
            + (f'<span class="wd-story__cat">{html.escape(cat)}</span>' if cat else "") +
            f'</div><p class="wd-story__event">{html.escape(event)}</p></article>')

PHONE = ('<div class="ws-phone" aria-label="A year in Rewind, on a phone"><div class="ws-phone__screen" data-theme="rewind">'
         '<div class="ws-phone__bar">' + mark("rewind", 28) + '<span>Your Rewind</span></div>'
         '<p class="ws-phone__year">2004</p><p class="ws-phone__age">You were 14.</p>'
         '<p class="ws-phone__intro">2004 was loud. Facebook, Gmail and an unbeaten Arsenal.</p>'
         + story_card("FEB 2004", "Facebook launches at Harvard from a dorm room.", "INTERNET")
         + story_card("APR 2004", "Gmail opens with 1 GB of free storage.", "INTERNET")
         + story_card("MAY 2004", "Arsenal finish the league season unbeaten: 26 wins, 12 draws.", "ARSENAL")
         + '</div></div>')

def values(fname):
    src = open(f"{SRC}/{fname}.dc.html").read()
    m = re.search(r'<script type="text/x-dc" data-dc-script[^>]*>(.*?)</script>', src, re.S)
    js = m.group(1)
    prog = ("class DCLogic{constructor(p){this.props=p||{};this.state={}}setState(u){Object.assign(this.state,u)}};" + js +
            ";var c=new Component({dark:false});var v=c.renderVals();console.log(JSON.stringify(v,(k,x)=>typeof x==='function'?null:x));")
    open("/tmp/r.js", "w").write(prog)
    r = subprocess.run(["node", "/tmp/r.js"], capture_output=True, text=True)
    if r.returncode: raise SystemExit(fname + ": " + r.stderr[-800:])
    return json.loads(r.stdout.strip().splitlines()[-1]), src

def build(fname, out, canon, meta):
    vals, src = values(fname)
    css = "\n".join(re.findall(r"<helmet>\s*<style>(.*?)</style>\s*</helmet>", src, re.S))
    body = re.search(r"<x-dc>(.*)</x-dc>", src, re.S).group(1)
    body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S)
    soup = BeautifulSoup(body, "html.parser")
    rendered = "".join(str(x) for x in render_children(soup, vals, soup))
    rendered = rendered.replace('<form style="display: flex;', '<form name="ai-crm-waitlist" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="company" style="display: flex;', 1)
    rendered = rendered.replace('<input aria-describedby="wh-wait-note"', '<input type="hidden" name="form-name" value="ai-crm-waitlist"><input name="email" type="email" aria-describedby="wh-wait-note"', 1)
    rendered = re.sub(r'<a href="#">Privacy</a>', '<a href="/privacy">Privacy</a>', rendered)
    rendered = re.sub(r'<a href="#">Terms</a>', '<a href="/terms">Terms</a>', rendered)
    rendered = rendered.replace("/_blob/a566e288d20aba2c4f384005a5053e4d", "/assets/img/faces.svg").replace("/_blob/18676ab0649745b5ca233dc098231767", "/assets/img/tiger-analytics.svg")
    rendered = re.sub(r'/_blob/([0-9a-f]{32})', r'/assets/img/\1.png', rendered)
    if fname == "Contact": rendered = rendered.replace("</main>", CONTACT_FORM + "</main>", 1)
    title, desc = meta
    depth = out.count("/")
    page = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://webdefy.com{canon}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="https://webdefy.com{canon}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#16151a">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/Geist-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/InstrumentSerif-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/tokens.css">
<link rel="stylesheet" href="/assets/components.css">
<link rel="stylesheet" href="/assets/site.css">
<style>{css}</style>
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Webdefy", "url": "https://webdefy.com", "email": "hello@webdefy.com", "logo": "https://webdefy.com/assets/favicon.svg", "founder": [{"@type": "Person", "name": n} for n in ("Maharaj", "Mohanavigneshwaran", "Russel")]})}</script>
</head>
<body data-theme="webdefy">
{rendered}
</body>
</html>
'''
    os.makedirs(os.path.dirname(f"{OUT}/{out}") or OUT, exist_ok=True)
    open(f"{OUT}/{out}", "w").write(page)
    return len(page)

CONTACT_FORM = """<section id="message" style="max-width: 1200px; margin: 0 auto; padding: 0 20px 72px; box-sizing: border-box">
<h2 style="font-family: var(--font-display); font-weight: 400; font-size: 40px; line-height: 44px; margin: 8px 0 16px">Or leave a message.</h2>
<form name="contact" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="company" class="ws-form">
<input type="hidden" name="form-name" value="contact">
<p hidden><label>Leave this empty <input name="company"></label></p>
<div class="wd-field"><label class="wd-field__label" for="c-name">Your name</label><input class="wd-field__input" id="c-name" name="name" autocomplete="name" required></div>
<div class="wd-field"><label class="wd-field__label" for="c-email">Email</label><input class="wd-field__input" id="c-email" name="email" type="email" autocomplete="email" required></div>
<div class="wd-field"><label class="wd-field__label" for="c-msg">What are you building, and when do you want to launch?</label><textarea class="wd-field__input" id="c-msg" name="message" rows="5" required style="height: auto; padding-top: 12px; padding-bottom: 12px"></textarea></div>
<p style="margin: 0; font-size: 14px; line-height: 20px; color: var(--ink-muted)">We use your details only to reply. See <a href="/privacy">Privacy</a>.</p>
<button type="submit" class="wd-btn wd-btn--cta">Send message</button>
</form></section>"""

META = {
    "Home": ("Webdefy: we grew up on the web. Now we rewind it.", "Webdefy builds AI products, starting with Rewind: the internet you grew up with, one year at a time. Plus governed AI rollout for business."),
    "Story": ("Our story · Webdefy", "Webdefy started young and creative in Chennai in 2012, built apps, websites, CRM and e-commerce, and is back as an AI-first studio."),
    "Work": ("Work · Webdefy", "Apps, websites, CRM and e-commerce platforms Webdefy has built for clients."),
    "WorkWithUs": ("Work with us · Webdefy", "Governed AI rollout for business: agentic systems, LLMs, RAG, MCP and evals, built so they can be trusted."),
    "Contact": ("Get in touch · Webdefy", "Talk to Webdefy about Rewind, AI products or a governed AI rollout. hello@webdefy.com"),
}
if __name__ == "__main__":
    for f, (out, canon) in PAGES.items():
        print(f, out, build(f, out, canon, META[f]))
