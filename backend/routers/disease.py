from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
import random

router = APIRouter()

MOCK_RESULTS = [
    {
        "disease":         "Tomato Late Blight",
        "confidence":      94.2,
        "severity":        "High",
        "organic_remedy":  "Spray neem oil (5ml/L water) every 7 days. Remove infected leaves.",
        "chemical_remedy": "Apply Mancozeb 75WP @ 2g/L or Chlorothalonil 75WP @ 2g/L.",
        "prevention":      "Avoid overhead irrigation. Ensure proper plant spacing."
    },
    {
        "disease":         "Bacterial Leaf Blight (Rice)",
        "confidence":      87.5,
        "severity":        "Moderate",
        "organic_remedy":  "Apply Pseudomonas fluorescens solution. Drain excess water.",
        "chemical_remedy": "Spray Streptocycline 500ppm + Copper oxychloride 0.3%.",
        "prevention":      "Use certified disease-free seeds. Avoid excess nitrogen."
    },
    {
        "disease":         "Powdery Mildew",
        "confidence":      91.8,
        "severity":        "Moderate",
        "organic_remedy":  "Spray diluted milk solution (1:9 ratio) or baking soda (1 tsp/L).",
        "chemical_remedy": "Apply Sulfur 80WP @ 2g/L or Hexaconazole 5EC @ 1ml/L.",
        "prevention":      "Improve air circulation. Avoid overhead watering in evenings."
    }
]

@router.post("/detect")
async def detect_disease(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file")
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large. Max 10MB.")
    result = random.choice(MOCK_RESULTS)
    return {
        "status":          "detected",
        "disease":         result["disease"],
        "confidence":      result["confidence"],
        "severity":        result["severity"],
        "organic_remedy":  result["organic_remedy"],
        "chemical_remedy": result["chemical_remedy"],
        "prevention":      result["prevention"],
        "timestamp":       datetime.utcnow().isoformat(),
        "note":            "Demo mode — real AI model coming in Week 2!"
    }