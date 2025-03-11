"""
Scheduler Agent
-------------
Optimizes content publishing schedules based on analytics data and audience engagement patterns.
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .base_agent import BaseAgent
from .analytics_agent import AnalyticsAgent

class SchedulerAgent(BaseAgent):
    """Agent for optimizing content publishing schedules."""
    
    def __init__(self):
        """Initialize the Scheduler Agent."""
        super().__init__("SchedulerAgent")
        self.analytics_agent = AnalyticsAgent()
        
    def analyze_best_publishing_days(self, days_lookback=90):
        """Analyze historical data to determine the best days for publishing content.
        
        Args:
            days_lookback (int): Number of days of historical data to analyze
            
        Returns:
            dict: Analysis of best publishing days and times
        """
        # Get video analytics data
        videos_df = self.analytics_agent.get_video_analytics(days=days_lookback)
        if videos_df is None or videos_df.empty:
            self.logger.error("No video data available for analysis")
            return None
            
        # Extract day of week and hour from published_at
        videos_df['day_of_week'] = videos_df['published_at'].dt.day_name()
        videos_df['hour'] = videos_df['published_at'].dt.hour
        
        # Analyze performance by day of week
        day_performance = videos_df.groupby('day_of_week').agg({
            'views': ['mean', 'count'],
            'likes': 'mean',
            'comments': 'mean'
        }).round(2)
        
        # Calculate engagement rate by day
        day_performance['engagement_rate'] = (
            (day_performance[('likes', 'mean')] + day_performance[('comments', 'mean')]) /
            day_performance[('views', 'mean')]
        ).round(4)
        
        # Sort days by engagement rate
        day_performance = day_performance.sort_values(('engagement_rate'), ascending=False)
        
        # Analyze performance by hour
        hour_performance = videos_df.groupby('hour').agg({
            'views': ['mean', 'count'],
            'likes': 'mean',
            'comments': 'mean'
        }).round(2)
        
        # Calculate engagement rate by hour
        hour_performance['engagement_rate'] = (
            (hour_performance[('likes', 'mean')] + hour_performance[('comments', 'mean')]) /
            hour_performance[('views', 'mean')]
        ).round(4)
        
        # Sort hours by engagement rate
        hour_performance = hour_performance.sort_values(('engagement_rate'), ascending=False)
        
        # Format results
        analysis = {
            "best_days": day_performance.head(3).index.tolist(),
            "best_hours": hour_performance.head(3).index.tolist(),
            "day_stats": day_performance.to_dict(),
            "hour_stats": hour_performance.to_dict(),
            "sample_size": len(videos_df)
        }
        
        return analysis
        
    def generate_monthly_schedule(self, month=None, year=None, posts_per_week=2):
        """Generate an optimized content publishing schedule for a month.
        
        Args:
            month (int, optional): Target month (1-12). Defaults to next month.
            year (int, optional): Target year. Defaults to current year.
            posts_per_week (int, optional): Number of posts per week. Defaults to 2.
            
        Returns:
            dict: Monthly publishing schedule
        """
        # Set default month and year if not provided
        if month is None or year is None:
            next_month = datetime.now() + timedelta(days=30)
            month = month or next_month.month
            year = year or next_month.year
            
        # Analyze best publishing days and times
        best_times = self.analyze_best_publishing_days()
        if not best_times:
            self.logger.error("Could not determine best publishing times")
            return None
            
        # Get all dates in the target month
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
            
        # Create calendar DataFrame
        dates = pd.date_range(start=start_date, end=end_date - timedelta(days=1))
        calendar_df = pd.DataFrame({
            'date': dates,
            'day_of_week': dates.day_name()
        })
        
        # Filter for best publishing days
        best_days = best_times["best_days"]
        publishing_dates = calendar_df[calendar_df['day_of_week'].isin(best_days)]
        
        # Select dates based on posts_per_week
        total_posts = posts_per_week * len(calendar_df) // 7
        if len(publishing_dates) > total_posts:
            publishing_dates = publishing_dates.sample(n=total_posts)
        
        # Assign best hours to each date
        best_hours = best_times["best_hours"]
        hour_cycle = 0
        schedule = []
        
        for _, row in publishing_dates.iterrows():
            publish_time = datetime.combine(
                row['date'].date(),
                datetime.min.time().replace(hour=best_hours[hour_cycle % len(best_hours)])
            )
            
            schedule.append({
                "date": publish_time.strftime("%Y-%m-%d"),
                "time": publish_time.strftime("%H:00"),
                "day_of_week": row['day_of_week']
            })
            
            hour_cycle += 1
            
        # Sort schedule by date
        schedule.sort(key=lambda x: x["date"])
        
        # Create schedule with metadata
        publishing_schedule = {
            "month": month,
            "year": year,
            "posts_per_week": posts_per_week,
            "total_posts": len(schedule),
            "best_days": best_days,
            "best_hours": best_hours,
            "schedule": schedule
        }
        
        # Save schedule
        self.save_results(publishing_schedule)
        
        return publishing_schedule
        
    def adjust_schedule_for_events(self, schedule, events):
        """Adjust publishing schedule based on special events or holidays.
        
        Args:
            schedule (dict): Base publishing schedule
            events (list): List of events with dates and importance
            
        Returns:
            dict: Adjusted publishing schedule
        """
        if not schedule or not events:
            return schedule
            
        adjusted_schedule = schedule.copy()
        schedule_dates = {item["date"]: idx for idx, item in enumerate(schedule["schedule"])}
        
        for event in events:
            event_date = event["date"]
            importance = event["importance"]
            
            # If we have a post scheduled near the event
            if event_date in schedule_dates:
                idx = schedule_dates[event_date]
                # Adjust time based on event importance
                if importance == "high":
                    # Move to peak hour
                    adjusted_schedule["schedule"][idx]["time"] = f"{schedule['best_hours'][0]:02d}:00"
                    adjusted_schedule["schedule"][idx]["event"] = event["name"]
            else:
                # For high importance events, add a new posting slot
                if importance == "high":
                    new_post = {
                        "date": event_date,
                        "time": f"{schedule['best_hours'][0]:02d}:00",
                        "day_of_week": datetime.strptime(event_date, "%Y-%m-%d").strftime("%A"),
                        "event": event["name"]
                    }
                    adjusted_schedule["schedule"].append(new_post)
                    adjusted_schedule["total_posts"] += 1
                    
        # Re-sort schedule
        adjusted_schedule["schedule"].sort(key=lambda x: x["date"])
        
        return adjusted_schedule
        
    def run(self):
        """Run the scheduler agent's main workflow."""
        self.logger.info("Starting scheduling workflow")
        
        # Generate next month's schedule
        schedule = self.generate_monthly_schedule()
        if schedule:
            self.logger.info(f"Generated schedule for {schedule['month']}/{schedule['year']} with {schedule['total_posts']} posts")
            
            # Print schedule summary
            print("\n=== Content Publishing Schedule ===")
            print(f"Month: {schedule['month']}/{schedule['year']}")
            print(f"Total Posts: {schedule['total_posts']}")
            print(f"Best Publishing Days: {', '.join(schedule['best_days'])}")
            print(f"Best Publishing Hours: {schedule['best_hours']}")
            print("\nSchedule:")
            for post in schedule['schedule']:
                print(f"{post['date']} {post['time']} ({post['day_of_week']})")
        
        self.logger.info("Scheduling workflow completed")