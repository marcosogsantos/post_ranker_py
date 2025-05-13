# Post Ranker

A Python package for fetching and analyzing posts from different social media platforms. Currently supports Twitter, with a flexible architecture that allows for easy addition of more platforms.

## Features

- Fetch posts from supported social media platforms
- Sort posts by engagement metrics (likes, etc.)
- Get top posts based on engagement
- Extensible architecture for adding new platforms
- Support for different source types (e.g., list timelines)
- Uses RapidAPI for Twitter integration, bypassing the restrictive official Twitter API limits

## Installation

```bash
pip install git+https://github.com/marcosogsantos/post_ranker_py.git
```

## Usage

Here's a basic example of how to use the Post Ranker:

```python
from post_ranker import PostRanker, PlatformValueObject, SourceTypeEnum
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Twitter platform
twitter_config = PlatformValueObject(
    name="twitter",
    max_posts=500,
    source_type=SourceTypeEnum.LIST_TIMELINE,
    source_id="your_list_id",
    api_hostname="twitter241.p.rapidapi.com",
    api_key=os.getenv("RAPIDAPI_KEY")
)

# Initialize Post Ranker
post_ranker = PostRanker(twitter_config)

# Get top posts by likes
top_posts = post_ranker.get_top_posts(limit=100)

# Process the results
for post in top_posts:
    print(f"Post URL: {post.url}, Likes: {post.likes}")
```

## Project Structure

```
post_ranker/
├── src/
│   ├── adapters/         # Platform-specific API adapters
│   ├── enums/            # Enumeration classes
│   ├── factories/        # Factory classes for creating adapters
│   ├── value_objects/    # Value objects for configuration
│   └── main.py           # Core functionality
├── setup.py              # Package configuration
└── README.md             # This file
```

## Requirements

- Python 3.10 or higher
- python-dotenv
- Platform-specific API keys (e.g., RapidAPI key or Bearer Token for Twitter)

> **Note:** The official API has become increasingly restrictive, with tighter rate limits and costly access tiers that limit its practicality for many use cases.  RapidAPI, as a marketplace for APIs, allows us to access public Twitter data through various third-party providers, some of which offer free tiers alongside flexible and affordable paid plans.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Marcos Santos (@marcosogs)