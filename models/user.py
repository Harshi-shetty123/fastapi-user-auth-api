from typing import Dict, Optional, Any

# Fake in-memory DB
fake_users_db: Dict[str, dict] = {}

def create_user(user_id: int, email: str, hashed_password: str, full_name: Optional[str] = None) -> dict:
    user = {
        "id": user_id,
        "email": email,
        "hashed_password": hashed_password,
        "full_name": full_name
    }
    fake_users_db[email] = user
    return user

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    return fake_users_db.get(email)