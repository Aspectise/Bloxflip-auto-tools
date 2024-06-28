from functions import balance, unrigger, cashout
from datetime import datetime
from rgbprint import Color
from src import cprint
import os
def _next(self, session, tiles, lost, data):
    wallet = balance.get(session)

    if lost:
        self.lost_streak += 1
        self.win_streak = 0

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.game_mode == "mines":
            for mine in data.get("game").get("mineLocations"):
                tiles[mine] = f"{Color(255, 0, 0)}X {Color(255, 255, 255)}"
            print("".join([f"{Color(190, 190, 190)}{timestamp} > {''.join(tiles[i:i + 5])}\n" for i in range(0, 25, 5)] ), end="")
        else:
            tower_levels = data.get('game').get('towerLevels')
            for level, row in enumerate(tower_levels):
                for place, cell in enumerate(row):
                    if cell == 1:
                        tiles[level][place] = f"{Color(255, 0, 0)}X {Color(255, 255, 255)}"
            print("".join([f"{Color(190, 190, 190)}{timestamp} > {''.join(row)}\n" for row in tiles[::-1]]), end="")
        cprint.lost(f"Lost Streak: {self.lost_streak} | Balance: {wallet:.2f} R$\n")

        unrigger.Unrigger(session).unrig()
    else:
        self.win_streak += 1
        self.lost_streak = 0
        data = cashout.start(self, session, self.game_mode)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.game_mode == "mines":
            for mine in data.get("game").get("mineLocations"):
                tiles[mine] = f"{Color(255, 0, 0)}X {Color(255, 255, 255)}"
            print("".join([f"{Color(190, 190, 190)}{timestamp} > {''.join(tiles[i:i + 5])}\n" for i in range(0, 25, 5)] ), end="")
        else:
            tower_levels = data.get('game').get('towerLevels')
            for level, row in enumerate(tower_levels):
                for place, cell in enumerate(row):
                    if cell == 1:
                        tiles[level][place] = f"{Color(255, 0, 0)}X {Color(255, 255, 255)}"
            print("".join([f"{Color(190, 190, 190)}{timestamp} > {''.join(row)}\n" for row in tiles[::-1]]), end="")
        winnings = data.get("winnings")
        profit = winnings - data.get("game").get("betAmount")
        wallet += winnings
        cprint.won(f"Win Streak: {self.win_streak}")
        cprint.won(f"Profit: {profit:.2f} R$ | Balance: {wallet:.2f} R$\n")

    self.mines_lg = data
    if float(wallet) <= float(self.stop_amt):
        cprint.warn(f"Your Balance has reached under your minimum stop amount of: {self.stop_amt} R$")
        os.system("pause")
        os._exit(0)