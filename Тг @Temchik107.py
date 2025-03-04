# meta developer: @Temchik107
# meta banner: Auto Approve Requests for Termux Channel

from telethon import events
from telethon.tl.functions.channels import GetParticipant
from telethon.tl.functions.channels import EditBanned
from telethon.tl.functions.messages import GetPeerDialogs
from telethon.tl.types import ChatAdminRights, ChannelParticipantCreator, ChannelParticipantAdmin, ChannelParticipantBanned

from hikka import loader, utils  # Для совместимости с Hikka

class AutoApproveRequests(loader.Module):
    """Автоматическое принятие заявок в канал Termux"""

    strings = {"name": "AutoApproveRequests"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "CHANNEL_ID", -1001234567890, "ID вашего канала", validator=loader.validators.Integer()
        )

    async def client_ready(self, client, db):
        self.client = client

    @loader.loop(interval=10)  # Проверка заявок каждые 10 секунд
    async def check_requests(self):
        channel_id = self.config["CHANNEL_ID"]

        try:
            # Получаем список заявок
            requests = await self.client(GetPeerDialogs([channel_id]))
            for request in requests.dialogs:
                if request.peer.user_id:
                    user_id = request.peer.user_id
                    await self.approve_request(channel_id, user_id)
        except Exception as e:
            print(f"Ошибка при получении заявок: {e}")

    async def approve_request(self, channel_id, user_id):
        try:
            await self.client(EditBanned(channel_id, user_id, ChannelParticipantBanned(False)))
            print(f"Заявка пользователя {user_id} одобрена.")
        except Exception as e:
            print(f"Ошибка при одобрении {user_id}: {e}")