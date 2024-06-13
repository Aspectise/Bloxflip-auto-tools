import threading
from src import cprint
from functions import roll

def start(self, session):
    full_gain = 0
    self.plinko_difficulty = "low" if self.plinko_difficulty == "easy" else "medium" if self.plinko_difficulty == "normal" else "high" if self.plinko_difficulty == "hard" else "low"
    cprint.info(f"Starting {self.game_amount} plinko games with difficulty set as {self.plinko_difficulty} and {self.bet_amt * self.game_amount} R$ in total...")

    def roll_wrapper():
        nonlocal full_gain
        full_gain += roll.start(session, {"amount": self.bet_amt, "risk": self.plinko_difficulty, "rows": self.plinko_row})

    threads = [threading.Thread(target=roll_wrapper) for _ in range(self.game_amount)]
    [t.start() for t in threads]
    [t.join() for t in threads]

    cprint.info(f"Finished all plinko games, spent {self.bet_amt * self.game_amount} R$ and got {full_gain:.1f} R$\n")
