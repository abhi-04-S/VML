from datetime import datetime, timedelta

from jose import JWTError, jwt

# Secret key to sign the JWT tokens. In a real app, keep this secret!
SECRET_KEY = "super_secret_internship_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

import bcrypt

def verify_password(plain_password, hashed_password):
    """Check if the provided password matches the hashed password"""
    # bcrypt requires bytes for both the password and the hash
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def get_password_hash(password):
    """Hash a plaintext password"""
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Decode back to a string to store in the database easily
    return hashed_bytes.decode('utf-8')

def create_access_token(data: dict):
    """Generate a new JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
