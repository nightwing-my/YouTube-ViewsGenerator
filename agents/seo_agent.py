"""
SEO Agent
---------
Optimizes video titles, descriptions, and tags for better discoverability on YouTube.
"""

import os
import json
import re
import random
from datetime import datetime
import requests
from .base_agent import BaseAgent

class SEOAgent(BaseAgent):
    """Agent for optimizing video SEO elements."""
    
    def __init__(self):
        """Initialize the SEO Agent."""
        super().__init__(name="SEOAgent")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.rapidapi_key = os.getenv("RAPIDAPI_KEY")
        self.seo_templates = self._load_seo_templates()
        
    def _load_seo_templates(self):
        """Load SEO templates from configuration file."""
        # Default SEO templates
        default_templates = {
            "title_templates": [
                "Top {number} {keyword} Tips That Will {benefit}",
                "How to {action} {keyword} in {timeframe}",
                "{keyword} Tutorial: {specific_topic} for Beginners",
                "The Ultimate Guide to {keyword} in {year}",
                "{keyword} vs {alternative}: Which is Better for {purpose}?",
                "Why {keyword} is {adjective} for {audience}",
                "{number} {adjective} {keyword} Hacks You Need to Know",
                "{keyword} {specific_topic}: Everything You Need to Know",
                "I Tried {keyword} for {timeframe} - Here's What Happened",
                "{action} Your {keyword} with These {adjective} Tips"
            ],
            "description_templates": [
                "In this video, I'll show you how to {action} {keyword} to {benefit}. If you're looking to {goal}, these {adjective} tips will help you {outcome}.\n\n{timestamps}\n\n#LINKS\n{links}\n\n#TAGS\n{tags}",
                "Discover the {adjective} ways to {action} {keyword} in this comprehensive guide. Whether you're a beginner or expert, you'll learn valuable insights about {specific_topic}.\n\n{timestamps}\n\n#LINKS\n{links}\n\n#TAGS\n{tags}",
                "Are you struggling with {problem}? In this video, I'll share my top {number} {keyword} strategies that will help you {benefit}.\n\n{timestamps}\n\n#LINKS\n{links}\n\n#TAGS\n{tags}"
            ],
            "tag_categories": {
                "main_keyword": [],
                "related_keywords": [],
                "broader_topics": [],
                "specific_topics": [],
                "questions": []
            }
        }
        
        # Try to load from config file
        config = self.load_config()
        if "seo_templates" in config:
            return config["seo_templates"]
        
        # If no config found, create one with defaults
        config_file = os.path.join(self.config_dir, "seo_agent_config.json")
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump({"seo_templates": default_templates}, f, indent=2)
            
        return default_templates
    
    def get_keyword_suggestions(self, seed_keyword, count=10):
        """Get keyword suggestions based on a seed keyword."""
        self.logger.info(f"Getting keyword suggestions for: {seed_keyword}")
        
        if self.rapidapi_key:
            try:
                # This would typically use a real API like RapidAPI's Keywords Everywhere
                # For demonstration, we'll use a simulated response
                return self._get_simulated_keywords(seed_keyword, count)
            except Exception as e:
                self.logger.error(f"Error getting keyword suggestions: {str(e)}")
                return self._get_simulated_keywords(seed_keyword, count)
        else:
            self.logger.warning("RapidAPI key not found. Using simulated keyword data.")
            return self._get_simulated_keywords(seed_keyword, count)
    
    def _get_simulated_keywords(self, seed_keyword, count=10):
        """Generate simulated keyword suggestions for demonstration."""
        tech_modifiers = [
            "best", "top", "how to use", "review", "tutorial", "guide", "vs", "alternatives",
            "tips", "tricks", "hacks", "for beginners", "advanced", "comparison", "setup",
            "problems", "solutions", "explained", "overview", "features"
        ]
        
        tech_topics = [
            "smartphone", "laptop", "AI", "machine learning", "coding", "programming",
            "software", "hardware", "gadget", "app", "camera", "gaming", "computer",
            "cloud", "cybersecurity", "data science", "blockchain", "VR", "AR", "IoT"
        ]
        
        # If seed keyword is a tech topic, use modifiers
        if any(topic in seed_keyword.lower() for topic in tech_topics):
            keywords = [f"{modifier} {seed_keyword}" for modifier in random.sample(tech_modifiers, min(count, len(tech_modifiers)))]
        # If seed keyword is a modifier, use tech topics
        elif any(modifier in seed_keyword.lower() for modifier in tech_modifiers):
            keywords = [f"{seed_keyword} {topic}" for topic in random.sample(tech_topics, min(count, len(tech_topics)))]
        # Otherwise mix both
        else:
            keywords = []
            for _ in range(count):
                if random.choice([True, False]):
                    keywords.append(f"{random.choice(tech_modifiers)} {seed_keyword}")
                else:
                    keywords.append(f"{seed_keyword} {random.choice(tech_topics)}")
        
        # Add some volume and competition data
        result = []
        for keyword in keywords[:count]:
            result.append({
                "keyword": keyword,
                "volume": random.randint(500, 10000),
                "competition": round(random.random(), 2),
                "cpc": round(random.uniform(0.5, 5.0), 2)
            })
            
        # Sort by volume
        result.sort(key=lambda x: x["volume"], reverse=True)
        
        return result
    
    def analyze_title(self, title):
        """Analyze a video title for SEO effectiveness."""
        self.logger.info(f"Analyzing title: {title}")
        
        analysis = {
            "length": len(title),
            "length_score": 0,
            "has_number": bool(re.search(r'\d+', title)),
            "has_power_words": False,
            "has_brackets": "[" in title or "(" in title,
            "has_year": bool(re.search(r'20\d\d', title)),
            "capitalization": "Title Case" if title.istitle() else "Sentence case" if title[0].isupper() else "lowercase",
            "suggestions": []
        }
        
        # Check length score (ideal: 50-60 characters)
        if 50 <= analysis["length"] <= 60:
            analysis["length_score"] = 10
        elif 40 <= analysis["length"] < 50 or 60 < analysis["length"] <= 70:
            analysis["length_score"] = 7
        else:
            analysis["length_score"] = 4
            
        # Check for power words
        power_words = ["ultimate", "essential", "amazing", "incredible", "powerful", "proven", 
                      "secret", "exclusive", "revealed", "stunning", "remarkable", "extraordinary",
                      "breakthrough", "revolutionary", "game-changing", "mind-blowing"]
        
        analysis["has_power_words"] = any(word.lower() in title.lower() for word in power_words)
        
        # Generate suggestions
        if analysis["length"] < 40:
            analysis["suggestions"].append("Title is too short. Add more descriptive keywords.")
        elif analysis["length"] > 70:
            analysis["suggestions"].append("Title is too long. YouTube may truncate it in search results.")
            
        if not analysis["has_number"]:
            analysis["suggestions"].append("Consider adding a number (e.g., '5 Ways to...' or 'Top 10...').")
            
        if not analysis["has_power_words"]:
            analysis["suggestions"].append("Add power words to make your title more compelling.")
            
        if not analysis["has_brackets"]:
            analysis["suggestions"].append("Consider using brackets or parentheses to highlight a key benefit.")
            
        if not analysis["has_year"]:
            analysis["suggestions"].append("Add the current year to show that your content is up-to-date.")
            
        # Calculate overall score
        base_score = analysis["length_score"]
        if analysis["has_number"]: base_score += 2
        if analysis["has_power_words"]: base_score += 2
        if analysis["has_brackets"]: base_score += 2
        if analysis["has_year"]: base_score += 2
        
        analysis["overall_score"] = min(10, base_score)
        
        return analysis
    
    def optimize_title(self, original_title, keywords=None):
        """Optimize a video title for better SEO."""
        self.logger.info(f"Optimizing title: {original_title}")
        
        # Analyze the original title
        analysis = self.analyze_title(original_title)
        
        # If the title is already good, return it
        if analysis["overall_score"] >= 8:
            return {
                "original_title": original_title,
                "optimized_title": original_title,
                "analysis": analysis,
                "changes_made": []
            }
            
        # Extract main topic from the title
        main_topic = re.sub(r'[0-9\[\]\(\)\{\}]', '', original_title)
        main_topic = re.sub(r'top|best|how to|guide|tutorial|review', '', main_topic, flags=re.IGNORECASE)
        main_topic = main_topic.strip()
        
        # Get current year
        current_year = datetime.now().year
        
        # Get keywords if not provided
        if not keywords:
            keywords = self.get_keyword_suggestions(main_topic, count=3)
            keywords = [k["keyword"] for k in keywords]
        
        # Select a template
        template = random.choice(self.seo_templates["title_templates"])
        
        # Fill in the template
        optimized_title = template
        
        # Replace placeholders
        replacements = {
            "{keyword}": main_topic,
            "{number}": str(random.choice([3, 5, 7, 10, 12])),
            "{year}": str(current_year),
            "{timeframe}": random.choice(["30 Days", "One Week", "2023", "One Month"]),
            "{action}": random.choice(["Master", "Improve", "Optimize", "Transform", "Boost"]),
            "{benefit}": random.choice(["Change Your Life", "Save You Time", "Boost Your Skills", "Improve Results"]),
            "{specific_topic}": keywords[0] if keywords else main_topic,
            "{alternative}": keywords[1] if len(keywords) > 1 else "Alternatives",
            "{purpose}": random.choice(["Beginners", "Professionals", "Daily Use", "Performance"]),
            "{audience}": random.choice(["Beginners", "Experts", "Everyone", "Tech Enthusiasts"]),
            "{adjective}": random.choice(["Amazing", "Essential", "Powerful", "Game-Changing", "Incredible"])
        }
        
        for placeholder, replacement in replacements.items():
            optimized_title = optimized_title.replace(placeholder, replacement)
        
        # Add brackets if suggested and not already present
        if "brackets" in str(analysis["suggestions"]) and not analysis["has_brackets"]:
            optimized_title += f" [{random.choice(['2023', 'Tutorial', 'Guide', 'Tips', 'Must Watch'])}]"
            
        # Ensure proper length
        if len(optimized_title) > 70:
            optimized_title = optimized_title[:67] + "..."
            
        # Track changes made
        changes_made = []
        if analysis["length"] != len(optimized_title):
            changes_made.append(f"Adjusted title length from {analysis['length']} to {len(optimized_title)} characters")
            
        if not analysis["has_number"] and bool(re.search(r'\d+', optimized_title)):
            changes_made.append("Added a number to the title")
            
        if not analysis["has_power_words"] and any(word.lower() in optimized_title.lower() for word in ["ultimate", "essential", "amazing", "incredible"]):
            changes_made.append("Added power words to the title")
            
        if not analysis["has_brackets"] and ("[" in optimized_title or "(" in optimized_title):
            changes_made.append("Added brackets to highlight key information")
            
        if not analysis["has_year"] and str(current_year) in optimized_title:
            changes_made.append(f"Added the current year ({current_year})")
            
        # Re-analyze the optimized title
        optimized_analysis = self.analyze_title(optimized_title)
        
        return {
            "original_title": original_title,
            "optimized_title": optimized_title,
            "original_analysis": analysis,
            "optimized_analysis": optimized_analysis,
            "changes_made": changes_made
        }
    
    def analyze_description(self, description):
        """Analyze a video description for SEO effectiveness."""
        self.logger.info("Analyzing video description")
        
        analysis = {
            "length": len(description),
            "length_score": 0,
            "has_timestamps": bool(re.search(r'\d+:\d+', description)),
            "has_links": bool(re.search(r'http[s]?://', description)),
            "has_tags": "#" in description,
            "has_call_to_action": bool(re.search(r'subscribe|like|comment|share', description, re.IGNORECASE)),
            "keyword_density": {},
            "suggestions": []
        }
        
        # Check length score (ideal: 250+ characters)
        if analysis["length"] >= 250:
            analysis["length_score"] = 10
        elif 150 <= analysis["length"] < 250:
            analysis["length_score"] = 7
        else:
            analysis["length_score"] = 4
            
        # Calculate keyword density
        words = re.findall(r'\b\w+\b', description.lower())
        word_count = len(words)
        
        if word_count > 0:
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Only count words with more than 3 characters
                    if word not in word_freq:
                        word_freq[word] = 0
                    word_freq[word] += 1
                    
            # Get top 5 keywords
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for word, count in top_keywords:
                analysis["keyword_density"][word] = round(count / word_count * 100, 2)
        
        # Generate suggestions
        if analysis["length"] < 150:
            analysis["suggestions"].append("Description is too short. Aim for at least 250 characters.")
            
        if not analysis["has_timestamps"]:
            analysis["suggestions"].append("Add timestamps to improve user experience and SEO.")
            
        if not analysis["has_links"]:
            analysis["suggestions"].append("Include relevant links to your social media or related content.")
            
        if not analysis["has_tags"]:
            analysis["suggestions"].append("Add hashtags to improve discoverability.")
            
        if not analysis["has_call_to_action"]:
            analysis["suggestions"].append("Include a call-to-action asking viewers to like, comment, or subscribe.")
            
        # Calculate overall score
        base_score = analysis["length_score"]
        if analysis["has_timestamps"]: base_score += 2
        if analysis["has_links"]: base_score += 2
        if analysis["has_tags"]: base_score += 2
        if analysis["has_call_to_action"]: base_score += 2
        
        analysis["overall_score"] = min(10, base_score)
        
        return analysis
    
    def optimize_description(self, original_description, title, keywords=None):
        """Optimize a video description for better SEO."""
        self.logger.info("Optimizing video description")
        
        # Analyze the original description
        analysis = self.analyze_description(original_description)
        
        # Extract main topic from the title
        main_topic = re.sub(r'[0-9\[\]\(\)\{\}]', '', title)
        main_topic = re.sub(r'top|best|how to|guide|tutorial|review', '', main_topic, flags=re.IGNORECASE)
        main_topic = main_topic.strip()
        
        # Get keywords if not provided
        if not keywords:
            keywords = self.get_keyword_suggestions(main_topic, count=5)
            keywords = [k["keyword"] for k in keywords]
        
        # Select a template
        template = random.choice(self.seo_templates["description_templates"])
        
        # Generate timestamps
        timestamps = "🕒 TIMESTAMPS:\n"
        timestamps += "00:00 Introduction\n"
        timestamps += f"01:30 What is {main_topic}?\n"
        timestamps += "03:45 Key Features and Benefits\n"
        timestamps += "07:20 Step-by-Step Tutorial\n"
        timestamps += "12:30 Tips and Best Practices\n"
        timestamps += "15:45 Common Mistakes to Avoid\n"
        timestamps += "18:30 Conclusion and Next Steps"
        
        # Generate links
        links = "🔗 FOLLOW ME:\n"
        links += "Website: https://example.com\n"
        links += "Twitter: https://twitter.com/example\n"
        links += "Instagram: https://instagram.com/example\n"
        links += "Discord: https://discord.gg/example"
        
        # Generate tags
        tags = "🏷️ "
        for keyword in keywords:
            tags += f"#{keyword.replace(' ', '')}" + " "
            
        # Fill in the template
        replacements = {
            "{keyword}": main_topic,
            "{number}": str(random.choice([3, 5, 7, 10])),
            "{action}": random.choice(["master", "improve", "optimize", "transform", "boost"]),
            "{benefit}": random.choice(["save time", "improve results", "boost productivity", "enhance skills"]),
            "{goal}": random.choice(["learn more about tech", "improve your skills", "stay updated", "master new tools"]),
            "{adjective}": random.choice(["amazing", "essential", "powerful", "game-changing", "incredible"]),
            "{specific_topic}": keywords[0] if keywords else main_topic,
            "{problem}": random.choice(["outdated technology", "slow performance", "technical issues", "learning curve"]),
            "{outcome}": random.choice(["achieve better results", "become more efficient", "master new skills", "stay ahead of the curve"]),
            "{timestamps}": timestamps,
            "{links}": links,
            "{tags}": tags
        }
        
        optimized_description = template
        for placeholder, replacement in replacements.items():
            optimized_description = optimized_description.replace(placeholder, replacement)
            
        # Add a call to action if missing
        if not analysis["has_call_to_action"]:
            optimized_description += "\n\n👍 If you found this video helpful, please LIKE, SUBSCRIBE, and hit the NOTIFICATION BELL to stay updated with our latest content!"
            
        # Track changes made
        changes_made = []
        if analysis["length"] != len(optimized_description):
            changes_made.append(f"Expanded description from {analysis['length']} to {len(optimized_description)} characters")
            
        if not analysis["has_timestamps"] and "TIMESTAMPS" in optimized_description:
            changes_made.append("Added timestamps for better user navigation")
            
        if not analysis["has_links"] and "FOLLOW ME" in optimized_description:
            changes_made.append("Added social media and website links")
            
        if not analysis["has_tags"] and "#" in optimized_description:
            changes_made.append("Added hashtags for better discoverability")
            
        if not analysis["has_call_to_action"] and "SUBSCRIBE" in optimized_description:
            changes_made.append("Added call-to-action to encourage engagement")
            
        # Re-analyze the optimized description
        optimized_analysis = self.analyze_description(optimized_description)
        
        return {
            "original_description": original_description,
            "optimized_description": optimized_description,
            "original_analysis": analysis,
            "optimized_analysis": optimized_analysis,
            "changes_made": changes_made
        }
    
    def generate_tags(self, title, count=15):
        """Generate optimized tags for a video based on the title."""
        self.logger.info(f"Generating tags for: {title}")
        
        # Extract main topic from the title
        main_topic = re.sub(r'[0-9\[\]\(\)\{\}]', '', title)
        main_topic = re.sub(r'top|best|how to|guide|tutorial|review', '', main_topic, flags=re.IGNORECASE)
        main_topic = main_topic.strip()
        
        # Get keyword suggestions
        keyword_suggestions = self.get_keyword_suggestions(main_topic, count=20)
        
        # Organize tags by category
        tags = {
            "main_keyword": [main_topic],
            "related_keywords": [k["keyword"] for k in keyword_suggestions[:5]],
            "broader_topics": ["tech", "technology", "tutorial", "how to", "guide"],
            "specific_topics": [k["keyword"] for k in keyword_suggestions[5:10]],
            "questions": [
                f"how to {main_topic}",
                f"what is {main_topic}",
                f"best {main_topic}",
                f"{main_topic} tutorial",
                f"{main_topic} guide"
            ]
        }
        
        # Flatten and deduplicate tags
        all_tags = []
        for category, category_tags in tags.items():
            all_tags.extend(category_tags)
            
        # Remove duplicates and limit to count
        unique_tags = []
        for tag in all_tags:
            if tag.lower() not in [t.lower() for t in unique_tags]:
                unique_tags.append(tag)
                
        return unique_tags[:count]
    
    def run(self):
        """Run the SEO Agent to optimize video metadata."""
        self.logger.info("Starting SEO Agent")
        
        # Sample video data to optimize
        sample_video = {
            "title": "Tech Review: New Gadgets in 2023",
            "description": "In this video I review some new tech gadgets. Let me know what you think in the comments!",
            "tags": ["tech", "review", "gadgets"]
        }
        
        # Get keyword suggestions
        keywords = self.get_keyword_suggestions("tech gadgets", count=10)
        keyword_list = [k["keyword"] for k in keywords]
        
        # Optimize title
        title_optimization = self.optimize_title(sample_video["title"], keyword_list)
        
        # Optimize description
        description_optimization = self.optimize_description(
            sample_video["description"],
            title_optimization["optimized_title"],
            keyword_list
        )
        
        # Generate tags
        optimized_tags = self.generate_tags(title_optimization["optimized_title"])
        
        # Compile results
        results = {
            "original_video": sample_video,
            "optimized_video": {
                "title": title_optimization["optimized_title"],
                "description": description_optimization["optimized_description"],
                "tags": optimized_tags
            },
            "title_optimization": title_optimization,
            "description_optimization": description_optimization,
            "keyword_suggestions": keywords
        }
        
        # Save results
        self.save_results(results)
        
        # Print summary
        print("\n=== SEO Optimization Results ===")
        print("Original Title:", sample_video["title"])
        print("Optimized Title:", title_optimization["optimized_title"])
        print(f"Title Score Improvement: {title_optimization['original_analysis']['overall_score']} → {title_optimization['optimized_analysis']['overall_score']}")
        
        print("\nOriginal Description Length:", len(sample_video["description"]))
        print("Optimized Description Length:", len(description_optimization["optimized_description"]))
        print(f"Description Score Improvement: {description_optimization['original_analysis']['overall_score']} → {description_optimization['optimized_analysis']['overall_score']}")
        
        print("\nOriginal Tags Count:", len(sample_video["tags"]))
        print("Optimized Tags Count:", len(optimized_tags))
        
        print("\nTop Keyword Suggestions:")
        for i, keyword in enumerate(keywords[:5], 1):
            print(f"{i}. {keyword['keyword']} (Volume: {keyword['volume']}, Competition: {keyword['competition']})")
            
        print("\nAll results saved to:", os.path.join(self.results_dir, f"seo_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"))
        
        return True 