from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from routes.auth_routes import router as auth_router
from routes.dividends_routes import router as dividends_router
from routes.user_routes import router as user_router
from routes.transaction_routes import router as transaction_router
from routes.portfolio_routes import router as portfolio_router
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


app.include_router(auth_router)
app.include_router(dividends_router)
app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(portfolio_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8000, log_level="info", reload=True)
