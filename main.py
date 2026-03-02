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

# CORS Configuration
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
    """Initialize database and seed data on startup"""
    print("🚀 Promobridge starting...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Test connection
    test_connection()
    
    # Seed influencers if database is empty
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
    """Root endpoint"""
    return {
        "name": "Promobridge API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {str(e)}"
        )

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

class InfluencerResponse(BaseModel):
    influencer_id: str
    full_name: str
    handle: str
    platform: str
    niche: Optional[str]
    followers_count: int
    engagement_rate: float
    
    class Config:
        orm_mode = True

# =====================================================
# AUTHENTICATION
# =====================================================

@app.post("/auth/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register new user"""
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
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
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint"""
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    return create_user_token(user)

@app.get("/auth/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user info"""
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
    """Get list of influencers with filters"""
    query = db.query(Influencer)
    
    # Apply filters
    if platform:
        query = query.filter(Influencer.platform == platform)
    if niche:
        query = query.filter(Influencer.niche == niche)
    if min_followers:
        query = query.filter(Influencer.followers_count >= min_followers)
    
    # Get results
    influencers = query.offset(skip).limit(limit).all()
    
    return influencers

@app.get("/influencers/{influencer_id}", response_model=InfluencerResponse)
def get_influencer(influencer_id: str, db: Session = Depends(get_db)):
    """Get single influencer by ID"""
    influencer = db.query(Influencer).filter(
        Influencer.influencer_id == influencer_id
    ).first()
    
    if not influencer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influencer not found"
        )
    
    return influencer

# =====================================================
# STATISTICS
# =====================================================

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get platform statistics"""
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
    """Calculate suggested pricing"""
    # Base CPM
    base_cpm = 10
    
    # Platform multipliers
    platform_multipliers = {
        "instagram": 1.0,
        "youtube": 1.5,
        "tiktok": 0.8,
        "twitter": 0.7
    }
    
    # Content multipliers
    content_multipliers = {
        "post": 1.0,
        "story": 0.5,
        "reel": 1.3,
        "video": 1.5
    }
    
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

# =====================================================
# RUN SERVER (Local only)
# =====================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
