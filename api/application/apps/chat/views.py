from fastapi import APIRouter, WebSocket, WebSocketDisconnect

app = APIRouter()


@app.websocket("/index")  # 因为当前接口写在chat分组应用中，所以websocket接口的访问地址: ws://1227.0.0.1:8000/chat/index
async def index(websocket: WebSocket):
    """AI应用助理的聊天接口"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('action') == 'chat':
                """与AI助理达到聊天互动 """
                # todo: 1.选择对话的AI大模型

                # todo: 2.选择本地的会话ID

                # todo: 3.获取会话的历史内容

                # todo: 4.调用AI大模型达到API接口，获取回答的结果

                # 5.判断结果的内容类型
                message = {
                    'action': 'chat',
                    'type': 'text',  # text表示文本， image表示图片
                    'message': 'AI回答问题的内容...'
                }
                await websocket.send_json(message)
            elif data.get('action') == 'session':
                """切换/新增会话记录"""
                pass
    except WebSocketDisconnect:
        """表示客户端断开了连接"""
        pass
