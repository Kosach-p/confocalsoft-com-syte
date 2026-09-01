from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent.parent / "templates")

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/developers")
async def developers(request: Request):
    return templates.TemplateResponse("developers.html", {"request": request})

@router.get("/updates")
async def updates(request: Request):
    # Данные для блочной структуры (заглушки)
    updates_data = [
        {"image": "/static/images/update1.png", "text": "Новый алгоритм фильтрации шумов (версия 2.1)"},
        {"image": "/static/images/update2.png", "text": "Поддержка мультиспектрального анализа (версия 2.2)"},
        {"image": "/static/images/update3.png", "text": "Оптимизация скорости обработки изображений (версия 2.3)"}
    ]
    return templates.TemplateResponse("updates.html", {"request": request, "updates": updates_data})

@router.get("/documentation")
async def documentation(request: Request):
    return templates.TemplateResponse("documentation.html", {"request": request})