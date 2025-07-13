from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user_session_history` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    `question` LONGTEXT NOT NULL COMMENT '问题',
    `answer` LONGTEXT NOT NULL COMMENT '回答',
    `created_time` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `session_id` INT NOT NULL COMMENT '会话'
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `user_session` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    `name` VARCHAR(255) NOT NULL COMMENT '会话名称',
    `created_time` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL COMMENT '用户'
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `user_session_history`;
        DROP TABLE IF EXISTS `user_session`;"""
