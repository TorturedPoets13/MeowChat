import os
from fastapi import APIRouter,HTTPException
from api.application.utils.logs import get_logger

app = APIRouter()

# 测试api接口
@app.get('/api')
async def api():
    return {'title': 'Hello World'}


# 测试自定义异常处理接口
@app.get('/exception')
async def exception(name):
    """测试异常接口"""
    try:
        print(username)
    except Exception as e:
        # logger = get_logger(os.environ.get('APP_NAME'))
        # logger.error(f"发生错误：{e}")
        raise HTTPException(detail=str(e), status_code=500)  # 预知或担心代码有异常 fastapi建议raise手动抛出异常
    return {'title': 'Exception'}
