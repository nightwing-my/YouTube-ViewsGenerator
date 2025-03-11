"""
Test Suite for YouTube Channel Growth AI Agents
---------------------------------------------
Tests the functionality of each agent in the YouTube Channel Growth AI Suite.
"""

import os
import sys
import unittest
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import numpy as np

# Add parent directory to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import (
    BaseAgent,
    ContentAgent,
    SEOAgent,
    AnalyticsAgent,
    EngagementAgent,
    SchedulerAgent
)

class TestBaseAgent(unittest.TestCase):
    """Test cases for the BaseAgent class."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = BaseAgent(name="TestAgent")
        
    def test_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertTrue(os.path.exists(self.agent.config_dir))
        self.assertTrue(os.path.exists(self.agent.results_dir))
        self.assertTrue(os.path.exists(self.agent.log_dir))
        
    def test_save_results(self):
        """Test saving results."""
        test_data = {"test": "data"}
        self.agent.save_results(test_data)
        
        # Check if results file was created
        results_files = os.listdir(self.agent.results_dir)
        self.assertTrue(any(file.startswith("test_agent_") for file in results_files))

class TestContentAgent(unittest.TestCase):
    """Test cases for the ContentAgent class."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = ContentAgent()
        
    def test_generate_video_ideas(self):
        """Test video idea generation."""
        ideas = self.agent.generate_video_ideas(count=3)
        self.assertEqual(len(ideas), 3)
        for idea in ideas:
            self.assertIn("title", idea)
            self.assertIn("description", idea)
            self.assertIn("category", idea)
            
    def test_generate_content_calendar(self):
        """Test content calendar generation."""
        calendar = self.agent.generate_content_calendar(weeks=2)
        self.assertIn("start_date", calendar)
        self.assertIn("weeks", calendar)
        self.assertEqual(len(calendar["weeks"]), 2)

class TestSEOAgent(unittest.TestCase):
    """Test cases for the SEOAgent class."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = SEOAgent()
        
    def test_analyze_title(self):
        """Test title analysis."""
        title = "Top 10 Tech Gadgets for 2023 [Must Watch!]"
        analysis = self.agent.analyze_title(title)
        self.assertIn("length", analysis)
        self.assertIn("has_number", analysis)
        self.assertIn("has_brackets", analysis)
        self.assertTrue(analysis["has_number"])
        self.assertTrue(analysis["has_brackets"])
        
    def test_generate_tags(self):
        """Test tag generation."""
        title = "Ultimate Python Programming Tutorial 2023"
        tags = self.agent.generate_tags(title, count=10)
        self.assertLessEqual(len(tags), 10)
        self.assertTrue(all(isinstance(tag, str) for tag in tags))

class TestAnalyticsAgent(unittest.TestCase):
    """Test cases for the AnalyticsAgent class."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = AnalyticsAgent()
        
    def test_load_kpi_targets(self):
        """Test KPI targets loading."""
        targets = self.agent._load_kpi_targets()
        self.assertIn("phase1", targets)
        self.assertIn("phase2", targets)
        self.assertIn("phase3", targets)
        
    def test_analyze_kpi_progress(self):
        """Test KPI progress analysis."""
        analysis = self.agent.analyze_kpi_progress()
        if analysis:  # Analysis might be None if API key is not set
            self.assertIn("current_phase", analysis)
            self.assertIn("metrics", analysis)
            self.assertIn("targets", analysis)

class TestEngagementAgent(unittest.TestCase):
    """Test cases for the EngagementAgent class."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = EngagementAgent()
        
    def test_generate_comment_replies(self):
        """Test comment reply generation."""
        comments = [
            {"id": "1", "text": "Great video! Very helpful."},
            {"id": "2", "text": "Could you make more content like this?"}
        ]
        replies = self.agent.generate_comment_replies(comments, "tech tutorials")
        self.assertEqual(len(replies), 2)
        for reply in replies:
            self.assertIn("comment_id", reply)
            self.assertIn("reply", reply)
            
    def test_generate_community_posts(self):
        """Test community post generation."""
        posts = self.agent.generate_community_posts(count=3)
        self.assertEqual(len(posts), 3)
        for post in posts:
            self.assertIn("type", post)
            self.assertIn("content", post)

class TestSchedulerAgent(unittest.TestCase):
    """Test cases for the SchedulerAgent class."""
    
    def setUp(self):
        """Set up test environment."""
        self.agent = SchedulerAgent()
        
        # Mock analytics data for testing
        self.mock_analytics_data = pd.DataFrame({
            'published_at': pd.date_range(start='2024-01-01', periods=30),
            'views': np.random.randint(100, 1000, 30),
            'likes': np.random.randint(10, 100, 30),
            'comments': np.random.randint(5, 50, 30)
        })
        
        # Patch the analytics agent's get_video_analytics method
        def mock_get_video_analytics(*args, **kwargs):
            return self.mock_analytics_data
            
        self.agent.analytics_agent.get_video_analytics = mock_get_video_analytics
        
    def test_analyze_best_publishing_days(self):
        """Test best publishing days analysis."""
        analysis = self.agent.analyze_best_publishing_days()
        self.assertIsNotNone(analysis)
        self.assertIn("best_days", analysis)
        self.assertIn("best_hours", analysis)
        self.assertIn("day_stats", analysis)
        self.assertIn("hour_stats", analysis)
        self.assertIn("sample_size", analysis)
        self.assertEqual(analysis["sample_size"], len(self.mock_analytics_data))
        
    def test_generate_monthly_schedule(self):
        """Test monthly schedule generation."""
        schedule = self.agent.generate_monthly_schedule()
        self.assertIsNotNone(schedule)
        self.assertIn("month", schedule)
        self.assertIn("year", schedule)
        self.assertIn("posts_per_week", schedule)
        self.assertIn("total_posts", schedule)
        self.assertIn("best_days", schedule)
        self.assertIn("best_hours", schedule)
        self.assertIn("schedule", schedule)
        self.assertGreater(len(schedule["schedule"]), 0)
        
        # Check schedule entry format
        first_post = schedule["schedule"][0]
        self.assertIn("date", first_post)
        self.assertIn("time", first_post)
        self.assertIn("day_of_week", first_post)

def main():
    """Run all tests."""
    # Load environment variables
    load_dotenv()
    
    # Run tests
    unittest.main(verbosity=2)

if __name__ == "__main__":
    main() 