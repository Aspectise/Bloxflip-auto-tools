import random
from rgbprint import Color

from src import cprint
from functions import click, create, _continue

def start(self, session):
    data = create.start(session, "towers", {"betAmount": self.bet_amt, "difficulty": self.difficulty})
    if data:
        cprint.custom("Towers Game started!", "STARTED", (89, 39, 176))

        current_game = data.get("game")
        round_id = current_game.get("uuid")
        client_seed = current_game.get("clientSeed")

        cprint.custom(f"Round ID: {round_id}", "GAME", (0, 150, 150))
        cprint.custom(f"Client Seed: {client_seed}", "GAME", (0, 150, 150))
        tower = [[f'{Color(255, 255, 255)}X {Color(255, 255, 255)}' for _ in range(2 if self.difficulty == "normal" else 3)] for _ in range(8)]

        count = 0
        level = -1
        lost = False

        while True:
            if count == self.click_amt:
                break
            _click = random.randint(0, 1 if self.difficulty == "normal" else 2)
            count += 1
            level += 1
            tower[count][_click] = f"{Color(0, 255, 0)}O {Color(255, 255, 255)}"
            click_data = click.start(session, "towers", {'cashout': False, 'tile': _click, 'towerLevel': level})

            if click_data.get("exploded"):
                cprint.lost(f"Clicked a wrong tile..")
                _continue._next(self, session, tower, True)
                lost = True
                break

            cprint.info(f"Clicked {count} times ({_click})")

        if not lost:
            _continue._next(self, session, tower)

