import os
from src import cprint
from functions import balance
async def start(self, session, _type):
    async with session.post(f"https://api.bloxflip.com/games/{_type}/action", json={"cashout": True}, ssl=False) as response:
        if response.status == 200:
            data = await response.json()
            winnings = data.get("winnings")
            profit = winnings - self.bet_amt
            wallet = await balance.get(session)
            
            cprint.won(f"Profit: {profit:.2f} R$ / Balance: {wallet:.2f} R$\n")
            if float(wallet) <= float(self.stop_amt):
                cprint.info(f"Your Balance has reached under your minimum stop amount of: {self.stop_amt} R$")
                os.system("pause")
                os._exit(0)
        else:
            text = await response.text()
            cprint.error(f"Failed to cash out: {text}")