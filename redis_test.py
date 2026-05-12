import asyncio
from redis.asyncio import Redis

async def main():
    r = await Redis.from_url("redis://localhost:6379", decode_responses=True)
    
    # ❌ 错误：没有 await
    result_no_await = r.get("test_key")
    print(f"没有 await: {result_no_await}")
    print(f"类型: {type(result_no_await)}")
    
    # ✅ 正确：有 await
    await r.set("test_key", "hello_world")
    result_with_await = await r.get("test_key")
    print(f"\n有 await: {result_with_await}")
    print(f"类型: {type(result_with_await)}")
    
    await r.close()

if __name__ == "__main__":
    asyncio.run(main())