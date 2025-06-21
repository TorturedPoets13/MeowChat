from tortoise import models, fields


class User(models.Model):
    id = fields.IntField(pk=True, description="主键")
    username = fields.CharField(max_length=255, unique=True, description="用户名")
    nickname = fields.CharField(max_length=255, index=True, description="昵称")
    password = fields.CharField(max_length=255, description='密码')
    openid = fields.CharField(max_length=255, unique=True, description='OpenID')  # 本平台id判断平台用户和微信用户是否同一人
    mobile = fields.CharField(max_length=15, index=True, description='手机')
    avatar = fields.CharField(max_length=500, null=True, description='头像')
    country = fields.CharField(max_length=255, null=True, description='国家')
    province = fields.CharField(max_length=255, null=True, description='省份')
    city = fields.CharField(max_length=255, null=True, description='城市')
    sex = fields.BooleanField(default=True, null=True, description='性别')
    created_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    updated_time = fields.DatetimeField(auto_now=True, description="更新时间")
    deleted_time = fields.DatetimeField(null=True, description="删除时间")

    # 元数据
    class Meta:
        table = "user_info"
        description = "用户信息"

    def __repr__(self):
        """__repr__终端打印"""
        return f"User (id={self.id}, username={self.username})"

    __str__ = __repr__  # __str__ pycharm打印， 这个写法就相当于复制了一份__repr__函数中一样的代码函数名改成了__str__
