from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from collections import defaultdict

app = FastAPI()

API_KEY = "ak_k6y590pvb5857adgly10ps41"
EMAIL = "24f2004664@ds.study.iitm.ac.in"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/analytics")
def analytics(
    data: AnalyticsRequest,
    x_api_key: str | None = Header(default=None)
):
    # Authentication check
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    events = data.events

    total_events = len(events)

    users = set()
    revenue = 0.0
    totals = defaultdict(float)

    for e in events:
        users.add(e.user)

        if e.amount > 0:
            revenue += e.amount
            totals[e.user] += e.amount

    top_user = max(
        totals,
        key=totals.get
    ) if totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user
    }
