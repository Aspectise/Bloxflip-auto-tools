import random
from rgbprint import Color

from src import cprint
from functions import click, create, _continue, balance

def start(self, session):
    bet_amount = self.bet_amt
    for _ in range(self.game_amount):
        data = create.start(session, "towers", {"betAmount": bet_amount, "difficulty": self.difficulty})
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
                    lost = True
                    if self.if_double:
                        bet_amount = self.bet_amt
                        cprint.info(f"Reseted bet amount to {bet_amount} R$.")
                    _continue._next(self, session, tower, True)
                    break

                cprint.info(f"Clicked {count} times ({_click})")

            if not lost:
                _continue._next(self, session, tower)
                if self.if_double:
                    bet_amount = min(bet_amount * 2, self.max_double)
                    user_balance = balance.get(session)
                    if bet_amount > user_balance:
                        cprint.error("Double bet exceeds your balance. Cannot continue.")
                        input("Press enter to continue. . .")
                        break
                    cprint.info(f"Doubling bet amount to {bet_amount} R$!")

