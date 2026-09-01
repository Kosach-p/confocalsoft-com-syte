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
FIGURES_DIR = BASE_DIR / "figures"  # Добавляем путь к папке figures

# Создаем папки, если их нет
DOWNLOADS_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
FIGURES_DIR.mkdir(exist_ok=True)  # Создаем папку figures

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Подключаем папку figures как статическую
app.mount("/figures", StaticFiles(directory=str(FIGURES_DIR)), name="figures")

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


# API для проверки файлов
@app.get("/check-files")
async def check_files():
    try:
        files = []
        if DOWNLOADS_DIR.exists():
            for file in DOWNLOADS_DIR.iterdir():
                if file.is_file():
                    files.append({
                        "name": file.name,
                        "size": file.stat().st_size,
                        "exists": True
                    })

        # Добавляем проверку папки figures
        figures_files = []
        if FIGURES_DIR.exists():
            for file in FIGURES_DIR.iterdir():
                if file.is_file():
                    figures_files.append({
                        "name": file.name,
                        "size": file.stat().st_size,
                        "exists": True
                    })

        return {
            "downloads_dir": str(DOWNLOADS_DIR),
            "dir_exists": DOWNLOADS_DIR.exists(),
            "files": files,
            "figures_dir": str(FIGURES_DIR),
            "figures_dir_exists": FIGURES_DIR.exists(),
            "figures_files": figures_files
        }
    except Exception as e:
        return {"error": str(e)}


# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)