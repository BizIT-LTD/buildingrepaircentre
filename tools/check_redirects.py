"""Check the .htaccess redirects on a real Apache/LiteSpeed server.

    python tools/check_redirects.py https://www.buildingrepaircentre.com.au
    python tools/check_redirects.py https://127.0.0.1:8443 --host www.buildingrepaircentre.com.au --insecure

--host sends that Host header (to test before DNS points at the server).
--insecure accepts a self-signed certificate (local Docker test only).
tools/serve.py does not read .htaccess, so run this against Apache, for
example the Docker test in docs/DEPLOY-HOSTINGER.md, or the live site.
"""
import http.client
import sys
from urllib.parse import urlsplit

# path -> (status, location or None)
EXPECT = {
    "/": (200, None),
    "/commercial/": (200, None),
    "/commnercial/": (301, "/commercial/"),
    "/commnercial": (301, "/commercial/"),
    "/home/": (301, "/"),
    "/home-2/": (301, "/"),
    "/sample-page/": (301, "/"),
    "/hello-world/": (301, "/"),
    "/uncategorized/hello-world/": (301, "/"),
    "/downloads/": (301, "/"),
    "/leave-a-review/": (301, "/"),
    "/privacy-policy/": (301, "/privacy/"),
    "/contact/": (301, "/contact-us/"),
    "/about/": (301, "/about-us/"),
    "/request-a-quote/": (301, "/contact-us/#quote"),
    "/wp-sitemap.xml": (301, "/sitemap.xml"),
    "/sitemap_index.xml": (301, "/sitemap.xml"),
    "/page-sitemap.xml": (301, "/sitemap.xml"),
    "/category/promotion/": (301, "/"),
    "/feed/": (301, "/"),
    "/about-us": (301, "/about-us/"),
    "/wp-admin/": (410, None),
    "/wp-login.php": (410, None),
    "/xmlrpc.php": (410, None),
    "/wp-content/uploads/2020/09/strata.jpeg": (410, None),
    "/.git/config": (403, None),
    "/no-such-page/": (404, None),
    "/api/enquiry.php": (405, None),
}


def main():
    args = sys.argv[1:]
    base = urlsplit(args[0])
    host = args[args.index("--host") + 1] if "--host" in args else base.hostname
    if base.scheme == "https":
        import ssl
        ctx = ssl._create_unverified_context() if "--insecure" in args else None
        conn_cls = lambda h, p, timeout: http.client.HTTPSConnection(h, p, timeout=timeout, context=ctx)
    else:
        conn_cls = http.client.HTTPConnection
    problems = 0
    for path, (want_status, want_loc) in EXPECT.items():
        c = conn_cls(base.hostname, base.port, timeout=20)
        headers = {"Host": host}
        c.request("GET", path, headers=headers)
        r = c.getresponse()
        r.read()
        loc = r.getheader("Location")
        if loc:
            loc = loc.replace(f"https://{host}", "").replace(f"http://{host}", "")
        ok = r.status == want_status and (want_loc is None or loc == want_loc)
        problems += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {path:45} {r.status} {loc or ''}" + ("" if ok else f"   (expected {want_status} {want_loc or ''})"))
        c.close()
    print("No problems found." if not problems else f"{problems} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
