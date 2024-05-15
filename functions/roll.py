from src import cprint
async def start(session, _data):
    async with session.post("https://api.bloxflip.com/games/plinko/roll", json=_data, ssl=False) as response:
        if response.status == 200:
            data = await response.json()
            gain = data.get("wallet")
            return gain
        else:
            text = await response.text()
            cprint.error(f"Failed to roll: {text}")
            return 0