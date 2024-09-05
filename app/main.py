from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from routes.api import api_router

#...

app = FastAPI(title='Invest.dividendos',version="0.0.1", openapi_url='/invest.dividendos')
templates = Jinja2Templates(directory='app/templates')

#...


@app.get('/')
def home(request:Request):
    context = {
        'request':request,
        'contexto':'Pong'
    }
    return templates.TemplateResponse('index.html', context=context)

app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8000, log_level="info", reload=True)
