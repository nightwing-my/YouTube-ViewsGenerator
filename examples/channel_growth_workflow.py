"""
YouTube Channel Growth AI Suite - Usage Example
--------------------------------------------
This script demonstrates how to use the various agents in the YouTube Channel Growth AI Suite
to optimize your YouTube channel's growth.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from agents import (
    ContentAgent,
    SEOAgent,
    AnalyticsAgent,
    EngagementAgent,
    SchedulerAgent
)

def main():
    """Run a complete channel growth workflow."""
    # Load environment variables
    load_dotenv()
    
    print("\n=== YouTube Channel Growth AI Suite ===\n")
    
    # 1. Analyze current channel performance
    print("1. Analyzing Channel Performance...")
    analytics = AnalyticsAgent()
    kpi_analysis = analytics.analyze_kpi_progress()
    
    if kpi_analysis:
        print(f"\nCurrent Phase: {kpi_analysis['current_phase'].upper()}")
        print("\nCurrent Metrics:")
        for metric, value in kpi_analysis["metrics"].items():
            if metric == "engagement_rate":
                print(f"- {metric}: {value:.2%}")
            else:
                print(f"- {metric}: {value:.0f}")
                
        print("\nPhase Targets:")
        for metric, target in kpi_analysis["targets"].items():
            if metric == "engagement_rate":
                print(f"- {metric}: {target:.2%}")
            else:
                print(f"- {metric}: {target}")
    
    # 2. Generate content ideas
    print("\n2. Generating Content Ideas...")
    content = ContentAgent()
    video_ideas = content.generate_video_ideas(count=5)
    
    if video_ideas:
        print("\nVideo Ideas:")
        for i, idea in enumerate(video_ideas, 1):
            print(f"\n{i}. {idea['title']}")
            print(f"   Category: {idea['category']}")
            print(f"   Description: {idea['description']}")
    
    # 3. Optimize SEO for the first video idea
    print("\n3. Optimizing SEO...")
    seo = SEOAgent()
    if video_ideas:
        first_video = video_ideas[0]
        title_analysis = seo.analyze_title(first_video["title"])
        tags = seo.generate_tags(first_video["title"], count=10)
        
        print(f"\nTitle Analysis for: {first_video['title']}")
        for metric, value in title_analysis.items():
            print(f"- {metric}: {value}")
            
        print("\nSuggested Tags:")
        print(", ".join(tags))
    
    # 4. Generate optimal publishing schedule
    print("\n4. Generating Publishing Schedule...")
    scheduler = SchedulerAgent()
    next_month = datetime.now().month + 1 if datetime.now().month < 12 else 1
    next_year = datetime.now().year + (1 if next_month == 1 else 0)
    
    schedule = scheduler.generate_monthly_schedule(
        month=next_month,
        year=next_year,
        posts_per_week=2
    )
    
    if schedule:
        print(f"\nSchedule for {schedule['month']}/{schedule['year']}:")
        print(f"Total Posts: {schedule['total_posts']}")
        print(f"Best Publishing Days: {', '.join(schedule['best_days'])}")
        print(f"Best Publishing Hours: {schedule['best_hours']}")
        print("\nUpcoming Posts:")
        for post in schedule['schedule'][:5]:  # Show first 5 posts
            print(f"- {post['date']} {post['time']} ({post['day_of_week']})")
    
    # 5. Adjust schedule for special events
    print("\n5. Adjusting Schedule for Events...")
    events = [
        {
            "name": "Channel Anniversary",
            "date": "2024-04-15",
            "importance": "high"
        },
        {
            "name": "Tech Conference",
            "date": "2024-04-20",
            "importance": "high"
        }
    ]
    
    if schedule:
        adjusted_schedule = scheduler.adjust_schedule_for_events(schedule, events)
        print("\nAdjusted Schedule:")
        for post in adjusted_schedule['schedule']:
            event_info = f" - {post['event']}" if 'event' in post else ""
            print(f"- {post['date']} {post['time']} ({post['day_of_week']}){event_info}")
    
    # 6. Generate engagement content
    print("\n6. Generating Engagement Content...")
    engagement = EngagementAgent()
    
    # Generate community posts
    community_posts = engagement.generate_community_posts(count=2)
    if community_posts:
        print("\nCommunity Post Ideas:")
        for i, post in enumerate(community_posts, 1):
            print(f"\n{i}. Type: {post['type']}")
            print(f"   Content: {post['content']}")
    
    # Generate comment replies for sample comments
    sample_comments = [
        {"id": "1", "text": "Great video! Could you make more content about AI?"},
        {"id": "2", "text": "What tools do you recommend for beginners?"}
    ]
    
    replies = engagement.generate_comment_replies(sample_comments, "tech tutorials")
    if replies:
        print("\nAuto-Generated Comment Replies:")
        for reply in replies:
            print(f"\nComment: {next(c['text'] for c in sample_comments if c['id'] == reply['comment_id'])}")
            print(f"Reply: {reply['reply']}")
    
    # 7. Generate performance report
    print("\n7. Generating Performance Report...")
    report = analytics.generate_performance_report(days=28)
    
    if report:
        print("\nPerformance Summary:")
        print(f"Period: {report['period']}")
        print(f"Total Views: {report['total_views']:,}")
        print(f"Average Views per Video: {report['avg_views_per_video']:.1f}")
        print(f"Total Engagement: {report['total_engagement']:,}")
        print("\nBest Performing Video:")
        print(f"Title: {report['best_performing_video']['title']}")
        print(f"Views: {report['best_performing_video']['views']:,}")
        print(f"\nPerformance visualization saved to: {report['plot_path']}")
    
    print("\n=== Workflow Complete ===")

if __name__ == "__main__":
    main() 