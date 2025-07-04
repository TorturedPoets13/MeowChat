from passlib.context import CryptContext
import string, secrets

class Hashing(object):
    """密码工具类"""

    def __init__(self, schemes='bcrypt'):
        self.crypt = CryptContext(schemes=schemes)

    def hash(self, raw_password):
        """
        密码加密
        :param raw_password: 用户输入的原始密码
        :return: 处理后的密码哈希值
        """
        return self.crypt.hash(raw_password)

    def verify(self, raw_password, hashed_password):
        """
        验证明文密码与哈希处理过后的密码是否正确
        :param raw_password: 用户输入的原始密码
        :param hashed_password: 处理后的密码哈希值
        :return: True or False
        """
        return self.crypt.verify(raw_password, hashed_password)


def genint(length):
    """
    生成指定长度的纯数字字符串
    :param length: 字符长度
    :return:
    """
    characters = string.digits  # string.digits是 Python 标准库 string 的一个常量，值为 '0123456789'，表示所有的十进制数字字符
    ret = "".join(secrets.choice(characters) for _ in range(length))    # secrets 比 random.choices 更安全 secrets 模块是一个专为生成加密强随机数
    return ret

# 测试生成随机数字工具代码
# if __name__ == '__main__':
#     print(genint(6))

# 测试密码加密工具代码
# if __name__ == '__main__':
#     hashing = Hashing()
#     # 对原始密码进行哈希加密
#     password_hash1 = hashing.hash("123456")
#     print(password_hash1)
#     password_hash2 = hashing.hash("123456")
#     print(password_hash2)
#
#     # 判断原始密码是否和密码哈希值是否匹配
#     ret = hashing.verify("123455", password_hash1)
#     print(ret)  # False
#     ret = hashing.verify("123456", password_hash2)
#     print(ret)  # True
