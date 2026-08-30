from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="LMX2820 Controller API", version="1.0")

# Модель данных для фичи
class Feature(BaseModel):
    id: int
    icon: str
    title: str
    description: str

# Модель для ответа со списком фич
class FeaturesResponse(BaseModel):
    features: List[Feature]
    current_version: str
    status: str

# Данные о планируемых обновлениях
features_data = [
    Feature(
        id=1,
        icon="🔧",
        title="Расширенный контроль LMX2820",
        description="Гибкая настройка всех регистров, управление мультипликатором и детектором фазы."
    ),
    Feature(
        id=2,
        icon="📊",
        title="Визуализация спектра",
        description="Графическое отображение выходного сигнала, измерение мощности и частоты в реальном времени."
    ),
    Feature(
        id=3,
        icon="⚙️",
        title="Мастер калибровки VCO",
        description="Автоматическая подстройка контура для стабильной работы во всем диапазоне частот."
    ),
    Feature(
        id=4,
        icon="💾",
        title="Профили настроек",
        description="Сохранение и загрузка конфигураций для разных частотных планов (A, B и т.д.)."
    ),
    Feature(
        id=5,
        icon="🛠️",
        title="Диагностика и отладка",
        description="Подробный лог SPI-команд, чтение статусных регистров и температуры кристалла."
    ),
    Feature(
        id=6,
        icon="📱",
        title="Удаленное управление",
        description="Возможность управлять синтезатором через веб-интерфейс или мобильное приложение."
    )
]

# API эндпоинты
@app.get("/", response_class=HTMLResponse)
async def root():
    """Главная страница с HTML интерфейсом"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/features", response_model=FeaturesResponse)
async def get_features():
    """Получить список всех планируемых функций"""
    return FeaturesResponse(
        features=features_data,
        current_version="v1.0",
        status="В разработке"
    )

@app.get("/api/features/{feature_id}", response_model=Feature)
async def get_feature(feature_id: int):
    """Получить конкретную функцию по ID"""
    for feature in features_data:
        if feature.id == feature_id:
            return feature
    return {"error": "Feature not found"}

@app.post("/api/features")
async def add_feature(feature: Feature):
    """Добавить новую функцию (для администрирования)"""
    # Проверяем, что ID уникален
    max_id = max([f.id for f in features_data]) if features_data else 0
    feature.id = max_id + 1
    features_data.append(feature)
    return {"status": "success", "feature": feature}

@app.delete("/api/features/{feature_id}")
async def delete_feature(feature_id: int):
    """Удалить функцию по ID (для администрирования)"""
    for i, feature in enumerate(features_data):
        if feature.id == feature_id:
            deleted = features_data.pop(i)
            return {"status": "success", "deleted": deleted}
    return {"error": "Feature not found"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Автоматическая перезагрузка при изменениях
        log_level="info"
    )