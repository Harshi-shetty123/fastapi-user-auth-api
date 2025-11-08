# FastAPI User Auth API 

A **user authentication API** built using **FastAPI**, featuring secure JWT authentication, password hashing, and Pydantic validation.  

---

## Overview

This project implements:
- **Secure Registration & Login**
- **JWT Tokens** with Expiry
- **bcrypt Password Hashing**
- **Pydantic Validation**
- **Environment Variables**
- **Protected `/me` Route**


---

## Project Structure

```bash
fastapi-user-auth-api/
├── main.py                
├── requirements.txt      
├── .env                     
├── .gitignore
├── README.md            
│
├── auth/
│   ├── __init__.py
│   └── jwt_handler.py       # JWT create/verify
│
├── models/
│   ├── __init__.py
│   └── user.py              # Fake DB+helpers
│
└── schemas/
    ├── __init__.py
    └── user.py              # Pydantic models
```

---

## Installation

```bash
git clone https://github.com/Harshi-shetty123/fastapi-user-auth-api.git
cd fastapi-user-auth-api
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## requirements.txt

```text
fastapi==0.121.0
uvicorn==0.38.0
python-dotenv==1.2.1
passlib[bcrypt]==1.7.4
bcrypt==4.0.1
python-jose[cryptography]==3.5.0
pydantic[email]==2.12.4
```

**Why pinned versions?**
- `bcrypt==4.0.1`: fixes `__about__` bug with `passlib`
- Pinned = no dependency conflicts

---

## .env

```env
SECRET_KEY=your-super-secret-jwt-key-2025-change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Route Summary

| Route | Method | Purpose |
|-------|---------|----------|
| `/register` | POST | To create new user (hashed password) |
| `/login` | POST | To validate credentials & return JWT |
| `/me` | GET | Protected route, returns current user |

---

## Security Features

| Feature | Implementation |
|----------|----------------|
| Password Hashing | `bcrypt` via `passlib` |
| JWT Signing | HS256 with secret from `.env` |
| Input Validation | Pydantic Models |
| Token Expiry | 30 minutes (configurable) |
| Protected Routes | Depends(`get_current_user`) |

---

## How It Works

1. **Register** → hash password → save user in fake DB  
2. **Login** → verify password → create JWT (`sub: email`)  
3. **Access `/me`** → verify JWT → return user info

```bash
# Run app
uvicorn main:app --reload

# Example flow (Swagger UI)
POST /register → create user  
POST /login → get JWT  
Authorize → Bearer <token>  
GET /me → current user
```

---


## Author

**Harshitha Ratna M**  
🔗 [GitHub Profile](https://github.com/Harshi-shetty123)

---
