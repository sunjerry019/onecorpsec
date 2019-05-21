#!/usr/bin/env python3

# SOURCE = https://bitbucket.org/vinay.sajip/python-gnupg/raw/1afe9d9bb187d4bb6c633175382ae7e600bf6d20/gnupg.py

import gnupg, base64
import json
import os

_confFile = "password.json"
with open(_confFile,'r') as f:
    _conf = json.load(f)

# initialize GPG
gpg = gnupg.GPG(gnupghome='/home/sunyudong/.gnupg')

# Encrypt the password first
_GPGpassword = _conf["pgpgpg"]
with open("mima.txt", 'r') as f:
    _EMAILpassword = f.readlines()[0].strip()

encrypted_ascii = gpg.encrypt(_EMAILpassword, ["test@test.com"], sign="test@test.com", passphrase=_GPGpassword)

if not encrypted_ascii.ok:
    print("ERROR: ", encrypted_ascii.status)

based64 = base64.b64encode(encrypted_ascii.data)
print("BASED64, length = {}".format(len(based64)))
# print("BASE64 = ", based64)

assert len(based64) <= 3500 # Database Limit

# Store the based64
with open("based64.txt", 'w') as f:
    f.write(based64.decode("utf-8"))

# Decrypt the password
with open("based64.txt", 'r') as f:
    encrypted_password = f.readlines()[0].strip()

_gpged_pw = base64.b64decode(encrypted_password)
decrypted_data = gpg.decrypt(_gpged_pw, passphrase=_GPGpassword)

# if decrypted_data.trust_level is not None and decrypted_data.trust_level >= decrypted_data.TRUST_FULLY:
#     print('Trust level: %s' % decrypted_data.trust_text)
# print(decrypted_data.username)
print(decrypted_data.data.decode('utf-8'))
