import os
import requests
from datetime import datetime
from typing import List, Dict, Any

from .platform_adapter import PlatformAdapter
from enums.source_type_enum import SourceTypeEnum
from value_objects.post_value_object import PostValueObject
from value_objects.platform_value_object import PlatformValueObject

class TwitterRapidAPIAdapter(PlatformAdapter):
    """RapidAPI Twitter241 (Twttr API) implementation of the platform adapter."""
    
    def __init__(self, platform_value_object: PlatformValueObject):
        """
        Initialize the RapidAPI Twitter adapter.
        
        Args:
            platform_value_object: PlatformValueObject containing API key and hostname
        """
        self.platform_value_object = platform_value_object
        self.api_key = platform_value_object.api_key
        self.api_host = platform_value_object.api_hostname
        self.base_url = "https://twitter241.p.rapidapi.com"
        
        if not self.api_key:
            raise ValueError("RapidAPI key not provided")
    
    def _convert_to_post_value_object(self, tweet: Dict[str, Any]) -> PostValueObject:
        """Convert a tweet to a Post object."""
        
        return PostValueObject(
            id=tweet["id_str"],
            content=tweet["full_text"],
            author=tweet["user_id_str"],
            url=f"https://twitter.com/{tweet['user_id_str']}/status/{tweet['id_str']}",
            likes=tweet["favorite_count"],
            created_at=datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y")
        )
    
    def _extract_tweets_from_response(self, response: Dict[str, Any]) -> List[PostValueObject]:
        """Extract tweets from the API response and convert them to Post objects."""
        entries = (
            response.get("result", {})
            .get("timeline", {})
            .get("instructions", [])[0]
            .get("entries", [])
        )

        tweets = []
        for entry in entries:
            content = entry.get("content")
            if not content or "itemContent" not in content:
                continue

            result = content["itemContent"].get("tweet_results", {}).get("result", {})
            if "legacy" not in result:
                continue

            tweet = result["legacy"]
            tweets.append(self._convert_to_post_value_object(tweet))

        return tweets
    
    def get_posts(
        self,
        max_posts: int,
        source_type: SourceTypeEnum,
        source_id: str
    ) -> List[PostValueObject]:
        """
        Fetch tweets from a Twitter source using RapidAPI Twitter241.
        
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
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }

        if source_type != SourceTypeEnum.LIST_TIMELINE:
            raise ValueError("RapidAPI Twitter241 only supports list timeline for now")

        all_tweets = []
        next_cursor = None
        page_count = 0

        while len(all_tweets) < max_posts:
            url = f"{self.base_url}/list-timeline"
            params = {
                "listId": source_id
            }
            if next_cursor:
                params["cursor"] = next_cursor

            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                response_data = response.json()
                
                if "errors" in response_data:
                    error_msg = response_data["errors"][0].get("message", "Unknown API error")
                    raise ValueError(f"RapidAPI Twitter241 error: {error_msg}")
                
                tweets = self._extract_tweets_from_response(response_data)
                all_tweets.extend(tweets)

                # Check if we've reached the desired number of posts
                if len(all_tweets) >= max_posts:
                    all_tweets = all_tweets[:max_posts]
                    break

                # Check if there's a next page
                cursors = response_data.get("cursor", {})
                next_cursor = cursors.get("bottom")  # Use 'bottom' cursor to indicate more pages
                if not next_cursor:
                    break  # No more pages available

                page_count += 1
                        
            except requests.exceptions.RequestException as e:
                raise requests.exceptions.RequestException(f"Failed to fetch tweets: {str(e)}")

        return all_tweets 