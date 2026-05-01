from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
sys.path.append("..")
from ml.crop_model import recommend_crops
from database.mongodb import crop_col
from datetime import datetime

router = APIRouter()

class CropInput(BaseModel):
    N:           float
    P:           float
    K:           float
    temperature: float
    humidity:    float
    ph:          float
    rainfall:    float

CROP_INFO = {
    "Rice":     {"season": "Kharif (Jun–Nov)",  "water": "High",   "price_range": "₹1800–2200/qtl"},
    "Maize":    {"season": "Kharif/Rabi",        "water": "Medium", "price_range": "₹1700–2000/qtl"},
    "Chickpea": {"season": "Rabi (Oct–Mar)",     "water": "Low",    "price_range": "₹4800–5400/qtl"},
    "Cotton":   {"season": "Kharif (Apr–Nov)",   "water": "Medium", "price_range": "₹6000–7000/qtl"},
    "Banana":   {"season": "Year-round",          "water": "High",   "price_range": "₹800–1500/qtl"},
    "Mango":    {"season": "Summer (Apr–Jun)",   "water": "Low",    "price_range": "₹2000–6000/qtl"},
    "Coffee":   {"season": "Year-round",          "water": "Medium", "price_range": "₹6000–8000/qtl"},
}

@router.post("/recommend")
async def crop_recommend(inputs: CropInput):
    if not (0 <= inputs.ph <= 14):
        raise HTTPException(status_code=400, detail="pH must be between 0 and 14")
    results = recommend_crops(
        inputs.N, inputs.P, inputs.K,
        inputs.temperature, inputs.humidity,
        inputs.ph, inputs.rainfall
    )
    for r in results:
        info = CROP_INFO.get(r["crop"], {})
        r["season"]      = info.get("season",      "Varies by region")
        r["water_need"]  = info.get("water",       "Moderate")
        r["price_range"] = info.get("price_range", "Check local mandi")
    await crop_col.insert_one({
        "inputs": inputs.dict(),
        "results": results,
        "timestamp": datetime.utcnow()
    })
    return {"top_crops": results, "tip": "Choose based on your local market demand and water availability."}