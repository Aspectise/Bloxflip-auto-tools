import json
import os
import traceback
import cloudscraper
from src import cprint
from modes import crash, mines, plinko, slides, towers

settings = json.load(open("config.json", "r"))
class Main:
    def __init__(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.token = settings.get("Token")
        self.session = cloudscraper.CloudScraper()
        self.session.headers.update({"x-auth-token": self.token})
        if not self.token:
            cprint.error("Token not found. Please add your token in the config file.")
            os.system("pause")
            os._exit(0)

        cprint.info("Checking Token...")
        self.wallet, self.username = self.verify_token(self.session)
        cprint.info(f"Logged in as {self.username} / Balance: {self.wallet:.2f} R$\n")

        while True:
            self.game_mode = cprint.user_input("What game mode do you want to play? (towers/mines/plinko/crash/slides) > ").lower()
            if self.game_mode in ["towers", "mines", "plinko", "crash", "slides"]:
                break
            else:
                cprint.error("Invalid game mode.")

        self.setup()
        self.game_amount = int(cprint.user_input("How many games do you want to play? > "))

    def verify_token(self, session):
        response = session.get("https://api.bloxflip.com/user")
        if response.status_code == 200:
            data = response.json()
            wallet = data.get("user").get("wallet") + data.get("user").get("bonusWallet")
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
        self.auto_cashout = settings.get("Crash").get("Auto_Cashout")
        self.crash_model = settings.get("Crash").get("ANN").get("Model").lower()
        self.ann_enabled = settings.get("Crash").get("ANN").get("Enabled")

        error_messages = []
        for setting, value in [
            ("Bet_Amount", self.bet_amt),
            ("Click_Amount", self.click_amt),
            ("Stop_Amount", self.stop_amt),
            ("Mines_Amount", self.bomb_amt),
            ("Difficulty", self.difficulty),
            ("Difficulty", self.plinko_difficulty),
            ("Row", self.plinko_row),
            ("Auto_Cashout", self.auto_cashout),
            ("Crash_Model", self.crash_model),
        ]:
            if setting not in ["Difficulty", "Auto_Cashout", "Crash_Model"] and not isinstance(value, int) and self.game_mode not in ["crash", "slides"]:
                error_messages.append(cprint.error(f"{setting} must be a valid number."))

            if setting == "Crash_Model" and self.crash_model not in ["random_forest", "linear", "svr"]:
                error_messages.append(cprint.error(f"{setting} must be one of the following models: random_forest, linear, svr."))

            if setting == "Auto_Cashout" and not isinstance(value, (int, float)):
                error_messages.append(cprint.error(f"{setting} must be a valid number."))

            if setting == "Mines_Amount" and value < 1:
                error_messages.append(cprint.error(f"{setting} can not be less then 1."))

            if setting == "Difficulty" and value not in ["easy","normal","hard"]:
                error_messages.append(cprint.error(f"{setting} is invalid."))

            if setting == "Bet_Amount" and value < 5 and self.game_mode not in ["plinko", "crash", "slides"]:
                error_messages.append(cprint.error(f"{setting} can not be less then 5."))

        if error_messages:
            os.system("pause")
            os._exit(0)
    
    def run(self):
        while True:
            try:
                self.lost_streak = 0
                self.win_streak = 0

                os.system('cls' if os.name == 'nt' else 'clear')
                if self.game_mode in ["mines", "towers"] and self.bet_amt < 5:
                    while self.bet_amt < 5:
                        try:
                            self.bet_amt = int(cprint.user_input("Bet amount can not be lower then 5. Enter new bet amount > "))
                        except ValueError:
                            continue

                if self.game_mode == "mines":
                    for _ in range(self.game_amount):
                        mines.start(self, self.session)
                if self.game_mode == "towers":
                    for _ in range(self.game_amount):
                        towers.start(self, self.session)
                if self.game_mode == "plinko":
                    plinko.start(self, self.session)
                if self.game_mode == "crash":
                    crash.Crash(self, self.session).connect()
                if self.game_mode == "slides":
                    slides.Slides(self, self.session).connect()

                while True:
                    choice = cprint.user_input("Done with all games, do you want to re-run? (y/N) > ").lower()
                    if choice not in ['y','n']:
                        continue
                    break
                if choice == 'y':
                    while True:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        self.game_mode = cprint.user_input("What game mode do you want to play? (towers/mines/plinko/crash/slides) > ").lower()
                        if self.game_mode in ["towers", "mines", "plinko", "crash", "slides"]:
                            break
                        else:
                            cprint.error("Invalid game mode.")

                    self.game_amount = int(cprint.user_input("How many games do you want to play? > "))
                else:
                    break

            except Exception:
                traceback.print_exc()
                break

if __name__ == "__main__":
    main = Main()
    main.run()

