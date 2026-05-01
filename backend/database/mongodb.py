import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

print(f"Connecting to: {MONGO_URL[:30]}...")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["kisanai"]

farmers_col = db["farmers"]
disease_col = db["disease_logs"]
crop_col    = db["crop_recommendations"]
schemes_col = db["schemes"]