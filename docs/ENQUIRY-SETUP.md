# Enquiry form setup

The quote form (home page and `/contact-us/`) posts to `/api/enquiry.php`, which emails the enquiry
with PHP `mail()` to **info@buildingrepaircentre.com.au** (confirmed by the owner).

## Fields

Name\*, phone\*, email\*, suburb, type of work (the five services or "Something else"), "I am a"
(homeowner, strata or building manager, real estate agent or landlord, insurance builder/assessor/
insurer, business or commercial property, tradesperson or supplier, other) and message\*.
Service pages link to `/contact-us/?service=<slug>#quote`, which preselects the type of work.

## What the old WordPress site did

The Contact Form 7 form ("Contact form 1": name, email, subject, message) sent to an old admin
address with Reply-To set to the visitor. Contact Form 7 had been disabled, so the old contact page
showed a raw shortcode and no form.

## Private settings (outside the web root and outside Git)

Settings live in `brc-enquiry-config.php` **in the folder that contains `public_html`**:

| Host | Path |
|---|---|
| Hostinger | `/home/u123456789/domains/buildingrepaircentre.com.au/brc-enquiry-config.php` (your own `u…` number) |

Start from `docs/brc-enquiry-config.example.php`. The real file is in `.gitignore` and must never be
placed in `public_html` or committed. Without it, the defaults in `website/api/enquiry.php` are used
(to `info@buildingrepaircentre.com.au`, from `website@buildingrepaircentre.com.au`).

## Testing without sending email

- `python tools/serve.py` mocks `/api/enquiry.php` and prints the enquiry in the terminal. PHP is
  not used and nothing is emailed.
- `tools/apache-test/` runs the real PHP handler in Docker with `'mail_log'` set, so enquiries are
  written to a file in the container and nothing is sent.
- Tested on 12 Oct 2026 (PHP 8.2, Apache 2.4):
  - valid enquiry → logged, JSON `ok`, or 303 to `/thank-you/` without JavaScript
  - missing or invalid fields → 422
  - cross-site Origin → 403
  - header injection → 400
  - GET → 405
  - honeypot or too-fast submission → silently accepted but not sent
  - config file not reachable over the web

## Needed before go-live

1. **SPF:** the domain currently has two SPF records, so SPF fails for all of its mail. Merge them
   into one that includes Hostinger's sending mechanism (value from hPanel or Hostinger support)
   and Google's `include:_spf.google.com`. See `DEPLOY-HOSTINGER.md`, Part C, step 1.
2. **Test from Hostinger:** submit the form on the temporary domain and confirm it arrives at
   `info@buildingrepaircentre.com.au` (check spam).
3. **If `mail()` is unreliable:** switch to authenticated SMTP through Google Workspace (for example
   PHPMailer with an app password or Google's SMTP relay). Keep any password in
   `brc-enquiry-config.php`, never in `public_html` or Git.

## Spam protection included

- A hidden honeypot field.
- A minimum fill time of 3 seconds.
- A same-origin check.
- A limit of 8 enquiries per hour per IP address.
- Header-injection guards and server-side validation.

No CAPTCHA is used.
