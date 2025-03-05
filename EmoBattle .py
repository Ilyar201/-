# meta developer: @Temchik107
# meta author: @xasterkarya
# meta name: RockPaperScissors
# meta version: 1.0
# meta description: Игра Камень-Ножницы-Бумага для Hikka

from telethon.tl.custom import Button
from .. import loader, utils

class RockPaperScissorsMod(loader.Module):
    """Игра Камень-Ножницы-Бумага для Hikka"""
    strings = {"name": "RPSGame"}

    def __init__(self):
        self.games = {}

    async def minerpscmd(self, message):
        """Запустить игру с другом — .minerps @username"""
        args = utils.get_args_raw(message)
        if not args:
            await message.reply("Укажи соперника через @.")
            return

        if message.chat_id in self.games:
            await message.reply("Игра уже идет в этом чате.")
            return

        self.games[message.chat_id] = {
            "players": [message.sender_id, None],
            "moves": [None, None]
        }

        await message.reply(
            f"Игра начата с {args}!\nВыбирайте свой ход, нажимая на кнопки ниже.",
            buttons=self.get_buttons()
        )

    def get_buttons(self):
        return [
            [Button.inline("✊ Камень", "rps:rock"),
             Button.inline("✌️ Ножницы", "rps:scissors"),
             Button.inline("✋ Бумага", "rps:paper")]
        ]

    async def on_callback_query(self, call):
        chat_id = call.peer_id.chat_id
        user_id = call.from_user.id

        if chat_id not in self.games:
            await call.answer("Игра не найдена.", alert=True)
            return

        game = self.games[chat_id]
        if user_id not in game["players"]:
            if game["players"][1] is None:
                game["players"][1] = user_id
            else:
                await call.answer("Ты не участник этой игры.", alert=True)
                return

        player_index = game["players"].index(user_id)
        if game["moves"][player_index] is not None:
            await call.answer("Ты уже сделал свой выбор.", alert=True)
            return

        move = call.data.decode().split(":")[1]
        game["moves"][player_index] = move

        if all(game["moves"]):
            await self.finish_game(chat_id, call)
        else:
            await call.edit(f"Ждем второго игрока...", buttons=self.get_buttons())

    async def finish_game(self, chat_id, call):
        game = self.games.pop(chat_id)
        p1, p2 = game["players"]
        m1, m2 = game["moves"]

        result = self.get_result(m1, m2)
        text = f"Игра завершена!\n\nИгрок 1 ({p1}): {self.emoji(m1)}\nИгрок 2 ({p2}): {self.emoji(m2)}\n\n"

        if result == 0:
            text += "Ничья!"
        elif result == 1:
            text += "Победил Игрок 1!"
        else:
            text += "Победил Игрок 2!"

        await call.edit(text)

    def get_result(self, move1, move2):
        if move1 == move2:
            return 0
        if (move1 == "rock" and move2 == "scissors") or \
           (move1 == "scissors" and move2 == "paper") or \
           (move1 == "paper" and move2 == "rock"):
            return 1
        return 2

    def emoji(self, move):
        return {"rock": "✊", "scissors": "✌️", "paper": "✋"}[move]