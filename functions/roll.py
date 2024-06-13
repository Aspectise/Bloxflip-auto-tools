from src import cprint
def start(session, _data):
    response = session.post("https://api.bloxflip.com/games/plinko/roll", json=_data)
    if response.status_code == 200:
        data = response.json()
        gain = data.get("wallet")
        return gain
    else:
        text = response.text
        cprint.error(f"Failed to roll: {text}")
        return 0