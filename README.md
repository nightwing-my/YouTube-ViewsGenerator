# YouTube Channel Growth AI Suite

An AI-powered suite of tools to optimize and automate your YouTube channel growth. This suite includes specialized agents for content planning, SEO optimization, analytics tracking, engagement management, and scheduling.

## Features

- 📊 **Analytics Agent**: Track KPIs and generate performance reports
- 📝 **Content Agent**: Generate video ideas and content calendars
- 🔍 **SEO Agent**: Optimize titles, descriptions, and tags
- 📅 **Scheduler Agent**: Optimize publishing times based on analytics
- 💬 **Engagement Agent**: Auto-generate community posts and comment replies

## Prerequisites

- Python 3.12 or higher
- A YouTube channel with API access
- OpenAI API key (for content generation)
- RapidAPI key (for trend analysis)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-growth-ai-suite.git
cd youtube-growth-ai-suite
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your API keys:
```env
# YouTube API credentials
YOUTUBE_API_KEY=your_youtube_api_key_here

# OpenAI API credentials (for content generation)
OPENAI_API_KEY=your_openai_api_key_here

# RapidAPI credentials (for trend analysis)
RAPIDAPI_KEY=your_rapidapi_key_here
```

## Getting Your API Keys

1. **YouTube API Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3
   - Create credentials (API key)
   - Add your YouTube channel to the OAuth consent screen

2. **OpenAI API Key**:
   - Visit [OpenAI API](https://platform.openai.com/api-keys)
   - Create an account or log in
   - Generate a new API key

3. **RapidAPI Key**:
   - Visit [RapidAPI](https://rapidapi.com/)
   - Create an account or log in
   - Subscribe to required APIs
   - Copy your API key

## Usage

1. **Quick Start**:
```bash
# Activate virtual environment (if not already activated)
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run the example workflow
python examples/channel_growth_workflow.py
```

2. **Individual Agent Usage**:
```python
from agents import (
    ContentAgent,
    SEOAgent,
    AnalyticsAgent,
    EngagementAgent,
    SchedulerAgent
)

# Analytics
analytics = AnalyticsAgent()
kpi_analysis = analytics.analyze_kpi_progress()
performance_report = analytics.generate_performance_report()

# Content Planning
content = ContentAgent()
video_ideas = content.generate_video_ideas(count=5)
calendar = content.generate_content_calendar(weeks=4)

# SEO Optimization
seo = SEOAgent()
title_analysis = seo.analyze_title("Your Video Title")
tags = seo.generate_tags("Your Video Title", count=10)

# Scheduling
scheduler = SchedulerAgent()
schedule = scheduler.generate_monthly_schedule(posts_per_week=2)

# Engagement
engagement = EngagementAgent()
community_posts = engagement.generate_community_posts(count=2)
replies = engagement.generate_comment_replies(your_comments, "your topic")
```

3. **Video Analysis Tool**:

The suite includes a powerful command-line tool for analyzing individual YouTube videos. You can analyze any video using its URL or ID:

```bash
# Basic usage (analyzes everything)
python examples/analyze_video.py https://www.youtube.com/watch?v=VIDEO_ID

# Or just use the video ID
python examples/analyze_video.py VIDEO_ID
```

**SEO Analysis Options**:
```bash
# Generate more tag suggestions
python examples/analyze_video.py VIDEO_ID --tag-count 20

# Include competitor analysis
python examples/analyze_video.py VIDEO_ID --competitors --competitor-count 10
```

**Engagement Analysis Options**:
```bash
# Generate community posts
python examples/analyze_video.py VIDEO_ID --post-count 5 --post-type question

# Generate video response ideas and comments
python examples/analyze_video.py VIDEO_ID \
    --response-ideas \
    --response-count 5 \
    --comment-suggestions \
    --comment-count 10
```

**Performance Analysis Options**:
```bash
# Get detailed analytics and retention data
python examples/analyze_video.py VIDEO_ID \
    --detailed-analytics \
    --analytics-days 90 \
    --retention
```

**Combining Analyses**:
```bash
# Run specific types of analysis
python examples/analyze_video.py VIDEO_ID -a seo
python examples/analyze_video.py VIDEO_ID -a engagement
python examples/analyze_video.py VIDEO_ID -a performance

# Comprehensive analysis with all features
python examples/analyze_video.py VIDEO_ID \
    --competitors \
    --tag-count 15 \
    --response-ideas \
    --comment-suggestions \
    --detailed-analytics \
    --retention
```

For a complete list of options:
```bash
python examples/analyze_video.py --help
```

## Directory Structure

```
youtube-growth-ai-suite/
├── agents/                 # AI agent modules
│   ├── __init__.py
│   ├── analytics_agent.py
│   ├── base_agent.py
│   ├── content_agent.py
│   ├── engagement_agent.py
│   ├── scheduler_agent.py
│   └── seo_agent.py
├── examples/              # Usage examples
│   └── channel_growth_workflow.py
├── results/              # Generated results and reports
├── tests/               # Test suite
├── .env                # API keys and configuration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Troubleshooting

1. **YouTube API Issues**:
   - Ensure your API key is correct in `.env`
   - Check if you've enabled YouTube Data API v3 in Google Cloud Console
   - Verify your channel has the necessary permissions
   - Check your API quota usage

2. **OpenAI API Issues**:
   - Verify your API key is valid and has sufficient credits
   - Check if you're using a supported model
   - Ensure your requests are properly formatted

3. **Common Errors**:
   - `KeyError: 'original_analysis'`: Make sure to run the full analysis before accessing results
   - `YouTube API client not initialized`: Check your YouTube API key and permissions
   - `No video data available`: Ensure your channel has uploaded videos
   - `ImportError`: Run `pip install -r requirements.txt` again

4. **Performance Issues**:
   - Consider reducing the number of API calls
   - Use caching for frequently accessed data
   - Optimize your requests to stay within API limits

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Open a new issue with:
   - Detailed description of the problem
   - Steps to reproduce
   - Error messages
   - Your environment details 