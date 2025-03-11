"""
Content Agent
------------
Generates video ideas, scripts, and content strategies based on channel performance and trends.
"""

import os
import json
import random
import requests
from datetime import datetime
from .base_agent import BaseAgent

class ContentAgent(BaseAgent):
    """Agent for generating video content ideas and scripts."""
    
    def __init__(self):
        """Initialize the Content Agent."""
        super().__init__(name="ContentAgent")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.content_categories = self._load_content_categories()
        
    def _load_content_categories(self):
        """Load content categories from configuration file."""
        # Default content categories based on tech channel focus
        default_categories = [
            "Tech News & Updates",
            "Product Reviews",
            "How-To Tutorials",
            "Tech Tips & Tricks",
            "Industry Trends",
            "Tech Comparisons",
            "Behind the Scenes",
            "Q&A Sessions",
            "Tech Debates",
            "Future Technology"
        ]
        
        # Try to load from config file
        config = self.load_config()
        if "content_categories" in config:
            return config["content_categories"]
        
        # If no config found, create one with defaults
        config_file = os.path.join(self.config_dir, "content_agent_config.json")
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump({"content_categories": default_categories}, f, indent=2)
            
        return default_categories
    
    def get_trending_topics(self, category="technology", count=5):
        """Get trending topics in the specified category."""
        self.logger.info(f"Fetching trending topics in {category}")
        
        # This would typically use a real API, but for demonstration we'll use some example topics
        trending_topics = {
            "technology": [
                "AI in everyday applications",
                "Latest smartphone comparisons",
                "Cybersecurity for beginners",
                "Cloud gaming platforms",
                "Smart home automation",
                "Foldable device reviews",
                "Coding for beginners",
                "Tech sustainability",
                "VR/AR developments",
                "Blockchain applications"
            ],
            "gaming": [
                "New game releases",
                "Gaming hardware reviews",
                "Esports tournaments",
                "Game development tutorials",
                "Retro gaming",
                "Mobile gaming trends",
                "Game streaming tips",
                "Gaming setup guides",
                "Game mods and customization",
                "Gaming industry news"
            ]
        }
        
        if category in trending_topics:
            topics = trending_topics[category]
            random.shuffle(topics)  # Randomize to get different results each time
            return topics[:count]
        else:
            self.logger.warning(f"Category '{category}' not found in trending topics")
            return []
    
    def generate_video_ideas(self, count=5, category=None):
        """Generate video ideas based on trending topics and channel focus."""
        self.logger.info(f"Generating {count} video ideas")
        
        # Get trending topics
        if not category:
            # Randomly select a category from our content categories
            category = random.choice(self.content_categories)
            
        trending_topics = self.get_trending_topics(category="technology", count=count)
        
        # Generate video ideas
        video_ideas = []
        
        for topic in trending_topics:
            # Generate a few title variations for each topic
            title_variations = [
                f"Top 10 {topic} in 2023",
                f"How to Master {topic} - Complete Guide",
                f"The Truth About {topic} Nobody Tells You",
                f"{topic} Explained in 10 Minutes",
                f"Why {topic} Is Changing Everything"
            ]
            
            # Randomly select one title variation
            title = random.choice(title_variations)
            
            # Generate a brief description
            descriptions = [
                f"In this video, we'll explore everything you need to know about {topic} and why it matters.",
                f"A comprehensive guide to understanding {topic} and how it can benefit you.",
                f"We dive deep into {topic} to uncover the facts and dispel the myths.",
                f"Everything you wanted to know about {topic} but were afraid to ask.",
                f"Join us as we explore the fascinating world of {topic} and its implications."
            ]
            description = random.choice(descriptions)
            
            # Generate key points to cover
            key_points = [
                f"Introduction to {topic}",
                "Historical context and development",
                "Current state and major players",
                "Future trends and predictions",
                "Practical applications and tips"
            ]
            
            # Generate tags
            tags = [topic.lower(), "tech", "tutorial", "guide", "explainer", "technology"]
            
            video_idea = {
                "title": title,
                "description": description,
                "category": category,
                "key_points": key_points,
                "tags": tags,
                "trending_topic": topic
            }
            
            video_ideas.append(video_idea)
        
        self.logger.info(f"Generated {len(video_ideas)} video ideas")
        return video_ideas
    
    def generate_video_script(self, video_idea):
        """Generate a complete video script based on a video idea."""
        self.logger.info(f"Generating script for video: {video_idea['title']}")
        
        if not self.openai_api_key:
            self.logger.warning("OpenAI API key not found. Using template script instead.")
            return self._generate_template_script(video_idea)
            
        try:
            # This would typically use the OpenAI API, but for demonstration we'll use a template
            return self._generate_template_script(video_idea)
        except Exception as e:
            self.logger.error(f"Error generating script with API: {str(e)}")
            return self._generate_template_script(video_idea)
    
    def _generate_template_script(self, video_idea):
        """Generate a template script based on the video idea structure."""
        title = video_idea["title"]
        topic = video_idea["trending_topic"]
        key_points = video_idea["key_points"]
        
        script = {
            "title": title,
            "topic": topic,
            "sections": []
        }
        
        # Introduction
        intro = {
            "name": "Introduction",
            "content": f"""
Hey everyone, welcome back to Alt Tech Tok! I'm your host, and today we're diving into {topic}.

In this video, we'll cover:
- {key_points[0]}
- {key_points[1]}
- {key_points[2]}
- {key_points[3]}
- {key_points[4]}

Before we get started, make sure to hit that like button and subscribe if you haven't already!
"""
        }
        script["sections"].append(intro)
        
        # Main content sections based on key points
        for i, point in enumerate(key_points):
            section = {
                "name": point,
                "content": f"""
[SECTION {i+1}: {point}]

Let's talk about {point}.

This is where you would discuss the details of {point} related to {topic}.

Key talking points:
- Important fact or statistic about {topic}
- Common misconception about {topic}
- Your personal experience or opinion
- Expert insights or quotes
- Practical examples or demonstrations

[B-ROLL SUGGESTION: Show relevant footage of {topic} in action or graphics explaining key concepts]
"""
            }
            script["sections"].append(section)
        
        # Call to action and conclusion
        conclusion = {
            "name": "Conclusion & Call to Action",
            "content": f"""
And that wraps up our exploration of {topic}!

Let's quickly recap what we've learned:
- We covered {key_points[0]}
- We explored {key_points[1]}
- We discussed {key_points[2]}
- We examined {key_points[3]}
- We looked at {key_points[4]}

If you found this video helpful, please give it a thumbs up and share it with anyone who might be interested in {topic}.

Don't forget to subscribe and hit the notification bell so you don't miss our upcoming videos on similar topics.

What's your experience with {topic}? Let me know in the comments below!

Thanks for watching, and I'll see you in the next video!
"""
        }
        script["sections"].append(conclusion)
        
        return script
    
    def generate_content_calendar(self, weeks=4, videos_per_week=2):
        """Generate a content calendar for the specified number of weeks."""
        self.logger.info(f"Generating content calendar for {weeks} weeks with {videos_per_week} videos per week")
        
        calendar = {
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "weeks": []
        }
        
        # Generate ideas for the entire calendar
        total_videos = weeks * videos_per_week
        all_ideas = self.generate_video_ideas(count=total_videos)
        
        # Distribute ideas across weeks
        idea_index = 0
        for week in range(1, weeks + 1):
            week_data = {
                "week_number": week,
                "videos": []
            }
            
            for _ in range(videos_per_week):
                if idea_index < len(all_ideas):
                    video_idea = all_ideas[idea_index]
                    
                    # Add publishing details
                    if week_data["videos"]:
                        # If we already have a video this week, schedule for later in the week
                        day = "Thursday" if len(week_data["videos"]) == 1 else "Saturday"
                    else:
                        day = "Monday"
                        
                    video_idea["publish_day"] = day
                    video_idea["publish_time"] = "18:00"
                    
                    week_data["videos"].append(video_idea)
                    idea_index += 1
            
            calendar["weeks"].append(week_data)
        
        self.logger.info(f"Generated content calendar with {total_videos} videos")
        return calendar
    
    def analyze_video_performance(self, video_data):
        """Analyze video performance data to provide content recommendations."""
        self.logger.info("Analyzing video performance data")
        
        if not video_data or len(video_data) == 0:
            self.logger.warning("No video data provided for analysis")
            return {
                "top_performing_categories": [],
                "recommended_focus": [],
                "content_gaps": []
            }
            
        # Group videos by category
        categories = {}
        for video in video_data:
            category = video.get("category", "Uncategorized")
            if category not in categories:
                categories[category] = []
                
            categories[category].append(video)
        
        # Calculate average performance by category
        category_performance = {}
        for category, videos in categories.items():
            total_views = sum(video.get("view_count", 0) for video in videos)
            total_engagement = sum(video.get("engagement_rate", 0) for video in videos)
            
            avg_views = total_views / len(videos) if videos else 0
            avg_engagement = total_engagement / len(videos) if videos else 0
            
            category_performance[category] = {
                "avg_views": avg_views,
                "avg_engagement": avg_engagement,
                "video_count": len(videos)
            }
        
        # Sort categories by performance
        sorted_categories = sorted(
            category_performance.items(),
            key=lambda x: (x[1]["avg_views"], x[1]["avg_engagement"]),
            reverse=True
        )
        
        # Identify top performing categories
        top_categories = [category for category, _ in sorted_categories[:3]]
        
        # Identify content gaps (categories with few videos)
        content_gaps = [
            category for category, data in category_performance.items()
            if data["video_count"] <= 2
        ]
        
        # Generate recommendations
        recommendations = []
        
        # Recommend focusing on top categories
        if top_categories:
            recommendations.append(f"Continue creating content in {', '.join(top_categories)} as these categories perform well")
        
        # Recommend exploring content gaps
        if content_gaps:
            recommendations.append(f"Consider creating more content in {', '.join(content_gaps)} to diversify your channel")
        
        # Recommend new content types
        all_categories = set(self.content_categories)
        current_categories = set(categories.keys())
        unexplored_categories = all_categories - current_categories
        
        if unexplored_categories:
            recommendations.append(f"Explore new content categories such as {', '.join(list(unexplored_categories)[:3])}")
        
        analysis = {
            "top_performing_categories": top_categories,
            "recommended_focus": recommendations,
            "content_gaps": content_gaps
        }
        
        self.logger.info("Completed video performance analysis")
        return analysis
    
    def run(self):
        """Run the Content Agent to generate video ideas and content calendar."""
        self.logger.info("Starting Content Agent")
        
        # Generate video ideas
        video_ideas = self.generate_video_ideas(count=5)
        
        # Generate a content calendar
        content_calendar = self.generate_content_calendar(weeks=4, videos_per_week=2)
        
        # Generate a sample script for the first video idea
        if video_ideas:
            script = self.generate_video_script(video_ideas[0])
        else:
            script = None
        
        # Save results
        results = {
            "video_ideas": video_ideas,
            "content_calendar": content_calendar,
            "sample_script": script
        }
        
        self.save_results(results)
        
        # Print summary
        print("\n=== Content Generation Results ===")
        print(f"Generated {len(video_ideas)} video ideas")
        print(f"Created content calendar for {len(content_calendar['weeks'])} weeks")
        
        print("\n=== Top Video Ideas ===")
        for i, idea in enumerate(video_ideas[:3], 1):
            print(f"{i}. {idea['title']}")
            print(f"   Category: {idea['category']}")
            print(f"   Description: {idea['description'][:100]}...")
            print()
            
        if script:
            print("\n=== Sample Script Generated ===")
            print(f"Title: {script['title']}")
            print(f"Sections: {len(script['sections'])}")
            print(f"First section: {script['sections'][0]['name']}")
            
        print("\nAll results saved to:", os.path.join(self.results_dir, f"content_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"))
        
        return True 