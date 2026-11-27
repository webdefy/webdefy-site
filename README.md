# webdefy.com

Static site. Deployed by Vercel on every push to `main`; DNS on Cloudflare.

- Pages: `/`, `/story`, `/work`, `/work-with-us`, `/contact`, `/rewind`, `/privacy`, `/terms`
- `vercel.json`: clean URLs, redirects, security headers, asset caching
- `assets/forms.js`: forms open an email to hello@webdefy.com (until a form backend is added)
- `build/`: scripts that render these pages from the design canvas
