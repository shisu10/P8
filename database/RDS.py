# -*- coding:utf-8 -*-
"""
@Time : 2022/4/25 2:09 PM
@Author: binkuolo
@Des: redis
"""

# database/redis.py
import os
from redis.asyncio import Redis, ConnectionPool

async def sys_cache() -> Redis:
    """
    系统缓存
    :return: cache 连接池
    """
    pool = ConnectionPool.from_url(
        f"redis://{os.getenv('CACHE_HOST', '127.0.0.1')}:{os.getenv('CACHE_PORT', 6379)}",
        db=int(os.getenv('CACHE_DB', 0)),
        decode_responses=True
    )
    return Redis(connection_pool=pool)
