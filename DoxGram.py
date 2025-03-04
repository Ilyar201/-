# meta developer: @Temchik107
# meta banner: https://imgur.com/your-banner-link.png

from .. import loader, utils
import asyncio

class FakeDoxGramMod(loader.Module):
    strings = {"name": "FakeDoxGram"}

    async def doxgramcmd(self, message):
        """Запускает фейковую докс-систему DoxGram"""
        await message.edit("<b>Запуск DoxGram...</b>")
        await asyncio.sleep(2)

        await message.edit("<b>DoxGram - Собираем данные в базе данных 1/140</b>")
        await asyncio.sleep(0.8)

        for i in range(2, 141):
            await message.edit(f"<b>DoxGram - Собираем данные в базе данных {i}/140</b>")
            await asyncio.sleep(0.3)

        await message.edit(
            "<b>✅ DoxGram - Сбор данных завершен.\n"
            "Данные сохранены в архив DoxGram.</b>"
        )