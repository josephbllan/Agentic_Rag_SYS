"""
Password hashing and verification.
Includes compatibility patches for passlib + bcrypt >= 4.1.
"""
import bcrypt as _bcrypt

# Patch 1: passlib reads bcrypt.__about__.__version__ which was removed in bcrypt 4.1
if not hasattr(_bcrypt, "__about__"):
    class _About:
        __version__ = getattr(_bcrypt, "__version__", "4.0.0")
    _bcrypt.__about__ = _About

# Patch 2: bcrypt 4.2+ raises on passwords > 72 bytes instead of silently
# truncating. passlib's internal wrap-bug detection sends a 73-byte password.
_original_hashpw = _bcrypt.hashpw

def _patched_hashpw(password: bytes, salt: bytes) -> bytes:
    if isinstance(password, bytes) and len(password) > 72:
        password = password[:72]
    return _original_hashpw(password, salt)

_bcrypt.hashpw = _patched_hashpw

from passlib.context import CryptContext  # noqa: E402

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
