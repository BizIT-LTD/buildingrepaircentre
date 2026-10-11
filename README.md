# Building Repair Centre website (buildingrepaircentre.com.au)

Static HTML/CSS/JS rebuild of the Building Repair Centre WordPress site, with a PHP enquiry handler.

```
website/   the deployable site: its CONTENTS go into Hostinger's public_html (the deploy branch)
tools/     content, image, build, preview and test scripts
docs/      deployment, enquiry setup, URL map, discovery notes, screenshots
```

The original cPanel backup stays outside this project, read-only, at
`C:\HostingerWebsites\roofcentre\reference\extracted\`. It is never copied here or committed.

## Preview locally

```
python tools/serve.py 8090
```

Open http://localhost:8090/. Form submissions are mocked and printed in that terminal; nothing is
emailed. Stop with Ctrl+C. Requires Python 3.10+.

## Edit and rebuild

| What | Where |
|---|---|
| Business details, services, trades, FAQs, project groups | `tools/content.py` |
| Page layouts, titles, meta descriptions | `tools/build.py` |
| Styles and behaviour | `website/assets/css/site.css`, `website/assets/js/site.js` |
| Photos (selection, alt text) | `tools/images.py` |
| Enquiry handler | `website/api/enquiry.php` (private settings: `docs/ENQUIRY-SETUP.md`) |
| Redirects, headers | `website/.htaccess` (URL map: `docs/MIGRATION-NOTES.md`) |

```
python tools/build.py             # regenerates all HTML, sitemap.xml, robots.txt, site.webmanifest
python tools/check.py             # with serve.py running: links, images, SEO tags, sitemap, excluded wording
python tools/package.py           # dist/buildingrepaircentre-website.zip for manual upload
```

`build.py` needs only the files in this repository. `images.py` (re-processing photos) needs the
original backup and Pillow (`pip install pillow`). Set `BRC_BACKUP` if the backup is elsewhere.

Real-server test of `.htaccess` and `enquiry.php` (Docker, no email sent): `tools/apache-test/README.md`,
then `python tools/check_redirects.py https://127.0.0.1:8443 --host www.buildingrepaircentre.com.au --insecure`.

## Pages

12 indexable pages (all in `sitemap.xml`): home, about, services, five service pages
(insurance building, strata & real estate maintenance, commercial, residential, tradie services),
projects, FAQ, contact and privacy. Also `/thank-you/` (noindex) and `/404.html`.

## Branches and deployment

- `main`: the full project (`website/`, `tools/`, `docs/`, `README.md`).
- `deploy`: only the contents of `website/` at its root, for Hostinger's Git deployment into
  `public_html`. Never deploy `main`.
  ```
  git subtree split --prefix=website -b deploy
  ```

See `docs/DEPLOY-HOSTINGER.md`. Private enquiry settings (`brc-enquiry-config.php`) live on the
server in the folder above `public_html` and are never committed.

## Screenshots

`docs/screenshots/`: desktop (1440px) and mobile (390px) full-page captures of the homepage, the
Insurance Building service page, the project gallery and the contact page.
