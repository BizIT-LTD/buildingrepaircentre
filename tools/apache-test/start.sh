#!/bin/sh
set -e
a2enmod rewrite headers ssl >/dev/null
sed -ri 's#/var/www/html#/var/www/site/public_html#g' /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/default-ssl.conf
sed -ri 's#AllowOverride None#AllowOverride All#g' /etc/apache2/apache2.conf
openssl req -x509 -nodes -newkey rsa:2048 -days 2 -subj "/CN=www.buildingrepaircentre.com.au" -keyout /etc/ssl/private/test.key -out /etc/ssl/certs/test.crt 2>/dev/null
sed -ri 's#/etc/ssl/certs/ssl-cert-snakeoil.pem#/etc/ssl/certs/test.crt#; s#/etc/ssl/private/ssl-cert-snakeoil.key#/etc/ssl/private/test.key#' /etc/apache2/sites-available/default-ssl.conf
a2ensite default-ssl >/dev/null
which sendmail || echo "no sendmail in container: mail() cannot send"
exec apache2-foreground
