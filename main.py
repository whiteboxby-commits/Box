from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# 1. Настройка CORS
# Разрешаем запросы откуда угодно ("*"). 
# Для безопасности потом можно заменить "*" на адрес вашего сайта на Тильде.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Ваш секретный ключ (он остается только здесь, на сервере)
MINIMAX_API_KEY = "sk-api-BIP_w45lABMW5-JP5B3V3x1xzA01HnNIArMb9pSgmK42-tSLh5ybeHRYdxf5vsvqrGnoo2SrRvJik9Tk_x_zD_2ooVnuHSO9DrjVlO8a2mZrboz1twgZyEs"

# 3. Маршрут, на который будет стучаться Тильда
@app.post("/api/generate-video")
async def minimax_proxy(request: Request):
    # Получаем данные, которые отправляет ваш код с Тильды
    body = await request.json()
    
    # URL для генерации видео от Minimax (убедитесь, что он совпадает с их документацией)
    minimax_url = "https://api.minimax.chat/v1/video_generation"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }

    # Безопасно пересылаем запрос к Minimax
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                minimax_url, 
                headers=headers, 
                json=body,
                timeout=60.0 # Видео генерируется не сразу, даем таймаут побольше
            )
            response.raise_for_status() 
            return response.json() # Возвращаем готовый ответ обратно на Тильду
            
        except httpx.HTTPStatusError as e:
            # Если Minimax вернул ошибку (например, неверный формат данных)
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            # Если сервер Minimax недоступен
            raise HTTPException(status_code=500, detail=f"Ошибка соединения с API: {str(e)}")

