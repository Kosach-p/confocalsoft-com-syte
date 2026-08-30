from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

app = FastAPI(title="Конфокальный микроскоп - Конфософт")

# Пути
BASE_DIR = Path(__file__).resolve().parent
DOWNLOADS_DIR = BASE_DIR / "download"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Создаем папки, если их нет
DOWNLOADS_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Настройка шаблонов
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# Главная страница
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_page": "home"}
    )


# Страница разработчиков
@app.get("/developers", response_class=HTMLResponse)
async def developers(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="developers.html",
        context={"active_page": "developers"}
    )


# Страница будущих обновлений
@app.get("/updates", response_class=HTMLResponse)
async def updates(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="updates.html",
        context={"active_page": "updates"}
    )

# Страница документации
@app.get("/docs-page", response_class=HTMLResponse)
async def docs_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="docs.html",
        context={"active_page": "docs"}
    )


# API для скачивания файлов
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = DOWNLOADS_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл не найден")

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Это не файл")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)