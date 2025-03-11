"""
YouTube Channel Growth AI Suite - Setup Test
-----------------------------------------
This script verifies your setup and API connections.
"""

import os
from dotenv import load_dotenv
from agents import (
    ContentAgent,
    SEOAgent,
    AnalyticsAgent,
    EngagementAgent,
    SchedulerAgent
)

def test_api_keys():
    """Test if all required API keys are set."""
    load_dotenv()
    
    required_keys = {
        "YOUTUBE_API_KEY": "YouTube API",
        "OPENAI_API_KEY": "OpenAI API",
        "RAPIDAPI_KEY": "RapidAPI"
    }
    
    missing_keys = []
    for key, name in required_keys.items():
        if not os.getenv(key):
            missing_keys.append(name)
    
    return missing_keys

def test_youtube_connection():
    """Test YouTube API connection."""
    analytics = AnalyticsAgent()
    try:
        stats = analytics.get_channel_stats()
        return bool(stats), "YouTube API connection successful" if stats else "No channel data found"
    except Exception as e:
        return False, f"YouTube API error: {str(e)}"

def test_agents():
    """Test basic functionality of each agent."""
    results = {}
    
    # Test Content Agent
    try:
        content = ContentAgent()
        ideas = content.generate_video_ideas(count=1)
        results["Content Agent"] = "✓ Working" if ideas else "⚠ No ideas generated"
    except Exception as e:
        results["Content Agent"] = f"✗ Error: {str(e)}"
    
    # Test SEO Agent
    try:
        seo = SEOAgent()
        analysis = seo.analyze_title("Test Video Title")
        results["SEO Agent"] = "✓ Working" if analysis else "⚠ No analysis generated"
    except Exception as e:
        results["SEO Agent"] = f"✗ Error: {str(e)}"
    
    # Test Analytics Agent
    try:
        analytics = AnalyticsAgent()
        kpis = analytics.analyze_kpi_progress()
        results["Analytics Agent"] = "✓ Working" if kpis else "⚠ No data available"
    except Exception as e:
        results["Analytics Agent"] = f"✗ Error: {str(e)}"
    
    # Test Engagement Agent
    try:
        engagement = EngagementAgent()
        posts = engagement.generate_community_posts(count=1)
        results["Engagement Agent"] = "✓ Working" if posts else "⚠ No posts generated"
    except Exception as e:
        results["Engagement Agent"] = f"✗ Error: {str(e)}"
    
    # Test Scheduler Agent
    try:
        scheduler = SchedulerAgent()
        schedule = scheduler.generate_monthly_schedule()
        results["Scheduler Agent"] = "✓ Working" if schedule else "⚠ No schedule generated"
    except Exception as e:
        results["Scheduler Agent"] = f"✗ Error: {str(e)}"
    
    return results

def main():
    """Run setup tests."""
    print("\n=== YouTube Channel Growth AI Suite - Setup Test ===\n")
    
    # Check API keys
    print("1. Checking API Keys...")
    missing_keys = test_api_keys()
    if missing_keys:
        print("❌ Missing API keys:")
        for key in missing_keys:
            print(f"   - {key} key not found in .env")
    else:
        print("✅ All required API keys found")
    
    # Test YouTube API connection
    print("\n2. Testing YouTube API Connection...")
    success, message = test_youtube_connection()
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    
    # Test agents
    print("\n3. Testing Agents...")
    agent_results = test_agents()
    for agent, status in agent_results.items():
        status_icon = "✅" if "✓" in status else "❌" if "✗" in status else "⚠️"
        print(f"{status_icon} {agent}: {status}")
    
    # Print setup summary
    print("\n=== Setup Summary ===")
    if not missing_keys and success and all("✓" in status for status in agent_results.values()):
        print("✅ All systems operational!")
        print("\nYou can now run the main workflow:")
        print("python examples/channel_growth_workflow.py")
    else:
        print("⚠️ Some issues were detected")
        print("\nPlease:")
        print("1. Check your API keys in .env")
        print("2. Verify your YouTube channel permissions")
        print("3. Run 'pip install -r requirements.txt' again")
        print("4. Review the troubleshooting section in README.md")

if __name__ == "__main__":
    main() 