import json
from redis.asyncio import Redis

redis_client = Redis(host="localhost",
                     port=6379,
                     decode_responses=True)

async def log_playlist(source_url:str,spotify_url:str):
    payload = {
        "type":"playlist_log",
        "source_url":source_url,
        "spotify_url":spotify_url
    }
    await redis_client.lpush("log_queue",json.dumps(payload))
