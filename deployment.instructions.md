Create the database onecorpsec
Create the user onecorpsec with password according to config.json
Move `config.json` to a location not accessible through the internet
Configure Django (secret_key)
install:
    python-dateutil
    https://pypi.org/project/mysql-connector-python/
    # django-html-emailer
    django-material

https://docs.djangoproject.com/en/dev/howto/static-files/ Deploy Static files appropriately

Install:
    pip install python-magic


==================== CUSTOM MAIL SERVER ====================

Install:
    pip install python-gnupg

change gnupg home
https://www.digitalocean.com/community/tutorials/how-to-setup-additional-entropy-for-cloud-servers-using-haveged

ALWAYS RUN make migrations ON THE SERVER

password has a backslash that needs to be escaped
