from setuptools import setup, find_packages

setup(
    name="youtube_growth_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.0",
        "colorama>=0.4.6",
        "requests>=2.31.0",
        "numpy>=1.26.0",
        "pandas>=2.0.0",
        "matplotlib>=3.8.0",
        "google-api-python-client>=2.97.0",
        "google-auth>=2.22.0",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=1.0.0",
        "openai>=1.3.0",
        "nltk>=3.8.1",
        "tqdm>=4.66.1",
        "pyyaml>=6.0.1"
    ],
    python_requires=">=3.12",
) 