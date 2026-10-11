# Migration notes

## Source

- Domain `buildingrepaircentre.com.au`, WordPress database **`roofcent_wp2`** (siteurl
  `http://www.buildingrepaircentre.com.au`). It is an addon domain in the Roof Centre cPanel backup
  `backup-10.9.2026_19-00-52_roofcent`. Details are in `docs/DISCOVERY.md`.
- The backup stays read-only in `C:\HostingerWebsites\roofcentre\reference\extracted\`. It is not
  copied into this project or committed.

## URL map

The canonical site is `https://www.buildingrepaircentre.com.au`. All redirects are in
`website/.htaccess`, apply only to the `buildingrepaircentre.com.au` host, and were tested on Apache
(`tools/check_redirects.py`, 28 checks).

| Original URL | New site |
|---|---|
| `/` | kept |
| `/about-us/`, `/projects/`, `/services/`, `/faq/`, `/contact-us/` | kept (`/services/` was empty and now has content) |
| `/insurance-building/`, `/strata-real-estate-maintenance/`, `/residential/`, `/tradie-services/` | kept |
| `/commnercial/` (misspelt) | **301 → `/commercial/`** (new canonical) |
| `/home/`, `/home-2/`, `/sample-page/`, `/hello-world/`, `/uncategorized/…`, `/downloads/`, `/leave-a-review/` | 301 → `/` (old, placeholder or empty pages) |
| `/category/…`, `/tag/…`, `/author/…`, `/feed/` | 301 → `/` |
| `/privacy-policy/` (was a draft) | 301 → `/privacy/` |
| `/contact/`, `/about/` | 301 → `/contact-us/`, `/about-us/` |
| `/request-a-quote/` | 301 → `/contact-us/#quote` |
| `/wp-sitemap.xml`, `/sitemap_index.xml`, `/*-sitemap.xml` | 301 → `/sitemap.xml` |
| `/wp-admin`, `/wp-login.php`, `/xmlrpc.php`, `/wp-content/…`, `/wp-includes/…`, `/wp-json` | 410 Gone |
| any `.git` path | 403 |

New pages: `/commercial/`, `/privacy/`, `/thank-you/` (noindex) and `/404.html`.

## Content decisions (owner instructions, 12 Oct 2026)

| Item | Old site | New site |
|---|---|---|
| Email and enquiry recipient | Several addresses, including an `austbuilding` link and an admin form recipient | `info@buildingrepaircentre.com.au` only |
| Phone | 0431 848 619 plus three other numbers on 2020 pages | **0431 848 619 only** |
| Insurance cover ($20M public liability), "10+ years", "15 years", "A++ KPI", "500+ jobs", 24/7 / 24-hour | Various pages | **Left out** until confirmed |
| "Licensed", "insured", licence number, ABN | Licences claimed, no number | **Left out** until supplied |
| Aust Building | Strata page text, emails, a photo of a branded shirt | **Not mentioned**; that photo is excluded |
| References / "positive feedback" | Insurance and Commercial pages | Left out |
| Reviews | Site Reviews plugin, no reviews stored | None shown |
| Free quotes | "Request a Free Quote" buttons | Kept |
| Hours / area | Mon–Fri 9 am–5 pm, Sydney-wide | Kept |
| Social links | Facebook/LinkedIn were `#` placeholders | Dropped |
| Roof Centre | Header link | Footer link "Roof Centre (roofing)" |

`tools/check.py` fails the build check if any excluded wording appears in a page (24/7, 24-hour,
licensed, insured, Aust Building, A++, KPI, $20…, 500, 10/15 years, the old numbers, ABN, reviews).

## Photos

40 confirmed job photos are used (`tools/images.py`): Camperdown fit-out, a college building, a café
fit-out, a Redfern apartment building, a Chipping Norton deck and pergola, a deck/pergola/roof build,
Lindfield, storm/tree damage, and other trade work. Captions describe only what each photo shows,
plus the suburb names used on the original site.

Excluded:
- staff portraits
- the Neutral Bay salon render
- suspected stock photos (`residential-page2`, `tradie-services`, `insurance-building`,
  `fencings`, `guttering`)
- all city, storm, laptop and illustration stock
- banner graphics with baked-in text
- 2018 theme demo images
- the photo showing an Aust Building shirt
- a skip-bin photo showing another company's phone number

The largest originals are 1600px wide, so every hero is a framed photo beside the text, never
stretched edge to edge.

## Still to confirm before launch

- Licence number and ABN (to add when supplied; NSW generally requires the licence number in
  advertising for residential building work).
- Whether any of the excluded claims (insurance cover, experience, 24/7) should be added back.
- Staff portraits and the Neutral Bay image, if wanted.
- Privacy statement wording.
