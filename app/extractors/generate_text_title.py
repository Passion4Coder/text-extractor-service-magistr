import asyncio
from concurrent.futures import ThreadPoolExecutor

import ollama

from app.core.config import settings

ollama_client = ollama.Client(host=settings.OLLAMA_HOST)
executor = ThreadPoolExecutor()


async def generate_text_title(text: str) -> str:
    prompt = f"""
    Текст:
    {text}

    Відповідай виключно українською мовою.

    Проаналізуй текст і створи максимально короткий та точний заголовок з 3, максимум 8 слів (це дуже ВАЖЛИВО), який передає головну тему даного тексту.

    Важливі вимоги:
    - Не копіюй перше речення текста.
    - Не створюй художніх або емоційних назв.
    - Формуй чіткий, нейтральний, по суті короткий заголовок.
    - Не використовуй лапки.

    Якщо текст занадто розмитий, то просто виведи абстрактний заголовок. Але, НЕ РЕЧЕННЯ!
    """

    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(
            executor,
            lambda: ollama_client.chat(
                model=settings.LLM_SUMMARY_MODEL,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.3, "num_predict": 100},
            ),
        )

        return response["message"]["content"].strip().strip("'\"")

    except Exception as e:
        return f"Помилка при генерації заголовку (title): {e}"
