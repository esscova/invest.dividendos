from fastapi import FastAPI
from routes.user_routes import router as users_router
from routes.transaction_routes import router as transactions_router
from routes.auth import router as auth_router


app = FastAPI(title='Agenda de dividendos',version="0.0.1", openapi_url='/agenda_dividendos')




@app.get('/')
def home():
    return{'ping':'pong'}

app.include_router(auth_router)
app.include_router(transactions_router)
app.include_router(users_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8000, log_level="info", reload=True)
