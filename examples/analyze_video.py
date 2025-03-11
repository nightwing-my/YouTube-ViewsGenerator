"""
YouTube Video Analysis CLI Tool
-----------------------------
Analyze any YouTube video using the YouTube Growth AI Suite.
"""

import os
import argparse
from dotenv import load_dotenv
from agents import (
    ContentAgent,
    SEOAgent,
    AnalyticsAgent,
    EngagementAgent
)

def extract_video_id(url_or_id):
    """Extract video ID from URL or return the ID if already in correct format."""
    if 'youtube.com' in url_or_id or 'youtu.be' in url_or_id:
        # Handle youtube.com URLs
        if 'v=' in url_or_id:
            return url_or_id.split('v=')[1].split('&')[0]
        # Handle youtu.be URLs
        elif 'youtu.be' in url_or_id:
            return url_or_id.split('/')[-1].split('?')[0]
    # Return as is if it looks like a video ID
    return url_or_id.strip()

def analyze_seo(video_id, seo_agent, args):
    """Analyze video SEO performance."""
    print("\n=== SEO Analysis ===")
    try:
        # Get video analytics first
        analytics = AnalyticsAgent()
        video_data = analytics.get_video_analytics(video_id=video_id)
        
        if video_data is not None and not video_data.empty:
            # Get the first (and should be only) video
            video_info = video_data.iloc[0]
            
            title = video_info['title']
            
            # Analyze title
            title_analysis = seo_agent.analyze_title(title)
            print("\nTitle Analysis:")
            for metric, value in title_analysis.items():
                print(f"- {metric}: {value}")
            
            # Generate tag suggestions
            tags = seo_agent.generate_tags(title, count=args.tag_count)
            print(f"\nSuggested Tags (top {args.tag_count}):")
            print(", ".join(tags))
            
            if args.competitors:
                print("\nCompetitor Analysis:")
                competitor_analysis = seo_agent.analyze_competitors(video_id, max_results=args.competitor_count)
                for i, comp in enumerate(competitor_analysis, 1):
                    print(f"\nCompetitor {i}:")
                    print(f"Title: {comp['title']}")
                    print(f"Views: {comp['views']:,}")
                    print(f"Engagement Rate: {comp['engagement_rate']:.2%}")
        else:
            print("No video data available")
    except Exception as e:
        print(f"Error in SEO analysis: {str(e)}")

def analyze_engagement(video_id, engagement_agent, args):
    """Analyze video engagement and generate suggestions."""
    print("\n=== Engagement Analysis ===")
    try:
        # Generate community posts
        posts = engagement_agent.generate_community_posts(count=args.post_count)
        if posts:
            print("\nSuggested Community Posts:")
            for i, post in enumerate(posts, 1):
                print(f"\n{i}. Type: {post['type']}")
                print(f"   Content: {post['content']}")
        
        # Generate video response suggestions
        if args.response_ideas:
            response_ideas = engagement_agent.generate_video_response_ideas(
                video_id,
                count=args.response_count
            )
            if response_ideas:
                print(f"\nVideo Response Ideas (top {args.response_count}):")
                for i, idea in enumerate(response_ideas, 1):
                    print(f"\n{i}. {idea['title']}")
                    print(f"   Description: {idea['description']}")
                    
        # Generate comment suggestions if requested
        if args.comment_suggestions:
            comments = engagement_agent.generate_comment_suggestions(
                video_id,
                count=args.comment_count
            )
            if comments:
                print(f"\nSuggested Comments (top {args.comment_count}):")
                for i, comment in enumerate(comments, 1):
                    print(f"\n{i}. {comment}")
    except Exception as e:
        print(f"Error in engagement analysis: {str(e)}")

def analyze_performance(video_id, analytics_agent, args):
    """Analyze video performance metrics."""
    print("\n=== Performance Analysis ===")
    try:
        # Get video analytics
        video_data = analytics_agent.get_video_analytics(video_id=video_id, days=args.analytics_days)
        
        if video_data is not None and not video_data.empty:
            # Get the first (and should be only) video
            video_info = video_data.iloc[0]
            
            print("\nVideo Statistics:")
            print(f"Title: {video_info['title']}")
            print(f"Published: {video_info['published_at']}")
            print(f"Views: {video_info['views']:,}")
            print(f"Likes: {video_info['likes']:,}")
            print(f"Comments: {video_info['comments']:,}")
            
            # Calculate engagement rate
            total_engagement = video_info['likes'] + video_info['comments']
            engagement_rate = total_engagement / video_info['views'] if video_info['views'] > 0 else 0
            print(f"Engagement Rate: {engagement_rate:.2%}")
        else:
            print("No video data available")
            
    except Exception as e:
        print(f"Error in performance analysis: {str(e)}")

def main():
    """Run the video analysis tool."""
    parser = argparse.ArgumentParser(
        description="Analyze YouTube videos using the Growth AI Suite",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Main arguments
    parser.add_argument(
        "video",
        help="YouTube video URL or ID to analyze"
    )
    
    parser.add_argument(
        "-a", "--analyze",
        choices=["all", "seo", "engagement", "performance"],
        default="all",
        help="Type of analysis to perform"
    )
    
    # SEO Agent arguments
    seo_group = parser.add_argument_group('SEO Analysis Options')
    seo_group.add_argument(
        "--tag-count",
        type=int,
        default=10,
        help="Number of tag suggestions to generate"
    )
    seo_group.add_argument(
        "--competitors",
        action="store_true",
        help="Include competitor analysis"
    )
    seo_group.add_argument(
        "--competitor-count",
        type=int,
        default=5,
        help="Number of competitors to analyze"
    )
    
    # Engagement Agent arguments
    engagement_group = parser.add_argument_group('Engagement Analysis Options')
    engagement_group.add_argument(
        "--post-count",
        type=int,
        default=2,
        help="Number of community posts to generate"
    )
    engagement_group.add_argument(
        "--response-ideas",
        action="store_true",
        help="Generate video response ideas"
    )
    engagement_group.add_argument(
        "--response-count",
        type=int,
        default=3,
        help="Number of video response ideas to generate"
    )
    engagement_group.add_argument(
        "--comment-suggestions",
        action="store_true",
        help="Generate comment suggestions"
    )
    engagement_group.add_argument(
        "--comment-count",
        type=int,
        default=5,
        help="Number of comment suggestions to generate"
    )
    
    # Analytics Agent arguments
    analytics_group = parser.add_argument_group('Performance Analysis Options')
    analytics_group.add_argument(
        "--analytics-days",
        type=int,
        default=28,
        help="Number of days to analyze for analytics"
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Extract video ID
    video_id = extract_video_id(args.video)
    print(f"\nAnalyzing video: {video_id}")
    
    # Initialize agents based on requested analysis
    if args.analyze in ["all", "seo"]:
        seo_agent = SEOAgent()
    if args.analyze in ["all", "engagement"]:
        engagement_agent = EngagementAgent()
    if args.analyze in ["all", "performance"]:
        analytics_agent = AnalyticsAgent()
    
    # Perform requested analysis
    if args.analyze in ["all", "seo"]:
        analyze_seo(video_id, seo_agent, args)
    if args.analyze in ["all", "engagement"]:
        analyze_engagement(video_id, engagement_agent, args)
    if args.analyze in ["all", "performance"]:
        analyze_performance(video_id, analytics_agent, args)

if __name__ == "__main__":
    main() 