import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Literal, Optional
from datetime import datetime

from adapters.twitter_adapter import TwitterAdapter
from adapters.twitter_rapidapi_adapter import TwitterRapidAPIAdapter
from value_objects.platform_value_object import PlatformValueObject
from enums.source_type_enum import SourceTypeEnum
from factories.platform_adapter_factory import PlatformAdapterFactory

class PostRanker:
    def __init__(
        self,
        platform_value_object: PlatformValueObject
    ):
        """
        Initialize the PostRanker with configuration for a single platform.
        
        Args:
            platform_value_object (PlatformValueObject): Configuration for the platform
        """
        self.platform_value_object = platform_value_object
        self.adapter = PlatformAdapterFactory.create_adapter(platform_value_object)
        
        if self.adapter is None:
            raise ValueError(f"Unsupported platform: {self.platform_value_object.name}")
        
    def fetch_timeline(self) -> List[Dict[str, Any]]:
        """
        Fetch the timeline using the appropriate adapter.
        
        Returns:
            List[Dict[str, Any]]: List of posts from the timeline
        """
        return self.adapter.get_posts(
            max_posts=self.platform_value_object.max_posts,
            source_id=self.platform_value_object.source_id,
            source_type=self.platform_value_object.source_type
        )
    
    def sort_by_likes(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort posts by their like count.
        
        Args:
            posts (List[Dict[str, Any]]): List of posts to sort
            
        Returns:
            List[Dict[str, Any]]: Sorted list of posts
        """
        return sorted(posts, key=lambda x: x.likes, reverse=True)
    
    def get_top_posts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the top posts by likes.
        
        Args:
            limit (int): Number of top posts to return
            
        Returns:
            List[Dict[str, Any]]: List of top posts
        """
        posts = self.fetch_timeline()
        sorted_posts = self.sort_by_likes(posts)
        return sorted_posts[:limit]

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Example usage
    twitter_config = PlatformValueObject(
        name="twitter",
        max_posts=500,
        source_type=SourceTypeEnum.LIST_TIMELINE,
        source_id="1847432246933762439",
        api_hostname="twitter241.p.rapidapi.com",
        api_key=os.getenv("RAPIDAPI_KEY")
    )
    
    post_ranker = PostRanker(twitter_config)
    
    # Get top posts
    top_posts = post_ranker.get_top_posts(100)
        
    print(f"\nFound {len(top_posts)} posts. Top posts by likes:")
    print("-" * 50)
    
    for i, post in enumerate(top_posts, 1):
        print(f"{i}. {post.url} {post.likes} likes")