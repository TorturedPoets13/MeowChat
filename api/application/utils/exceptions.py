import os
from fastapi import Request
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.application.utils.logs import get_logger

# 使用日志记录一下异常
logger = get_logger(os.environ.get('APP_NAME'))


# http异常处理
def global_http_exception_handler(request: Request, exc: HTTPException):
    """
    全局http请求异常
    :param request: HTTP 请求对象
    :param exc:  本次发生的异常对象
    :return:
    """
    logger.error(f'发生异常：{exc.detail}')

    return JSONResponse({
        'code': exc.status_code,
        'err_msg': exc.detail,
        'status': 'Http Failed'
    })


# 校验url格式参数异常
def global_request_exception_handler(request: Request, exc: RequestValidationError):
    """
    全局请求校验异常处理函数
    :param request:
    :param exc:
    :return:
    """

    return JSONResponse({
        'code': status.HTTP_400_BAD_REQUEST,
        'err_msg': exc.errors()[0],
        'status': 'Validate Failed'
    })
