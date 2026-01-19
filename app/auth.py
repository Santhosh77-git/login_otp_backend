import hashlib
import random
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def otp_expiry():
    return datetime.utcnow() + timedelta(minutes=5)
