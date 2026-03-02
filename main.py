# backend/main.py
"""
Promobridge Backend API
Main FastAPI application
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uvicorn

# =====================================================
# DATABASE & MODELS
# =====================================================

from database import (
    get_db,
    test_connection,
    engine,
    SessionLocal
)
from models import (
    Base,
    User,
    Influencer,
    Brand,
    Campaign,
    Match
)

from seed_data import seed_influencers

from auth import (
    hash_password,
    authenticate_user,
    create_user_token,
    get_current_active_user,
    require_role
)

# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="Promobridge API",
    description="Smart Influencer-Brand Matching Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# STARTUP EVENTS
# =====================================================

@app.on_event("startup")
def on_startup():
    print("🚀 Promobridge starting...")

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready")

    # Test DB
    test_connection()

    # Seed influencers if empty
    db = SessionLocal()
    try:
        count = db.query(Influencer).count()
        if count == 0:
            seed_influencers(db)
            print("🌱 Influencers seeded successfully")
        else:
            print(f"ℹ️ Influencers already exist ({count})")
    finally:
        db.close()

# =====================================================
# ROOT & HEALTH
# =====================================================

@app.get("/")
def root():
    return {
        "name": "Promobridge API",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
def health(db: Session = Depends(get_db)):
    from sqlalchemy import text
    db.execute(text("SELECT 1"))
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }

# =====================================================
# AUTH
# =====================================================

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str

class UserResponse(BaseModel):
    user_id: str
    email: str
    role: str
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True

@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email already exists")

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return create_user_token(user)

@app.get("/auth/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_active_user)):
    return current_user

# =====================================================
# INFLUENCERS
# =====================================================

class InfluencerResponse(BaseModel):
    influencer_id: str
    full_name: str
    platform: str
    niche: Optional[str]
    followers_count: int
    engagement_rate: float

    class Config:
        orm_mode = True

@app.get("/influencers", response_model=List[InfluencerResponse])
def get_influencers(
    niche: Optional[str] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Influencer)

    if niche:
        q = q.filter(Influencer.niche == niche)
    if platform:
        q = q.filter(Influencer.platform == platform)

    return q.all()

# =====================================================
# STATS (FIXES YOUR 0 ISSUE)
# =====================================================

@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    return {
        "total_influencers": db.query(Influencer).count(),
        "total_brands": db.query(Brand).count(),
        "total_campaigns": db.query(Campaign).count(),
        "total_matches": db.query(Match).count()
    }

# =====================================================
# RUN LOCAL ONLY
# =====================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
