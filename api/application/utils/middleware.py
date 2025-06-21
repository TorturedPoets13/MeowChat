import os
import time
from api.application.utils.logs import get_logger


async def log_middleware(request, call_next):
    """
    日志中间件
    :param request:HTTP请求对象
    :param call_next: 下一步调用的中间/ 没有下一步中间件就是 视图函数
    :return:
    """
    # 记录接口的运行时间
    logger = get_logger(os.environ.get('APP_NAME'))  # logger单例模式 而且APP_NAME唯一 所以每次创建的日志对象都是同一个日志对象
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # 记录毫秒
    formatted_time = '{:.2f}'.format(process_time)  # 运行时间保留两位小数
    # 通过logger的INFO级别记录运行时间日志
    logger.info(f'path={request.url.path} timer={formatted_time}ms status_code={response.status_code}')
    return response
