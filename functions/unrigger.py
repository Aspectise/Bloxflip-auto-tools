import aiohttp
import json

from src import cprint

class Unrigger:
    def __init__(self, session):
        self.session = session

    async def _make_request(self, request, endpoint, data=None):
        async with request(f"https://api.bloxflip.com{endpoint}", json=data) as response:
            if response.status != 200:
                cprint.error(f"An error has occurred while trying to unrig.")
                return None
            return await response.json()

    async def _get_server_hash(self):
        response_data = await self._make_request(self.session.get, "/provably-fair")
        return response_data.get("serverHash")

    async def _get_client_seed(self):
        response_data = await self._make_request(self.session.get, "/games/mines/history?size=5000&page=0")
        seed_json = response_data.get("data", [])
        get_seeds = [item["serverSeed"][:32] for item in seed_json if not item["exploded"]]
        return get_seeds[0] if get_seeds else None

    async def _post_new_seed(self, client_seed):
        response_data = await self._make_request(self.session.post, "/provably-fair/clientSeed", data={"clientSeed": client_seed})
        if response_data:
            cprint.info("You have been unrigged!\n")
        else:
            cprint.error("An error has occurred while trying to unrig.")

    async def unrig(self):
        server_hash = await self._get_server_hash()
        if server_hash:
            client_seed = await self._get_client_seed()
            if client_seed:
                await self._post_new_seed(client_seed)
            else:
                cprint.error("You need to be on a valid gamemode to unrig.")
