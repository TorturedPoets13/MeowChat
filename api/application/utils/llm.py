from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


class ChatGPT(object):
    def __init__(self, model, api_key=None, base_url='https://api.chat.openai.com', proxy=None):
        # 选择调用的OpenAI的模型
        # 如果传递了代理字典，就从中提取 https 的代理
        proxy_url = proxy.get("https") if proxy else None
        self.model = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            openai_proxy=proxy_url,  # LangChain只接受 https 代理地址字符串
        )

    def send(self, prompt, history=None):
        if history is None:
            history = []

        # 将聊天历史按顺序“展开”为一个消息列表传给模型
        response = self.model.invoke([
            *history,  # 把 history 这个列表里的元素挨个取出
            HumanMessage(content=prompt),
        ])
        return response

# if __name__ == '__main__':
#     from api.application import settings
#
#     model = settings.AI_ROBOT['openai_model']
#     api_key = settings.AI_ROBOT['openai_api_key']
#     base_url = settings.AI_ROBOT['openai_baseurl']
#
#     print(f'获取到apikey为：{api_key}。模型{model}。地址{base_url}')
#     robot = ChatGPT(model, api_key, base_url)
#     response = robot.send("写一个haiku about疯女人聊天室")
#     print(f"GPT回复的净输出：{response}")
#     print(response.content)
#
#     """
#     GPT回复的净输出：content='喧嚣声中笑，  \n疯女谈天说地，  \n梦中醒无常。  ' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 24, 'prompt_tokens': 15, 'total_tokens': 39, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': None, 'id': 'chatcmpl-Bt7OHnQtanP4vgZt6BXnj4dgNu5YG', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='run--50ede169-4e6d-4e35-89dd-ac82dac42065-0' usage_metadata={'input_tokens': 15, 'output_tokens': 24, 'total_tokens': 39, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
#     喧嚣声中笑，
#     疯女谈天说地，
#     梦中醒无常。
#     """
