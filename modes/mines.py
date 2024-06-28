import random
from rgbprint import Color

from src import cprint
from functions import click, create, _continue, balance

def start(self, session):
    bet_amount = self.bet_amt
    for _ in range(self.game_amount):
        data = create.start(session, "mines", {"betAmount": bet_amount, "mines": self.bomb_amt})
        if data:
            cprint.custom("Mines Game started!", "STARTED", (89, 39, 176))

            current_game = data.get("game")
            round_id = current_game.get("uuid")
            client_seed = current_game.get("clientSeed")

            count = 0
            lost = False
            game_data = None

            cprint.custom(f"Round ID: {round_id}", "GAME", (0, 150, 150))
            cprint.custom(f"Client Seed: {client_seed}", "GAME", (0, 150, 150))
            mines = [f"{Color(255, 255, 255)}X {Color(255, 255, 255)}" for _ in range(25)]

            click_positions = random.sample(range(25), self.click_amt)  

            if self.mines_algo == "safe":
                click_positions = [10, 15]
            elif self.mines_algo == "last_game":
                if self.mines_lg is not None:
                    click_positions = self.mines_lg.get("game").get("mineLocations")

            for _click in click_positions:
                mines[_click] = f"{Color(0, 255, 0)}O {Color(255, 255, 255)}"
                count += 1
                click_data = click.start(session, "mines", {'cashout': False, 'mine': _click})

                if click_data.get("exploded"):
                    cprint.lost(f"Clicked a mine..")
                    lost = True
                    game_data = click_data
                    break

                cprint.info(f"Clicked {count} times ({_click+1})")


            if self.if_double:
                user_balance = balance.get(session)
                if lost and self.on_loss or not lost and not self.on_loss:
                    bet_amount = min(bet_amount * 2, self.max_double)
                    if bet_amount > user_balance:
                        cprint.error("Double bet exceeds your balance. Cannot continue.")
                        input("Press enter to continue. . .")
                        break
                    cprint.info(f"Doubling bet amount to {bet_amount} R$!")
                else:
                    bet_amount = self.bet_amt
                    cprint.info(f"Resetting bet amount to {bet_amount} R$.")

            _continue._next(self, session, mines, lost, game_data)
