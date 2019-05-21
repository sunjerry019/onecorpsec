#!/usr/bin/env python3
import gnupg, base64
import sys

sys.path.insert(0, "../")
import dashboard.settings as settings

class GPGPassError(Exception):
    """Generic error for errors in this GPGPass helper"""
    pass

class GPGPass():
    def __init__(self):
        self.GPGConfig = settings.GPG_CONFIG

        # initialize GPG
        self.gpg = gnupg.GPG(gnupghome=self.GPGConfig["gnupghome"])

    def encrypt(self, data, b64 = True):
        # Encrypt data using the GPG user
        # This user's key should be ultimately trusted

        encrypted_ascii = self.gpg.encrypt(data, [self.GPGConfig["user"]], sign=self.GPGConfig["user"], passphrase=self.GPGConfig["ukpp"])
        # Note that the above outputs a bytestring

        if not encrypted_ascii.ok:
            raise GPGPassError("ENC ERROR: ", encrypted_ascii.status)

        ret = base64.b64encode(encrypted_ascii.data) if b64 else encrypted_ascii.data

        # return a normal string
        return ret.decode("utf-8")

    def decrypt(self, enc_data, b64 = True):
        # Decrupt data using the GPG user

        # If b64 is required, we decode it first
        if b64:
            enc_data = base64.b64decode(enc_data)

        decrypted_data = gpg.decrypt(enc_data, passphrase=self.GPGConfig["ukpp"])
        # Note that the above outputs a bytestring

        if not decrypted_data.ok:
            raise GPGPassError("DEC ERROR: ", decrypted_data.status)

        return decrypted_data.data.decode('utf-8')
