from enum import Enum

class SourceTypeEnum(Enum):
    """Types of sources that can be fetched."""
    TIMELINE = 1
    USER_TIMELINE = 2
    LIST_TIMELINE = 3
    SEARCH_TIMELINE = 4