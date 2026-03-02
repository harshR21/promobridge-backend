from database import SessionLocal
from models import Influencer

def seed_influencers(db):

    influencers = [

        # 🔥 FITNESS
        {
            "name": "Virat Kohli",
            "username": "virat.kohli",
            "platform": "instagram",
            "niche": "Fitness",
            "followers": 266000000,
            "engagement_rate": 4.7,
            "estimated_price": 3000000
        },
        {
            "name": "Gaurav Taneja",
            "username": "flyingbeast",
            "platform": "youtube",
            "niche": "Fitness",
            "followers": 9200000,
            "engagement_rate": 5.4,
            "estimated_price": 350000
        },
        {
            "name": "Sahil Khan",
            "username": "sahilkhan",
            "platform": "instagram",
            "niche": "Fitness",
            "followers": 14000000,
            "engagement_rate": 3.9,
            "estimated_price": 280000
        },
        {
            "name": "BeerBiceps",
            "username": "ranveerallahbadia",
            "platform": "youtube",
            "niche": "Fitness",
            "followers": 6100000,
            "engagement_rate": 4.6,
            "estimated_price": 200000
        },

        # 👗 FASHION
        {
            "name": "Kusha Kapila",
            "username": "kusha.kapila",
            "platform": "instagram",
            "niche": "Fashion",
            "followers": 4300000,
            "engagement_rate": 5.1,
            "estimated_price": 150000
        },
        {
            "name": "Komal Pandey",
            "username": "komalpandeyofficial",
            "platform": "instagram",
            "niche": "Fashion",
            "followers": 1900000,
            "engagement_rate": 6.4,
            "estimated_price": 90000
        },
        {
            "name": "Masoom Minawala",
            "username": "masoomminawala",
            "platform": "instagram",
            "niche": "Fashion",
            "followers": 1300000,
            "engagement_rate": 4.2,
            "estimated_price": 110000
        },
        {
            "name": "Sejal Kumar",
            "username": "sejalkumar1195",
            "platform": "youtube",
            "niche": "Fashion",
            "followers": 1500000,
            "engagement_rate": 4.9,
            "estimated_price": 85000
        },

        # 💻 TECH
        {
            "name": "Technical Guruji",
            "username": "technicalguruji",
            "platform": "youtube",
            "niche": "Tech",
            "followers": 23000000,
            "engagement_rate": 3.8,
            "estimated_price": 450000
        },
        {
            "name": "GeekyRanjit",
            "username": "geekyranjit",
            "platform": "youtube",
            "niche": "Tech",
            "followers": 3400000,
            "engagement_rate": 4.1,
            "estimated_price": 160000
        },
        {
            "name": "Tech Burner",
            "username": "techburner",
            "platform": "youtube",
            "niche": "Tech",
            "followers": 12000000,
            "engagement_rate": 4.5,
            "estimated_price": 280000
        },
        {
            "name": "Trakin Tech",
            "username": "trakintech",
            "platform": "youtube",
            "niche": "Tech",
            "followers": 16000000,
            "engagement_rate": 3.6,
            "estimated_price": 300000
        },

        # 🍔 FOOD
        {
            "name": "Kabita Singh",
            "username": "kabitaskitchen",
            "platform": "youtube",
            "niche": "Food",
            "followers": 14000000,
            "engagement_rate": 5.2,
            "estimated_price": 250000
        },
        {
            "name": "Nisha Madhulika",
            "username": "nishamadhulika",
            "platform": "youtube",
            "niche": "Food",
            "followers": 15000000,
            "engagement_rate": 4.9,
            "estimated_price": 270000
        },
        {
            "name": "Sanjeev Kapoor",
            "username": "sanjeevkapoor",
            "platform": "instagram",
            "niche": "Food",
            "followers": 5600000,
            "engagement_rate": 3.8,
            "estimated_price": 180000
        },
        {
            "name": "Shivesh Bhatia",
            "username": "bakewithshivesh",
            "platform": "instagram",
            "niche": "Food",
            "followers": 2300000,
            "engagement_rate": 5.6,
            "estimated_price": 120000
        },

        # ✈️ TRAVEL
        {
            "name": "Mumbiker Nikhil",
            "username": "mumbiker_nikhil",
            "platform": "youtube",
            "niche": "Travel",
            "followers": 4100000,
            "engagement_rate": 4.3,
            "estimated_price": 190000
        },
        {
            "name": "Passenger Paramvir",
            "username": "passengerparamvir",
            "platform": "youtube",
            "niche": "Travel",
            "followers": 1900000,
            "engagement_rate": 5.1,
            "estimated_price": 110000
        },
        {
            "name": "Kritika Goel",
            "username": "kritika_goel",
            "platform": "instagram",
            "niche": "Travel",
            "followers": 1200000,
            "engagement_rate": 4.8,
            "estimated_price": 95000
        },
        {
            "name": "Savi & Vid",
            "username": "saviandvid",
            "platform": "instagram",
            "niche": "Travel",
            "followers": 900000,
            "engagement_rate": 6.2,
            "estimated_price": 80000
        },
    ]

    for inf in influencers:
        db.add(Influencer(**inf))

    db.commit()
    db.close()
