<?php
/**
 * Building Repair Centre: private enquiry settings.
 *
 * Copy this file to the server as brc-enquiry-config.php in the folder that
 * CONTAINS public_html (never inside public_html), for example:
 *   /home/u123456789/domains/buildingrepaircentre.com.au/brc-enquiry-config.php
 *
 * The real file is listed in .gitignore and must never be committed.
 */
return [
    'to'        => 'info@buildingrepaircentre.com.au',
    'bcc'       => '',                                     // optional second recipient
    'from'      => 'website@buildingrepaircentre.com.au',  // an address on the domain
    'from_name' => 'Building Repair Centre Website',
    // 'mail_log' => '/tmp/brc-mail.log',                  // testing only: write to a file instead of sending
];
