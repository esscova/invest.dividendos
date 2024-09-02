from fastapi import FastAPI


from routes.auth_routes import router as auth_router
from routes.dividends_routes import router as dividends_router
from routes.user_routes import router as user_router
from routes.transaction_routes import router as transaction_router

#...

app = FastAPI(title='Invest.dividendos',version="0.0.1", openapi_url='/invest.dividendos')

#...


@app.get('/')
def home():
    return{'ping':'pong'}

app.include_router(auth_router)
app.include_router(dividends_router)
app.include_router(user_router)
app.include_router(transaction_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8000, log_level="info", reload=True)
