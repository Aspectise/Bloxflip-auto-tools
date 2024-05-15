import asyncio

from src import cprint
from functions import roll

async def start(self, session):
    full_gain = 0
    self.plinko_difficulty = "low" if self.plinko_difficulty == "easy" else "medium" if self.plinko_difficulty == "normal" else "high" if self.plinko_difficulty == "hard" else "low"
    cprint.info(f"Starting {self.game_amount} plinko games with difficulty set as {self.plinko_difficulty} and {self.bet_amt * self.game_amount} R$ in total...")
    tasks = [asyncio.create_task(roll.start(session, {"amount": self.bet_amt, "risk": self.plinko_difficulty, "rows": self.plinko_row})) for _ in range(self.game_amount)]
    data = await asyncio.gather(*tasks)
    for result in data: full_gain += result
    cprint.info(f"Finished all plinko games, spent {self.bet_amt * self.game_amount} R$ and got {full_gain:.1f} R$\n")

