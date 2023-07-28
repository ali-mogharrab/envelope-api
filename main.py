from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import authentication
from db import models
from db.database import engine
from routers import email, message, user

app = FastAPI()
app.include_router(user.router)
app.include_router(message.router)
app.include_router(email.router)
app.include_router(authentication.router)

@app.get('/')
def root():
    return {'message': 'Welcome to envelope'}


# CORS settings
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


models.Base.metadata.create_all(engine)
