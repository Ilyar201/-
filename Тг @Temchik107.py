import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import ApproveAllJoinRequests
from telethon.errors import ChatAdminRequiredError

# Заполни свои данные
api_id = 123456  # замени на свое
api_hash = 'your_api_hash'  # замени на свое
bot_token = 'your_bot_token'  # замени на свое

client = TelegramClient('auto_approver_session', api_id, api_hash).start(bot_token=bot_token)

async def approve_all_requests():
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if not dialog.is_channel:
            continue
        try:
            await client(ApproveAllJoinRequests(dialog.id))
            print(f"Все заявки в {dialog.title} приняты")
        except ChatAdminRequiredError:
            print(f"Нет прав на принятие заявок в {dialog.title}")
        except Exception as e:
            print(f"Ошибка в {dialog.title}: {e}")

@client.on(events.NewMessage(pattern='/start'))
async def handler(event):
    await event.reply("✅ Бот активен и принимает заявки в каналы!")

async def main():
    print("Бот запущен и следит за заявками...")
    while True:
        try:
            await approve_all_requests()
        except Exception as e:
            print(f"Ошибка при проверке заявок: {e}")
        await asyncio.sleep(10)  # каждые 10 секунд проверка

with client:
    client.loop.run_until_complete(main())