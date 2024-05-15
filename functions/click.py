async def start(session, _type, _data):
    async with session.post(f'https://api.bloxflip.com/games/{_type}/action', json=_data, ssl=False) as response:
        return await response.json()