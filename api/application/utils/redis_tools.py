from redis import asyncio as aioredis
from fastapi import FastAPI


def register_redis(app, config):
    """
    注册Redis连接对象到App应用对象中
    :param app: App应用对象
    :param config: redis配置信息
    :return:
    """

    async def redis_pool():
        # 一般redis同步时的写法时from redis import Redis
        # Redis.fromurl(...)实际都是一样的 只是把它换成了asyncio
        # redis = await aioredis.from_url(f"redis://账号:密码@IP:端口/数据库ID", decode_responses=True) # decode_responses=True 设置redis返回的字符串格式从bytes自动转换成普通字符串
        redis = await aioredis.from_url(
            f"redis://{config.get('username')}:{config.get('password')}@{config.get('host')}:{config.get('port')}/{config.get('db')}",
            decode_responses=True)
        return redis

    @app.on_event("startup")    # startup事件：当App应用对象启动时，自动执行这里
    async def startup_event():
        app.state.redis = await redis_pool()
