from typing import List, Dict

# Fake database
fake_users_db: Dict[str, dict] = {}

def create_user(user_id: int, email: str, hashed_password: str, full_name: str = None):
    user = {
        "id": user_id,
        "email": email,
        "hashed_password": hashed_password,
        "full_name": full_name
    }
    fake_users_db[email] = user
    return user

def get_user_by_email(email: str):
    return fake_users_db.get(email)
