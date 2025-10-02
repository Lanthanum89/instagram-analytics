import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo_data import DemoDataGenerator
from data_analyzer import InstagramDataAnalyzer
from utils import MetricsCalculator, ContentAnalyzer, DateUtils
from config import Config

class TestDemoDataGenerator(unittest.TestCase):
    """Test the demo data generator"""
    
    def setUp(self):
        self.generator = DemoDataGenerator()
    
    def test_generate_account_info(self):
        """Test account info generation"""
        account_info = self.generator.generate_account_info()
        
        self.assertIn('username', account_info)
        self.assertIn('name', account_info)
        self.assertIn('followers_count', account_info)
        self.assertIn('follows_count', account_info)
        self.assertIn('media_count', account_info)
        
        # Check data types
        self.assertIsInstance(account_info['followers_count'], int)
        self.assertIsInstance(account_info['follows_count'], int)
        self.assertIsInstance(account_info['media_count'], int)
        
        # Check reasonable ranges
        self.assertGreaterEqual(account_info['followers_count'], 5000)
        self.assertLessEqual(account_info['followers_count'], 50000)
    
    def test_generate_media_data(self):
        """Test media data generation"""
        media_data = self.generator.generate_media_data(10)
        
        self.assertEqual(len(media_data), 10)
        
        for post in media_data:
            self.assertIn('id', post)
            self.assertIn('caption', post)
            self.assertIn('media_type', post)
            self.assertIn('like_count', post)
            self.assertIn('comments_count', post)
            self.assertIn('engagement', post)
            
            # Check that engagement is calculated correctly
            expected_engagement = post['like_count'] + post['comments_count']
            self.assertEqual(post['engagement'], expected_engagement)
    
    def test_generate_complete_dataset(self):
        """Test complete dataset generation"""
        dataset = self.generator.generate_complete_dataset()
        
        required_keys = [
            'account_info', 'media_data', 'insights_data',
            'audience_insights', 'hashtag_performance'
        ]
        
        for key in required_keys:
            self.assertIn(key, dataset)
        
        # Check that media_data is not empty
        self.assertGreater(len(dataset['media_data']), 0)

class TestInstagramDataAnalyzer(unittest.TestCase):
    """Test the data analyzer"""
    
    def setUp(self):
        self.analyzer = InstagramDataAnalyzer()
        self.generator = DemoDataGenerator()
        self.sample_data = self.generator.generate_complete_dataset()
    
    def test_process_account_data(self):
        """Test account data processing"""
        account_info = self.sample_data['account_info']
        processed = self.analyzer.process_account_data(account_info)
        
        self.assertIn('username', processed)
        self.assertIn('followers_count', processed)
        self.assertEqual(processed['username'], account_info['username'])
    
    def test_calculate_engagement_rate(self):
        """Test engagement rate calculation"""
        media_data = self.sample_data['media_data']
        followers_count = self.sample_data['account_info']['followers_count']
        
        engagement_rate = self.analyzer.calculate_engagement_rate(media_data, followers_count)
        
        self.assertIsInstance(engagement_rate, float)
        self.assertGreaterEqual(engagement_rate, 0)
        self.assertLessEqual(engagement_rate, 100)  # Should be reasonable percentage
    
    def test_get_top_performing_posts(self):
        """Test top performing posts retrieval"""
        media_data = self.sample_data['media_data']
        top_posts = self.analyzer.get_top_performing_posts(media_data, 5)
        
        self.assertLessEqual(len(top_posts), 5)
        
        # Check that posts are sorted by engagement (descending)
        if len(top_posts) > 1:
            for i in range(len(top_posts) - 1):
                self.assertGreaterEqual(
                    top_posts[i]['engagement'],
                    top_posts[i + 1]['engagement']
                )
    
    def test_analyze_posting_patterns(self):
        """Test posting pattern analysis"""
        media_data = self.sample_data['media_data']
        patterns = self.analyzer.analyze_posting_patterns(media_data)
        
        if patterns:  # Only test if patterns were generated
            self.assertIn('best_hour', patterns)
            self.assertIn('best_day', patterns)
            
            # Check hour is valid (0-23)
            self.assertGreaterEqual(patterns['best_hour'], 0)
            self.assertLessEqual(patterns['best_hour'], 23)

class TestMetricsCalculator(unittest.TestCase):
    """Test metrics calculation utilities"""
    
    def test_calculate_engagement_rate(self):
        """Test engagement rate calculation"""
        # Test normal case
        rate = MetricsCalculator.calculate_engagement_rate(100, 50, 1000)
        self.assertEqual(rate, 15.0)  # (100+50)/1000 * 100 = 15%
        
        # Test zero followers
        rate = MetricsCalculator.calculate_engagement_rate(100, 50, 0)
        self.assertEqual(rate, 0.0)
        
        # Test zero engagement
        rate = MetricsCalculator.calculate_engagement_rate(0, 0, 1000)
        self.assertEqual(rate, 0.0)
    
    def test_calculate_growth_rate(self):
        """Test growth rate calculation"""
        # Test positive growth
        rate = MetricsCalculator.calculate_growth_rate(1100, 1000)
        self.assertEqual(rate, 10.0)  # 10% growth
        
        # Test negative growth
        rate = MetricsCalculator.calculate_growth_rate(900, 1000)
        self.assertEqual(rate, -10.0)  # 10% decline
        
        # Test zero previous value
        rate = MetricsCalculator.calculate_growth_rate(1000, 0)
        self.assertEqual(rate, 0.0)
    
    def test_get_engagement_benchmarks(self):
        """Test engagement benchmarks"""
        # Test different follower ranges
        benchmarks_small = MetricsCalculator.get_engagement_benchmarks(500)
        benchmarks_large = MetricsCalculator.get_engagement_benchmarks(100000)
        
        # Smaller accounts should have higher benchmark expectations
        self.assertGreater(benchmarks_small['average'], benchmarks_large['average'])
        
        # All benchmarks should have required keys
        required_keys = ['low', 'average', 'good', 'excellent']
        for key in required_keys:
            self.assertIn(key, benchmarks_small)
            self.assertIn(key, benchmarks_large)

class TestContentAnalyzer(unittest.TestCase):
    """Test content analysis utilities"""
    
    def test_extract_hashtags(self):
        """Test hashtag extraction"""
        caption = "Beautiful sunset #sunset #beach #photography #nature"
        hashtags = ContentAnalyzer.extract_hashtags(caption)
        
        expected_hashtags = ['#sunset', '#beach', '#photography', '#nature']
        self.assertEqual(len(hashtags), 4)
        
        for hashtag in expected_hashtags:
            self.assertIn(hashtag, hashtags)
    
    def test_extract_hashtags_empty(self):
        """Test hashtag extraction with empty caption"""
        hashtags = ContentAnalyzer.extract_hashtags("")
        self.assertEqual(hashtags, [])
        
        hashtags = ContentAnalyzer.extract_hashtags(None)
        self.assertEqual(hashtags, [])
    
    def test_analyze_caption_length(self):
        """Test caption length analysis"""
        posts_data = [
            {'caption': 'Short caption'},
            {'caption': 'This is a much longer caption with more words and details'},
            {'caption': 'Medium length caption here'}
        ]
        
        analysis = ContentAnalyzer.analyze_caption_length(posts_data)
        
        self.assertIn('average_length', analysis)
        self.assertIn('min_length', analysis)
        self.assertIn('max_length', analysis)
        
        # Check that min <= average <= max
        self.assertLessEqual(analysis['min_length'], analysis['average_length'])
        self.assertLessEqual(analysis['average_length'], analysis['max_length'])

class TestDateUtils(unittest.TestCase):
    """Test date utility functions"""
    
    def test_parse_instagram_date(self):
        """Test Instagram date parsing"""
        # Test ISO format with Z
        date_str = "2023-10-01T15:30:00Z"
        parsed = DateUtils.parse_instagram_date(date_str)
        self.assertIsNotNone(parsed)
        
        # Test ISO format without Z
        date_str = "2023-10-01T15:30:00"
        parsed = DateUtils.parse_instagram_date(date_str)
        self.assertIsNotNone(parsed)
        
        # Test date only format
        date_str = "2023-10-01"
        parsed = DateUtils.parse_instagram_date(date_str)
        self.assertIsNotNone(parsed)
    
    def test_get_date_range(self):
        """Test date range generation"""
        start_date, end_date = DateUtils.get_date_range(7)
        
        self.assertIsInstance(start_date, str)
        self.assertIsInstance(end_date, str)
        
        # Check format
        self.assertRegex(start_date, r'\d{4}-\d{2}-\d{2}')
        self.assertRegex(end_date, r'\d{4}-\d{2}-\d{2}')

class TestConfig(unittest.TestCase):
    """Test configuration"""
    
    def test_validate_config(self):
        """Test configuration validation"""
        # Since config will likely be empty in test environment,
        # we expect missing fields
        missing_fields = Config.validate_config()
        self.assertIsInstance(missing_fields, list)
    
    def test_get_headers(self):
        """Test header generation"""
        headers = Config.get_headers()
        self.assertIsInstance(headers, dict)
        self.assertIn('Authorization', headers)
        self.assertIn('Content-Type', headers)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_complete_workflow(self):
        """Test complete data processing workflow"""
        # Generate demo data
        generator = DemoDataGenerator()
        demo_data = generator.generate_complete_dataset()
        
        # Process with analyzer
        analyzer = InstagramDataAnalyzer()
        
        # Process account data
        account_processed = analyzer.process_account_data(demo_data['account_info'])
        self.assertIsInstance(account_processed, dict)
        
        # Process media data
        media_processed = analyzer.process_media_data({'data': demo_data['media_data']})
        self.assertIsInstance(media_processed, list)
        
        # Analyze posting patterns
        patterns = analyzer.analyze_posting_patterns(media_processed)
        
        # Calculate engagement rate
        if account_processed.get('followers_count'):
            engagement_rate = analyzer.calculate_engagement_rate(
                media_processed, account_processed['followers_count']
            )
            self.assertIsInstance(engagement_rate, float)
        
        # Get top posts
        top_posts = analyzer.get_top_performing_posts(media_processed, 5)
        self.assertIsInstance(top_posts, list)

def run_tests():
    """Run all tests"""
    # Create test suite
    test_classes = [
        TestDemoDataGenerator,
        TestInstagramDataAnalyzer,
        TestMetricsCalculator,
        TestContentAnalyzer,
        TestDateUtils,
        TestConfig,
        TestIntegration
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Running Instagram Analytics App Tests...")
    print("=" * 50)
    
    success = run_tests()
    
    if success:
        print("\n" + "=" * 50)
        print("All tests passed! ✅")
    else:
        print("\n" + "=" * 50)
        print("Some tests failed! ❌")
        sys.exit(1)