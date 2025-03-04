# meta developer: Temchik107
# meta name: AntiSticker
# meta description: Защита чатов от спама стикеров в Hikka

import time
from telethon.tl.types import Message
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from .. import loader, utils  # Обязательно для Hikka

@loader.tds
class AntiStickerMod(loader.Module):
    """Модуль для защиты чатов от спама стикеров"""
    strings = {
        "name": "AntiSticker",
        "user_kicked": "👮 Пользователь {user} кикнут за спам стикеров.",
        "cant_kick": "❌ Не удалось кикнуть пользователя {user}: {error}",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "spam_threshold",
                5,
                "Сколько стикеров подряд считается спамом"
            ),
            loader.ConfigValue(
                "time_window",
                10,
                "За сколько секунд эти стикеры должны быть отправлены"
            )
        )
        self.sticker_count = {}

    async def client_ready(self, client, db):
        self.client = client

    async def watcher(self, message: Message):
        if not message.is_group or not message.sticker:
            return

        chat_id = message.chat_id
        user_id = message.sender_id
        current_time = time.time()

        if chat_id not in self.sticker_count:
            self.sticker_count[chat_id] = {}

        if user_id not in self.sticker_count[chat_id]:
            self.sticker_count[chat_id][user_id] = []

        self.sticker_count[chat_id][user_id].append(current_time)

        # Очищаем старые записи
        self.sticker_count[chat_id][user_id] = [
            t for t in self.sticker_count[chat_id][user_id]
            if current_time - t <= self.config["time_window"]
        ]

        if len(self.sticker_count[chat_id][user_id]) >= self.config["spam_threshold"]:
            try:
                await message.delete()
                await self.client(EditBannedRequest(
                    chat_id,
                    user_id,
                    ChatBannedRights(
                        until_date=None,
                        view_messages=True
                    )
                ))
                await message.respond(self.strings("user_kicked").format(user=f"[{user_id}](tg://user?id={user_id})"))
            except Exception as e:
                await message.respond(self.strings("cant_kick").format(user=f"[{user_id}](tg://user?id={user_id})", error=str(e)))

            self.sticker_count[chat_id][user_id] = []