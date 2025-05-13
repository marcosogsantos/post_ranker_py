import http.client
import os
import requests
from datetime import datetime
from typing import List, Dict, Any

from .platform_adapter import PlatformAdapter
from enums.source_type_enum import SourceTypeEnum    
from value_objects.post_value_object import PostValueObject
from value_objects.platform_value_object import PlatformValueObject

class TwitterAdapter(PlatformAdapter):
    """Twitter-specific implementation of the platform adapter."""
    
    def __init__(self, platform_value_object: PlatformValueObject):
        """
        Initialize the Twitter adapter.
        
        Args:
            platform_value_object: PlatformValueObject containing API key and hostname
        """
        self.platform_value_object = platform_value_object
        self.api_key = platform_value_object.api_key
        self.api_host = platform_value_object.api_hostname
        
        if not self.api_key or not self.api_host:
            raise ValueError("Twitter API key or hostname not provided")
    
    def _convert_to_platform_post(self, tweet: Dict[str, Any]) -> PostValueObject:
        """Convert a tweet to a Post object."""
        return PostValueObject(
            id=str(tweet.id),
            content=tweet.text,
            author=tweet.user.screen_name,
            url=f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}",
            likes=tweet.favorite_count,
            created_at=tweet.created_at
        )
    
    def get_posts(
        self,
        max_posts: int,
        source_type: SourceTypeEnum,
        source_id: str
    ) -> List[PostValueObject]:
        """
        Fetch tweets from a Twitter source (list, user profile, or user timeline).
        
        Args:
            source_id: The ID of the source (list ID or user ID)
            max_posts: Maximum number of tweets to fetch in total
            source_type: Type of timeline to fetch (default: LIST)
            
        Returns:
            List of Post objects from the specified source
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If the response contains an error
        """
        url = f"https://api.twitter.com/2/lists/{source_id}/tweets"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        params = {
            "max_results": max_posts,
            "tweet.fields": "created_at,public_metrics"
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            data = response.json()
            
            # Check for Twitter API errors
            if "errors" in data:
                error_msg = data["errors"][0].get("detail", "Unknown Twitter API error")
                raise ValueError(f"Twitter API error: {error_msg}")
            
            return [self._convert_to_plataform_post(tweet) for tweet in data["data"]]
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to fetch tweets: {str(e)}") 