import os
from fastapi import APIRouter,HTTPException, Request
from api.application .utils import tools
from api.application import settings
from api.application.utils.logs import get_logger

app = APIRouter()

# 测试api接口
@app.get('/api')
async def api():
    return {'title': 'Hello World'}


# 测试自定义异常处理接口
# @app.get('/exception')
# async def exception(name):
#     """测试异常接口"""
#     try:
#         print(username)
#     except Exception as e:
#         # logger = get_logger(os.environ.get('APP_NAME'))
#         # logger.error(f"发生错误：{e}")
#         raise HTTPException(detail=str(e), status_code=500)  # 预知或担心代码有异常 fastapi建议raise手动抛出异常
#     return {'title': 'Exception'}

@app.get('/sms/{mobile}')
async def sms(request:Request, mobile:str):
    """发送验证码"""
    redis = request.app.state.redis
    # 1.生成指定长度随机验证码[4位纯数字]
    sms_code = tools.genint(settings.SMS['length'])
    # 2.调用redis保存验证码和手机号
    ret = await redis.setex(f'sms_{mobile}', settings.SMS['expire'], sms_code)  # redis.setex 是用来设置一个带有过期时间（TTL）的键值对
    # 3.发送验证码短信

    # 4.返回操作结果
    return {}
