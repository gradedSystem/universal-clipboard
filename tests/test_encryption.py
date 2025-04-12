import pytest
from shared.encryption import EncryptionManager

def test_encryption_manager():
    # Test basic encryption/decryption
    manager = EncryptionManager()
    original_data = b"Hello, World!"
    
    encrypted_data = manager.encrypt(original_data)
    decrypted_data = manager.decrypt(encrypted_data)
    
    assert decrypted_data == original_data
    assert encrypted_data != original_data

def test_key_generation():
    # Test key generation from password
    password = "test_password"
    key1 = EncryptionManager.generate_key_from_password(password)
    key2 = EncryptionManager.generate_key_from_password(password)
    
    # Same password should generate different keys due to random salt
    assert key1 != key2

def test_key_persistence():
    # Test that the same key can be used for multiple encryptions and decryptions
    key = EncryptionManager().get_key()
    manager1 = EncryptionManager(key)
    manager2 = EncryptionManager(key)
    
    data = b"Test data"
    encrypted1 = manager1.encrypt(data)
    encrypted2 = manager2.encrypt(data)
    
    # Both managers should be able to decrypt both ciphertexts
    assert manager1.decrypt(encrypted1) == data
    assert manager1.decrypt(encrypted2) == data
    assert manager2.decrypt(encrypted1) == data
    assert manager2.decrypt(encrypted2) == data 