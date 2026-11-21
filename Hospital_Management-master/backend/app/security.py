import hashlib
import hmac
import os
import json
import base64
import time
from typing import Optional, Dict, Any
from backend.app.config import settings

def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with a unique salt."""
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return salt.hex() + "$" + key.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against salt$hash representation."""
    try:
        if "$" not in hashed_password:
            # Fallback for plain demo passwords
            return plain_password == hashed_password
        salt_hex, key_hex = hashed_password.split("$", 1)
        salt = bytes.fromhex(salt_hex)
        expected_key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, 100000)
        return hmac.compare_digest(expected_key.hex(), key_hex)
    except Exception:
        return False

def create_access_token(data: Dict[str, Any], expires_delta_seconds: Optional[int] = None) -> str:
    """Create a tamper-proof signed token without external heavy dependencies."""
    payload = data.copy()
    expire = int(time.time()) + (expires_delta_seconds if expires_delta_seconds else settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    payload["exp"] = expire
    
    payload_json = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode("utf-8")
    payload_b64 = base64.urlsafe_b64encode(payload_json).decode("utf-8").rstrip("=")
    
    sig = hmac.new(settings.SECRET_KEY.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{sig}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify token integrity and expiration."""
    try:
        if "." not in token:
            return None
        payload_b64, sig = token.split(".", 1)
        expected_sig = hmac.new(settings.SECRET_KEY.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        
        # Add padding back if necessary
        padded = payload_b64 + "=" * (-len(payload_b64) % 4)
        payload_json = base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8")
        payload = json.loads(payload_json)
        
        if "exp" in payload and time.time() > payload["exp"]:
            return None
        return payload
    except Exception:
        return None
