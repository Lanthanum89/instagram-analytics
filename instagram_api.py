import requests
import json
from datetime import datetime, timedelta
from config import Config
import logging

class InstagramAPI:
    """Instagram API client using Meta Graph API"""
    
    def __init__(self):
        self.base_url = Config.GRAPH_API_BASE_URL
        self.access_token = Config.ACCESS_TOKEN
        self.account_id = Config.INSTAGRAM_ACCOUNT_ID
        self.headers = Config.get_headers()
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, endpoint, params=None):
        """Make API request to Meta Graph API"""
        try:
            url = f"{self.base_url}/{endpoint}"
            if params is None:
                params = {}
            params['access_token'] = self.access_token
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return None
    
    def get_account_info(self):
        """Get Instagram business account information"""
        endpoint = self.account_id
        params = {
            'fields': 'id,username,name,biography,followers_count,follows_count,media_count,profile_picture_url'
        }
        return self._make_request(endpoint, params)
    
    def get_media_insights(self, media_id):
        """Get insights for a specific media post"""
        endpoint = f"{media_id}/insights"
        params = {
            'metric': 'engagement,impressions,reach,saved,video_views,likes,comments,shares'
        }
        return self._make_request(endpoint, params)
    
    def get_account_insights(self, period='day', since=None, until=None):
        """Get account-level insights"""
        if since is None:
            since = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if until is None:
            until = datetime.now().strftime('%Y-%m-%d')
        
        endpoint = f"{self.account_id}/insights"
        params = {
            'metric': 'impressions,reach,profile_views,website_clicks',
            'period': period,
            'since': since,
            'until': until
        }
        return self._make_request(endpoint, params)
    
    def get_recent_media(self, limit=25):
        """Get recent media posts"""
        endpoint = f"{self.account_id}/media"
        params = {
            'fields': 'id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,like_count,comments_count',
            'limit': limit
        }
        return self._make_request(endpoint, params)
    
    def get_hashtag_info(self, hashtag_name):
        """Get hashtag information"""
        # First get hashtag ID
        search_endpoint = 'ig_hashtag_search'
        search_params = {
            'user_id': self.account_id,
            'q': hashtag_name
        }
        search_result = self._make_request(search_endpoint, search_params)
        
        if search_result and search_result.get('data'):
            hashtag_id = search_result['data'][0]['id']
            
            # Get hashtag details
            endpoint = hashtag_id
            params = {
                'fields': 'id,name,media_count'
            }
            return self._make_request(endpoint, params)
        return None
    
    def get_audience_insights(self):
        """Get audience demographic insights"""
        endpoint = f"{self.account_id}/insights"
        params = {
            'metric': 'audience_gender_age,audience_locale,audience_country',
            'period': 'lifetime'
        }
        return self._make_request(endpoint, params)
    
    def validate_token(self):
        """Validate the access token"""
        endpoint = 'me'
        params = {'fields': 'id,name'}
        result = self._make_request(endpoint, params)
        return result is not None