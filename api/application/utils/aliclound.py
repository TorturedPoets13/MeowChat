import os, json
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from api.application.utils.logs import get_logger


logger = get_logger(os.environ.get('APP_NAME'))


class AliClound(object):
    def __init__(self, key, secret):
        """
        初始化函数
        :param key: 阿里云的access_key_id
        :param secret:  阿里云的access_key_secret
        """
        self.config = open_api_models.Config(
            access_key_id=key,
            access_key_secret=secret
        )

    @property
    def client(self) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        self.config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(self.config)

    def sms(self, mobile: str, template_param: dict, sign_name: str, template_code: str):
        """
        同步发送短信
        @param :mobile 手机号码
        @param :template_param 短信模板变量字典{'code': '随机验证码'}
        @param :sign_name 短信签名
        @param :template_code 短信模板ID
        @return
        """
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name=sign_name,
            template_code=template_code,
            phone_numbers=mobile,
            template_param=json.dumps(template_param)
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 发送短信
            response = self.client.send_sms_with_options(send_sms_request, runtime)
            return response.body
        except Exception as error:
            # 异常处理
            logger.error(f"短信发送异常：{error}")

    async def sms_async(self, mobile: str, template_param: dict, sign_name: str, template_code: str):
        """
        异步发送短信
        @param :mobile 手机号码
        @param :template_param 短信模板变量字典{'code': '随机验证码'}
        @param :sign_name 短信签名
        @param :template_code 短信模板ID
        @return
        """
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name=sign_name,
            template_code=template_code,
            phone_numbers=mobile,
            template_param=json.dumps(template_param)
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 发送短信
            response = await self.client.send_sms_with_options_async(send_sms_request, runtime)
            return response.body
        except Exception as error:
            # 异常处理
            logger.error(f"短信发送异常：{error}")


# if __name__ == '__main__':
#     aliyun = AliClound(key='xxxx', secret='xxxx')
#     mobile = '1234567890'
#     template_param = {'code': '55555'}
#     sign_name = '阿里云短信测试'
#     template_code = 'SMS_154950909'
#     result = aliyun.sms(mobile, template_param, sign_name, template_code)
#     print(result)
