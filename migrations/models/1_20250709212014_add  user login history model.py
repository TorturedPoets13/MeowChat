from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user_login_history` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    `create_time` DATETIME(6) NOT NULL COMMENT '登陆时间' DEFAULT CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL COMMENT '用户'
) CHARACTER SET utf8mb4 COMMENT='用于记录会话';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `user_login_history`;"""
