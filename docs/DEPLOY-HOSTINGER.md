# Deploying to a new Hostinger website

This puts the new Building Repair Centre site on a **new** Hostinger website and tests it on
Hostinger's temporary domain first. Nothing here has been done yet.

- Only the **contents of `website/`** go into `public_html`. In Git terms that is the **`deploy`**
  branch. Never deploy `main`, which also contains `tools/` and `docs/`.
- Private enquiry settings (`brc-enquiry-config.php`) go in the folder **above** `public_html`.
- The old Crazy Domains hosting **stays active**. It handles Roof Centre's email forwarder, and BRC's
  DNS zone may be managed there (see "Current setup").
- DNS changes happen only in Part C, later, and only when approved. Email (Google Workspace) is not
  moved and its records are not changed.

hPanel menu names change from time to time. If a label below differs, look for the nearest equivalent.

---

## Current setup (checked 12 Oct 2026, from `ns1.syrahost.com`)

| Record | Live value | TTL |
|---|---|---|
| Nameservers | `ns1.syrahost.com`, `ns2.syrahost.com` (Crazy Domains / Dreamscape) | |
| `buildingrepaircentre.com.au` A | `103.20.200.233` (old Crazy Domains cPanel server) | 14400 |
| `buildingrepaircentre.com.au` AAAA | `2405:3f00:a222:bbbb:bba1:27:ffff:ffff` (old server, IPv6) | 14400 |
| `www` | CNAME → `buildingrepaircentre.com.au` | 14400 |
| `mail` | CNAME → `buildingrepaircentre.com.au` (not used for Google mail) | 14400 |
| `webmail` | A → `103.20.200.233` | 14400 |
| MX | Google Workspace: `ASPMX.L.GOOGLE.COM` (1), `ALT1`/`ALT2.ASPMX.L.GOOGLE.COM` (5), `ALT3`/`ALT4.ASPMX.L.GOOGLE.COM` (10) | 14400 |
| TXT | `google-site-verification=…` | 14400 |
| SPF | **two records**: `v=spf1 include:_spf.google.com ~all` and `v=spf1 +a +mx +ip4:122.201.124.64 ~all` | 14400 |
| DKIM | `google._domainkey` (Google Workspace) and `default._domainkey` (cPanel) | |
| DMARC | `v=DMARC1; p=Quarntine; rua=mailto:dmarc-reports@buildingrepaircentre.com.au` | 3600 |

Notes:

- **Website status:** the old WordPress site returned **503 Service Unavailable** on every page
  tested (12 Oct 2026).
- **Email does not depend on the website A record.** The MX records point at Google, so moving
  the website does not move email.
- **Two SPF records make SPF fail** (permerror) for all mail from the domain. Fix this before
  launch (Part C, step 1).
- **DMARC `p=Quarntine` is misspelt.** The tag is invalid, so the policy is not applied as intended.
- **Where the zone is edited:** BRC's zone also appears in the Roof Centre cPanel account's DNS
  files, and the live serial changed on 11 Oct 2026. Ask Crazy Domains whether BRC's DNS is
  managed in the Crazy Domains account DNS manager or in that cPanel's Zone Editor. **Do not
  close the cPanel account until BRC's DNS is confirmed to live elsewhere.**

---

## Part A: create the Hostinger website (no DNS change)

1. **Build and check on this PC**
   ```
   python tools/build.py
   python tools/serve.py 8090        # in a second terminal
   python tools/check.py             # expect "No problems found."
   ```
   Optional real-server test (Apache + PHP, no email sent): `tools/apache-test/README.md`.

2. **Create a new website in hPanel**
   - Websites → **Add website** → an empty/custom PHP & HTML website (not WordPress, not the
     builder). Do not reuse an existing Hostinger website.
   - If asked for a domain, enter `buildingrepaircentre.com.au` as an **existing domain you own**,
     and **skip** any offer to change nameservers or point the domain now.
   - Note the **temporary domain** (for example `something.hostingersite.com`). Part B uses it.
   - Do **not** create Hostinger email accounts for this domain, and ignore any prompt to add MX
     records. Email stays on Google Workspace.

3. **PHP:** Websites → Manage → Advanced → PHP Configuration → PHP **8.2 or newer** (`mbstring` on).

4. **Deploy the files into `public_html`.** Use one of these:

   **Git (recommended)**
   - First create the `deploy` branch locally and push it (only when pushing is approved):
     ```
     git subtree split --prefix=website -b deploy
     git push origin main deploy
     ```
   - hPanel → Websites → Manage → Advanced → **Git**:
     - Repository: the GitHub URL of this project (HTTPS for a public repository; for a private
       repository add Hostinger's SSH deploy key to GitHub as a read-only deploy key and use the
       SSH URL).
     - Branch: **`deploy`**
     - Directory: **leave empty** (that means `public_html` itself). Never enter `website`.
   - Hostinger only installs into an **empty** directory. Delete the placeholder `default.php` /
     `index.php` first. Then **Deploy**.

   **ZIP upload (alternative)**
   - `python tools/package.py` → `dist/buildingrepaircentre-website.zip` (contents of `website/`,
     including `.htaccess`, no wrapping folder).
   - File Manager → `public_html` → delete placeholders → upload → **Extract** into `public_html`
     itself → delete the zip.

   Either way, `public_html` must directly contain `index.html`, `.htaccess`, `404.html`,
   `sitemap.xml`, `robots.txt`, `assets/`, `api/` and the page folders (turn on "show hidden
   files" to see `.htaccess`). It must **not** contain `website/`, `tools/`, `docs/` or `README.md`.

5. **Private enquiry settings (above `public_html`)**
   - File Manager → go **up one level** from `public_html` (for example
     `/home/u123456789/domains/buildingrepaircentre.com.au/`).
   - Create `brc-enquiry-config.php` there from `docs/brc-enquiry-config.example.php`. The
     recipient is `info@buildingrepaircentre.com.au`.
   - `api/enquiry.php` reads it from two levels above `public_html/api/`. Never put it in
     `public_html` or Git.

---

## Part B: test on the temporary domain (no DNS change)

The `.htaccess` redirects only fire on `buildingrepaircentre.com.au`, so they stay inactive on the
temporary domain. That is expected.

- [ ] Home, About, Services, the five service pages, Projects, FAQ, Contact and Privacy load with
      images, on desktop and mobile.
- [ ] The mobile bottom bar shows **Call** (`0431 848 619`) and **Request a Quote**.
- [ ] The mobile menu opens and closes, and the Services submenu expands.
- [ ] The project filter and photo viewer work on `/projects/`.
- [ ] A made-up URL shows the Building Repair Centre 404 page.
- [ ] `https://<temporary-domain>/api/enquiry.php` in a browser shows "Method not allowed".
- [ ] `https://<temporary-domain>/brc-enquiry-config.php` returns 404.
- [ ] Submit the form with real test details. The success message appears. Check that the email
      arrives at `info@buildingrepaircentre.com.au` (and the spam folder). Until SPF is fixed
      (Part C, step 1) it may be rejected or filtered.
- [ ] `/sitemap.xml` and `/robots.txt` load.

---

## Part C: go live (LATER, only when approved)

Done in whichever DNS manager holds BRC's zone (confirm with Crazy Domains first). Keep the
nameservers as they are.

### 1. Fix SPF and DMARC first (use the providers' values, do not guess)

- Get the exact SPF mechanism for PHP mail from this Hostinger website (hPanel → Emails / DNS
  records, or Hostinger support).
- Google Workspace's value is already live: `include:_spf.google.com`.
- Ask Crazy Domains whether anything still sends **as** `@buildingrepaircentre.com.au` from the
  old cPanel server (`ip4:122.201.124.64` / `+a +mx`). If not, that mechanism can be dropped.
- Replace the **two** SPF records with **one** that combines the confirmed senders.
- DKIM: Google Workspace DKIM (`google._domainkey`) is live. Hostinger PHP mail is normally not
  DKIM-signed for a domain whose email is hosted elsewhere; confirm with Hostinger. If it can't be
  signed, delivery relies on SPF passing, or switch the form to authenticated SMTP through Google
  Workspace (see `docs/ENQUIRY-SETUP.md`).
- DMARC: correct the misspelt policy (`quarantine`, or `none` while monitoring) as the domain
  owner decides. Check the reports at `dmarc-reports@buildingrepaircentre.com.au` before enforcing.
- Retest the form on the temporary domain and check the received headers for `spf=pass`.

### 2. Point the website to Hostinger

- A day before: lower the TTL of the root A and AAAA records (and `www`) to 300 if the DNS manager
  allows it. They are 14400 (4 hours) now.
- Get the website's IPv4 address (and IPv6 if Hostinger provides one) from hPanel.
- Change `buildingrepaircentre.com.au` **A** to the Hostinger IPv4 address.
- **AAAA:** change it to Hostinger's IPv6 address if provided; otherwise **remove** it. If the old
  AAAA record is left, IPv6 visitors will still reach the old server.
- `www` is a CNAME to the root, so it follows automatically.
- **Do not touch** the MX records, the Google TXT/DKIM records, `_dmarc` (other than the step 1
  fix) or `webmail`.
- `mail` is a CNAME to the root and will then point to Hostinger. Google Workspace does not use it.
  Leave it unless the owner uses that name for something.

### 3. SSL

In hPanel, connect `buildingrepaircentre.com.au` to the website if not already done, then install
the free SSL certificate once DNS resolves to Hostinger. `.htaccess` forces
`https://www.buildingrepaircentre.com.au`, so install SSL promptly.

### 4. Verify

```
python tools/check_redirects.py https://www.buildingrepaircentre.com.au
```
Expect "No problems found." (old URLs such as `/commnercial/` → `/commercial/`, WordPress paths →
410). Then:

- [ ] `http://buildingrepaircentre.com.au/` redirects to `https://www.buildingrepaircentre.com.au/`.
- [ ] The form sends and the email arrives at `info@buildingrepaircentre.com.au`.
- [ ] Email to `info@buildingrepaircentre.com.au` from an outside account still arrives (Google).
- [ ] Mail to `info@roofcentre.com.au` still forwards here (that forwarder lives on the old cPanel).

### 5. Search Console

Submit `https://www.buildingrepaircentre.com.au/sitemap.xml`.

### 6. Keep the old hosting

Keep the Crazy Domains cPanel account while it:
- runs the `info@roofcentre.com.au` forwarder,
- may hold BRC's DNS zone, and
- holds the backups.

Closing it is a separate, later decision.

---

## Updating the site later

```
python tools/build.py
python tools/check.py                       # with serve.py running
git add -A && git commit -m "…"
git subtree split --prefix=website -b deploy
git push origin main deploy                 # then Deploy in hPanel, or use the webhook
```

`git subtree split` is deterministic, so `deploy` fast-forwards and never needs a force-push.

---

## Rollback

| If this fails | Undo |
|---|---|
| Part A or B | Nothing to undo in DNS. Fix or delete the Hostinger website. |
| Part C, step 1 (mail problems after the SPF/DMARC change) | Restore the previous TXT values exactly as listed in "Current setup". |
| Part C, steps 2–4 (website problems after cut-over) | Set the root A back to `103.20.200.233` and restore the AAAA `2405:3f00:a222:bbbb:bba1:27:ffff:ffff`. `www` follows via its CNAME. The old WordPress install is untouched on Crazy Domains (it was returning 503 on 12 Oct 2026, so check it first). MX and Google records are never changed, so email is unaffected. |

With TTL 300, changes take effect for most visitors within minutes. Before the TTL is lowered,
allow up to 4 hours.
