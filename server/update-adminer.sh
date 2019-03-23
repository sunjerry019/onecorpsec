#!/bin/bash

# Updates adminer with wget
cd "/usr/local/nginx/adminer/"
wget -N "http://www.adminer.org/latest.php"
chown -R www-data:www-data "/usr/local/nginx/adminer"
