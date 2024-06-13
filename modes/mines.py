import random
from rgbprint import Color

from src import cprint
from functions import click, create, _continue

def start(self, session):
    data = create.start(session, "mines", {"betAmount": self.bet_amt, "mines": self.bomb_amt})
    if data:
        cprint.custom("Mines Game started!", "STARTED", (89, 39, 176))

        current_game = data.get("game")
        round_id = current_game.get("uuid")
        client_seed = current_game.get("clientSeed")

        cprint.custom(f"Round ID: {round_id}", "GAME", (0, 150, 150))
        cprint.custom(f"Client Seed: {client_seed}", "GAME", (0, 150, 150))
        mines = [f"{Color(255, 255, 255)}X {Color(255, 255, 255)}" for _ in range(25)]

        count = 0
        clicked_positions = set()
        lost = False
        safe_click = [10, 15]

        while True:
            if not self.safe_pred:
                if count == self.click_amt:
                    break
                _click = random.randint(0, 24)
            else:
                if count == len(safe_click):
                    break
                _click = safe_click[count]

            if _click not in clicked_positions:
                mines[_click] = f"{Color(0, 255, 0)}O {Color(255, 255, 255)}"
                count += 1
                clicked_positions.add(_click)
                click_data = click.start(session, "mines", {'cashout': False, 'mine': _click})

                if click_data.get("exploded"):
                    cprint.lost(f"Clicked a mine..")
                    lost = True
                    _continue._next(self, session, mines, True)
                    break

                cprint.info(f"Clicked {count} times ({_click+1})")

        if not lost:
            _continue._next(self, session, mines)

