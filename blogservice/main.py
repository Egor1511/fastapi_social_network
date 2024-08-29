from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), 'static')


