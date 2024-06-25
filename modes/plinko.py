from concurrent.futures import ThreadPoolExecutor, as_completed
from src import cprint
from functions import roll

def start(self, session):
    full_gain = 0
    self.plinko_difficulty = {"easy": "low", "normal": "medium", "hard": "high"}.get(self.plinko_difficulty, "low")

    cprint.info(f"Starting {self.game_amount} plinko games with difficulty set as "
              f"{self.plinko_difficulty} and {self.bet_amt * self.game_amount} R$ in total...")

    with ThreadPoolExecutor(max_workers=self.game_amount) as executor:
        futures = [executor.submit(roll.start, session, 
                                   {"amount": self.bet_amt, "risk": self.plinko_difficulty, "rows": self.plinko_row}) 
                   for _ in range(self.game_amount)]
        
        for future in as_completed(futures):
            full_gain += future.result()

    cprint.info(f"Finished all plinko games:")
    cprint.info(f"  - Total spent: {self.bet_amt * self.game_amount:.1f} R$")
    cprint.info(f"  - Total profit: {full_gain:.1f} R$")