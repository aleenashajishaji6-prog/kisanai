from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FarmerProfile(BaseModel):
    state:     str
    land_ha:   float
    caste:     str
    has_bank:  bool
    crop_type: str
    is_woman:  bool = False

ALL_SCHEMES = [
    {"id":"pm-kisan","name":"PM KISAN Samman Nidhi","ministry":"Ministry of Agriculture","benefit":"Rs 6000 per year direct bank transfer","deadline":"Ongoing","documents":["Aadhaar","Bank Passbook","Land Records"],"portal":"https://pmkisan.gov.in","conditions":{"has_bank":True,"max_land_ha":2.0}},
    {"id":"pmfby","name":"PMFBY Fasal Bima Yojana","ministry":"Ministry of Agriculture","benefit":"Crop insurance at 2 percent premium","deadline":"Before sowing season","documents":["Aadhaar","Bank Account","Land Records"],"portal":"https://pmfby.gov.in","conditions":{}},
    {"id":"kcc","name":"Kisan Credit Card KCC","ministry":"NABARD RBI","benefit":"Credit up to Rs 3 lakh at 4 percent interest","deadline":"Ongoing","documents":["Aadhaar","PAN Card","Land Records"],"portal":"https://www.nabard.org","conditions":{"has_bank":True}},
    {"id":"soil","name":"Soil Health Card Scheme","ministry":"Ministry of Agriculture","benefit":"Free soil testing and recommendations","deadline":"Ongoing","documents":["Aadhaar","Land Records"],"portal":"https://soilhealth.dac.gov.in","conditions":{}},
    {"id":"drip","name":"PM Krishi Sinchai Drip Irrigation","ministry":"Ministry of Jal Shakti","benefit":"55 to 75 percent subsidy on drip equipment","deadline":"Before March 31","documents":["Aadhaar","Land Records","Bank Account"],"portal":"https://pmksy.gov.in","conditions":{"max_land_ha":5.0}},
    {"id":"mahila","name":"Mahila Kisan Sashaktikaran","ministry":"Ministry of Rural Development","benefit":"Training seeds tools and financial support","deadline":"Ongoing","documents":["Aadhaar","Bank Passbook","Land Records"],"portal":"https://aajeevika.gov.in","conditions":{"is_woman":True}},
    {"id":"sc-st","name":"SC ST Farmers Input Subsidy","ministry":"State Agriculture Departments","benefit":"Up to 50 percent subsidy on seeds and equipment","deadline":"Varies by state","documents":["Aadhaar","Caste Certificate","Land Records"],"portal":"https://agricoop.nic.in","conditions":{"caste_in":["sc","st"]}},
]

def matches(scheme, profile):
    cond = scheme.get("conditions", {})
    if "has_bank" in cond and not profile.has_bank:
        return False
    if "max_land_ha" in cond and profile.land_ha > cond["max_land_ha"]:
        return False
    if "is_woman" in cond and cond["is_woman"] and not profile.is_woman:
        return False
    if "caste_in" in cond and profile.caste.lower() not in cond["caste_in"]:
        return False
    return True

@router.post("/match")
async def match_schemes(profile: FarmerProfile):
    matched = [s for s in ALL_SCHEMES if matches(s, profile)]
    return {"total_matched":len(matched),"schemes":matched,"message":f"Found {len(matched)} schemes you are eligible for!"}

@router.get("/all")
async def list_all():
    return {"schemes":ALL_SCHEMES,"total":len(ALL_SCHEMES)}