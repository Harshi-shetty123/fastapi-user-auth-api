# FastAPI User Auth API

Secure user registration and login with JWT, bcrypt, and Pydantic.

## Features
- Register `/register`
- Login `/login` → JWT
- Protected `/me`
- Password hashing (bcrypt)
- Environment variables

## Run
```bash
uvicorn main:app --reload

## API Docs
http://127.0.0.1:8000/docs


---

## Final Setup Commands (Run All)

```bash
# 1. Go to project
cd ~/Hitha_Shetty/Projects/fastapi-user-auth-api

# 2. Create fresh venv
rm -rf venv
python -m venv venv
source venv/bin/activate

# 3. Install deps
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create folders
mkdir -p auth models schemas

# 5. Create __init__.py
touch auth/__init__.py models/__init__.py schemas/__init__.py

# 6. Run
uvicorn main:app --reload
