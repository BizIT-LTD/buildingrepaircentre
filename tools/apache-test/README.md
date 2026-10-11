# Local Apache + PHP test (Docker)

`tools/serve.py` is a quick preview: it mocks the enquiry endpoint and does not read `.htaccess`.
This test runs the real files on Apache with PHP 8.2, so the redirects and `api/enquiry.php` can be
checked before deployment. **No email is sent.** The test config writes enquiries to
`/tmp/brc-mail.log` inside the container, and the container has no mail program.

From the project folder, in Git Bash:

```
docker run -d --name brc-test -p 127.0.0.1:8091:80 -p 127.0.0.1:8443:443 \
  -v "$(pwd -W)/website:/var/www/site/public_html:ro" \
  -v "$(pwd -W)/tools/apache-test/test-enquiry-config.php:/var/www/site/brc-enquiry-config.php:ro" \
  -v "$(pwd -W)/tools/apache-test/start.sh:/start.sh:ro" \
  php:8.2-apache sh /start.sh

python tools/check_redirects.py https://127.0.0.1:8443 --host www.buildingrepaircentre.com.au --insecure
MSYS_NO_PATHCONV=1 docker exec brc-test cat /tmp/brc-mail.log   # after submitting a test enquiry
docker rm -f brc-test
```

The container mirrors Hostinger's layout: the site is `public_html`, and the private config sits
one level above it (`/var/www/site/brc-enquiry-config.php`). A throwaway self-signed certificate
is created so the HTTPS rules can be tested.
