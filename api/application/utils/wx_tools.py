import requests
from api.application import settings


def get_wx_info(code):
    """
    获取微信用户信息code openid等
    官方文档：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
    :param code: 小程序端用户的授权码
    :return:响应json格式数据包
    """
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={settings.WECHAT['app_id']}&secret={settings.WECHAT['app_secret']}&js_code={code}&grant_type=authorization_code"
    response = requests.get(url)
    return response.json()
