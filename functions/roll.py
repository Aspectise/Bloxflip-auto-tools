from src import cprint
import time
def start(session, _data):
    while True:
        response = session.post("https://api.bloxflip.com/games/plinko/roll", json=_data)
        text = response.text
        if response.status_code == 200:
            data = response.json()
            gain = data.get("wallet")
            return gain
        elif "already playing" in text:
            time.sleep(0.5)
        else:
            cprint.error(f"Failed to roll: {text}")
            return 0