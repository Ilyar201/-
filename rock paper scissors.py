# meta developer: @Temchik107
# meta author: @xasterkarya
# meta name: EmojiRockPaperScissors
# meta version: 1.0

class EmojiRockPaperScissorsMod:
    def __init__(self):
        self.games = {}

        self.emojis = {
            "камень": "🪨",
            "ножницы": "✂️",
            "бумага": "📄"
        }

    async def rpscmd(self, message):
        """Начать игру Камень-Ножницы-Бумага с другом. Использование: .rps @username"""
        args = message.raw_text.split()
        if len(args) < 2:
            await message.reply("Укажи, с кем хочешь играть. Например: .rps @username")
            return
        
        opponent = args[1]
        chat_id = message.chat_id
        self.games[chat_id] = {
            "player1": message.sender_id,
            "player2": None,
            "moves": {},
            "status": "waiting"
        }
        await message.reply(f"Игра началась! Ждем подтверждения от {opponent}. Напиши: .rpsaccept")

    async def rpsacceptcmd(self, message):
        """Принять вызов на игру"""
        chat_id = message.chat_id
        if chat_id not in self.games or self.games[chat_id]["status"] != "waiting":
            await message.reply("Нет активных вызовов.")
            return

        self.games[chat_id]["player2"] = message.sender_id
        self.games[chat_id]["status"] = "playing"
        await message.reply("Игра началась! Оба игрока должны выбрать: .move камень / .move ножницы / .move бумага")

    async def movecmd(self, message):
        """Сделать ход: .move камень / ножницы / бумага"""
        chat_id = message.chat_id
        if chat_id not in self.games or self.games[chat_id]["status"] != "playing":
            await message.reply("Сейчас нет активной игры.")
            return

        move = message.raw_text.split()[1].lower()
        if move not in ["камень", "ножницы", "бумага"]:
            await message.reply("Выбери один из вариантов: камень, ножницы или бумага.")
            return

        player_id = message.sender_id
        if player_id not in [self.games[chat_id]["player1"], self.games[chat_id]["player2"]]:
            await message.reply("Ты не участвуешь в этой игре.")
            return

        self.games[chat_id]["moves"][player_id] = move

        if len(self.games[chat_id]["moves"]) < 2:
            await message.reply("Ход принят. Ждем второго игрока.")
        else:
            await self.finish_game(chat_id, message)

    async def finish_game(self, chat_id, message):
        moves = self.games[chat_id]["moves"]
        player1 = self.games[chat_id]["player1"]
        player2 = self.games[chat_id]["player2"]

        move1 = moves[player1]
        move2 = moves[player2]

        emoji1 = self.emojis[move1]
        emoji2 = self.emojis[move2]

        await message.reply(f"Результат игры:\n\n"
                            f"Игрок 1 выбрал {move1} {emoji1}\n"
                            f"Игрок 2 выбрал {move2} {emoji2}")

        result = self.determine_winner(move1, move2)
        if result == "draw":
            await message.reply("Ничья!")
        elif result == "player1":
            await message.reply("Победил Игрок 1!")
        else:
            await message.reply("Победил Игрок 2!")

        del self.games[chat_id]

    def determine_winner(self, move1, move2):
        if move1 == move2:
            return "draw"
        elif (move1 == "камень" and move2 == "ножницы") or \
             (move1 == "ножницы" and move2 == "бумага") or \
             (move1 == "бумага" and move2 == "камень"):
            return "player1"
        else:
            return "player2"