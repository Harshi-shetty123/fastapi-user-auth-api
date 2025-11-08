from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from dotenv import load_dotenv
from typing import Optional
import os

from schemas.user import UserCreate, UserLogin, UserOut
from models.user import create_user, get_user_by_email, fake_users_db
from auth.jwt_handler import create_access_token, verify_token

load_dotenv()

app = FastAPI(title="FastAPI User Auth API", version="1.0.0")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# === Helpers ===
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    if len(password.encode('utf-8')) > 72:
        raise HTTPException(status_code=400, detail="Password too long (max 72 chars)")
    return pwd_context.hash(password)

def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[dict]:
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# === Routes ===
@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(user.password)
    user_id = len(fake_users_db) + 1
    db_user = create_user(user_id, user.email, hashed, user.full_name)
    return UserOut(id=db_user["id"], email=db_user["email"], full_name=db_user["full_name"])

# LOGIN ROUTE
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = get_user_by_email(form_data.username)
    if not db_user or not verify_password(form_data.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", response_model=UserOut)
def read_users_me(current_user: dict = Depends(get_current_user)):
    return UserOut(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"]
    )