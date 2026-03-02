# backend/seed_data.py
from models import Influencer

def seed_influencers(db):
    influencers = [
        # 🔥 FITNESS
        Influencer(full_name="Virat Kohli",        handle="virat.kohli",         platform="instagram", niche="Fitness",  bio="Cricket legend & fitness enthusiast 🏏", location="Mumbai",    followers_count=266000000, engagement_rate=4.7),
        Influencer(full_name="Gaurav Taneja",       handle="flyingbeast",         platform="youtube",   niche="Fitness",  bio="Pilot & fitness vlogger ✈️💪",           location="Delhi",     followers_count=9200000,   engagement_rate=5.4),
        Influencer(full_name="Sahil Khan",          handle="sahilkhan",           platform="instagram", niche="Fitness",  bio="Bodybuilder & motivator 💪",             location="Mumbai",    followers_count=14000000,  engagement_rate=3.9),
        Influencer(full_name="Ranveer Allahbadia",  handle="beerbiceps",          platform="youtube",   niche="Fitness",  bio="Fitness & entrepreneurship 🧠",          location="Mumbai",    followers_count=6100000,   engagement_rate=4.6),

        # 👗 FASHION
        Influencer(full_name="Kusha Kapila",        handle="kusha.kapila",        platform="instagram", niche="Fashion",  bio="Fashion & comedy creator 😂👗",          location="Delhi",     followers_count=4300000,   engagement_rate=5.1),
        Influencer(full_name="Komal Pandey",        handle="komalpandeyofficial", platform="instagram", niche="Fashion",  bio="Thrift queen & style icon 👑",           location="Delhi",     followers_count=1900000,   engagement_rate=6.4),
        Influencer(full_name="Masoom Minawala",     handle="masoomminawala",      platform="instagram", niche="Fashion",  bio="Global fashion influencer 🌍",           location="Mumbai",    followers_count=1300000,   engagement_rate=4.2),
        Influencer(full_name="Sejal Kumar",         handle="sejalkumar1195",      platform="youtube",   niche="Fashion",  bio="Fashion, travel & lifestyle ✈️",         location="Delhi",     followers_count=1500000,   engagement_rate=4.9),

        # 💻 TECH
        Influencer(full_name="Technical Guruji",    handle="technicalguruji",     platform="youtube",   niche="Tech",     bio="Tech in Hindi 🤖",                       location="Dubai",     followers_count=23000000,  engagement_rate=3.8),
        Influencer(full_name="GeekyRanjit",         handle="geekyranjit",         platform="youtube",   niche="Tech",     bio="Gadget reviews & unboxing 📦",           location="Delhi",     followers_count=3400000,   engagement_rate=4.1),
        Influencer(full_name="Tech Burner",         handle="techburner",          platform="youtube",   niche="Tech",     bio="Tech reviews & gadgets 📱",              location="Delhi",     followers_count=12000000,  engagement_rate=4.5),
        Influencer(full_name="Trakin Tech",         handle="trakintech",          platform="youtube",   niche="Tech",     bio="Mobile & gadget reviews 📲",             location="Delhi",     followers_count=16000000,  engagement_rate=3.6),

        # 🍔 FOOD
        Influencer(full_name="Kabita Singh",        handle="kabitaskitchen",      platform="youtube",   niche="Food",     bio="Simple Indian recipes 🍛",               location="Bhubaneswar", followers_count=14000000, engagement_rate=5.2),
        Influencer(full_name="Nisha Madhulika",     handle="nishamadhulika",      platform="youtube",   niche="Food",     bio="Vegetarian cooking expert 🥗",           location="Noida",     followers_count=15000000,  engagement_rate=4.9),
        Influencer(full_name="Sanjeev Kapoor",      handle="sanjeevkapoor",       platform="instagram", niche="Food",     bio="Celebrity chef & food lover 👨‍🍳",     location="Mumbai",    followers_count=5600000,   engagement_rate=3.8),
        Influencer(full_name="Shivesh Bhatia",      handle="bakewithshivesh",     platform="instagram", niche="Food",     bio="Pastry chef & food stylist 🎂",          location="Delhi",     followers_count=2300000,   engagement_rate=5.6),

        # ✈️ TRAVEL
        Influencer(full_name="Mumbiker Nikhil",     handle="mumbiker_nikhil",     platform="youtube",   niche="Travel",   bio="Riding across India 🏍️",               location="Mumbai",    followers_count=4100000,   engagement_rate=4.3),
        Influencer(full_name="Passenger Paramvir",  handle="passengerparamvir",   platform="youtube",   niche="Travel",   bio="Budget travel across India 🗺️",        location="Punjab",    followers_count=1900000,   engagement_rate=5.1),
        Influencer(full_name="Kritika Goel",        handle="kritika_goel",        platform="instagram", niche="Travel",   bio="Solo female traveller 🌸",               location="Delhi",     followers_count=1200000,   engagement_rate=4.8),
        Influencer(full_name="Savi and Vid",        handle="saviandvid",          platform="instagram", niche="Travel",   bio="Couple travel bloggers 💑",              location="Pune",      followers_count=900000,    engagement_rate=6.2),
    ]
    for inf in influencers:
        db.add(inf)
    db.commit()
    print(f"✅ Seeded {len(influencers)} influencers!")
