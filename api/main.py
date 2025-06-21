import os
import uvicorn
from api.application import create_app


app = create_app()


if __name__ == '__main__':
    uvicorn.run('main:app', host=os.environ.get('APP_HOST'),
                port=int(os.environ.get('APP_PORT', default=8000)),
                reload=bool(os.environ.get('APP_DEBUG')))
