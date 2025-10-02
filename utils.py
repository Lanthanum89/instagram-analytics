import json
import csv
from datetime import datetime, timedelta
import os
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import pandas as pd

class DataExporter:
    """Handle data export functionality"""
    
    @staticmethod
    def export_to_csv(data: List[Dict], filename: str) -> bool:
        """Export data to CSV file"""
        try:
            if not data:
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    @staticmethod
    def export_to_json(data: Any, filename: str) -> bool:
        """Export data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False

class DateUtils:
    """Date and time utility functions"""
    
    @staticmethod
    def parse_instagram_date(date_string: str) -> Optional[datetime]:
        """Parse Instagram API date string"""
        try:
            # Handle different date formats from Instagram API
            if 'T' in date_string:
                if date_string.endswith('Z'):
                    return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
                else:
                    return datetime.fromisoformat(date_string)
            else:
                return datetime.strptime(date_string, '%Y-%m-%d')
        except Exception as e:
            print(f"Error parsing date {date_string}: {e}")
            return None
    
    @staticmethod
    def get_date_range(days_back: int = 30) -> tuple:
        """Get date range for API queries"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    
    @staticmethod
    def format_relative_time(date_obj: datetime) -> str:
        """Format datetime as relative time (e.g., '2 hours ago')"""
        now = datetime.now()
        if date_obj.tzinfo:
            now = now.replace(tzinfo=date_obj.tzinfo)
        
        diff = now - date_obj
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"

class MetricsCalculator:
    """Calculate various Instagram metrics"""
    
    @staticmethod
    def calculate_engagement_rate(likes: int, comments: int, followers: int) -> float:
        """Calculate engagement rate percentage"""
        if followers == 0:
            return 0.0
        engagement = likes + comments
        return round((engagement / followers) * 100, 2)
    
    @staticmethod
    def calculate_average_engagement(posts_data: List[Dict]) -> float:
        """Calculate average engagement across posts"""
        if not posts_data:
            return 0.0
        
        total_engagement = sum(
            post.get('like_count', 0) + post.get('comments_count', 0) 
            for post in posts_data
        )
        return round(total_engagement / len(posts_data), 1)
    
    @staticmethod
    def calculate_reach_rate(reach: int, followers: int) -> float:
        """Calculate reach rate percentage"""
        if followers == 0:
            return 0.0
        return round((reach / followers) * 100, 2)
    
    @staticmethod
    def calculate_growth_rate(current: int, previous: int) -> float:
        """Calculate growth rate percentage"""
        if previous == 0:
            return 0.0
        return round(((current - previous) / previous) * 100, 2)
    
    @staticmethod
    def get_engagement_benchmarks(followers_count: int) -> Dict[str, float]:
        """Get engagement rate benchmarks based on follower count"""
        # Industry benchmarks (approximate)
        if followers_count < 1000:
            return {'low': 0.5, 'average': 8.0, 'good': 15.0, 'excellent': 25.0}
        elif followers_count < 10000:
            return {'low': 0.5, 'average': 4.0, 'good': 8.0, 'excellent': 15.0}
        elif followers_count < 100000:
            return {'low': 0.5, 'average': 2.5, 'good': 5.0, 'excellent': 10.0}
        else:
            return {'low': 0.3, 'average': 1.5, 'good': 3.0, 'excellent': 6.0}

class ContentAnalyzer:
    """Analyze content patterns and performance"""
    
    @staticmethod
    def extract_hashtags(caption: str) -> List[str]:
        """Extract hashtags from caption"""
        if not caption:
            return []
        
        hashtags = []
        words = caption.split()
        for word in words:
            if word.startswith('#') and len(word) > 1:
                hashtags.append(word.lower())
        return hashtags
    
    @staticmethod
    def analyze_caption_length(posts_data: List[Dict]) -> Dict[str, Any]:
        """Analyze caption length patterns"""
        if not posts_data:
            return {}
        
        lengths = []
        for post in posts_data:
            caption = post.get('caption', '')
            if caption:
                lengths.append(len(caption))
        
        if not lengths:
            return {}
        
        return {
            'average_length': round(sum(lengths) / len(lengths), 1),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'median_length': sorted(lengths)[len(lengths) // 2]
        }
    
    @staticmethod
    def find_top_hashtags(posts_data: List[Dict], limit: int = 10) -> List[tuple]:
        """Find most frequently used hashtags"""
        hashtag_counts = {}
        
        for post in posts_data:
            caption = post.get('caption', '')
            hashtags = ContentAnalyzer.extract_hashtags(caption)
            for hashtag in hashtags:
                hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
        
        # Sort by frequency and return top hashtags
        sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_hashtags[:limit]
    
    @staticmethod
    def analyze_posting_frequency(posts_data: List[Dict]) -> Dict[str, Any]:
        """Analyze posting frequency patterns"""
        if not posts_data:
            return {}
        
        # Count posts by date
        post_dates = {}
        for post in posts_data:
            timestamp = post.get('timestamp')
            if timestamp:
                date_obj = DateUtils.parse_instagram_date(timestamp)
                if date_obj:
                    date_str = date_obj.strftime('%Y-%m-%d')
                    post_dates[date_str] = post_dates.get(date_str, 0) + 1
        
        if not post_dates:
            return {}
        
        daily_counts = list(post_dates.values())
        
        return {
            'total_days_active': len(post_dates),
            'average_posts_per_day': round(sum(daily_counts) / len(daily_counts), 2),
            'max_posts_in_day': max(daily_counts),
            'min_posts_in_day': min(daily_counts),
            'most_active_date': max(post_dates.items(), key=lambda x: x[1])[0]
        }

class ChartGenerator:
    """Generate various charts for analytics"""
    
    @staticmethod
    def create_engagement_by_media_type_chart(posts_data: List[Dict]) -> plt.Figure:
        """Create engagement comparison by media type"""
        media_types = {}
        
        for post in posts_data:
            media_type = post.get('media_type', 'UNKNOWN')
            engagement = post.get('like_count', 0) + post.get('comments_count', 0)
            
            if media_type not in media_types:
                media_types[media_type] = []
            media_types[media_type].append(engagement)
        
        # Calculate average engagement by media type
        avg_engagement = {}
        for media_type, engagements in media_types.items():
            avg_engagement[media_type] = sum(engagements) / len(engagements)
        
        # Create chart
        fig, ax = plt.subplots(figsize=(10, 6))
        types = list(avg_engagement.keys())
        values = list(avg_engagement.values())
        
        bars = ax.bar(types, values, color=['#E4405F', '#833AB4', '#FD5949'])
        ax.set_xlabel('Media Type')
        ax.set_ylabel('Average Engagement')
        ax.set_title('Average Engagement by Media Type')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{value:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_follower_growth_chart(historical_data: List[Dict]) -> plt.Figure:
        """Create follower growth chart (requires historical data)"""
        # This would require historical follower data
        # For now, return a placeholder chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Follower Growth Chart\n(Requires Historical Data)', 
               ha='center', va='center', transform=ax.transAxes, fontsize=14)
        ax.set_title('Follower Growth Over Time')
        return fig

class ConfigValidator:
    """Validate configuration and environment"""
    
    @staticmethod
    def validate_api_credentials(config_dict: Dict[str, str]) -> List[str]:
        """Validate API credentials"""
        required_fields = [
            'META_ACCESS_TOKEN',
            'META_APP_ID',
            'META_APP_SECRET',
            'INSTAGRAM_ACCOUNT_ID'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not config_dict.get(field):
                missing_fields.append(field)
        
        return missing_fields
    
    @staticmethod
    def validate_environment() -> Dict[str, bool]:
        """Validate required packages and environment"""
        validation_results = {}
        
        # Check required packages
        required_packages = [
            'requests', 'matplotlib', 'pandas', 'tkinter', 
            'PIL', 'numpy', 'seaborn'
        ]
        
        for package in required_packages:
            try:
                __import__(package)
                validation_results[package] = True
            except ImportError:
                validation_results[package] = False
        
        return validation_results

class FileManager:
    """Handle file operations"""
    
    @staticmethod
    def ensure_directory_exists(directory_path: str) -> bool:
        """Ensure directory exists, create if it doesn't"""
        try:
            os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory {directory_path}: {e}")
            return False
    
    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """Get safe filename by removing invalid characters"""
        invalid_chars = '<>:"/\\|?*'
        safe_filename = filename
        for char in invalid_chars:
            safe_filename = safe_filename.replace(char, '_')
        return safe_filename
    
    @staticmethod
    def load_json_file(filepath: str) -> Optional[Dict]:
        """Load data from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON file {filepath}: {e}")
            return None
    
    @staticmethod
    def save_json_file(data: Any, filepath: str) -> bool:
        """Save data to JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            print(f"Error saving JSON file {filepath}: {e}")
            return False