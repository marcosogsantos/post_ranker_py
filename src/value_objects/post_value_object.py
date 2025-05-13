from dataclasses import dataclass
from datetime import datetime

@dataclass
class PostValueObject:
    """
    Value object representing a post from a social media platform.
    
    Attributes:
        id (str): Unique identifier of the post
        content (str): The text content of the post
        author (str): Username or identifier of the post author
        url (str): URL to access the post
        likes (int): Number of likes/reactions on the post
        created_at (datetime): Timestamp when the post was created
    """
    id: str
    content: str
    author: str
    url: str
    likes: int
    created_at: datetime 