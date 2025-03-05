# meta developer: @Temchik107
# meta author: @xasterkarya
# meta name: EmojiRPSInline
# meta version: 1.0
# meta description: Игра Камень-Ножницы-Бумага с inline кнопками

from .. import loader, utils
from telethon.tl.custom import Button

class EmojiRPSInline(loader.Module):
    """Камень-Ножницы-Бумага через inline-кнопки"""
    strings = {"name": "EmojiRPSInline"}

    def __init__(self):
        self.games = {}

    async def minerpscmd(self, message):
        """Запустить игру с другом: .minerps @юзернейм"""
        args = utils.get_args_raw(message)
        if not args:
            await message.reply("Укажи противника: .minerps @username")
            return

        chat_id = message.chat_id
        if chat_id in self.games:
            await message.reply("В этом чате уже идет игра.")
            return

        self.games[chat_id] = {
            "player1": message.sender_id,
            "player2": None,
            "moves": {}
        }

        buttons = [
            [Button.inline("✂️ Ножницы", b"rps_move:scissors")],
            [Button.inline("🪨 Камень", b"rps_move:rock")],
            [Button.inline("📄 Бумага", b"rps_move:paper")]
        ]

        await message.reply(
            f"Игра начата с {args}!\nВыбирайте свой ход, нажимая на кнопки ниже.",
            buttons=buttons
        )

        self.games[chat_id]["player2_mention"] = args

    async def on_callback_query(self, call):
        data = call.data.decode("utf-8").split(":")
        if data[0] != "rps_move":
            return

        move = data[1]
        chat_id = call.peer_id.user_id if call.peer_id else call.chat_id

        if chat_id not in self.games:
            await call.answer("Игра уже завершена или не начата.")
            return

        game = self.games[chat_id]
        user_id = call.from_user.id

        if user_id not in [game["player1"], game["player2"]]:
            if game["player2"] is None:
                game["player2"] = user_id  # Второй игрок автоматически присоединяется
            else:
                await call.answer("Ты не участвуешь в этой игре.")
                return

        if user_id in game["moves"]:
            await call.answer("Ты уже сделал выбор.")
            return

        game["moves"][user_id] = move
        await call.answer(f"Вы выбрали {self.emoji(move)}")

        if len(game["moves"]) == 2:
            await self.finish_game(chat_id, call)

    async def finish_game(self, chat_id, call):
        game = self.games[chat_id]
        p1, p2 = game["player1"], game["player2"]
        m1, m2 = game["moves"][p1], game["moves"][p2]

        result = (
            f"⚔️ Результаты игры Камень-Ножницы-Бумага\n\n"
            f"Игрок 1 выбрал: {self.emoji(m1)}\n"
            f"Игрок 2 выбрал: {self.emoji(m2)}\n\n"
        )

        winner = self.determine_winner(m1, m2)
        if winner == "draw":
            result += "Ничья!"
        elif winner == "p1":
            result += "✨ Победил Игрок 1!"
        else:
            result += "✨ Победил Игрок 2!"

        await call.edit(result, buttons=None)
        del self.games[chat_id]

    def determine_winner(self, move1, move2):
        rules = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
        if move1 == move2:
            return "draw"
        if rules[move1] == move2:
            return "p1"
        return "p2"

    def emoji(self, move):
        return {
            "rock": "🪨 Камень",
            "scissors": "✂️ Ножницы",
            "paper": "📄 Бумага"
        }[move]