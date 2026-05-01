from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from database.mongodb import farmers_col

router = APIRouter()
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "kisanai-secret-key-2024"
ALGORITHM  = "HS256"

class RegisterRequest(BaseModel):
    name:     str
    phone:    str
    password: str
    state:    str
    district: str

class LoginRequest(BaseModel):
    phone:    str
    password: str

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=7)
    return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
async def register(req: RegisterRequest):
    existing = await farmers_col.find_one({"phone": req.phone})
    if existing:
        raise HTTPException(status_code=400, detail="Phone already registered")
    farmer = req.dict()
    farmer["password"] = pwd_ctx.hash(req.password)
    farmer["created_at"] = datetime.utcnow()
    result = await farmers_col.insert_one(farmer)
    token = create_token({"sub": str(result.inserted_id)})
    return {"token": token, "name": req.name, "message": "Registered successfully!"}

@router.post("/login")
async def login(req: LoginRequest):
    farmer = await farmers_col.find_one({"phone": req.phone})
    if not farmer or not pwd_ctx.verify(req.password, farmer["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": str(farmer["_id"])})
    return {"token": token, "name": farmer["name"]}