from src import cprint
def start(session, _type, _data):
    response = session.post(f"https://api.bloxflip.com/games/{_type}/create", json=_data)
    if response.status_code == 200:
        return response.json()

    if response.status_code == 400:
        text = response.text
        if "You already have an active" in text:
            cprint.error(f"You already have an active {_type} game.")
            return None
        else:
            cprint.error(f"Unknown error occurred: {text}")
            return None

