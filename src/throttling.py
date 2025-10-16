import json
import time
import os
from collections import deque

class Throttler:
    """
    A smart throttler to manage API call rates for different platforms.
    """
    def __init__(self, config_path="src/social/rate_limits.json"):
        self.limits = self._load_limits(config_path)
        self.call_logs = {platform: deque() for platform in self.limits}

    def _load_limits(self, config_path):
        """Loads rate limit configurations from a JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Rate limit config file not found at {config_path}. Throttling will be disabled.")
            return {}

    def wait_if_needed(self, platform: str):
        """
        Checks if a call can be made for the given platform. If not, it
        sleeps until the rate limit window allows for a new call.
        """
        if platform not in self.limits:
            return # No limits for this platform

        limit = self.limits[platform]["requests"]
        window = self.limits[platform]["window_seconds"]
        log = self.call_logs[platform]

        # Remove timestamps older than the window
        current_time = time.time()
        while log and log[0] <= current_time - window:
            log.popleft()

        # If we have reached the limit, we need to wait
        if len(log) >= limit:
            time_to_wait = log[0] - (current_time - window)
            if time_to_wait > 0:
                print(f"Rate limit for {platform} reached. Waiting for {time_to_wait:.2f} seconds.")
                time.sleep(time_to_wait)
            # After waiting, remove the oldest timestamp
            log.popleft()

        # Log the new call
        self.call_logs[platform].append(time.time())
        print(f"Call allowed for {platform}. Current count in window: {len(log)}/{limit}")

# Global throttler instance to be used across the application
throttler = Throttler()