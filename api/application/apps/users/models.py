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


class UserLoginHistory(models.Model):
    """
    用于记录会话
    每个用户每天每次登录能获取几次的免费调用AI次数
    """
    id = fields.IntField(pk=True, description='主键')
    # db_constraint=False 开启逻辑外键/虚拟外键，不使用数据库本身提供的物理外键，大表都强烈建议使用逻辑外键
    # on_delete=fields.OnDelete.NO_ACTION 设置外键的级联操作，NO_ACTION表示删除主键是不进行任何操作，CASCADE表示删除主键时同时删除对应的外键，RESTRICT表示删除外键前必须先删除所有对应的外键，SET_NULL表示删除主键时，把对应外键的值全部改成NULL，SET_DEFAULT表示删除主键时，把对应外键的值全部改成默认值
    user = fields.ForeignKeyField('models.User', related_name='login_history_list', on_delete=fields.OnDelete.CASCADE,
                                  db_constraint=False, description='用户')
    create_time = fields.DatetimeField(auto_now_add=True, description='登陆时间')

    class Meta:
        # 元数据
        table = "user_login_history"
        description = "用户登陆历史"

    def __repr__(self):
        return f"UserLoginHistory (id={self.id}, username={self.user.username}, {self.create_time.strftime('%Y-%m-%d %H:%M:%S')})"

    __str__ = __repr__
