"""
VAPID keys - load from files
"""

# Load keys from files
with open('private_key.pem', 'r') as f:
    VAPID_PRIVATE_KEY = f.read()

with open('public_key.pem', 'r') as f:
    VAPID_PUBLIC_KEY = f.read().strip()

VAPID_CLAIMS = {
    "sub": "mailto:admin@ronniec2.bigbicep"
}

print(f"[+] VAPID keys loaded from files")
print(f"[+] Public key: {VAPID_PUBLIC_KEY}")
