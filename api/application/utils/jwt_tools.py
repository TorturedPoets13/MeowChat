import uuid
from jose import jwt
from datetime import datetime, timedelta
from api.application import settings
from typing import Optional


class JWTTools(object):
    """JWT工具类"""
    # 异常类
    JWTError = jwt.JWTError
    ExpiredSignatureError = jwt.ExpiredSignatureError

    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """
        生成JWT token
        :param data: 需要进行JWT加密的用户信息（解密时也会用到）
        :param expires_delta: token有效期，单位:秒
        :return: jwt
        """
        now_time = datetime.utcnow()
        if expires_delta:
            expire = now_time + timedelta(seconds=expires_delta)
        else:
            expire = now_time + timedelta(seconds=settings.JWT['expire_time'])

        # 组装载荷数据的标准声明
        payload = {
            'exp': expire,  # 过期时间
            'iat': now_time,  # 生成时间
            'nbf': now_time,  # 启用时间
            'jti': str(uuid.uuid4())  # 唯一标记
        }
        # 组装载荷数据的公共声明
        payload.update(data)
        # 自动生成jwt
        return jwt.encode(payload, settings.JWT['secret_key'], algorithm=settings.JWT['algorithm'])

    def verify_token(self, token: str):
        """
        验证token,可以添加功能：验证是否在有效expires_delta
        :param token: 客户端发过来的token
        :return: 以字典格式返回用户信息
        """
        payload = jwt.decode(token, settings.JWT['secret_key'], algorithms=[settings.JWT['algorithm']])
        return payload


JWTToken = JWTTools()
