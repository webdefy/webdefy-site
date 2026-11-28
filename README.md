# webdefy.com

Static site. Deployed by Vercel on every push to `main`; DNS on Cloudflare.

- Pages: `/`, `/story`, `/work`, `/work-with-us`, `/contact`, `/rewind`, `/privacy`, `/terms`
- `vercel.json`: clean URLs, redirects, security headers, asset caching
- `assets/forms.js`: forms open an email to hello@webdefy.com (until a form backend is added)
- `build/`: scripts that render these pages from the design canvas; run `python3 build/bust.py` after any CSS or JS change
- After building, run `python3 build/seo_head.py` (icons, share image, logo) then `python3 build/bust.py`
