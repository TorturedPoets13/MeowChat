import logging, os
from logging import handlers, Logger


def get_logger(name='root'):
    """
    获取日志器对象
    :param name: 日期器名字，默认为root
    :return: 日志器对象
    """
    # 1、创建一个logger日志器对象
    logger = logging.getLogger(name)
    # 2、设置logger的日志等级
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        # 3、创建合适的Handler（FIleHandler要有保存路径）
        th = logging.StreamHandler()    # 终端输出的日志处理器

        try:
            os.makedirs("logs", exist_ok=True)
        except OSError as e:
            print(f"日志文件创建失败: {e}")
        rf = handlers.RotatingFileHandler(  # 按大小滚动保存日志到文件的处理器
            filename=f"logs/{name}.log",  # 日志文件名，日志目录log需要手动创建
            mode='a',  # a=append 追加写入
            maxBytes=300 * 1024 * 1024,  # 单个日志文件大小的最大值300M
            backupCount=10,  # 备份日志文件的数量，所有日志数量 = backupCount+filename
            encoding='utf-8'  # 日志文件内容的编码
        )

        # 4、设置每个Handler的日志等级【Handler的日志等级会覆盖上面logger的日志的等级】
        th.setLevel(logging.DEBUG)
        rf.setLevel(logging.INFO)

        # 5、创建日志格式器对象
        simple_formatter = logging.Formatter(   # 简单的日志格式，终端输出用
            fmt="{levelname} {asctime} {pathname}:{lineno} {message}",
            style="{"
        )
        verbose_formatter: logging.Formatter = logging.Formatter(  # 正常日志格式，写入日志文件用
            fmt="【{name}】{levelname} {asctime} {pathname}:{lineno} {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{"
        )

        # 6、将不同日志器与格式绑定
        th.setFormatter(simple_formatter)
        rf.setFormatter(verbose_formatter)

        # 7、通过调用logger同时记录两份日志 一份记录到终端(th) 一份记录到日志文件(rf)
        logger.addHandler(th)
        logger.addHandler(rf)
    return logger

# ----- 以下为测试log处理器是否生效代码 -----

# if __name__ == '__main__':
#     # 8. 调用日志器对象logger打印输出日志
#     logger = get_logger('dl')
#     logger.info("这里是常规运行日志")
#     logger.debug("开发人员在调试程序时自己手动打印的日志")
#     logger.warning("这里是程序遇到未来会废弃的函数/方法时，输出的警告日志")
#     logger.error("这里是程序发生错误时输出的日志")
#     logger.critical("这是致命级别的日志，需要紧急修复的")
#
#     # 多次调用实例化出来的日志对象，如果name相同，则得到的是同一个日志器对象（单例模式）
#     logger1 = get_logger('dl')
#     print(id(logger1), id(logger))
