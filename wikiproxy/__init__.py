from fastapi import FastAPI as _FastAPI

from .routers import router as _router

_m1sta = _FastAPI()
_m1sta.include_router(_router, prefix='/wikiproxy')
