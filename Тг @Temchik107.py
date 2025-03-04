# meta developer: @Temchik107
# meta banner: Auto Approve Requests (100% Termux Safe)

from telethon.tl.functions.channels import ApproveAllJoinRequests
from hikka import loader, utils

class AutoApproveRequests(loader.Module):
    """Автоматическое одобрение заявок в канал"""

    strings = {"name": "AutoApproveRequests"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "CHANNEL_ID", 2420582000, "ID канала, где бот должен одобрять заявки."
        )

    async def client_ready(self, client, db):
        self.client = client

    @loader.loop(interval=10)  # Проверка заявок каждые 10 секунд
    async def check_requests(self):
        channel_id = self.config["CHANNEL_ID"]
        try:
            await self.client(ApproveAllJoinRequests(channel_id))
            print(f"✅ Все заявки в канал {channel_id} одобрены.")
        except Exception as e:
            print(f"❌ Ошибка при одобрении заявок: {e}")