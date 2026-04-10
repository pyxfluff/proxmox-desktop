# pyxfluff 2026

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/auth")

@router.get("/status")
def status():
    return JSONResponse({"code": 200, "message": "OK"})
