from typing import List
from models import User, Gender, Role, UserUpdateRequest
from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4


app = FastAPI()

db: List[User] = [
    User(
        id = UUID("422cc447-526e-4ae5-985a-e351ba31ae1c"),
        first_name ="John",
        last_name = "Doe",
        gender = Gender.male,
        roles = [Role.admin, Role.user]

    ),
    User(
        id = UUID("587455d3-3f90-45c2-acd1-992a3c886590"),
        first_name="Jane",
        last_name="Doe",
        gender = Gender.female,
        roles = [Role.user]

    )

]

@app.get("/")
async def root():
    return{
        "message":"Welcome to my APIs"
    }


@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.put("/api/v1/users/{user_id}")
async def update_users(user_update: UserUpdateRequest, user_id: UUID):
    for i in db:
        if i.id == user_id:
            if user_update.first_name is not None:
               i.first_name = user_update.first_name
            if user_update.last_name is not None:
               i.last_name = user_update.last_name
            if user_update.middle_name is not None:
               i.middle_name = user_update.middle_name
            if user_update.gender is not None:
               i.gender = user_update.gender
            if user_update.first_name is not None:
               i.roles = user_update.roles
            return

    raise HTTPException(
        status_code=404,
        detail=f"user with {user_id} does not exist"
    ) 

    

@app.post("/api/v1/users")
async def create_user(user: User):
    if user not in db:
        db.append(user)
        return {"id": user.id}

    else:
        raise HTTPException(status_code=409, detail=f"The user with {user.id} already exists")
