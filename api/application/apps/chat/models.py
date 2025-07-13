from tortoise import models, fields


class Session(models.Model):
    # 字段列表
    id = fields.IntField(pk=True, description='主键')
    user = fields.ForeignKeyField('models.User', related_name='session_list',
                                  on_delete=fields.OnDelete.CASCADE, db_constraint=False, description='用户')
    name = fields.CharField(max_length=255, description='会话名称')
    created_time = fields.DatetimeField(auto_now_add=True, description='创建时间')

    # 元数据
    class Meta:
        table = 'user_session'
        description = "会话信息"

    def __repr__(self):
        return f"Session (id={self.id}, name={self.name}, username={self.user.username}"

    __str__ = __repr__


class History(models.Model):
    id = fields.IntField(pk=True, description='主键')
    session = fields.ForeignKeyField('models.Session', related_name='history_list', on_delete=fields.OnDelete.CASCADE,
                                     db_constraint=False, description='会话')
    question = fields.TextField(description='问题')
    answer = fields.TextField(description='回答')
    created_time = fields.DatetimeField(auto_now_add=True, description='创建时间')

    # 元数据
    class Meta:
        table = "user_session_history"
        description = "会话历史"

    def __repr__(self):
        return f"History (id={self.id}, username={self.session.username}, session={self.session})"

    __str__ = __repr__
