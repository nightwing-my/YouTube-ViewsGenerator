"""
Analytics Agent
-------------
Handles YouTube channel analytics and KPI tracking for the Alt Tech Tok channel.
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from .base_agent import BaseAgent

class AnalyticsAgent(BaseAgent):
    """Agent for analyzing YouTube channel performance and tracking KPIs."""
    
    def __init__(self):
        """Initialize the Analytics Agent."""
        super().__init__("AnalyticsAgent")
        self.youtube = None
        self._setup_youtube_api()
        
    def _setup_youtube_api(self):
        """Set up YouTube API client."""
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            self.logger.error("YouTube API key not found in environment variables")
            return
            
        try:
            self.youtube = build("youtube", "v3", developerKey=api_key)
            self.logger.info("YouTube API client initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing YouTube API client: {str(e)}")
            
    def _load_kpi_targets(self):
        """Load KPI targets from configuration file."""
        config = self.load_config()
        if not config:
            # Default KPI targets if no config exists
            config = {
                "phase1": {
                    "subscribers": 1000,
                    "watch_hours": 4000,
                    "avg_views": 100,
                    "engagement_rate": 0.05
                },
                "phase2": {
                    "subscribers": 10000,
                    "watch_hours": 20000,
                    "avg_views": 1000,
                    "engagement_rate": 0.08
                },
                "phase3": {
                    "subscribers": 100000,
                    "watch_hours": 100000,
                    "avg_views": 10000,
                    "engagement_rate": 0.10
                }
            }
            self.save_config(config)
            
        return config
        
    def get_channel_stats(self):
        """Get current channel statistics."""
        if not self.youtube:
            self.logger.error("YouTube API client not initialized")
            return None
            
        try:
            request = self.youtube.channels().list(
                part="statistics",
                mine=True
            )
            response = request.execute()
            
            if not response["items"]:
                self.logger.error("No channel data found")
                return None
                
            stats = response["items"][0]["statistics"]
            return {
                "subscribers": int(stats["subscriberCount"]),
                "total_views": int(stats["viewCount"]),
                "video_count": int(stats["videoCount"])
            }
        except Exception as e:
            self.logger.error(f"Error fetching channel stats: {str(e)}")
            return None
            
    def get_video_analytics(self, video_id=None, days=28):
        """Get analytics for videos in the specified time period."""
        if not self.youtube:
            self.logger.error("YouTube API client not initialized")
            return None
            
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            request = self.youtube.videos().list(
                part="statistics,snippet",
                maxResults=50,
                id=video_id if video_id else None
            )
            response = request.execute()
            
            videos_data = []
            for video in response.get("items", []):
                stats = video["statistics"]
                snippet = video["snippet"]
                
                # Skip videos outside the date range
                published_at = datetime.strptime(
                    snippet["publishedAt"], 
                    "%Y-%m-%dT%H:%M:%SZ"
                )
                if published_at < start_date:
                    continue
                    
                videos_data.append({
                    "title": snippet["title"],
                    "published_at": published_at,
                    "views": int(stats["viewCount"]),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0))
                })
                
            return pd.DataFrame(videos_data)
        except Exception as e:
            self.logger.error(f"Error fetching video analytics: {str(e)}")
            return None
            
    def analyze_kpi_progress(self):
        """Analyze progress towards KPI targets."""
        stats = self.get_channel_stats()
        if not stats:
            return None
            
        targets = self._load_kpi_targets()
        videos_df = self.get_video_analytics()
        
        if videos_df is not None and not videos_df.empty:
            avg_views = videos_df["views"].mean()
            total_engagement = videos_df["likes"].sum() + videos_df["comments"].sum()
            total_views = videos_df["views"].sum()
            engagement_rate = total_engagement / total_views if total_views > 0 else 0
        else:
            avg_views = 0
            engagement_rate = 0
            
        # Determine current phase based on subscriber count
        current_phase = "phase1"
        if stats["subscribers"] >= targets["phase3"]["subscribers"]:
            current_phase = "phase3"
        elif stats["subscribers"] >= targets["phase2"]["subscribers"]:
            current_phase = "phase2"
            
        analysis = {
            "current_phase": current_phase,
            "metrics": {
                "subscribers": stats["subscribers"],
                "avg_views": avg_views,
                "engagement_rate": engagement_rate
            },
            "targets": targets[current_phase]
        }
        
        # Save analysis results
        self.save_results(analysis)
        
        return analysis
        
    def generate_performance_report(self, days=28):
        """Generate a detailed performance report with visualizations."""
        videos_df = self.get_video_analytics(days)
        if videos_df is None or videos_df.empty:
            self.logger.error("No video data available for report generation")
            return None
            
        # Create visualizations
        plt.figure(figsize=(15, 10))
        
        # Views trend
        plt.subplot(2, 2, 1)
        plt.plot(videos_df["published_at"], videos_df["views"])
        plt.title("Views Trend")
        plt.xticks(rotation=45)
        
        # Engagement by video
        plt.subplot(2, 2, 2)
        engagement = videos_df["likes"] + videos_df["comments"]
        plt.bar(range(len(videos_df)), engagement)
        plt.title("Total Engagement by Video")
        
        # Save plot
        plot_path = os.path.join(self.results_dir, f"performance_report_{datetime.now().strftime('%Y%m%d')}.png")
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
        
        # Generate report data
        report = {
            "period": f"Last {days} days",
            "total_views": videos_df["views"].sum(),
            "avg_views_per_video": videos_df["views"].mean(),
            "total_engagement": (videos_df["likes"] + videos_df["comments"]).sum(),
            "best_performing_video": {
                "title": videos_df.loc[videos_df["views"].idxmax(), "title"],
                "views": videos_df["views"].max()
            },
            "plot_path": plot_path
        }
        
        # Save report
        self.save_results(report)
        
        return report
        
    def run(self):
        """Run the analytics agent's main workflow."""
        self.logger.info("Starting analytics workflow")
        
        # Analyze KPI progress
        kpi_analysis = self.analyze_kpi_progress()
        if kpi_analysis:
            self.logger.info(f"Current phase: {kpi_analysis['current_phase']}")
            
        # Generate performance report
        report = self.generate_performance_report()
        if report:
            self.logger.info(f"Performance report generated: {report['plot_path']}")
            
        self.logger.info("Analytics workflow completed")