from typing import Optional

from adapters.twitter_adapter import TwitterAdapter
from adapters.twitter_rapidapi_adapter import TwitterRapidAPIAdapter
from value_objects.platform_value_object import PlatformValueObject

class PlatformAdapterFactory:
    @staticmethod
    def create_adapter(platform_value_object: PlatformValueObject) -> Optional[TwitterAdapter | TwitterRapidAPIAdapter]:
        """
        Factory method to create the appropriate adapter based on platform configuration.

        Args:
            platform_value_object (PlatformValueObject): Configuration for the platform

        Returns:
            Optional[TwitterAdapter | TwitterRapidAPIAdapter]: The appropriate adapter instance or None if platform is not supported
        """
        platform = platform_value_object.name.lower()
        
        if platform == "twitter":
            if platform_value_object.api_hostname == "twitter241.p.rapidapi.com":
                return TwitterRapidAPIAdapter(platform_value_object)
            return TwitterAdapter(platform_value_object)
            
        # Add other platform adapters here
        # elif platform == "facebook":
        #     return FacebookAdapter()
        # elif platform == "linkedin":
        #     return LinkedInAdapter()
            
        return None 