from dataclasses import dataclass
from typing import Literal, Optional

from enums.source_type_enum import SourceTypeEnum


@dataclass
class PlatformValueObject:
    """Configuration for a social media platform.
    
    Attributes:
        name: The name of the social media platform
        source_type: The type of timeline to fetch
        source_id: Unique identifier for the platform source
        api_key: API key for authentication
        api_hostname: Optional hostname for API requests
        max_posts: Maximum number of posts to fetch (default: 100)
    """
    name: str
    source_type: SourceTypeEnum
    source_id: str
    api_key: str
    api_hostname: Optional[Literal["api.twitter.com", "twitter241.p.rapidapi.com"]] = None
    max_posts: int = 100 