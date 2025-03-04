# meta developer: Temchik107
# meta name: AntiSticker
# meta description: Модуль для защиты от спама стикеров в чатах

from telethon import events
import time

class AntiStickerMod:
    def __init__(self):
        self.name = "AntiSticker"
        self.sticker_count = {}
        self.spam_threshold = 5  # сколько стикеров подряд считается спамом
        self.time_window = 10  # за сколько секунд

    async def watcher(self, message):
        if not message.is_group:
            return

        if message.sticker:
            user_id = message.sender_id
            chat_id = message.chat_id
            current_time = time.time()

            if chat_id not in self.sticker_count:
                self.sticker_count[chat_id] = {}

            if user_id not in self.sticker_count[chat_id]:
                self.sticker_count[chat_id][user_id] = []

            # Запоминаем время стикера
            self.sticker_count[chat_id][user_id].append(current_time)

            # Очищаем старые записи
            self.sticker_count[chat_id][user_id] = [
                t for t in self.sticker_count[chat_id][user_id] if current_time - t <= self.time_window
            ]

            # Если стикеров слишком много - удаляем и кикаем
            if len(self.sticker_count[chat_id][user_id]) >= self.spam_threshold:
                await message.client.delete_messages(chat_id, [message.id])
                try:
                    await message.client.kick_participant(chat_id, user_id)
                    await message.respond(f"Пользователь [{user_id}](tg://user?id={user_id}) кикнут за спам стикеров.")
                except Exception as e:
                    await message.respond(f"Не удалось кикнуть пользователя за спам стикеров: {str(e)}")

                self.sticker_count[chat_id][user_id] = []