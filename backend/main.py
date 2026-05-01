from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, crop, disease, schemes

app = FastAPI(title="KisanAI API", version="1.0.0")

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    "https://reliable-clafoutis-a11d59.netlify.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/api/auth",    tags=["Auth"])
app.include_router(crop.router,     prefix="/api/crop",    tags=["Crop"])
app.include_router(disease.router,  prefix="/api/disease", tags=["Disease"])
app.include_router(schemes.router,  prefix="/api/schemes", tags=["Schemes"])

@app.get("/health")
def health():
    return {"status": "ok", "app": "KisanAI"}