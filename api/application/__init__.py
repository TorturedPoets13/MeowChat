import os
from fastapi import FastAPI
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise
from api.application.utils import middleware, exceptions
from api.application.apps.common.views import app as common_app
from api.application.apps.users.views import app as users_app

from api.application import settings


def create_app():
    """工厂函数：创建app对象"""
    # 读取环境配置文件的信息，加载到环境变量
    load_dotenv()

    app = FastAPI(
        # fastapi的一些基础信息 app名字 摘要 版本等等
        title=os.environ.get('APP_NAME'),
        summary=os.environ.get('APP_SUMMARY'),
        description=os.environ.get('APP_DESCRIPTION'),
        version=os.environ.get('APP_VERSION'),
        # 注册自定义全局异常处理
        exception_handlers={
            # 或者用app.add_exception_handler()方法注册
            exceptions.HTTPException: exceptions.global_http_exception_handler,
            exceptions.RequestValidationError: exceptions.global_request_exception_handler,

        }
    )
    # 在实例化app对象中添加了异常处理此处就不用了
    # app.add_exception_handler(HTTPException, global_http_exception_handler)
    # app.add_exception_handler(RequestValidationError, global_request_exception_handler)

    # # 测试是否已经读到环境变量
    # import os
    # print(os.environ.get('APP_TIMEZONE')) # Asia/Shanghai

    # 把Tortoise-orm注册到App应用对象中
    register_tortoise(
        app,
        config=settings.TORTOISE_ORM,
        # 数据迁移可用aerich代替
        generate_schemas=False,  # 是否自动生成表结构[自动根据配置项中apps.models的路径自动识别模型],每次都会创建表，存在则报错，一般不用
        add_exception_handlers=True,  # 是否启用自动异常处理
    )
    # 注册各个应用分组下的路由信息，合并到App应用对象中
    app.include_router(common_app, prefix='')
    app.include_router(users_app, prefix='/users')  # prefix url路径添加前缀

    # 注册中间件函数
    # 该写法其实是 @app.middleware('http') 装饰器的底层用法。
    # 也可以用用 app.add_middleware 结合自定义中间件类 进行注册
    http_middleware = app.middleware('http')
    http_middleware(middleware.log_middleware)

    return app
