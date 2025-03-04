# meta developer: Temchik107
# meta name: AntiSticker
# meta description: Антиспам стикеров для групп в Hikka

import time
from telethon.tl.types import Message
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from .. import loader, utils

@loader.tds
class AntiStickerMod(loader.Module):
    """Простой антиспам стикеров для чатов"""
    strings = {"name": "AntiSticker"}

    def __init__(self):
        self.sticker_log = {}
        self.config = loader.ModuleConfig(
            loader.ConfigValue("max_stickers", 5, "Максимум стикеров за период"),
            loader.ConfigValue("time_window", 10, "Время в секундах для подсчёта стикеров"),
        )

    async def client_ready(self, client, db):
        self.client = client

    async def watcher(self, message: Message):
        if not message.is_group or not message.sticker:
            return

        chat_id = message.chat_id
        user_id = message.sender_id
        now = time.time()

        if chat_id not in self.sticker_log:
            self.sticker_log[chat_id] = {}

        if user_id not in self.sticker_log[chat_id]:
            self.sticker_log[chat_id][user_id] = []

        self.sticker_log[chat_id][user_id].append(now)

        # Удаляем старые записи (вне окна time_window)
        self.sticker_log[chat_id][user_id] = [
            t for t in self.sticker_log[chat_id][user_id]
            if now - t <= self.config["time_window"]
        ]

        # Если стикеров слишком много — кик
        if len(self.sticker_log[chat_id][user_id]) >= self.config["max_stickers"]:
            await message.delete()

            try:
                await self.client(EditBannedRequest(
                    chat_id,
                    user_id,
                    ChatBannedRights(
                        until_date=None,
                        send_stickers=True,
                        send_gifs=True,
                        send_photos=True
                    )
                ))
                await utils.answer(message, f"⚠️ Пользователь [id{user_id}](tg://user?id={user_id}) получил мут за спам стикеров.")
            except Exception as e:
                await utils.answer(message, f"❌ Не удалось замутить пользователя: {e}")

            self.sticker_log[chat_id][user_id] = []