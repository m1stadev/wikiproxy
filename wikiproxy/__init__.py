from contextlib import asynccontextmanager as _asynccontextmanager

from fastapi import FastAPI as _FastAPI
from plykos import Client as _Client

from .routers import router as _router


# https://stackoverflow.com/a/76322910/17865804
@_asynccontextmanager
async def _lifespan(app: _FastAPI):
    async with _Client() as client:
        yield {'client': client}


_m1sta = _FastAPI(lifespan=_lifespan, openapi_url=None)
_m1sta.include_router(_router, prefix='/wikiproxy')
