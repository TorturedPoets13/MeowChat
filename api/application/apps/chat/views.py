from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from api.application.utils import llm
from api.application import settings
from api.application.apps.chat import models

app = APIRouter()


@app.websocket("/index")  # 因为当前接口写在chat分组应用中，所以websocket接口的访问地址: ws://1227.0.0.1:8000/chat/index
async def index(websocket: WebSocket):
    """AI应用助理的聊天接口"""
    redis = websocket.app.state.redis
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('action') == 'chat':
                """与AI助理达到聊天互动 """
                # todo: 从Token中提取用户的ID
                user_id = 2

                # 1.选择对话的AI大模型
                gpt = llm.ChatGPT(model=settings.AI_ROBOT['openai_model'],
                                  api_key=settings.AI_ROBOT['openai_api_key'],
                                  proxy=settings.AI_ROBOT['proxies'])
                # 2.选择本地的会话ID
                session_id = await redis.get(f'session_{user_id}')
                if not session_id:
                    session = await models.Session.filter(user_id=user_id).order_by('-id').first()
                    if not session:
                        session = await models.Session.create(name="默认", user_id=user_id)
                        session_id = session.id
                        await redis.set(f'session_{user_id}', session_id)
                # 3.获取会话的历史内容
                history = await models.History.filter(session_id=session_id).all().order_by().limit(100)
                """
                [
                    {'role': 'user', 'content': '你能不能联网帮我查询下？'},
                    {'role': 'system', 'content': '作为一个AI模型，我无法预测未来，因为我的知识是基于历史数据和当前信息....'},
                ]
                """
                # todo: 把提问的问题和AI回答问题的内容作为历史记录到数据表

                # 4.调用AI大模型达到API接口，获取回答的结果
                response = gpt.send(data.get('message'))
                print(f"AI返回的回答为{response}")

                # 5.判断结果的内容类型
                message = {
                    'action': 'chat',
                    'type': 'text',  # text表示文本， image表示图片
                    # 'message': 'AI回答问题的内容...'
                    'message': response
                }
                await websocket.send_json(message)
            elif data.get('action') == 'session':
                """切换/新增会话记录"""
                pass
    except WebSocketDisconnect:
        """表示客户端断开了连接"""
        pass
