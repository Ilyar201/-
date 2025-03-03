import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipant, ApproveAllJoinRequests
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

# Вставь свои данные
api_id = 123456  # замени на свой api_id
api_hash = 'your_api_hash'  # замени на свой api_hash
bot_token = 'your_bot_token'  # токен бота, который будет одобрять заявки

client = TelegramClient('auto_approver', api_id, api_hash).start(bot_token=bot_token)

async def approve_requests_in_channel(channel):
    try:
        # Проверяем, админ ли бот
        participant = await client(GetParticipant(channel, 'me'))
        if not isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            print(f'Нет прав на управление в {channel.title}')
            return

        # Одобряем все заявки
        await client(ApproveAllJoinRequests(channel.id))
        print(f'✅ Все заявки в канал {channel.title} приняты')

    except Exception as e:
        print(f'❌ Ошибка при обработке {channel.title}: {e}')

async def main():
    print("Бот запущен и принимает заявки...")
    while True:
        try:
            dialogs = await client.get_dialogs()

            for dialog in dialogs:
                if dialog.is_channel:
                    await approve_requests_in_channel(dialog)

        except Exception as e:
            print(f"❌ Общая ошибка: {e}")

        await asyncio.sleep(10)  # Каждые 10 секунд проверка всех каналов

with client:
    client.loop.run_until_complete(main())