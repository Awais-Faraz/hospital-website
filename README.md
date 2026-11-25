# Hospital Website (SEO-optimised, static HTML)

Fast, mobile-friendly, 19-page hospital website. No database, no framework: works on any hosting (cPanel, Hostinger, Netlify, GitHub Pages, Cloudflare Pages).

## 1. Customise (5 minutes)
1. Open `config.json` and change: name, city, phone, emergency number, email, address, domain, social links, Google Maps link, latitude/longitude.
2. Run: `python build.py`  (Python 3 needed; this regenerates every page, sitemap.xml, robots.txt).
3. Edit doctors, departments, FAQs and blog posts in `build.py` (lists `DOCTORS`, `DEPTS`, `FAQS`, `POSTS` at the top), then run `python build.py` again.
4. Replace the placeholder doctor names and facts (beds, doctors, founded year) with your real data.
5. Optional: put real photos in `assets/img/` (use WebP, add `alt` text, `loading="lazy"`, `width` and `height`).
6. Replace the map box on `contact.html` with the Google Maps embed iframe (add `loading="lazy"`).

## 2. Upload
Upload everything except `build.py`, `config.json`, `README.md`, `SEO-GUIDE.md` to `public_html`. The `.htaccess` file gives HTTPS redirect, compression, caching and a 404 page (Apache). On Netlify/Cloudflare it is ignored safely.

## 3. Appointment form
The form opens WhatsApp with the patient's details prefilled (number from `whatsapp_raw`). For email delivery, connect a form service such as Formspree or Web3Forms.

## Included SEO features (On-page + Technical)
- Unique title + meta description, canonical URL, robots meta on every page
- One H1 per page, proper H2/H3 hierarchy, semantic HTML5, skip link, ARIA labels
- Open Graph + Twitter cards, og-image, favicon, apple-touch icon, web manifest
- Structured data (JSON-LD): Hospital/MedicalOrganization, BreadcrumbList, FAQPage, Article, ContactPage
- Local SEO: NAP (name, address, phone) in header/footer/contact, geo meta, opening hours schema, city keyword in titles/H1
- Dedicated page per department (keyword targeting) + health blog + FAQ page (long-tail keywords)
- Internal linking, breadcrumbs, descriptive anchor text
- sitemap.xml, robots.txt, 404 page (noindex)
- Speed: no frameworks, 1 small CSS + 1 small JS (deferred), system fonts, SVG graphics, gzip + caching rules
- Mobile-first responsive design, keyboard-visible focus, reduced-motion support, good contrast

Off-page SEO cannot be put in code. Follow `SEO-GUIDE.md`.
