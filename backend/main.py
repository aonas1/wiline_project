# main.py
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request/response validation
class User(BaseModel):
    _id: str
    firstName: str
    lastName: str
    email: str
    phoneNumber: Optional[str] = None

# Seed data
users_data = [
    {"_id": "5f0f36345628b2bb08ddcf83", "firstName": "Marina", "lastName": "Orozco", "email": "marina@wiline.com"},
    {"_id": "5f0f3634a3357afc09a0333d", "firstName": "Kip", "lastName": "Winters", "email": "kip@wiline.com"},
    # (others omitted for brevity)
    {"_id": "5f0f3634e8dfd9bbde33c703", "firstName": "Delores", "lastName": "Sanchez", "email": "delores@wiline.com"}
]

phones_data = [
    {"email": "liliana@wiline.com", "phoneNumber": "051656592"},
    {"email": "florencio@wiline.com", "phoneNumber": "051329392"},
    {"email": "delores@wiline.com", "phoneNumber": "051334392"}
]

# Merge users and phones by email
def seed_users():
    user_list = []
    for u in users_data:
        phone = next((p["phoneNumber"] for p in phones_data if p["email"] == u["email"]), None)
        user_list.append(User(**u, phoneNumber=phone))
    return user_list

# In-memory database
users = seed_users()

@app.get("/users", response_model=List[User])
def get_users(query: Optional[str] = None, email: Optional[str] = None, phoneNumber: Optional[str] = None):
    """
    Get all users or filter by query, email, or phoneNumber
    """
    result = users
    if query:
        result = [u for u in result if query.lower() in (u.firstName + u.lastName).lower()]
    if email:
        result = [u for u in result if u.email == email]
    if phoneNumber:
        result = [u for u in result if u.phoneNumber == phoneNumber]
    return result

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    """
    Get a single user by ID
    """
    for user in users:
        if user._id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users", response_model=User)
def create_user(user: User):
    """
    Create a new user entry
    """
    user._id = str(uuid4())  # Generate a new unique ID
    users.append(user)
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, updated_user: User):
    """
    Update user by ID
    """
    for i, user in enumerate(users):
        if user._id == user_id:
            updated_user._id = user_id
            users[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")
