"""
NearDeals — Hyperlocal Deals Platform
Backend API built with FastAPI
College project by: [Your Name] | Dept. of Computer Science
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx
import os
import json

app = FastAPI(
    title="NearDeals API",
    description="Hyperlocal deals discovery backend with AI assistant",
    version="1.0.0"
)

# Allow frontend on any origin (dev-friendly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory deals store (replace with DB in production)
# ---------------------------------------------------------------------------
DEALS_DB = [
    {
        "id": 1, "shop": "Annapoorna Mess", "cat": "food",
        "deal": "Unlimited thali lunch special", "discount": 35,
        "distance": 0.4, "expiry": "Today 3pm", "urgent": True,
        "hasSeats": True, "icon": "🍛",
        "address": "12, Gandhi Nagar, Coimbatore",
        "lat": 11.0168, "lng": 76.9558,
        "seats": [1,2,3,4,5,6], "occupiedSeats": [3,6],
        "stock": None
    },
    {
        "id": 2, "shop": "VRM Textiles", "cat": "textile",
        "deal": "Cotton sarees buy 2 get 1 free", "discount": 33,
        "distance": 0.9, "expiry": "2 days left", "urgent": False,
        "hasSeats": False, "icon": "🧵",
        "address": "45, Textile Market, Coimbatore",
        "lat": 11.0020, "lng": 76.9629,
        "stock": None
    },
    {
        "id": 3, "shop": "PhoneBazaar", "cat": "electronics",
        "deal": "Earbuds flat ₹500 off + free case", "discount": 28,
        "distance": 1.1, "expiry": "3 days left", "urgent": False,
        "hasSeats": False, "icon": "📱",
        "address": "77, Cross Cut Road, Coimbatore",
        "lat": 11.0115, "lng": 76.9712,
        "stock": None
    },
    {
        "id": 4, "shop": "Daily Fresh Mart", "cat": "grocery",
        "deal": "Organic vegetables 20% off", "discount": 20,
        "distance": 0.6, "expiry": "Today 8pm", "urgent": True,
        "hasSeats": False, "icon": "🛒",
        "address": "3, Ram Nagar, Coimbatore",
        "lat": 11.0200, "lng": 76.9500,
        "stock": [
            {"name": "Tomatoes", "status": "high"},
            {"name": "Spinach", "status": "low"},
            {"name": "Onions", "status": "high"},
            {"name": "Brinjal", "status": "out"}
        ]
    },
    {
        "id": 5, "shop": "CureWell Pharmacy", "cat": "health",
        "deal": "Generic medicines 15% off on all brands", "discount": 15,
        "distance": 1.5, "expiry": "Week end", "urgent": False,
        "hasSeats": False, "icon": "💊",
        "address": "19, LGB Nagar, Coimbatore",
        "lat": 11.0080, "lng": 76.9670,
        "stock": [
            {"name": "Paracetamol", "status": "high"},
            {"name": "Cetrizine", "status": "low"},
            {"name": "Vitamins", "status": "high"}
        ]
    },
    {
        "id": 6, "shop": "Brew Lab Café", "cat": "cafe",
        "deal": "Buy any cold brew, get a croissant free", "discount": 40,
        "distance": 0.7, "expiry": "Today 9pm", "urgent": True,
        "hasSeats": True, "icon": "☕",
        "address": "88, Avinashi Road, Coimbatore",
        "lat": 11.0140, "lng": 76.9600,
        "seats": [1,2,3,4,5], "occupiedSeats": [2,4],
        "stock": None
    },
    {
        "id": 7, "shop": "Inox Cinemas", "cat": "entertainment",
        "deal": "Wednesday flat ₹100 off on all shows", "discount": 25,
        "distance": 2.1, "expiry": "Today only", "urgent": True,
        "hasSeats": False, "icon": "🎬",
        "address": "Brookefields Mall, Coimbatore",
        "lat": 11.0050, "lng": 76.9750,
        "stock": None
    },
    {
        "id": 8, "shop": "Sri Murugan Mess", "cat": "food",
        "deal": "Chettinad meals ₹60 flat (was ₹92)", "discount": 35,
        "distance": 1.8, "expiry": "4 days left", "urgent": False,
        "hasSeats": True, "icon": "🍱",
        "address": "56, Saibaba Colony, Coimbatore",
        "lat": 11.0230, "lng": 76.9480,
        "seats": [1,2,3,4,5,6,7,8], "occupiedSeats": [1,5,7],
        "stock": None
    },
    {
        "id": 9, "shop": "TechZone", "cat": "electronics",
        "deal": "Laptop accessories 30% off clearance", "discount": 30,
        "distance": 3.2, "expiry": "2 days left", "urgent": False,
        "hasSeats": False, "icon": "💻",
        "address": "DR. Nanjappa Road, Coimbatore",
        "lat": 11.0010, "lng": 76.9820,
        "stock": None
    },
    {
        "id": 10, "shop": "Nature's Basket", "cat": "grocery",
        "deal": "Dry fruits combo pack ₹199 (was ₹350)", "discount": 43,
        "distance": 4.5, "expiry": "5 days left", "urgent": False,
        "hasSeats": False, "icon": "🥜",
        "address": "Peelamedu, Coimbatore",
        "lat": 11.0280, "lng": 76.9920,
        "stock": [
            {"name": "Cashews", "status": "high"},
            {"name": "Almonds", "status": "low"},
            {"name": "Raisins", "status": "high"}
        ]
    }
]

BOOKINGS_DB = []
PENDING_SHOPS = []

# ---------------------------------------------------------------------------
# Deals endpoints
# ---------------------------------------------------------------------------

@app.get("/deals")
def get_deals(radius: float = 5.0, cat: str = "all", sort: str = "distance"):
    deals = [d for d in DEALS_DB if d["distance"] <= radius]
    if cat != "all":
        deals = [d for d in deals if d["cat"] == cat]
    if sort == "discount":
        deals.sort(key=lambda d: d["discount"], reverse=True)
    elif sort == "expiry":
        deals.sort(key=lambda d: d["urgent"], reverse=True)
    else:
        deals.sort(key=lambda d: d["distance"])
    return {"deals": deals, "count": len(deals)}


@app.get("/deals/{deal_id}")
def get_deal(deal_id: int):
    deal = next((d for d in DEALS_DB if d["id"] == deal_id), None)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@app.get("/stats")
def get_stats(radius: float = 5.0):
    in_radius = [d for d in DEALS_DB if d["distance"] <= radius]
    avg_disc = round(sum(d["discount"] for d in in_radius) / len(in_radius)) if in_radius else 0
    urgent = sum(1 for d in in_radius if d["urgent"])
    shops = len(set(d["shop"] for d in in_radius))
    return {
        "total_deals": len(in_radius),
        "total_shops": shops,
        "avg_discount": avg_disc,
        "expiring_soon": urgent
    }

# ---------------------------------------------------------------------------
# Booking endpoint
# ---------------------------------------------------------------------------

class BookingRequest(BaseModel):
    deal_id: int
    table_num: int
    time_slot: str
    guest_count: int
    name: str
    phone: str
    note: Optional[str] = ""


@app.post("/book")
def book_table(req: BookingRequest):
    deal = next((d for d in DEALS_DB if d["id"] == req.deal_id), None)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    if not deal.get("hasSeats"):
        raise HTTPException(status_code=400, detail="This deal does not support table booking")
    if req.table_num in deal.get("occupiedSeats", []):
        raise HTTPException(status_code=409, detail="Table already occupied")

    # Mark seat occupied
    deal.setdefault("occupiedSeats", []).append(req.table_num)

    booking = {
        "id": len(BOOKINGS_DB) + 1,
        "deal_id": req.deal_id,
        "shop": deal["shop"],
        "table": req.table_num,
        "time": req.time_slot,
        "guests": req.guest_count,
        "name": req.name,
        "phone": req.phone,
        "note": req.note,
        "deal": deal["deal"]
    }
    BOOKINGS_DB.append(booking)
    return {"success": True, "booking": booking}

# ---------------------------------------------------------------------------
# Shop registration endpoint
# ---------------------------------------------------------------------------

class ShopRegistration(BaseModel):
    name: str
    category: str
    city: str
    phone: str
    deal: str
    discount: int
    expiry: str
    address: Optional[str] = ""


@app.post("/register-shop")
def register_shop(req: ShopRegistration):
    PENDING_SHOPS.append(req.dict())
    return {"success": True, "message": "Submitted! Goes live after review — usually < 2 hours."}

# ---------------------------------------------------------------------------
# AI Deal Assistant endpoint  (calls Anthropic API server-side)
# ---------------------------------------------------------------------------

class AIRequest(BaseModel):
    question: str
    radius: float = 5.0
    city: Optional[str] = ""


@app.post("/ai-chat")
async def ai_chat(req: AIRequest):
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not set on server")

    in_radius = [d for d in DEALS_DB if d["distance"] <= req.radius]
    deal_list = "\n".join(
        f"• {d['shop']} ({d['cat']}) — {d['deal']} | {d['discount']}% off | {d['distance']} km"
        f" | expiry: {d['expiry']}{' [URGENT]' if d['urgent'] else ''}"
        f"{' [TABLE BOOKING]' if d['hasSeats'] else ''}"
        for d in in_radius
    ) or "(No deals in current radius)"

    urgent_shops = ", ".join(d["shop"] for d in in_radius if d["urgent"]) or "none"

    system_prompt = f"""You are a friendly hyperlocal deals assistant for NearDeals — a student-built app showing deals from nearby shops.

CURRENT DEALS (within {req.radius} km of user):
{deal_list}

USER CITY: {req.city or 'not detected'}
URGENT / EXPIRING TODAY: {urgent_shops}

GUIDELINES:
- Be warm, conversational, helpful. 2-4 sentences max.
- Mention exact shop names and discount percentages.
- If asked about table booking, mention clicking "Book" on relevant cards.
- Use 1-2 emojis per reply. Never invent deals not in the list.
- If no deals match, suggest widening the radius or different category."""

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 300,
        "system": system_prompt,
        "messages": [{"role": "user", "content": req.question}]
    }

    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            text = data.get("content", [{}])[0].get("text", "")
            return {"reply": text}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"AI API error: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "project": "NearDeals API", "version": "1.0.0"}
