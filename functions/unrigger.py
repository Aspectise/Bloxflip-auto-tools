import requests
from src import cprint

class Unrigger:
    def __init__(self, session):
        self.session = session

    def _make_request(self, request_method, endpoint, data=None):
        url = f"https://api.bloxflip.com{endpoint}"
        response = request_method(url, json=data)
        if response.status_code != 200:
            cprint.error(f"An error has occurred while trying to unrig.")
            return None
        return response.json()

    def _get_server_hash(self):
        response_data = self._make_request(self.session.get, "/provably-fair")
        return response_data.get("serverHash") if response_data else None

    def _get_client_seed(self):
        response_data = self._make_request(self.session.get, "/games/mines/history?size=5000&page=0")
        if not response_data:
            return None
        seed_json = response_data.get("data", [])
        get_seeds = [item["serverSeed"][:32] for item in seed_json if not item["exploded"]]
        return get_seeds[0] if get_seeds else None

    def _post_new_seed(self, client_seed):
        response_data = self._make_request(self.session.post, "/provably-fair/clientSeed", data={"clientSeed": client_seed})
        if response_data:
            cprint.info("You have been unrigged!\n")
        else:
            cprint.error("An error has occurred while trying to unrig.")

    def unrig(self):
        server_hash = self._get_server_hash()
        if server_hash:
            client_seed = self._get_client_seed()
            if client_seed:
                self._post_new_seed(client_seed)
            else:
                cprint.error("You need to be on a valid gamemode to unrig.")
