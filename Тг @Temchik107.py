# meta developer: @Temchik107
# meta name: Modul auto
# meta description: Автоматически принимает все заявки на вступление в каналы

from hikka import loader
from telethon.tl.functions.channels import GetAdminLog, ApproveAllJoinRequests
from telethon.tl.types import ChannelAdminLogEventsFilter
import asyncio

class AutoJoinAllMod(loader.Module):
    """Автоматически принимает все заявки на вступление во все каналы"""

    strings = {"name": "AutoJoinAll"}

    async def client_ready(self, client, db):
        self.client = client
        self.approved_chats = set()
        asyncio.create_task(self.approve_loop())

    async def approve_loop(self):
        while True:
            try:
                dialogs = await self.client.get_dialogs()
                for dialog in dialogs:
                    if not dialog.is_channel or not dialog.admin_rights or not dialog.admin_rights.approve_users:
                        continue
                    chat_id = dialog.id
                    try:
                        await self.client(ApproveAllJoinRequests(chat_id=chat_id))
                    except Exception as e:
                        print(f"Ошибка при одобрении заявок в чате {chat_id}: {e}")
            except Exception as e:
                print(f"Ошибка в основном цикле: {e}")
            await asyncio.sleep(10)  # Проверяет каждые 10 секунд