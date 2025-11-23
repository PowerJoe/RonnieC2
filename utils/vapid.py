"""
VAPID key management utilities
"""
import os
from py_vapid import Vapid

VAPID_PRIVATE_KEY = None
VAPID_PUBLIC_KEY = None
VAPID_CLAIMS = {
    "sub": "mailto:admin@browserc2.local"
}

def init_vapid_keys():
    """Initialize or load VAPID keys"""
    global VAPID_PRIVATE_KEY, VAPID_PUBLIC_KEY
    
    private_key_file = 'private_key.pem'
    public_key_file = 'public_key.pem'
    
    if os.path.exists(private_key_file):
        # Load private key
        VAPID_PRIVATE_KEY = open(private_key_file, 'r').read()
        
        # Load and convert public key to base64url format for JavaScript
        vapid = Vapid.from_file(private_key_file)
        
        # Get raw public key bytes (65 bytes for P-256 uncompressed)
        from cryptography.hazmat.primitives import serialization
        public_key_bytes = vapid.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        
        # Convert to base64url (web-safe base64)
        import base64
        VAPID_PUBLIC_KEY = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8').rstrip('=')
        
        print(f"[+] Loaded existing VAPID keys")
    else:
        print(f"[!] No VAPID keys found - run key generation first")
        return
    
    print(f"[+] VAPID Public Key (base64url): {VAPID_PUBLIC_KEY[:50]}...")

def get_vapid_private_key():
    """Get VAPID private key"""
    return VAPID_PRIVATE_KEY

def get_vapid_public_key():
    """Get VAPID public key"""
    return VAPID_PUBLIC_KEY

def get_vapid_claims():
    """Get VAPID claims"""
    return VAPID_CLAIMS
