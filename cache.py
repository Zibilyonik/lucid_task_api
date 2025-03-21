"""
In-memory caching functionality.

This module implements a simple caching system for posts
that expires after 5 minutes to improve API performance.
"""

import time

# In-memory cache
CACHE = {}


def get_cached_posts(user_id):
    """
    Get cached posts for a user if available and not expired

    Args:
        user_id: User ID to get cached posts for

    Returns:
        list: Cached posts or None if not in cache or expired
    """
    if user_id in CACHE and time.time() - CACHE[user_id]["time"] < 300:  # 5 minutes
        return CACHE[user_id]["posts"]
    return None


def set_cached_posts(user_id, posts):
    """
    Cache posts for a user

    Args:
        user_id: User ID to cache posts for
        posts: List of posts to cache
    """
    CACHE[user_id] = {"posts": posts, "time": time.time()}
