# seed_data.py
"""
Seed database with sample influencer data
"""

from models import Influencer

def seed_influencers(db):
    """Add sample influencers to database"""
    
    influencers_data = [
        # FITNESS
        {
            "full_name": "Virat Kohli",
            "handle": "virat.kohli",
            "platform": "instagram",
            "niche": "Fitness",
            "followers_count": 266000000,
            "engagement_rate": 4.7
        },
        {
            "full_name": "Gaurav Taneja",
            "handle": "flyingbeast",
            "platform": "youtube",
            "niche": "Fitness",
            "followers_count": 9200000,
            "engagement_rate": 5.4
        },
        {
            "full_name": "Sahil Khan",
            "handle": "sahilkhan",
            "platform": "instagram",
            "niche": "Fitness",
            "followers_count": 14000000,
            "engagement_rate": 3.9
        },
        {
            "full_name": "BeerBiceps",
            "handle": "ranveerallahbadia",
            "platform": "youtube",
            "niche": "Fitness",
            "followers_count": 6100000,
            "engagement_rate": 4.6
        },
        
        # FASHION
        {
            "full_name": "Kusha Kapila",
            "handle": "kusha.kapila",
            "platform": "instagram",
            "niche": "Fashion",
            "followers_count": 4300000,
            "engagement_rate": 5.1
        },
        {
            "full_name": "Komal Pandey",
            "handle": "komalpandeyofficial",
            "platform": "instagram",
            "niche": "Fashion",
            "followers_count": 1900000,
            "engagement_rate": 6.4
        },
        {
            "full_name": "Masoom Minawala",
            "handle": "masoomminawala",
            "platform": "instagram",
            "niche": "Fashion",
            "followers_count": 1300000,
            "engagement_rate": 4.2
        },
        {
            "full_name": "Sejal Kumar",
            "handle": "sejalkumar1195",
            "platform": "youtube",
            "niche": "Fashion",
            "followers_count": 1500000,
            "engagement_rate": 4.9
        },
        
        # TECH
        {
            "full_name": "Technical Guruji",
            "handle": "technicalguruji",
            "platform": "youtube",
            "niche": "Tech",
            "followers_count": 23000000,
            "engagement_rate": 3.8
        },
        {
            "full_name": "GeekyRanjit",
            "handle": "geekyranjit",
            "platform": "youtube",
            "niche": "Tech",
            "followers_count": 3400000,
            "engagement_rate": 4.1
        },
        {
            "full_name": "Tech Burner",
            "handle": "techburner",
            "platform": "youtube",
            "niche": "Tech",
            "followers_count": 12000000,
            "engagement_rate": 4.5
        },
        {
            "full_name": "Trakin Tech",
            "handle": "trakintech",
            "platform": "youtube",
            "niche": "Tech",
            "followers_count": 16000000,
            "engagement_rate": 3.6
        },
        
        # FOOD
        {
            "full_name": "Kabita Singh",
            "handle": "kabitaskitchen",
            "platform": "youtube",
            "niche": "Food",
            "followers_count": 14000000,
            "engagement_rate": 5.2
        },
        {
            "full_name": "Nisha Madhulika",
            "handle": "nishamadhulika",
            "platform": "youtube",
            "niche": "Food",
            "followers_count": 15000000,
            "engagement_rate": 4.9
        },
        {
            "full_name": "Sanjeev Kapoor",
            "handle": "sanjeevkapoor",
            "platform": "instagram",
            "niche": "Food",
            "followers_count": 5600000,
            "engagement_rate": 3.8
        },
        {
            "full_name": "Shivesh Bhatia",
            "handle": "bakewithshivesh",
            "platform": "instagram",
            "niche": "Food",
            "followers_count": 2300000,
            "engagement_rate": 5.6
        },
        
        # TRAVEL
        {
            "full_name": "Mumbiker Nikhil",
            "handle": "mumbiker_nikhil",
            "platform": "youtube",
            "niche": "Travel",
            "followers_count": 4100000,
            "engagement_rate": 4.3
        },
        {
            "full_name": "Passenger Paramvir",
            "handle": "passengerparamvir",
            "platform": "youtube",
            "niche": "Travel",
            "followers_count": 1900000,
            "engagement_rate": 5.1
        },
        {
            "full_name": "Kritika Goel",
            "handle": "kritika_goel",
            "platform": "instagram",
            "niche": "Travel",
            "followers_count": 1200000,
            "engagement_rate": 4.8
        },
        {
            "full_name": "Savi & Vid",
            "handle": "saviandvid",
            "platform": "instagram",
            "niche": "Travel",
            "followers_count": 900000,
            "engagement_rate": 6.2
        }
    ]
    
    # Add influencers to database
    for data in influencers_data:
        influencer = Influencer(**data)
        db.add(influencer)
    
    db.commit()
    print(f"✅ Added {len(influencers_data)} influencers to database")
