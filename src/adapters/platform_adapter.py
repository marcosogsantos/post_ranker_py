from abc import ABC, abstractmethod
from typing import List

from enums.source_type_enum import SourceTypeEnum
from value_objects.post_value_object import PostValueObject

class PlatformAdapter(ABC):
    """Base class for platform-specific adapters."""
    
    @abstractmethod
    def get_posts(
        self,
        max_posts: int,
        source_type: SourceTypeEnum,
        source_id: str
    ) -> List[PostValueObject]:
        """
        Fetch posts from a platform source.
        
        Args:
            source_id: The ID of the source
            max_posts: Maximum number of posts to fetch
            source_type: Type of timeline to fetch
            
        Returns:
            List of PostValueObject objects
        """
        pass 