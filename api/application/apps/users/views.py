from fastapi import APIRouter

app = APIRouter()


@app.get('/login')
async def api():
    return {'title': '测试login'}
