from redis import Redis
from redis.commands.core import Script


# A Lua script to update counters and calculate a running average
# of how much time has elapsed per message.
lua_script = """
    local current_sum = redis.call('GET', KEYS[1])
    local current_count = redis.call('GET', KEYS[2])
    local current_failed = redis.call('GET', KEYS[4])

    if not current_sum or not current_count then
        current_sum = 0
        current_count = 0
    else
        current_sum = tonumber(current_sum)
        current_count = tonumber(current_count)
    end
    
    if not current_failed then
        current_failed = 0
    else
        current_failed = tonumber(current_failed)
    end

    local new_sum = current_sum + tonumber(ARGV[1])
    local new_count = current_count + 1
    local new_average = new_sum / new_count
    local new_failed = current_failed + tonumber(ARGV[2])

    redis.call('SET', KEYS[1], new_sum)
    redis.call('SET', KEYS[2], new_count)
    redis.call('SET', KEYS[3], new_average)
    redis.call('SET', KEYS[4], new_failed)
    
    return new_average
"""

# Caching the Redis connection and the Script instance... maybe premature optimization
_redis_conn: Redis | None = None
_lua_script: Script | None = None


def connect() -> Redis:
    """Reuse the Redis connection pool if it's available"""
    global _redis_conn
    if _redis_conn is None:
        _redis_conn = Redis(host="localhost", port=6379, db=0)
    return _redis_conn


def script(redis_conn: Redis) -> Script:
    """Reuse the Script object if it's available to avoid recalculating
    the SHA1 on every call. Maybe a premature optimization.
    """
    global _lua_script
    if _lua_script is None:
        _lua_script = redis_conn.register_script(lua_script)
    return _lua_script


def update_counts(redis_conn: Redis, time_to_complete: float, failed: bool) -> float:
    """Update counters on Redis. Returns the updated average."""
    keys = ("messages:sum", "messages:count", "messages:average", "failed")
    args = (time_to_complete, int(failed))
    return float(script(redis_conn)(keys, args, redis_conn) or 0)


def reset_counts(redis_conn: Redis) -> None:
    """Reset counters on Redis"""
    redis_conn.set("messages:sum", 0)
    redis_conn.set("messages:count", 0)
    redis_conn.set("messages:average", 0)
    redis_conn.set("failed", 0)


def read_counts(redis_conn: Redis) -> dict:
    """Read counters from Redis"""
    average = round(float(redis_conn.get("messages:average") or 0), 4)
    return {
        "count": int(redis_conn.get("messages:count") or 0),
        "failed": int(redis_conn.get("failed") or 0),
        "average_time": average,
    }
