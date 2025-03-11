"""
Engagement Agent
---------------
Helps increase viewer interaction and build community through comments, polls, and social media.
"""

import os
import json
import random
from datetime import datetime
from .base_agent import BaseAgent

class EngagementAgent(BaseAgent):
    """Agent for increasing viewer engagement and building community."""
    
    def __init__(self):
        """Initialize the Engagement Agent."""
        super().__init__(name="EngagementAgent")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.engagement_templates = self._load_engagement_templates()
        
    def _load_engagement_templates(self):
        """Load engagement templates from configuration file."""
        # Default engagement templates
        default_templates = {
            "comment_replies": [
                "Thanks for your comment! {personalized_response}",
                "Great point! {personalized_response} What do you think about {follow_up_question}?",
                "I appreciate your feedback! {personalized_response} Would love to hear more of your thoughts on this.",
                "Thanks for watching! {personalized_response} Let me know if you have any other questions.",
                "You're absolutely right about {comment_topic}. {personalized_response}"
            ],
            "community_post_templates": [
                "🔥 NEW VIDEO ALERT! 🔥\n\n{video_title} is now live! In this video, I {video_description}\n\nCheck it out here: {video_link}\n\nWhat topic would you like to see next?",
                "📊 POLL TIME! 📊\n\nWhich topic should I cover next?\n\n{option_1}\n{option_2}\n{option_3}\n{option_4}\n\nLet me know in the comments!",
                "🤔 QUESTION OF THE DAY 🤔\n\n{question}\n\nShare your thoughts in the comments below!",
                "🎁 GIVEAWAY TIME! 🎁\n\nI'm giving away {giveaway_item} to one lucky subscriber!\n\nTo enter:\n1. Like this post\n2. Subscribe to the channel\n3. Comment with {comment_prompt}\n\nWinner will be announced on {announcement_date}!",
                "📱 BEHIND THE SCENES 📱\n\n{behind_the_scenes_content}\n\nWhat kind of behind-the-scenes content would you like to see more of?"
            ],
            "call_to_action_templates": [
                "If you found this video helpful, please give it a thumbs up and subscribe for more content like this!",
                "Don't forget to hit the notification bell so you never miss a new upload!",
                "What's your experience with {video_topic}? Let me know in the comments below!",
                "If you have any questions about {video_topic}, drop them in the comments and I'll do my best to answer!",
                "Want to see more videos like this? Let me know by liking and sharing this video!"
            ],
            "social_media_templates": {
                "twitter": [
                    "🆕 New video alert! 🎬 {video_title} is now live on my channel. Check it out here: {video_link} #TechTok #YouTuber",
                    "Just dropped a new video about {video_topic}! 🚀 Watch now: {video_link} #TechTips #{hashtag}",
                    "🤔 Question for my tech friends: {question} Share your thoughts and check out my latest video for my take: {video_link}",
                    "The secrets of {video_topic} REVEALED in my latest video! 🔍 {video_link} #TechTutorial #{hashtag}"
                ],
                "instagram": [
                    "🎬 NEW VIDEO ALERT! 🎬\n\nJust uploaded a new video about {video_topic}!\n\nIn this video, you'll learn:\n✅ {point_1}\n✅ {point_2}\n✅ {point_3}\n\nLink in bio to watch! 👆\n\n#TechTok #{hashtag} #YouTuber #TechTips",
                    "Behind the scenes of my latest video! 📱\n\n{behind_the_scenes_content}\n\nFull video now live - link in bio!\n\n#BehindTheScenes #ContentCreator #TechTok #{hashtag}"
                ],
                "facebook": [
                    "🆕 New video alert! 🎬\n\nI just uploaded a new video about {video_topic}!\n\nIn this video, I cover:\n- {point_1}\n- {point_2}\n- {point_3}\n\nCheck it out here: {video_link}",
                    "Have you ever wondered about {video_topic}? 🤔\n\nIn my latest video, I break down everything you need to know!\n\nWatch now: {video_link}"
                ]
            }
        }
        
        # Try to load from config file
        config = self.load_config()
        if "engagement_templates" in config:
            return config["engagement_templates"]
        
        # If no config found, create one with defaults
        config_file = os.path.join(self.config_dir, "engagement_agent_config.json")
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump({"engagement_templates": default_templates}, f, indent=2)
            
        return default_templates
    
    def generate_comment_replies(self, comments, video_topic):
        """Generate personalized replies to user comments."""
        self.logger.info(f"Generating replies for {len(comments)} comments")
        
        replies = []
        
        for comment in comments:
            # Select a random template
            template = random.choice(self.engagement_templates["comment_replies"])
            
            # Generate a personalized response based on the comment
            personalized_response = self._generate_personalized_response(comment["text"], video_topic)
            
            # Generate a follow-up question
            follow_up_question = self._generate_follow_up_question(comment["text"], video_topic)
            
            # Extract the main topic from the comment
            comment_topic = self._extract_comment_topic(comment["text"])
            
            # Fill in the template
            reply = template.replace("{personalized_response}", personalized_response)
            reply = reply.replace("{follow_up_question}", follow_up_question)
            reply = reply.replace("{comment_topic}", comment_topic)
            
            replies.append({
                "comment_id": comment["id"],
                "comment_text": comment["text"],
                "reply": reply
            })
            
        self.logger.info(f"Generated {len(replies)} comment replies")
        return replies
    
    def _generate_personalized_response(self, comment_text, video_topic):
        """Generate a personalized response to a comment."""
        # This would typically use the OpenAI API, but for demonstration we'll use templates
        
        # Simple sentiment analysis
        positive_words = ["great", "good", "love", "awesome", "amazing", "helpful", "thanks", "thank you"]
        negative_words = ["bad", "poor", "hate", "terrible", "awful", "useless", "waste"]
        
        sentiment = "neutral"
        if any(word in comment_text.lower() for word in positive_words):
            sentiment = "positive"
        elif any(word in comment_text.lower() for word in negative_words):
            sentiment = "negative"
            
        # Generate response based on sentiment
        if sentiment == "positive":
            responses = [
                f"I'm glad you enjoyed the video about {video_topic}!",
                f"Thanks for the positive feedback! I put a lot of effort into making my {video_topic} content valuable.",
                f"Your support means a lot to me! I'll keep making more content about {video_topic}.",
                "I appreciate your kind words! Comments like yours motivate me to create better content."
            ]
        elif sentiment == "negative":
            responses = [
                f"I'm sorry to hear that. I'm always looking to improve my content on {video_topic}.",
                "Thank you for your honest feedback. I'll take it into consideration for future videos.",
                f"I appreciate your perspective. What specific aspects of {video_topic} would you like me to cover better?",
                "Thanks for sharing your thoughts. I'm constantly working to make my content more valuable."
            ]
        else:
            responses = [
                f"Thanks for watching my video on {video_topic}!",
                f"I appreciate you taking the time to comment on my {video_topic} video.",
                f"Thanks for engaging with my content about {video_topic}!",
                "I value your input! Let me know if you have any questions."
            ]
            
        return random.choice(responses)
    
    def _generate_follow_up_question(self, comment_text, video_topic):
        """Generate a follow-up question based on a comment."""
        # Generic follow-up questions related to the video topic
        follow_up_questions = [
            f"what other aspects of {video_topic} you'd like me to cover",
            f"how you've been using {video_topic} in your own projects",
            f"what challenges you've faced with {video_topic}",
            f"what your favorite {video_topic} tools or resources are",
            f"how long you've been interested in {video_topic}"
        ]
        
        return random.choice(follow_up_questions)
    
    def _extract_comment_topic(self, comment_text):
        """Extract the main topic from a comment."""
        # This would typically use NLP, but for demonstration we'll use a simple approach
        
        # Split the comment into words
        words = comment_text.lower().split()
        
        # Remove common words
        common_words = ["the", "and", "is", "in", "to", "a", "of", "for", "on", "with", "as", "this", "that"]
        filtered_words = [word for word in words if word not in common_words and len(word) > 3]
        
        if filtered_words:
            # Return the longest word as the topic
            return max(filtered_words, key=len)
        else:
            return "this topic"
    
    def generate_community_posts(self, video_data=None, count=5):
        """Generate community posts to engage with subscribers."""
        self.logger.info(f"Generating {count} community posts")
        
        posts = []
        
        for _ in range(count):
            # Select a random template
            template = random.choice(self.engagement_templates["community_post_templates"])
            
            # Generate video data if not provided
            if not video_data:
                video_data = {
                    "title": "Ultimate Guide to Tech Gadgets in 2023",
                    "description": "review the latest tech gadgets and show you which ones are worth your money",
                    "link": "https://youtu.be/example",
                    "topic": "tech gadgets"
                }
                
            # Generate poll options
            poll_options = [
                "Option 1: Smartphone Comparison (iPhone vs Android)",
                "Option 2: Budget Tech Gadgets Under $100",
                "Option 3: Home Office Setup Guide",
                "Option 4: Future Tech Trends for 2024"
            ]
            
            # Generate question of the day
            questions = [
                "What's your favorite tech gadget of 2023 so far?",
                "If you could only use one tech device for a year, what would it be?",
                "What tech skill do you think is most valuable to learn right now?",
                "What upcoming tech are you most excited about?",
                "What's your biggest tech-related challenge?"
            ]
            
            # Generate giveaway details
            giveaway_items = [
                "a brand new wireless charger",
                "a premium tech accessory bundle",
                "a $50 Amazon gift card",
                "a one-year subscription to my favorite productivity app"
            ]
            
            # Generate behind the scenes content
            behind_the_scenes = [
                "Here's a look at my filming setup! I recently upgraded my lighting to get better video quality.",
                "Editing this week's video took over 15 hours! Here's a timelapse of the process.",
                "Testing out new equipment for upcoming videos. What do you think of this setup?",
                "Planning content for the next month. Here's a sneak peek at what's coming!"
            ]
            
            # Fill in the template
            post = template
            post = post.replace("{video_title}", video_data["title"])
            post = post.replace("{video_description}", video_data["description"])
            post = post.replace("{video_link}", video_data["link"])
            post = post.replace("{video_topic}", video_data["topic"])
            
            post = post.replace("{option_1}", poll_options[0])
            post = post.replace("{option_2}", poll_options[1])
            post = post.replace("{option_3}", poll_options[2])
            post = post.replace("{option_4}", poll_options[3])
            
            post = post.replace("{question}", random.choice(questions))
            
            post = post.replace("{giveaway_item}", random.choice(giveaway_items))
            post = post.replace("{comment_prompt}", "#AltTechTok")
            post = post.replace("{announcement_date}", (datetime.now().replace(day=datetime.now().day + 7)).strftime("%B %d, %Y"))
            
            post = post.replace("{behind_the_scenes_content}", random.choice(behind_the_scenes))
            
            posts.append({
                "type": self._determine_post_type(template),
                "content": post
            })
            
        self.logger.info(f"Generated {len(posts)} community posts")
        return posts
    
    def _determine_post_type(self, template):
        """Determine the type of community post based on the template."""
        if "NEW VIDEO ALERT" in template:
            return "video_promotion"
        elif "POLL TIME" in template:
            return "poll"
        elif "QUESTION OF THE DAY" in template:
            return "question"
        elif "GIVEAWAY TIME" in template:
            return "giveaway"
        elif "BEHIND THE SCENES" in template:
            return "behind_the_scenes"
        else:
            return "general"
    
    def generate_call_to_actions(self, video_topic):
        """Generate effective call-to-actions for video scripts."""
        self.logger.info(f"Generating call-to-actions for topic: {video_topic}")
        
        ctas = []
        
        for template in self.engagement_templates["call_to_action_templates"]:
            # Fill in the template
            cta = template.replace("{video_topic}", video_topic)
            
            ctas.append(cta)
            
        self.logger.info(f"Generated {len(ctas)} call-to-actions")
        return ctas
    
    def generate_social_media_posts(self, video_data, platforms=None):
        """Generate social media posts to promote a video across platforms."""
        self.logger.info(f"Generating social media posts for video: {video_data['title']}")
        
        if not platforms:
            platforms = ["twitter", "instagram", "facebook"]
            
        posts = {}
        
        for platform in platforms:
            if platform in self.engagement_templates["social_media_templates"]:
                templates = self.engagement_templates["social_media_templates"][platform]
                
                # Select a random template
                template = random.choice(templates)
                
                # Generate key points
                points = [
                    f"How to optimize your {video_data['topic']} setup",
                    f"Top {video_data['topic']} recommendations for 2023",
                    f"Common {video_data['topic']} mistakes to avoid",
                    f"Budget-friendly {video_data['topic']} options",
                    f"Advanced {video_data['topic']} tips and tricks"
                ]
                
                # Generate hashtag
                hashtag = video_data['topic'].replace(" ", "")
                
                # Generate behind the scenes content
                behind_the_scenes = [
                    f"Setting up to film my {video_data['topic']} video! It took 3 hours to research and prepare.",
                    f"The lighting setup for my {video_data['topic']} video was tricky, but worth it for the final result!",
                    f"Editing my {video_data['topic']} video and adding some special effects to make the demonstrations clearer."
                ]
                
                # Fill in the template
                post = template
                post = post.replace("{video_title}", video_data["title"])
                post = post.replace("{video_topic}", video_data["topic"])
                post = post.replace("{video_link}", video_data["link"])
                post = post.replace("{hashtag}", hashtag)
                
                post = post.replace("{point_1}", points[0])
                post = post.replace("{point_2}", points[1])
                post = post.replace("{point_3}", points[2])
                
                post = post.replace("{question}", f"What's your favorite thing about {video_data['topic']}?")
                
                post = post.replace("{behind_the_scenes_content}", random.choice(behind_the_scenes))
                
                if platform not in posts:
                    posts[platform] = []
                    
                posts[platform].append(post)
                
        self.logger.info(f"Generated social media posts for {len(posts)} platforms")
        return posts
    
    def analyze_engagement_metrics(self, metrics):
        """Analyze engagement metrics and provide recommendations."""
        self.logger.info("Analyzing engagement metrics")
        
        analysis = {
            "metrics_summary": {},
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        # Calculate average metrics
        avg_likes = sum(video["likes"] for video in metrics["videos"]) / len(metrics["videos"])
        avg_comments = sum(video["comments"] for video in metrics["videos"]) / len(metrics["videos"])
        avg_shares = sum(video["shares"] for video in metrics["videos"]) / len(metrics["videos"])
        
        # Calculate engagement rate
        avg_views = sum(video["views"] for video in metrics["videos"]) / len(metrics["videos"])
        engagement_rate = (avg_likes + avg_comments + avg_shares) / avg_views if avg_views > 0 else 0
        
        # Store metrics summary
        analysis["metrics_summary"] = {
            "avg_likes": avg_likes,
            "avg_comments": avg_comments,
            "avg_shares": avg_shares,
            "avg_views": avg_views,
            "engagement_rate": engagement_rate
        }
        
        # Identify strengths
        if avg_likes > 50:
            analysis["strengths"].append("Good like-to-view ratio, indicating viewers enjoy your content")
            
        if avg_comments > 10:
            analysis["strengths"].append("Healthy comment section, showing an engaged community")
            
        if avg_shares > 5:
            analysis["strengths"].append("Videos are being shared, expanding your reach organically")
            
        if engagement_rate > 0.05:
            analysis["strengths"].append("Above-average engagement rate compared to industry standards")
            
        # Identify weaknesses
        if avg_likes < 20:
            analysis["weaknesses"].append("Low like count, may indicate content isn't resonating with viewers")
            
        if avg_comments < 5:
            analysis["weaknesses"].append("Few comments, suggesting viewers aren't feeling compelled to engage")
            
        if avg_shares < 2:
            analysis["weaknesses"].append("Low share count, limiting organic growth potential")
            
        if engagement_rate < 0.02:
            analysis["weaknesses"].append("Below-average engagement rate, indicating passive viewership")
            
        # Generate recommendations
        if avg_comments < 10:
            analysis["recommendations"].append({
                "area": "comments",
                "recommendation": "Ask specific questions in your videos to encourage viewers to share their thoughts",
                "implementation": "Add 2-3 direct questions throughout each video, especially at the beginning and end"
            })
            
        if avg_likes < 50:
            analysis["recommendations"].append({
                "area": "likes",
                "recommendation": "Add clear call-to-actions for likes at strategic points in your videos",
                "implementation": "Include a like reminder within the first 30 seconds and again after delivering key value"
            })
            
        if avg_shares < 5:
            analysis["recommendations"].append({
                "area": "shares",
                "recommendation": "Create more shareable content with practical value or entertainment",
                "implementation": "Include 'share-worthy' segments like quick tips, surprising facts, or humorous moments"
            })
            
        # General recommendations
        analysis["recommendations"].append({
            "area": "community",
            "recommendation": "Post consistently on the Community tab to maintain engagement between uploads",
            "implementation": "Schedule 2-3 community posts per week (polls, updates, questions, behind-the-scenes)"
        })
        
        analysis["recommendations"].append({
            "area": "comments",
            "recommendation": "Respond to comments within 24 hours to foster community and encourage more interaction",
            "implementation": "Set aside 15-30 minutes daily to reply to new comments, prioritizing questions and detailed feedback"
        })
        
        analysis["recommendations"].append({
            "area": "cross-promotion",
            "recommendation": "Promote videos across social media platforms to increase reach and engagement",
            "implementation": "Create platform-specific posts for each new video using the social media templates"
        })
        
        self.logger.info("Completed engagement metrics analysis")
        return analysis
    
    def run(self):
        """Run the Engagement Agent to generate engagement content."""
        self.logger.info("Starting Engagement Agent")
        
        # Sample video data
        video_data = {
            "title": "10 Must-Have Tech Gadgets for 2023",
            "description": "review the latest tech gadgets and show you which ones are worth your money",
            "link": "https://youtu.be/example",
            "topic": "tech gadgets"
        }
        
        # Sample comments
        sample_comments = [
            {"id": "comment1", "text": "Great video! I really enjoyed your review of the new smartphone."},
            {"id": "comment2", "text": "I've been looking for a good tech review channel. Subscribed!"},
            {"id": "comment3", "text": "What do you think about the new wireless earbuds? Worth the price?"},
            {"id": "comment4", "text": "This video was too long. Could have been more concise."},
            {"id": "comment5", "text": "Thanks for the detailed comparison. Really helped me decide!"}
        ]
        
        # Sample engagement metrics
        sample_metrics = {
            "videos": [
                {"title": "Video 1", "views": 1200, "likes": 85, "comments": 12, "shares": 5},
                {"title": "Video 2", "views": 950, "likes": 63, "comments": 8, "shares": 3},
                {"title": "Video 3", "views": 1500, "likes": 110, "comments": 15, "shares": 7},
                {"title": "Video 4", "views": 800, "likes": 45, "comments": 6, "shares": 2},
                {"title": "Video 5", "views": 1100, "likes": 75, "comments": 10, "shares": 4}
            ]
        }
        
        # Generate comment replies
        comment_replies = self.generate_comment_replies(sample_comments, video_data["topic"])
        
        # Generate community posts
        community_posts = self.generate_community_posts(video_data, count=3)
        
        # Generate call-to-actions
        ctas = self.generate_call_to_actions(video_data["topic"])
        
        # Generate social media posts
        social_media_posts = self.generate_social_media_posts(video_data)
        
        # Analyze engagement metrics
        engagement_analysis = self.analyze_engagement_metrics(sample_metrics)
        
        # Compile results
        results = {
            "comment_replies": comment_replies,
            "community_posts": community_posts,
            "call_to_actions": ctas,
            "social_media_posts": social_media_posts,
            "engagement_analysis": engagement_analysis
        }
        
        # Save results
        self.save_results(results)
        
        # Print summary
        print("\n=== Engagement Content Generation Results ===")
        print(f"Generated {len(comment_replies)} comment replies")
        print(f"Generated {len(community_posts)} community posts")
        print(f"Generated {len(ctas)} call-to-actions")
        print(f"Generated social media posts for {len(social_media_posts)} platforms")
        
        print("\n=== Sample Comment Reply ===")
        if comment_replies:
            sample_reply = comment_replies[0]
            print(f"Comment: {sample_reply['comment_text']}")
            print(f"Reply: {sample_reply['reply']}")
            
        print("\n=== Sample Community Post ===")
        if community_posts:
            sample_post = community_posts[0]
            print(f"Type: {sample_post['type']}")
            print(f"Content: {sample_post['content'][:150]}...")
            
        print("\n=== Engagement Analysis ===")
        print("Strengths:")
        for strength in engagement_analysis["strengths"]:
            print(f"- {strength}")
            
        print("\nTop Recommendations:")
        for i, rec in enumerate(engagement_analysis["recommendations"][:3], 1):
            print(f"{i}. {rec['recommendation']}")
            
        print("\nAll results saved to:", os.path.join(self.results_dir, f"engagement_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"))
        
        return True 