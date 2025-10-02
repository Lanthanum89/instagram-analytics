import random
from datetime import datetime, timedelta
import json

class DemoDataGenerator:
    """Generate demo data for testing the Instagram Analytics app"""
    
    def __init__(self):
        self.sample_captions = [
            "Beautiful sunset at the beach 🌅 #sunset #beach #nature",
            "Coffee and productivity ☕ #mondaymotivation #coffee #work",
            "New product launch! Excited to share this with you all 🚀 #newproduct #launch",
            "Behind the scenes at our photoshoot 📷 #bts #photoshoot #creative",
            "Weekend vibes 🎉 #weekend #relaxation #goodvibes",
            "Throwback to last summer's adventure 🏤 #throwback #travel #memories",
            "Team meeting discussing exciting new projects 💼 #teamwork #projects #business",
            "Delicious homemade pasta recipe 🍝 #food #cooking #homemade",
            "Morning workout complete! 💪 #fitness #morning #workout",
            "Art exhibition opening night 🎨 #art #exhibition #culture",
            "Reading my new favorite book 📚 #reading #books #literature",
            "Concert was absolutely amazing! 🎵 #music #concert #livemusic",
            "Holiday decorations are up! 🎄 #holidays #decorations #festive",
            "Collaboration with amazing brand partners 🤝 #collaboration #partnership",
            "Exploring the local farmers market 🌽 #farmersmarket #local #fresh",
            "Late night coding session 💻 #coding #developer #latenight",
            "Meditation and mindfulness practice 🧘 #meditation #mindfulness #peace",
            "Dog walk in the park 🐕 #dogs #park #nature",
            "Trying out new recipe experiments 🍳 #cooking #experiments #kitchen",
            "Client presentation went great! 📈 #business #presentation #success"
        ]
        
        self.media_types = ['IMAGE', 'VIDEO', 'CAROUSEL_ALBUM']
    
    def generate_account_info(self):
        """Generate demo account information"""
        return {
            'username': 'demo_analytics_account',
            'name': 'Demo Analytics Account',
            'biography': 'This is a demo account for testing Instagram Analytics features. Real data would come from Meta API.',
            'followers_count': random.randint(5000, 50000),
            'follows_count': random.randint(500, 2000),
            'media_count': random.randint(100, 1000)
        }
    
    def generate_media_data(self, count=25):
        """Generate demo media posts data"""
        media_posts = []
        
        for i in range(count):
            # Generate timestamp (last 30 days)
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
            
            # Generate engagement metrics
            like_count = random.randint(50, 2000)
            comments_count = random.randint(5, 200)
            
            post = {
                'id': f'demo_post_{i+1}',
                'caption': random.choice(self.sample_captions),
                'media_type': random.choice(self.media_types),
                'timestamp': timestamp.isoformat(),
                'like_count': like_count,
                'comments_count': comments_count,
                'engagement': like_count + comments_count
            }
            media_posts.append(post)
        
        return media_posts
    
    def generate_insights_data(self):
        """Generate demo insights data"""
        return {
            'impressions': random.randint(10000, 100000),
            'reach': random.randint(8000, 80000),
            'profile_views': random.randint(1000, 10000),
            'website_clicks': random.randint(100, 1000)
        }
    
    def generate_audience_insights(self):
        """Generate demo audience insights"""
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
        countries = ['United States', 'Canada', 'United Kingdom', 'Australia', 'Germany', 'France', 'Brazil', 'Mexico', 'India', 'Japan']
        
        return {
            'top_cities': random.sample(cities, 5),
            'top_countries': random.sample(countries, 5),
            'age_groups': {
                '18-24': random.randint(15, 30),
                '25-34': random.randint(25, 40),
                '35-44': random.randint(20, 35),
                '45-54': random.randint(10, 20),
                '55+': random.randint(5, 15)
            },
            'gender_split': {
                'female': random.randint(45, 65),
                'male': random.randint(35, 55)
            }
        }
    
    def generate_hashtag_performance(self):
        """Generate demo hashtag performance data"""
        hashtags = [
            '#business', '#entrepreneur', '#success', '#motivation',
            '#lifestyle', '#photography', '#art', '#design',
            '#food', '#travel', '#fitness', '#fashion',
            '#technology', '#innovation', '#startup', '#marketing'
        ]
        
        hashtag_data = []
        for hashtag in random.sample(hashtags, 10):
            hashtag_data.append({
                'hashtag': hashtag,
                'reach': random.randint(1000, 10000),
                'impressions': random.randint(2000, 20000),
                'uses': random.randint(500, 5000)
            })
        
        return hashtag_data
    
    def generate_engagement_timeline(self, days=30):
        """Generate demo engagement timeline data"""
        timeline_data = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            timeline_data.append({
                'date': date,
                'likes': random.randint(50, 500),
                'comments': random.randint(10, 100),
                'shares': random.randint(5, 50),
                'saves': random.randint(15, 150),
                'profile_visits': random.randint(20, 200)
            })
        
        return sorted(timeline_data, key=lambda x: x['date'])
    
    def generate_story_insights(self):
        """Generate demo story insights"""
        return {
            'story_impressions': random.randint(5000, 25000),
            'story_reach': random.randint(4000, 20000),
            'story_exits': random.randint(500, 2500),
            'story_replies': random.randint(50, 500),
            'story_taps_forward': random.randint(1000, 5000),
            'story_taps_back': random.randint(200, 1000)
        }
    
    def generate_competitor_data(self):
        """Generate demo competitor analysis data"""
        competitors = [
            {'name': 'Competitor A', 'followers': random.randint(10000, 100000), 'engagement_rate': round(random.uniform(1.5, 5.0), 2)},
            {'name': 'Competitor B', 'followers': random.randint(10000, 100000), 'engagement_rate': round(random.uniform(1.5, 5.0), 2)},
            {'name': 'Competitor C', 'followers': random.randint(10000, 100000), 'engagement_rate': round(random.uniform(1.5, 5.0), 2)},
            {'name': 'Competitor D', 'followers': random.randint(10000, 100000), 'engagement_rate': round(random.uniform(1.5, 5.0), 2)},
            {'name': 'Competitor E', 'followers': random.randint(10000, 100000), 'engagement_rate': round(random.uniform(1.5, 5.0), 2)}
        ]
        return competitors
    
    def generate_complete_dataset(self):
        """Generate a complete demo dataset"""
        return {
            'account_info': self.generate_account_info(),
            'media_data': self.generate_media_data(25),
            'insights_data': self.generate_insights_data(),
            'audience_insights': self.generate_audience_insights(),
            'hashtag_performance': self.generate_hashtag_performance(),
            'engagement_timeline': self.generate_engagement_timeline(30),
            'story_insights': self.generate_story_insights(),
            'competitor_data': self.generate_competitor_data()
        }
    
    def save_demo_data_to_file(self, filename='demo_data.json'):
        """Save demo data to JSON file"""
        demo_data = self.generate_complete_dataset()
        
        # Convert datetime objects to strings for JSON serialization
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, list):
                return [convert_datetime(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_datetime(value) for key, value in obj.items()}
            return obj
        
        demo_data = convert_datetime(demo_data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(demo_data, f, indent=2, ensure_ascii=False)
        
        return demo_data

if __name__ == "__main__":
    # Generate and save demo data when script is run directly
    generator = DemoDataGenerator()
    data = generator.save_demo_data_to_file()
    print("Demo data generated and saved to demo_data.json")
    print(f"Generated data for account: @{data['account_info']['username']}")
    print(f"Total posts: {len(data['media_data'])}")
    print(f"Followers: {data['account_info']['followers_count']:,}")