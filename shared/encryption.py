from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class EncryptionManager:
    def __init__(self, key=None):
        if key is None:
            self.key = Fernet.generate_key()
        else:
            # If key is already base64 encoded, decode it
            if isinstance(key, str):
                self.key = base64.urlsafe_b64decode(key)
            else:
                self.key = key
        self.fernet = Fernet(self.key)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt the given data using AES-256."""
        return self.fernet.encrypt(data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypt the given encrypted data."""
        return self.fernet.decrypt(encrypted_data)

    def get_key(self) -> str:
        """Get the encryption key as a base64 string."""
        return base64.urlsafe_b64encode(self.key).decode()

    @staticmethod
    def generate_key_from_password(password: str, salt: bytes = None) -> bytes:
        """Generate a key from a password using PBKDF2."""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode())) 