from src import cprint
async def start(session, _type, _data):
    async with session.post(f"https://api.bloxflip.com/games/{_type}/create", json=_data, ssl=False) as response:
        if response.status == 200:
            return await response.json()

        if response.status == 400:
            text = await response.text()
            if "You already have an active" in text:
                cprint.error(f"You already have an active {_type} game.")
                return None
            else:
                cprint.error(f"Unknown error occurred: {text}")
                return None

