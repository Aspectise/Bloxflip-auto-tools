from functions import balance, unrigger, cashout
from datetime import datetime
from rgbprint import Color
from src import cprint
async def _next(self, session, tiles, lost=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if self.game_mode == "mines":
        print("\n".join([f"{Color(190, 190, 190)}{timestamp} > {''.join(tiles[:5])}"] + [f"{Color(190, 190, 190)}{timestamp} > {''.join(tiles[i:i + 5])}" for i in range(5, 25, 5)]))
    else:
        print("\n".join([f"{Color(190, 190, 190)}{timestamp} > {''.join(row)}" for row in tiles[::-1]]))
    wallet = await balance.get(session)

    if lost:
        self.lost_streak += 1
        self.win_streak = 0
        cprint.lost(f"Lost Streak: {self.lost_streak}")
        cprint.lost(f"You lost / Balance: {wallet:.2f} R$\n")
        await unrigger.Unrigger(session).unrig()
    else:
        self.win_streak += 1
        self.lost_streak = 0
        cprint.won(f"Win Streak: {self.win_streak}")
        await cashout.start(self, session, self.game_mode)