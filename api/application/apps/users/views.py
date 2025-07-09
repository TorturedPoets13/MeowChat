import os
from fastapi import APIRouter, HTTPException, status, Request
from api.application.apps.users import models, schemas
from api.application.utils import wx_tools, tools
from api.application.utils.jwt_tools import JWTToken
from tortoise.expressions import Q
from datetime import datetime, timedelta
from api.application import settings
from api.application.utils.logs import get_logger

app = APIRouter()


@app.post('/login', response_model=schemas.UserRegisterResponse)
async def login(request: Request, user_info: schemas.UserLoginRequest):
    """用户登录操作"""
    # 0.判断验证码是否正确
    redis = request.app.state.redis
    sms_code = await redis.get(f"sms_{user_info.mobile}")

    if not sms_code:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='验证码不存在或填写错误')
    if sms_code != user_info.sms_code:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='验证码不存在或填写错误')
    # 判断当前用户是否存在
    # 1.基于code请求微信服务器获取用户的openid以及将来调用用户信息的session_key
    result = wx_tools.get_wx_info(user_info.code)
    # 2.根据手机号或微信openid判断是否重复注册
    # select * from User where mobile=xxx or openid=xxx
    user = await models.User.filter(Q(mobile=user_info.mobile) | Q(openid=result['openid'])).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='当前账号错误')
    # 3.判断密码是否正确
    hashing = tools.Hashing()
    ret = hashing.verify(user_info.password, user.password)
    if not ret:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='当前账号或密码错误！')
    # 生成token
    token = JWTToken.create_token({
        'id': user.id,
        # 'username': user.username
    })
    # 记录用户登录历史
    await models.UserLoginHistory.create(user=user)
    # 将token保存到redis中
    await redis.setex(f'token_{user.id}', settings.JWT['expire_time'], token)
    # 如果打开限流功能，则初始化用户每天免费使用AI助理的次数到redis中，次日过期
    if settings.AI_ROBOT['limit'] == 1:
        current_time = datetime.now()
        tomorrow_time = current_time + timedelta(days=1)
        tomorrow_zero = datetime.strptime(f'{tomorrow_time.year}-{tomorrow_time.month}-{tomorrow_time.day}', '%Y-%m-%d')
        delta = tomorrow_zero - current_time
        redis.setex(f'api_{user.id}', delta.seconds, settings.AI_ROBOT['count'])

    # 删除短信验证码，防止一码多用
    await redis.delete(f'sms_{user_info.mobile}')
    return {
        'id': user.id,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'code': 200,
        'err_msg': '用户登录成功',
        'status': 'SUCCESS',
        'token': token,
    }


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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='验证码不正确')

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
