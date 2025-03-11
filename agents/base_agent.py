"""
Base Agent
---------
Base class for all AI agents in the YouTube Channel Growth AI Suite.
"""

import os
import json
import logging
from datetime import datetime

class BaseAgent:
    """Base class for all agents."""
    
    def __init__(self, name):
        """Initialize the base agent.
        
        Args:
            name (str): Name of the agent
        """
        self.name = name
        
        # Set up directories
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_dir = os.path.join(self.base_dir, "config")
        self.results_dir = os.path.join(self.base_dir, "results")
        self.log_dir = os.path.join(self.base_dir, "logs")
        
        # Create directories if they don't exist
        for directory in [self.config_dir, self.results_dir, self.log_dir]:
            os.makedirs(directory, exist_ok=True)
            
        # Set up logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Set up logging configuration."""
        log_file = os.path.join(self.log_dir, f"{self.name.lower()}.log")
        
        # Create logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        
        # Create handlers
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()
        
        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add formatters to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def load_config(self):
        """Load agent configuration from file."""
        config_file = os.path.join(self.config_dir, f"{self.name.lower()}_config.json")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                self.logger.error(f"Error loading config: {str(e)}")
                return {}
        else:
            return {}
            
    def save_config(self, config):
        """Save agent configuration to file.
        
        Args:
            config (dict): Configuration to save
        """
        config_file = os.path.join(self.config_dir, f"{self.name.lower()}_config.json")
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            self.logger.info(f"Configuration saved to {config_file}")
        except Exception as e:
            self.logger.error(f"Error saving config: {str(e)}")
            
    def save_results(self, results, file_path=None):
        """Save agent results to file.
        
        Args:
            results (dict): Results to save
            file_path (str, optional): Custom file path for results
        """
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"test_agent_{timestamp}.json" if self.name == "TestAgent" else f"{self.name.lower()}_{timestamp}.json"
            file_path = os.path.join(self.results_dir, file_name)
            
        try:
            with open(file_path, 'w') as f:
                json.dump(results, f, indent=2)
            self.logger.info(f"Results saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
            
    def run(self):
        """Run the agent. To be implemented by child classes."""
        raise NotImplementedError("Subclasses must implement run()") 