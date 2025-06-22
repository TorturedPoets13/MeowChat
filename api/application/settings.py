import os

"""tortoise-orm数据库配置"""
TORTOISE_ORM = {
    "connections": {
        "default": {
            'engine': 'tortoise.backends.mysql',  # MySQL or Mariadb
            'credentials': {  # 连接参数
                'host': os.environ.get('DB_HOST', '127.0.0.1'),  # 数据库IP/域名地址
                'port': int(os.environ.get('DB_PORT', 3306)),  # 端口
                'user': os.environ.get('DB_USER', 'root'),  # 连接账户
                'password': os.environ.get('DB_PASSWORD', '123'),  # 连接密码
                'database': os.environ.get('DB_DATABASE', 'meowchat'),  # 数据库
                'charset': os.environ.get('DB_CHARSET', 'utf8mb4'),  # 编码
                'minsize': int(os.environ.get('DB_POOL_MINSIZE', 1)),  # 连接池中的最小连接数
                'maxsize': int(os.environ.get('DB_POOL_MAXSIZE', 5)),  # 连接池中的最大连接数
                "echo": bool(os.environ.get('DEBUG', True))  # 执行数据库操作时，是否打印SQL语句
            }
        }
    },
    'apps': {  # 默认所在的应用目录
        'models': {  # 数据模型的分组名
            'models': ['api.application.apps.users.models', 'aerich.models'],
            # 模型所在目录文件的导包路径[字符串格式],'aerich.models'使用aerich模块进行数据迁移
            '''
            pip install aerich
            cd api/
            aerich init -t application.settings.TORTOISE_ORM
            aerich init-db
            '''
            'default_connection': 'default',  # 上一行配置中的模型列表的默认连接配置
        }
    },
    # 时区设置
    # 当use_tz=True，当前tortoise-orm会默认使用当前程序所在操作系统的时区，
    # 当use_tz=False时，当前tortoise-orm会默认使用timezone配置项中的时区
    'use_tz': False,
    'timezone': os.environ.get('APP_TIMEZONE', 'Asia/Shanghai')
}


# 短信验证码相关配置
"""
 os.environ.get() 的返回值永远是字符串（即使默认值是整数）
 返回的也是 字符串 '4'，不是整数 4。

所以最终 settings.SMS['length'] 是 '4'（str），就会导致 Pydantic 报：

TypeError: 'str' object cannot be interpreted as an integer
"""
SMS = {
    'length': int(os.environ.get('SMS_CODE_LENGTH', 4))
}


# 微信openid相关配置
WECHAT = {
    'app_id': os.environ.get('WECHAT_APP_ID', ''),
    'app_secret': os.environ.get('WECHAT_APP_SECRET', ''),
}
