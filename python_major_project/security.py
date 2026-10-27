import hashlib
import secrets
import hmac


class Security:

    @staticmethod
    def hash_password(password):

        salt = secrets.token_hex(16)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            200000
        ).hex()

        return salt + "$" + password_hash

    @staticmethod
    def verify_password(password, stored_hash):

        try:
            salt, original_hash = stored_hash.split("$", 1)

            new_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                200000
            ).hex()

            return hmac.compare_digest(
                new_hash,
                original_hash
            )

        except (ValueError, AttributeError):
            return False