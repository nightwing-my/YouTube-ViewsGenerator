"""
YouTube Channel Growth AI Suite
-------------------------------
A collection of AI agents to help optimize and grow your YouTube channel.
"""

import os
import argparse
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Import agents
from agents.content_agent import ContentAgent
from agents.seo_agent import SEOAgent
from agents.analytics_agent import AnalyticsAgent
from agents.engagement_agent import EngagementAgent
from agents.scheduler_agent import SchedulerAgent

# Initialize colorama for cross-platform colored terminal output
init()

def print_header():
    """Print a stylized header for the application."""
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.YELLOW}YouTube Channel Growth AI Suite - Alt Tech Tok")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

def main():
    """Main entry point for the YouTube AI Suite."""
    # Load environment variables
    load_dotenv()
    
    # Check for API keys
    if not os.getenv("YOUTUBE_API_KEY"):
        print(f"{Fore.RED}Error: YouTube API key not found. Please add it to your .env file.{Style.RESET_ALL}")
        print("Create a .env file with: YOUTUBE_API_KEY=your_api_key_here")
        return
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="YouTube Channel Growth AI Suite")
    parser.add_argument("--agent", choices=["content", "seo", "analytics", "engagement", "scheduler", "all"], 
                        default="all", help="Specify which agent to run")
    args = parser.parse_args()
    
    print_header()
    
    # Initialize agents
    content_agent = ContentAgent()
    seo_agent = SEOAgent()
    analytics_agent = AnalyticsAgent()
    engagement_agent = EngagementAgent()
    scheduler_agent = SchedulerAgent()
    
    # Run the specified agent or all agents
    if args.agent == "all" or args.agent == "content":
        print(f"{Fore.GREEN}Running Content Agent...{Style.RESET_ALL}")
        content_agent.run()
        
    if args.agent == "all" or args.agent == "seo":
        print(f"{Fore.GREEN}Running SEO Agent...{Style.RESET_ALL}")
        seo_agent.run()
        
    if args.agent == "all" or args.agent == "analytics":
        print(f"{Fore.GREEN}Running Analytics Agent...{Style.RESET_ALL}")
        analytics_agent.run()
        
    if args.agent == "all" or args.agent == "engagement":
        print(f"{Fore.GREEN}Running Engagement Agent...{Style.RESET_ALL}")
        engagement_agent.run()
        
    if args.agent == "all" or args.agent == "scheduler":
        print(f"{Fore.GREEN}Running Scheduler Agent...{Style.RESET_ALL}")
        scheduler_agent.run()
    
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.GREEN}All tasks completed successfully!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main() 