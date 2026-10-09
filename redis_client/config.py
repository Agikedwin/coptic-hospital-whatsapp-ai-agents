from redis_fastapi import FastAPIRedis, AsyncRedisDep

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
