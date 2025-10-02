import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import json

class InstagramDataAnalyzer:
    """Analyze Instagram data and generate insights"""
    
    def __init__(self):
        self.data = {}
        self.insights = {}
        
        # Set style for plots
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def process_account_data(self, account_info):
        """Process account information"""
        if not account_info:
            return {}
        
        return {
            'username': account_info.get('username', 'N/A'),
            'name': account_info.get('name', 'N/A'),
            'followers_count': account_info.get('followers_count', 0),
            'follows_count': account_info.get('follows_count', 0),
            'media_count': account_info.get('media_count', 0),
            'biography': account_info.get('biography', 'N/A')
        }
    
    def process_media_data(self, media_data):
        """Process media posts data"""
        if not media_data or 'data' not in media_data:
            return []
        
        processed_media = []
        for post in media_data['data']:
            processed_post = {
                'id': post.get('id'),
                'caption': post.get('caption', '')[:100] + '...' if post.get('caption') else 'No caption',
                'media_type': post.get('media_type'),
                'timestamp': post.get('timestamp'),
                'like_count': post.get('like_count', 0),
                'comments_count': post.get('comments_count', 0),
                'engagement': post.get('like_count', 0) + post.get('comments_count', 0)
            }
            processed_media.append(processed_post)
        
        return processed_media
    
    def process_insights_data(self, insights_data):
        """Process insights data"""
        if not insights_data or 'data' not in insights_data:
            return {}
        
        processed_insights = {}
        for metric in insights_data['data']:
            metric_name = metric.get('name')
            values = metric.get('values', [])
            
            if values:
                # Get the most recent value
                latest_value = values[-1].get('value', 0)
                processed_insights[metric_name] = latest_value
        
        return processed_insights
    
    def calculate_engagement_rate(self, media_data, followers_count):
        """Calculate engagement rate for posts"""
        if not media_data or followers_count == 0:
            return 0
        
        total_engagement = sum(post['engagement'] for post in media_data)
        avg_engagement = total_engagement / len(media_data) if media_data else 0
        engagement_rate = (avg_engagement / followers_count) * 100 if followers_count > 0 else 0
        
        return round(engagement_rate, 2)
    
    def analyze_posting_patterns(self, media_data):
        """Analyze posting patterns"""
        if not media_data:
            return {}
        
        # Extract posting times
        posting_times = []
        for post in media_data:
            if post.get('timestamp'):
                try:
                    dt = datetime.fromisoformat(post['timestamp'].replace('Z', '+00:00'))
                    posting_times.append({
                        'hour': dt.hour,
                        'day_of_week': dt.weekday(),
                        'date': dt.date()
                    })
                except:
                    continue
        
        if not posting_times:
            return {}
        
        # Analyze patterns
        hour_counts = defaultdict(int)
        day_counts = defaultdict(int)
        
        for time_data in posting_times:
            hour_counts[time_data['hour']] += 1
            day_counts[time_data['day_of_week']] += 1
        
        # Find best posting times
        best_hour = max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else 0
        best_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else 0
        
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        return {
            'best_hour': best_hour,
            'best_day': day_names[best_day],
            'hour_distribution': dict(hour_counts),
            'day_distribution': {day_names[k]: v for k, v in day_counts.items()}
        }
    
    def get_top_performing_posts(self, media_data, limit=5):
        """Get top performing posts by engagement"""
        if not media_data:
            return []
        
        # Sort by engagement
        sorted_posts = sorted(media_data, key=lambda x: x['engagement'], reverse=True)
        return sorted_posts[:limit]
    
    def generate_growth_insights(self, historical_data):
        """Generate growth insights from historical data"""
        # This would require historical data tracking
        # For now, return placeholder insights
        return {
            'follower_growth_rate': 'N/A - Requires historical data',
            'engagement_trend': 'N/A - Requires historical data',
            'posting_frequency': 'N/A - Requires historical data'
        }
    
    def create_engagement_chart(self, media_data):
        """Create engagement chart"""
        if not media_data:
            return None
        
        # Prepare data for plotting
        posts = media_data[-10:]  # Last 10 posts
        post_numbers = list(range(1, len(posts) + 1))
        engagements = [post['engagement'] for post in posts]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(post_numbers, engagements, marker='o', linewidth=2, markersize=6)
        ax.set_xlabel('Recent Posts')
        ax.set_ylabel('Total Engagement (Likes + Comments)')
        ax.set_title('Engagement Trend - Last 10 Posts')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def create_posting_pattern_chart(self, posting_patterns):
        """Create posting pattern visualization"""
        if not posting_patterns.get('hour_distribution'):
            return None
        
        hours = list(posting_patterns['hour_distribution'].keys())
        counts = list(posting_patterns['hour_distribution'].values())
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(hours, counts, color='#E4405F', alpha=0.7)
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Number of Posts')
        ax.set_title('Posting Pattern by Hour')
        ax.set_xticks(range(0, 24, 2))
        
        return fig