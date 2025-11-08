from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# === Correct relative imports ===
from schemas.user import UserCreate, UserLogin, UserOut
from models.user import create_user, get_user_by_email, fake_users_db
from auth.jwt_handler import create_access_token

load_dotenv()

app = FastAPI(title="My FastAPI Auth Project")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# === Helper Functions ===
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # bcrypt limit: 72 bytes
    if len(password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password too long. Maximum 72 characters allowed."
        )
    return pwd_context.hash(password)

# === Routes ===

@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    # Check if user exists
    if get_user_by_email(user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = get_password_hash(user.password)

    # Create user (assign ID)
    user_id = len(fake_users_db) + 1
    db_user = create_user(
        user_id=user_id,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )

    # Return user without password
    return UserOut(id=db_user["id"], email=db_user["email"], full_name=db_user["full_name"])


@app.post("/login")
def login(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
