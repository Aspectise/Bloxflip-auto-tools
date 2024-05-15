import aiohttp
import asyncio
import json
import os
import traceback

from src import cprint
from modes import mines, towers, plinko
settings = json.load(open("config.json", "r"))
class Main:
    def __init__(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.token = settings.get("Token")
        if not self.token:
            cprint.error("Token not found. Please add your token in the config file.")
            os.system("pause")
            os._exit(0)

        cprint.info("Checking Token...")
        self.wallet, self.username = asyncio.run(self.verify_token())
        cprint.info(f"Logged in as {self.username} / Balance: {self.wallet:.2f} R$\n")

        while True:
            self.game_mode = cprint.user_input("What game mode do you want to play? (towers/mines/plinko) > ").lower()
            if self.game_mode in ["towers", "mines", "plinko"]:
                break
            else:
                cprint.error("Invalid game mode.")

        self.setup()
        self.game_amount = int(cprint.user_input("How many games do you want to play? > "))

    async def verify_token(self):
        async with aiohttp.ClientSession(headers={"x-auth-token": self.token}) as session:
            async with session.get("https://api.bloxflip.com/user") as response:
                if response.status == 200:
                    data = await response.json()
                    wallet = data.get("user").get("wallet")
                    username = data.get("user").get("robloxUsername")
                    return wallet, username
                else:
                    cprint.error(f"Invalid Token.")
                    os.system("pause")
                    os._exit(0)

    def setup(self):
        self.bet_amt = settings.get("Bet_Amount")
        self.click_amt = settings.get("Click_Amount")
        self.stop_amt = settings.get("Stop_Amount")
        self.difficulty = settings.get("Towers").get("Difficulty")
        self.difficulty = self.difficulty.lower()
        self.bomb_amt = settings.get("Mines").get("Mines_Amount")
        self.safe_pred = settings.get("Mines").get("Safe_Prediction")
        self.plinko_difficulty = settings.get("Plinko").get("Difficulty")
        self.plinko_row = settings.get("Plinko").get("Row")

        error_messages = []
        for setting, value in [
            ("Bet_Amount", self.bet_amt),
            ("Click_Amount", self.click_amt),
            ("Stop_Amount", self.stop_amt),
            ("Mines_Amount", self.bomb_amt),
            ("Difficulty", self.difficulty),
            ("Difficulty", self.plinko_difficulty),
            ("Row", self.plinko_row),
        ]:
            if setting != "Difficulty" and not isinstance(value, int):
                error_messages.append(f"{setting} must be a valid number.")
            if setting == "Mines_Amount" and value < 1:
                error_messages.append(f"{setting} can not be less then 1.")
            if setting == "Difficulty" and value not in ["easy","normal","hard"]:
                error_messages.append(f"{setting} is invalid.")
            if setting == "Bet_Amount" and value < 5 and self.game_mode != "plinko":
                error_messages.append(f"{setting} can not be less then 5.")

        if error_messages:
            cprint.error("\n".join(error_messages))
            os.system("pause")
            os._exit(0)
    
    async def run(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                session = aiohttp.ClientSession(headers={"x-auth-token": self.token})
                if self.game_mode == "mines":
                    for _ in range(self.game_amount):
                        await mines.start(self, session)
                if self.game_mode == "towers":
                    for _ in range(self.game_amount):
                        await towers.start(self, session)
                if self.game_mode == "plinko":
                    await plinko.start(self, session)
                while True:
                    choice = cprint.user_input("Done with all games, do you want to re-run? (y/N) > ").lower()
                    if choice not in ['y','n']:
                        continue
                    break
                if choice == 'n':
                    break

            except Exception:
                traceback.print_exc()
                break
            finally:
                await session.close()

if __name__ == "__main__":
    main = Main()
    asyncio.run(main.run())

