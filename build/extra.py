# Extra pages and site files for webdefy.com
import json, os, re, html
from render import mark

OUT = "/home/claude/site"
SRC = open(f"{OUT}/story/index.html").read().replace('="../assets/', '="/assets/')
HEAD = SRC
STYLE_LINKS = """<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/tokens.css">
<link rel="stylesheet" href="/assets/components.css">
<link rel="stylesheet" href="/assets/site.css">""" + "\n" + "\n".join(re.findall(r'<style[^>]*>.*?</style>', SRC, re.S))
FOOTER = re.search(r'<div class="wh-wrap" style="padding-bottom: 32px">\s*<footer class="wd-footer".*?</footer>\s*</div>', SRC, re.S).group(0)
HEADER = re.search(r'<header class="wh-wrap".*?</header>', SRC, re.S).group(0)
BODY_OPEN = re.search(r'<body[^>]*>\s*(<div data-theme="webdefy"[^>]*>)', SRC, re.S).group(1)

def page(path, title, desc, body, noindex=False):
    canon = "/" + path.replace("index.html", "").rstrip("/") if path != "404.html" else "/404"
    doc = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="https://webdefy.com{canon}">'}
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta name="theme-color" content="#16151a">
{STYLE_LINKS}
</head>
<body data-theme="webdefy">
{BODY_OPEN}
{HEADER}
<main class="ws-legal">
{body}
</main>
{FOOTER}
</div>
</body>
</html>
"""
    full = f"{OUT}/{path}"
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(doc)

page("rewind/index.html", "Rewind · the internet you grew up with", "Rewind shows you the internet you grew up with, one year at a time, then turns it into one good thing to do this week. Join the waitlist.", """
<p class="ws-eyebrow">Rewind · by Webdefy</p>
<h1>The internet you grew up with, one year at a time.</h1>
<p>Pick your birth year and Rewind walks you through the moments that shaped your internet, with your age on every card. Then it turns what you loved into one good thing to do this week, and it ends. No feed, no scrolling.</p>
<ul class="ws-list"><li><strong>Look back:</strong> your years, the moments you remember, hearted in one tap.</li><li><strong>Notice what was good:</strong> what went well this week, built from what you actually did.</li><li><strong>Do one thing:</strong> a plan with people, from your own past. Say it or type it.</li></ul>
<h2>Rewind opens in early 2027.</h2>
<p>Join the waitlist and we'll send one email when it's ready. Nothing else.</p>
<form name="rewind-waitlist" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="company" class="ws-form">
<input type="hidden" name="form-name" value="rewind-waitlist">
<p hidden><label>Leave this empty <input name="company"></label></p>
<div class="wd-field"><label class="wd-field__label" for="w-email">Email</label><input class="wd-field__input" id="w-email" name="email" type="email" autocomplete="email" required></div>
<div class="wd-field"><label class="wd-field__label" for="w-uni">University or city (optional)</label><input class="wd-field__input" id="w-uni" name="where" autocomplete="off"></div>
<p class="ws-small">We use your email only to tell you when Rewind opens. See <a href="/privacy">Privacy</a>.</p>
<button type="submit" class="wd-btn wd-btn--cta">Join the waitlist</button>
</form>""")

page("thanks/index.html", "Thank you · Webdefy", "Thanks for getting in touch.", """
<h1>Thank you.</h1>
<p>We've got it. If you joined a waitlist, we'll send one email when it opens. If you sent a message, we'll reply from hello@webdefy.com.</p>
<p><a class="wd-btn wd-btn--secondary" href="/">Back to webdefy.com</a></p>""", noindex=True)

page("privacy/index.html", "Privacy · Webdefy", "How Webdefy handles the details you share on webdefy.com.", """
<h1>Privacy</h1>
<p class="ws-small">Last updated 27 November 2026</p>
<p>This page covers webdefy.com. Rewind will have its own privacy notice when it opens.</p>
<h2>What we collect</h2>
<ul class="ws-list"><li>What you type into a form: your email, and for messages your name and what you write.</li><li>Nothing else. We don't use advertising trackers or analytics cookies on this site.</li></ul>
<h2>Why we use it</h2>
<p>Only to reply to you, or to send the one email you asked for when a waitlist opens. We never sell or share your details for marketing.</p>
<h2>Where it's kept</h2>
<p>Form entries are stored by our hosting provider, which processes them for us, and in our email. We delete waitlist emails once the product opens and you've been told, unless you sign up. Messages are kept for as long as we're talking, then up to two years.</p>
<h2>Your rights</h2>
<p>You can ask to see, correct or delete what we hold about you at any time. Email <a href="mailto:hello@webdefy.com">hello@webdefy.com</a>. If you're in the UK and unhappy with how we've handled it, you can complain to the Information Commissioner's Office (ico.org.uk).</p>""")

page("terms/index.html", "Terms · Webdefy", "Terms for using webdefy.com.", """
<h1>Terms</h1>
<p class="ws-small">Last updated 27 November 2026</p>
<p>webdefy.com tells you about Webdefy, our products and our work. You're welcome to read, share and link to it.</p>
<h2>Products shown here</h2>
<p>Products marked "coming soon" aren't available yet, and what they do may change before they open. Each product will have its own terms.</p>
<h2>Client work</h2>
<p>Client names and logos are shown with their permission. They remain the property of their owners.</p>
<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:hello@webdefy.com">hello@webdefy.com</a>.</p>""")

page("404.html", "Page not found · Webdefy", "This page doesn't exist.", """
<h1>This page isn't here.</h1>
<p>The link may be old, or the page may have moved.</p>
<p><a class="wd-btn wd-btn--cta" href="/">Go to webdefy.com</a> <a class="wd-btn wd-btn--secondary" href="/rewind">See Rewind</a></p>""", noindex=True)

open(f"{OUT}/assets/favicon.svg", "w").write(mark("webdefy", 64).replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ').replace("var(--mark-edge)", "#ffbc06").replace("var(--mark-leaf)", "#16151a").replace("var(--mark-glyph)", "#ffffff"))

urls = ["/", "/rewind", "/work-with-us", "/work", "/story", "/contact", "/privacy", "/terms"]
open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>https://webdefy.com{u}</loc><lastmod>2026-11-27</lastmod></url>\n" for u in urls) + "</urlset>\n")
open(f"{OUT}/robots.txt", "w").write("User-agent: *\nAllow: /\nDisallow: /thanks/\n\nSitemap: https://webdefy.com/sitemap.xml\n")
open(f"{OUT}/llms.txt", "w").write("""# Webdefy

> Webdefy is a remote, AI-first studio, started in Chennai in 2012 by Maharaj, Mohanavigneshwaran and Russel. Its first AI product for everyone is Rewind.

## Products
- [Rewind](https://webdefy.com/rewind): the internet you grew up with, one year at a time, turned into one good thing to do this week. Opens in early 2027.
- AI CRM: coming soon.
- AI E-com: coming soon.

## Services
- [Governed AI Rollout for Business](https://webdefy.com/work-with-us): agentic systems, LLMs, RAG, MCP and evals, taken from pilot to production with a human in the loop.

## Company
- [Story](https://webdefy.com/story)
- [Work](https://webdefy.com/work): apps, websites, CRM and e-commerce platforms built for clients.
- [Contact](https://webdefy.com/contact): hello@webdefy.com
""")
open(f"{OUT}/_redirects", "w").write("/home  /  301\n/about  /story  301\n/services  /work-with-us  301\n/clients  /work  301\n/start  /rewind  302\n")
open(f"{OUT}/netlify.toml", "w").write("""[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
""")
print("ok")
