# main.py
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

from database import get_db, test_connection, engine, SessionLocal
from models import Base, User, Influencer, Brand, Campaign, Match
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# STARTUP EVENT
# =====================================================

@app.on_event("startup")
def on_startup():
    print("🚀 Promobridge starting...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    test_connection()
    db = SessionLocal()
    try:
        count = db.query(Influencer).count()
        if count == 0:
            print("🌱 Seeding influencers...")
            seed_influencers(db)
            print(f"✅ Added {db.query(Influencer).count()} influencers")
        else:
            print(f"ℹ️  Database already has {count} influencers")
    except Exception as e:
        print(f"⚠️  Seeding error: {e}")
    finally:
        db.close()

# =====================================================
# ROOT & HEALTH
# =====================================================

@app.get("/")
def root():
    return {
        "name": "Promobridge API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected", "timestamp": datetime.utcnow()}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")

# =====================================================
# PYDANTIC SCHEMAS
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

class InfluencerCreate(BaseModel):
    full_name: str
    handle: str
    platform: str
    niche: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    followers_count: Optional[int] = 0
    engagement_rate: Optional[float] = 0.0

class InfluencerResponse(BaseModel):
    influencer_id: str
    full_name: str
    handle: str
    platform: str
    niche: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    followers_count: int
    engagement_rate: float
    class Config:
        orm_mode = True

class BrandCreate(BaseModel):
    brand_name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None

class CampaignCreate(BaseModel):
    title: str
    description: Optional[str] = None
    niche: Optional[str] = None
    platform: Optional[str] = None
    budget: Optional[float] = None
    min_followers: Optional[int] = None

class CampaignResponse(BaseModel):
    campaign_id: str
    title: str
    description: Optional[str]
    niche: Optional[str]
    platform: Optional[str]
    budget: Optional[float]
    min_followers: Optional[int]
    status: Optional[str]
    class Config:
        orm_mode = True

# =====================================================
# AUTHENTICATION
# =====================================================

@app.post("/auth/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return create_user_token(user)

@app.get("/auth/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    return current_user

# =====================================================
# INFLUENCERS
# =====================================================

@app.get("/influencers", response_model=List[InfluencerResponse])
def get_influencers(
    skip: int = 0,
    limit: int = 50,
    platform: Optional[str] = None,
    niche: Optional[str] = None,
    min_followers: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Influencer)
    if platform:
        query = query.filter(Influencer.platform == platform)
    if niche:
        query = query.filter(Influencer.niche == niche)
    if min_followers:
        query = query.filter(Influencer.followers_count >= min_followers)
    return query.offset(skip).limit(limit).all()

@app.get("/influencers/{influencer_id}", response_model=InfluencerResponse)
def get_influencer(influencer_id: str, db: Session = Depends(get_db)):
    influencer = db.query(Influencer).filter(Influencer.influencer_id == influencer_id).first()
    if not influencer:
        raise HTTPException(status_code=404, detail="Influencer not found")
    return influencer

@app.post("/influencers", response_model=InfluencerResponse)
def create_influencer(
    data: InfluencerCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    existing = db.query(Influencer).filter(Influencer.user_id == current_user.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Influencer profile already exists")
    new_inf = Influencer(
        user_id=current_user.user_id,
        full_name=data.full_name,
        handle=data.handle,
        platform=data.platform,
        niche=data.niche,
        bio=data.bio,
        location=data.location,
        followers_count=data.followers_count or 0,
        engagement_rate=data.engagement_rate or 0.0
    )
    db.add(new_inf)
    db.commit()
    db.refresh(new_inf)
    return new_inf

# =====================================================
# BRANDS
# =====================================================

@app.post("/brands")
def create_brand(
    brand_data: BrandCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    existing = db.query(Brand).filter(Brand.user_id == current_user.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Brand profile already exists")
    new_brand = Brand(
        user_id=current_user.user_id,
        brand_name=brand_data.brand_name,
        industry=brand_data.industry,
        website=brand_data.website,
        description=brand_data.description
    )
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return {"brand_id": new_brand.brand_id, "brand_name": new_brand.brand_name}

@app.get("/brands")
def get_brands(db: Session = Depends(get_db)):
    brands = db.query(Brand).all()
    return [{"brand_id": b.brand_id, "brand_name": b.brand_name, "industry": b.industry, "website": b.website, "description": b.description} for b in brands]

# =====================================================
# CAMPAIGNS
# =====================================================

@app.post("/campaigns", response_model=CampaignResponse)
def create_campaign(
    data: CampaignCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    new_campaign = Campaign(
        user_id=current_user.user_id,
        title=data.title,
        description=data.description,
        niche=data.niche,
        platform=data.platform,
        budget=data.budget,
        min_followers=data.min_followers,
        status="active"
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

@app.get("/campaigns", response_model=List[CampaignResponse])
def get_campaigns(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return db.query(Campaign).offset(skip).limit(limit).all()

# =====================================================
# STATS
# =====================================================

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "total_influencers": db.query(Influencer).count(),
        "total_brands": db.query(Brand).count(),
        "total_campaigns": db.query(Campaign).count(),
        "active_campaigns": db.query(Campaign).filter(Campaign.status == 'active').count(),
        "total_matches": db.query(Match).count(),
        "success_rate": 95.0
    }

# =====================================================
# PRICING CALCULATOR
# =====================================================

@app.post("/calculate-pricing")
def calculate_pricing(
    followers: int,
    engagement_rate: float,
    platform: str,
    content_type: str = "post"
):
    base_cpm = 10
    platform_multipliers = {"instagram": 1.0, "youtube": 1.5, "tiktok": 0.8, "twitter": 0.7}
    content_multipliers = {"post": 1.0, "story": 0.5, "reel": 1.3, "video": 1.5}
    platform_mult = platform_multipliers.get(platform.lower(), 1.0)
    content_mult = content_multipliers.get(content_type.lower(), 1.0)
    engagement_mult = 1 + (engagement_rate / 100)
    suggested_price = (followers / 1000) * base_cpm * engagement_mult * platform_mult * content_mult
    return {
        "suggested_price": round(suggested_price, 2),
        "min_price": round(suggested_price * 0.8, 2),
        "max_price": round(suggested_price * 1.2, 2),
        "currency": "USD"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
