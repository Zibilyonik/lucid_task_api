import time

CACHE = {}

def get_cached_posts(user_id):
    if user_id in CACHE and time.time() - CACHE[user_id]["time"] < 300:
        return CACHE[user_id]["posts"]
    return None

def set_cached_posts(user_id, posts):
    CACHE[user_id] = {"posts": posts, "time": time.time()}