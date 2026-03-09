"""
Promobridge - FIXED Seed Brands + Campaigns Script
Fixes:
  1. status_code check updated (200 and 201 both accepted)
  2. Better error logging to see exact server error
  3. Login re-attempted before campaign creation
  4. Timeout increased for cold-start
"""
import requests
import json

BASE_URL = "https://promobridge-backend0.onrender.com"
print(f"🌱 Seeding Brands & Campaigns")
print(f"📡 {BASE_URL}\n")

# ── Wake up the server (cold start can take 30-60s on free tier) ──────────────
print("⏳ Waking up server (may take 30-60s on first request)...")
try:
    r = requests.get(f"{BASE_URL}/health", timeout=90)
    print(f"✅ Server alive: {r.json()}\n")
except Exception as e:
    print(f"⚠️  Health check failed: {e} — trying anyway...\n")


def register(email, password, role):
    try:
        r = requests.post(
            f"{BASE_URL}/auth/register",
            json={"email": email, "password": password, "role": role},
            timeout=60
        )
        return r.status_code in (200, 201)
    except Exception as e:
        print(f"    register error: {e}")
        return False


def login(email, password):
    try:
        r = requests.post(
            f"{BASE_URL}/auth/login",
            data={"username": email, "password": password},
            timeout=60
        )
        if r.status_code == 200:
            return r.json().get("access_token")
        print(f"    login failed {r.status_code}: {r.text[:80]}")
        return None
    except Exception as e:
        print(f"    login error: {e}")
        return None


# ── Brand data: 4 per niche x 5 niches = 20 brands ───────────────────────────
brand_data = [
    # FITNESS
    ("fit1@pb.com",  "Fit@001",  {"brand_name": "Cult.fit",      "industry": "Fitness", "website": "cult.fit",           "description": "India's leading fitness platform"}),
    ("fit2@pb.com",  "Fit@002",  {"brand_name": "Boldfit",       "industry": "Fitness", "website": "boldfit.in",         "description": "Fitness supplements & equipment"}),
    ("fit3@pb.com",  "Fit@003",  {"brand_name": "Healthify Me",  "industry": "Fitness", "website": "healthifyme.com",    "description": "AI-powered nutrition & fitness app"}),
    ("fit4@pb.com",  "Fit@004",  {"brand_name": "Oziva",         "industry": "Fitness", "website": "oziva.in",           "description": "Clean plant-based nutrition"}),
    # FASHION
    ("fash1@pb.com", "Fash@001", {"brand_name": "Myntra",        "industry": "Fashion", "website": "myntra.com",         "description": "India's leading fashion platform"}),
    ("fash2@pb.com", "Fash@002", {"brand_name": "Ajio",          "industry": "Fashion", "website": "ajio.com",           "description": "Reliance's fashion destination"}),
    ("fash3@pb.com", "Fash@003", {"brand_name": "H&M India",     "industry": "Fashion", "website": "hm.com",             "description": "Affordable fast fashion"}),
    ("fash4@pb.com", "Fash@004", {"brand_name": "Zara India",    "industry": "Fashion", "website": "zara.com",           "description": "Premium international fashion"}),
    # TECH
    ("tech1@pb.com", "Tech@001", {"brand_name": "boAt",          "industry": "Tech",    "website": "boat-lifestyle.com", "description": "India's top audio lifestyle brand"}),
    ("tech2@pb.com", "Tech@002", {"brand_name": "Noise",         "industry": "Tech",    "website": "gonoise.com",        "description": "Smart wearables & gadgets"}),
    ("tech3@pb.com", "Tech@003", {"brand_name": "Lenskart",      "industry": "Tech",    "website": "lenskart.com",       "description": "Smart eyewear solutions"}),
    ("tech4@pb.com", "Tech@004", {"brand_name": "Mivi",          "industry": "Tech",    "website": "mivi.in",            "description": "Made in India audio products"}),
    # FOOD
    ("food1@pb.com", "Food@001", {"brand_name": "Zomato",        "industry": "Food",    "website": "zomato.com",         "description": "India's food delivery giant"}),
    ("food2@pb.com", "Food@002", {"brand_name": "Swiggy",        "industry": "Food",    "website": "swiggy.com",         "description": "Fast food & grocery delivery"}),
    ("food3@pb.com", "Food@003", {"brand_name": "Blinkit",       "industry": "Food",    "website": "blinkit.com",        "description": "10-minute grocery delivery"}),
    ("food4@pb.com", "Food@004", {"brand_name": "Mamaearth",     "industry": "Food",    "website": "mamaearth.in",       "description": "Natural & toxin-free products"}),
    # TRAVEL
    ("trav1@pb.com", "Trav@001", {"brand_name": "MakeMyTrip",    "industry": "Travel",  "website": "makemytrip.com",     "description": "India's top travel booking platform"}),
    ("trav2@pb.com", "Trav@002", {"brand_name": "Airbnb India",  "industry": "Travel",  "website": "airbnb.co.in",       "description": "Unique stays worldwide"}),
    ("trav3@pb.com", "Trav@003", {"brand_name": "Yatra",         "industry": "Travel",  "website": "yatra.com",          "description": "Travel booking & holiday packages"}),
    ("trav4@pb.com", "Trav@004", {"brand_name": "OYO Rooms",     "industry": "Travel",  "website": "oyorooms.com",       "description": "Affordable hotel network India"}),
]

# ── Campaigns: 2 per niche = 10 total ────────────────────────────────────────
campaigns_data = [
    ("fit1@pb.com",  "Fit@001",  [
        {"title": "Summer Fitness Challenge 2025", "niche": "Fitness", "platform": "instagram", "budget": 250000, "min_followers": 100000,
         "description": "Promote our summer fitness challenge with workout routines and supplement reviews."},
        {"title": "New Year New You - Healthify",  "niche": "Fitness", "platform": "youtube",   "budget": 400000, "min_followers": 500000,
         "description": "YouTube campaign for New Year fitness resolutions featuring our AI nutrition app."},
    ]),
    ("fash1@pb.com", "Fash@001", [
        {"title": "Myntra End of Reason Sale",     "niche": "Fashion", "platform": "instagram", "budget": 600000, "min_followers": 200000,
         "description": "Promote EORS with haul videos, OOTD posts and discount codes."},
        {"title": "Festive Fashion Collection",    "niche": "Fashion", "platform": "youtube",   "budget": 350000, "min_followers": 300000,
         "description": "Showcase our Diwali festive collection through YouTube lookbooks."},
    ]),
    ("tech1@pb.com", "Tech@001", [
        {"title": "boAt Rockerz Series Launch",    "niche": "Tech",    "platform": "youtube",   "budget": 500000, "min_followers": 500000,
         "description": "Unboxing and review campaign for our new Rockerz wireless headphones."},
        {"title": "boAt Storm Smartwatch Campaign","niche": "Tech",    "platform": "instagram", "budget": 300000, "min_followers": 100000,
         "description": "Instagram reels showcasing features of our new Storm smartwatch."},
    ]),
    ("food1@pb.com", "Food@001", [
        {"title": "Zomato Gold Membership Drive",  "niche": "Food",    "platform": "instagram", "budget": 450000, "min_followers": 200000,
         "description": "Food influencers promote Zomato Gold benefits with restaurant reviews."},
        {"title": "Weekend Foodie Challenge",      "niche": "Food",    "platform": "youtube",   "budget": 280000, "min_followers": 100000,
         "description": "Weekend food challenges and mukbang content featuring Zomato deliveries."},
    ]),
    ("trav1@pb.com", "Trav@001", [
        {"title": "MakeMyTrip Summer Holidays",    "niche": "Travel",  "platform": "youtube",   "budget": 700000, "min_followers": 300000,
         "description": "Travel vloggers showcase holiday packages and flight deals across India."},
        {"title": "Hidden Gems of India Series",   "niche": "Travel",  "platform": "instagram", "budget": 350000, "min_followers": 100000,
         "description": "Instagram travel series featuring unexplored Indian destinations."},
    ]),
]


# ═══════════════════════════════════════════════════════
#  STEP 1 — Create Brands
# ═══════════════════════════════════════════════════════
print(f"👔 Creating {len(brand_data)} brands...\n")
brand_tokens = {}
b_success = 0

for email, pwd, profile in brand_data:
    # Register (ignore if already exists)
    register(email, pwd, "brand")

    # Login
    token = login(email, pwd)
    if not token:
        print(f"  ❌ Could not login as {email}")
        continue

    # Create brand profile
    r = requests.post(
        f"{BASE_URL}/brands",
        json=profile,
        headers={"Authorization": f"Bearer {token}"},
        timeout=60
    )

    if r.status_code in (200, 201):
        b_success += 1
        brand_tokens[email] = token
        print(f"  ✅ [{b_success:02d}] {profile['brand_name']} ({profile['industry']})")
    elif r.status_code == 400 and "already exists" in r.text:
        # Brand already created — still save token for campaigns
        brand_tokens[email] = token
        print(f"  ℹ️  {profile['brand_name']} already exists — token saved")
    else:
        brand_tokens[email] = token   # save token anyway
        print(f"  ⚠️  {profile['brand_name']}: {r.status_code} — {r.text[:100]}")


# ═══════════════════════════════════════════════════════
#  STEP 2 — Create Campaigns
# ═══════════════════════════════════════════════════════
print(f"\n📢 Creating campaigns...\n")
c_success = 0

for email, pwd, camps in campaigns_data:
    # Get token (re-login if needed)
    token = brand_tokens.get(email) or login(email, pwd)
    if not token:
        print(f"  ❌ No token for {email}, skipping campaigns")
        continue

    for camp in camps:
        r = requests.post(
            f"{BASE_URL}/campaigns",
            json=camp,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=60
        )

        if r.status_code in (200, 201):
            c_success += 1
            budget = camp["budget"]
            budget_str = f"Rs.{budget // 100000} L" if budget >= 100000 else f"Rs.{budget:,}"
            print(f"  ✅ [{c_success}] {camp['title']} — {budget_str}")
        else:
            # Print FULL error so we can debug
            print(f"  ❌ {camp['title']}: {r.status_code} — {r.text[:200]}")


# ═══════════════════════════════════════════════════════
#  STEP 3 — Final Stats
# ═══════════════════════════════════════════════════════
print("\n📊 Final Stats:")
try:
    stats = requests.get(f"{BASE_URL}/stats", timeout=30).json()
    print(f"""
  ================================
  👤 Influencers : {stats.get('total_influencers', 0)}
  🏢 Brands      : {stats.get('total_brands', 0)}
  📢 Campaigns   : {stats.get('total_campaigns', 0)}
  ================================
""")
except Exception as e:
    print(f"  Could not fetch stats: {e}")

print("🎉 Done!")
