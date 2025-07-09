import os
from fastapi import APIRouter, HTTPException, status, Request
from api.application.apps.users import models, schemas
from api.application.utils import wx_tools
from api.application.utils.jwt_tools import JWTToken
from api.application.utils.logs import get_logger

app = APIRouter()


@app.get('/login')
async def api():
    return {'title': '测试login'}


@app.post('/register', response_model=schemas.UserRegisterResponse)
async def register(request: Request, user_info: schemas.UserRegisterRequest):
    """处理用户注册请求"""
    # 1.验证用户账号是否重复注册【mobile】
    # 查询手机号存在则抛出异常，异步中涉及io操作就要await
    user_mobile = await models.User.filter(mobile=user_info.mobile).first()
    if user_mobile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='当前手机号已注册！')
    # 判断验证码是否正确
    redis = request.app.state.redis
    redis_sms = await redis.get(f'sms_{user_info.mobile}')
    if redis_sms is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='验证码已过期')
    if redis_sms != user_info.sms_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='验证码不正确')

    # 2.通过小程序提交的code授权码到微信官方获取当前微信用户的openid和session_key
    wx_user = wx_tools.get_wx_info(user_info.code)

    # 再次验证当前用户的微信openid是否重复注册
    user_openid = await models.User.filter(openid=wx_user['openid']).first()
    if user_openid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='当前微信已绑定其他账号，不能重复注册')

    # 3.进行用户注册，将用户数据写入数据库
    """
    当你使用 **dict1, key=value 的形式时，后面的关键字参数会覆盖前面字典中同名的 key。
    即：username=user_info.mobile 会覆盖 dict(user_info) 中的 'username'(如果有)，只会生效一次。
    """
    user = await models.User.create(
        **dict(user_info),  # 打散字典，username="alice", password="123456", email="alice@example.com"
        username=user_info.mobile,
        avatar=user_info.avatarUrl,
        nickname=user_info.nickName,
        sex=user_info.gender,
        openid=wx_user['openid']
    )

    """
    user = await models.User.create(...)
    这一步执行后，Tortoise ORM 会自动返回带有主键和字段数据的 User 实例对象，就像你从数据库查出的一样。
    所以可以user.访问这些字段
    """
    # 注册后删除redis中保存的验证码，防止一码多用
    await redis.delete(f'sms_{user_info.mobile}')

    # 4. 注册成功后返回的数据包，按照schemas/UserRegisterResponse的数据结构返回响应
    return {
        'id': user.id,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'code': status.HTTP_200_OK,
        'err_msg': '用户注册成功',
        'status': 'Success',
        'token': JWTToken.create_token({
            'id': user.id
        }),  # Jwt token生成
    }
