# Building Repair Centre: discovery (12 Oct 2026)

> Findings before the build. The owner's decisions that followed (contact details, claims left out,
> `/commercial/` as the canonical URL, photo exclusions) are recorded in `docs/MIGRATION-NOTES.md`.

Source: the cPanel backup `backup-10.9.2026_19-00-52_roofcent`, kept read-only at
`C:\HostingerWebsites\roofcentre\reference\extracted\`. It is not copied into this project.

## Confirmed domain, database and files

| Item | Value | Evidence |
|---|---|---|
| Domain | `buildingrepaircentre.com.au` (canonical `www.`) | `wp_options` siteurl/home = `http://www.buildingrepaircentre.com.au`, blogname "Building Repair Centre" |
| Database | **`roofcent_wp2`**, prefix `wp_` | `public_html/buildingrepaircentre.com.au/wp-config.php` → `DB_NAME roofcent_wp2` |
| Not this site | `roofcent_wp1` = Roof Centre, `roofcent_wp3` = Pergola Building Centre | their own `wp-config.php` files |
| Site files | `homedir/public_html/buildingrepaircentre.com.au/` (a copy also exists under `homedir/restore/`) | cPanel `userdata`: document root `/home1/roofcent/public_html/buildingrepaircentre.com.au` |
| Hosting | cPanel **addon domain** on the `roofcent` account (Crazy Domains, `103.20.200.233`) | `addons`, `userdata` |
| Theme | VW Construction Estate Pro. Pages were built in Elementor | `template` option, `_elementor_data` |

The Elementor, Contact Form 7, Yoast, Site Reviews and Header/Footer plugins have been moved to
`wp-content/plugins_`, so they are **disabled**. Only the 2026 homepage (`/home-2/`, block editor)
renders as designed. The other pages show unstyled fallback text, and the contact form shows a raw
shortcode.

**Live site check:** at 12 Oct 2026 08:32 AEDT, `https://www.buildingrepaircentre.com.au/` and
every page tested returned **503 Service Unavailable** from Apache on `103.20.200.233`. This
included `robots.txt`.

## Pages (published)

| URL | Title | Content state |
|---|---|---|
| `/` (page `/home-2/`, Sept 2026) | Home | Hero, intro, 6 service cards, "Why choose us", 6 completed-work photos, call to action |
| `/about-us/` | About Us | 3 paragraphs |
| `/services/` | Services | **empty** (menu parent only) |
| `/insurance-building/` | Insurance Building | 2 paragraphs + 4 bullet points |
| `/strata-real-estate-maintenance/` | Strata & Real Estate Maintenance | 2 paragraphs + 4 bullets (mentions "Aust Building") |
| `/commnercial/` (misspelt) | Commercial | 3 paragraphs + 5 bullets |
| `/residential/` | Residential | 2 paragraphs + 9 bullets |
| `/tradie-services/` | Tradie Services | 21 trades (titles and icons only) |
| `/projects/` | Projects | intro + 18 photos, no captions |
| `/faq/` | FAQ | 6 questions |
| `/contact-us/` | Contact Us | heading + broken CF7 form |
| `/downloads/`, `/leave-a-review/` | | **empty** |
| `/home/` (2022 Elementor home), `/sample-page/`, `/hello-world/` | | old/placeholder |
| `/privacy-policy/` | | draft, WordPress template |

Menus:
- Primary: Home, About Us, Projects, Services (Insurance Building, Strata & Real Estate
  Maintenance, Commercial, Residential, Tradie Services), FAQ, Contact Us.
- The header also links to Roof Centre.

## Services (from the existing content)

- **Insurance Building:** 24-hour emergency make safe, building maintenance, all repair jobs, all trade services.
- **Strata & Real Estate Maintenance:** exterior and interior building services, work with tenants,
  landlords and strata communities.
- **Commercial:** project management, building maintenance, office fit-out, development &
  subdivision, all trade services.
- **Residential:** project management, maintenance, bathroom and house renovation, new homes, decks &
  pergolas, development & subdivision, granny flats, trade services.
- **Tradie Services (21):**
  - Carpentry, painting, electrical, plastering, rubbish removal, plumbing & drainage, concreting,
    waterproofing, landscaping, guttering
  - Tiling, roofing, joinery, scaffolding, cleaning, flooring, bricklaying, aluminium windows &
    doors, rendering, fencing
- **FAQ** also lists: garage doors, air-conditioning, insulation; and clients including insurers,
  strata, builders, real estate, colleges/schools/universities, and private and government projects.

## Contact details and form recipients

| Item | Value | Where |
|---|---|---|
| Phone (current) | **0431 848 619** | header, footer, 2026 home (the same number as Roof Centre) |
| Phones (2020 pages) | 0410 193 087, 02 8320 3060, 02 7209 9123 | service pages, Tradie page. **Confirm whether still valid** |
| Email shown | `info@buildingrepaircentre.com.au` | footer, header |
| Email link target | another company's address | footer `mailto:` (does not match the text shown) |
| Other email | `support@buildingrepaircentre.com.au` | Tradie Services "Email us" button |
| Hours | Monday–Friday 9 am–5 pm | header, footer, FAQ |
| Service area | "Servicing Sydney-wide" | header, footer |
| Address, ABN, licence no. | **none** anywhere | |
| Social | Facebook and LinkedIn links are `#` placeholders | footer |
| Form | CF7 "Contact form 1": name*, email*, subject, message | **recipient: an old admin address**, Reply-To the visitor. The plugin is disabled, so the form is not working |
| WordPress admin email | an old admin address | `admin_email` |
| Mail sending | GoSMTP active but **not configured** (no settings stored) | `wp_options` |

## Images

The uploads contain 266 originals (78 registered WordPress attachments). Nothing has camera
metadata, so the classification below is by content.

**Logo:**
- `2020/09/BRC-final-logo.png` (500×200, navy "BRC / BUILDING REPAIR CENTRE" with a house mark)
- `BRC-favicon.png` (512×512)

**Real job photos (use):**

| Set | Files | Size |
|---|---|---|
| Chipping Norton (deck/pergola) | `2020/09/chipping-norton-1600x1200-1.jpeg`, `2020/07/chipping-norton-1/2/4/6.png`, `2020/07/4.jpeg` | 1600×1200, 1200×500 |
| Camperdown (commercial shell fit-out) | `2020/09/camperdown-1600x1200-1.jpeg`, `2020/07/camperdown-1/3/4/6.png` | 1600×1195, 1200×500 |
| Redfern (apartment block) | `2020/07/redburn-1..4.png`, `2020/09/Redfern-*.png`, `2020/09/2.jpeg`, `strata.jpeg` | 1200×500, 640×480, 1600×1200 |
| College building (steel-frame) | `2020/07/College-1..4.png`, `2020/07/pic-1.png` | 1200×500, 640×480 |
| Lindfield (steel frame) | `2020/07/640x480.png` | 640×480 |
| Deck/pergola/roof build (Nov 2020) | `2020/11/1.jpeg` … `12.jpeg` | 1024×768 |
| Insurance (tree on roof, fallen tree) | `2020/09/Insurance_1024.png`, `2020/09/6.jpeg`, `2020/06/insurance.jpeg` | 1024–1276 |
| Commercial café fit-out | `2020/09/Commercial_1024.png`, `2020/06/commercial.jpeg` | 1024–1600 |
| Misc. jobs | `2020/09/8.jpeg` (tile roof skylight), `concrete.jpeg`, `12.jpeg`, `13.jpeg`, `rubbish-removal.jpeg` (skip bin), `2020/06/residential.jpeg` (hallway) | ≤1600 |

**Needs confirmation:**
- **Staff portraits** (Alex, Allen, Amir, Shahin in BRC shirts). Use only with permission.
- **"Neutral Bay"** (`pic.png`, Dair Salon) looks like a 3D render, not a completed-work photo.
- `residential-page2.jpg`, `tradie-services.jpg`, `insurance-building.jpg`, `fencings.jpeg` and
  `guttering.jpeg` (cat on gutter): 2400 px or stock-style. They may be stock.

**Excluded (stock or template):**
- Laptop, portrait, blueprints, city skylines, storms and lightning, star fields, torii gate,
  illustrations.
- Banner graphics with baked-in text, the 2018 theme demo images, client logos from the theme
  demo, and the "ABC Aust Building Construction & Renovation" logo.

The largest genuine photos are 1600 px wide, so heroes should use a framed (split) layout rather
than stretching photos across a full-width screen.

## Claims in the existing content that need confirmation

The existing content contains these claims. They will only be used once the business confirms they
are current:

| Claim | Source | Issue |
|---|---|---|
| $20,000,000 public liability insurance | FAQ (2020), 2026 home | confirm current policy |
| "more than 10-year track record with insurance companies", "A++ KPI on more than 500 jobs" | Insurance page (2020), 2026 home | dated 2020; confirm |
| "Building Works and Maintenance business for the past 15 years" | FAQ (2020) | conflicts with "10 years" |
| 24/7 / 24-hour emergency make safe | several pages | conflicts with Mon–Fri 9–5 hours |
| "We hold all necessary … licences" | About, FAQ | **no licence number**. NSW generally requires it in advertising for residential building work |
| "references available upon request", "positive feedback" | Insurance, Commercial | keep wording, no testimonials |
| "Aust Building" / austbuilding.com.au | Strata page, emails, logo file | related business? confirm whether to mention |
| Reviews | Site Reviews plugin | **no reviews stored**. None will be shown |

## Shared hosting and email dependencies

- **Website hosting:**
  - BRC is an addon domain on the same Crazy Domains cPanel account as Roof Centre
    (`103.20.200.233`).
  - Cancelling that account removes the old BRC site.
- **DNS:**
  - BRC's nameservers are `ns1/ns2.syrahost.com`. The zone also appears in this cPanel account's
    DNS files (`dnszones/buildingrepaircentre.com.au.db`).
  - The live zone serial (2026101101) is newer than the backup's (2026100900), so the zone is still
    being edited.
  - **Confirm with Crazy Domains where this zone is managed before closing anything.** If it lives
    in the cPanel account, closing the account could remove BRC's MX records.
- **Email: Google Workspace:**
  - MX records point to `ASPMX.L.GOOGLE.COM` and the ALT1–ALT4 servers. There are no cPanel mailboxes
    or forwarders for BRC.
- **Roof Centre dependency:** `info@roofcentre.com.au` forwards to `info@buildingrepaircentre.com.au`,
  so Roof Centre enquiries end up in BRC's Google Workspace.
- **DNS problems to fix later (not now):**
  - **Two SPF records** (`include:_spf.google.com` and `+a +mx +ip4:122.201.124.64`). This makes SPF
    fail.
  - The DMARC record has `p=Quarntine` (misspelt, so the policy is invalid).
- **Pergola Building Centre:** `pergolabuildingcentre.com.au` does not resolve, though its files and
  database (`roofcent_wp3`) remain.

## Proposed page structure

Existing URLs are kept, except the misspelt `/commnercial/`, which now redirects to `/commercial/`.

| URL | Page |
|---|---|
| `/` | Home |
| `/about-us/` | About |
| `/services/` | Services overview (new content; was empty) |
| `/insurance-building/` | Insurance Building |
| `/strata-real-estate-maintenance/` | Strata & Real Estate Maintenance |
| `/commercial/` | Commercial (`/commnercial/` 301s here, as decided by the owner) |
| `/residential/` | Residential |
| `/tradie-services/` | Trade services (21 trades, grouped) |
| `/projects/` | Projects: grouped by job with suburb captions, filter, lightbox |
| `/faq/` | FAQ (existing 6 Q&As, rewritten for clarity, plus factual additions) |
| `/contact-us/` | Contact and quote form (PHP handler, private config above `public_html`) |
| `/privacy/` | Privacy (new) |
| `/thank-you/`, `/404.html` | utility pages |

**Redirects:**
- `/home/`, `/home-2/`, `/sample-page/`, `/hello-world/`, `/uncategorized/hello-world/`,
  `/downloads/`, `/leave-a-review/` → `/`
- `/privacy-policy/` → `/privacy/`
- WordPress admin, login and content paths → 410 Gone

## Design direction

- **Same build system as Roof Centre:**
  - `tools/content.py`, `tools/build.py`, `tools/images.py`, `tools/serve.py`, `tools/check.py` and
    `tools/package.py`.
  - Static HTML/CSS/JS, WebP srcset, PHP enquiry handler.
- **Its own identity, aimed at insurers, strata and property managers, and commercial clients:**
  - Colours from the logo and the existing site: navy `#0A2552` / `#164086` with sky `#24A3D6`.
  - Clean, professional, less "roofing", more "building maintenance".
- **Home page:**
  - Split hero with a real job photo and a clear "Call 0431 848 619 / Request a Quote".
  - "Who we work for" (Insurance, Strata & Real Estate, Commercial, Residential).
  - Trade services grid with SVG icons (replacing the 259 px PNG tiles).
  - Project highlights, FAQ teaser, contact strip.
- **Projects:** grouped photo sets per job with suburb names, a filter by type, and a lightbox.
- **Mobile:** a sticky Call / Request a Quote bar. Subtle reveal animation with reduced-motion support.
- **Links:** Roof Centre is linked as a sister business (as the current header does).

## Repository plan

- `main`: full project:
  - `website/`, `tools/`, `docs/`, `README.md`, `.gitignore`, `.gitattributes`
  - no backups, databases or credentials
- `deploy`: only the contents of `website/` at its root. Created with
  `git subtree split --prefix=website -b deploy`.
- Private enquiry settings: `brc-enquiry-config.php` in the folder above `public_html`, never in Git.
- The image pipeline reads the backup from its existing location (configurable path). The backup is
  never copied into this project.
