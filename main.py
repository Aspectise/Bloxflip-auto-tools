import json
import os
import traceback
import cloudscraper
from src import cprint
from rgbprint import Color, rgbprint
from modes import crash, mines, plinko, slides, towers
import shutil
import time

settings = json.load(open("config.json", "r"))
class Main:
    def __init__(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.version = "5.1"
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

    def display_info(self, banner=None):
        os.system('cls' if os.name == 'nt' else 'clear')
        MAIN_COLOR: Color = Color(0xFDA81A)
        ACCENT_COLOR: Color = Color(255, 255, 255)

        TITLE: str = f"""
        ░▒▓███████▓▒░░▒▓████████▓▒░░▒▓██████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓████████▓▒░ ░▒▓█▓▒░   ░▒▓████████▓▒░ 
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 
        ░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 
        """

        TEXT_IN_BOX: str = "Bloxflip-Auto-Tools"

        SIGNATURE: str = f"""
        ╔═{"═" * (len(TEXT_IN_BOX) + len(self.version) + 1)}═╗
        ║ {TEXT_IN_BOX} {self.version} ║
        ╚═{"═" * (len(TEXT_IN_BOX) + len(self.version) + 1)}═╝
        """

        OPTIONS: dict[str, str] = {
    "01": "Mines",
    "02": "Towers",
    "03": "Plinko",
    "04": "Crash",
    "05": "Slides",
    "06": "Coming Soon.",
    }
        
        OPTIONS_SPACING: str = f"{str().ljust(30)}"

        def _get_shell_size() -> int:
            return shutil.get_terminal_size().columns

        def _print_centered(text: str, *, color: Color = None, end: str = "\n") -> None:
            for line in text.splitlines():
                rgbprint(line.center(_get_shell_size()), color=color, end=end)

        def batched(iterable, n):
            import itertools
            it = iter(iterable)
            while batch := tuple(itertools.islice(it, n)):
                yield batch

        _print_centered(TITLE, color=MAIN_COLOR)
        _print_centered(SIGNATURE, color=ACCENT_COLOR)
        print()

        if banner is None:
            previous_batch = None
            for batch in batched(map(lambda x: f"[{x[0]}] -> {x[1]}", OPTIONS.items()), 3):
                if previous_batch is None:
                    previous_batch = batch
                    continue

                max_previous_page = max(len(x) for x in previous_batch)
                max_page = max(len(x) for x in batch)

                for i, previous_element in enumerate(previous_batch):
                    _print_centered(f"{previous_element:{max_previous_page}}{OPTIONS_SPACING}{batch[i]:{max_page}}", color=ACCENT_COLOR)
        print()

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
                self.display_info()
                choice = input(f"""{Color(0x20278C)}┌───({Color(255, 255, 255)}{self.username}@root{Color(0x20278C)})─[{Color(255, 255, 255)}~{Color(0x20278C)}]
└──{Color(255, 255, 255)}$ """)
                
                if choice == "exit":
                    break

                if not choice.isdigit():
                    cprint.error(f"Please provide a valid option.")
                    time.sleep(1)
                    continue

                choice = int(choice)
                if f"{choice:02d}" not in [f"{i:02d}" for i in range(6)]:
                    cprint.error(f"Please provide a valid option.")
                    time.sleep(1)
                    continue

                self.lost_streak = 0
                self.win_streak = 0

                self.game_mode = {'01': "mines", '02': "towers", '03': "plinko", '04': "crash", '05': "slides"}.get(f"{choice:02d}")
                self.setup()
                self.game_amount = int(cprint.user_input(f"How many {self.game_mode.capitalize()} games do you want to play? > "))

                if self.game_mode in ["mines", "towers"] and self.bet_amt < 5:
                    while self.bet_amt < 5:
                        try:
                            self.bet_amt = int(cprint.user_input("Bet amount can not be lower then 5. Enter new bet amount > "))
                        except ValueError:
                            continue
                
                self.display_info(1)
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
                
                while (rerun := cprint.user_input(f"Done with all {self.game_mode.capitalize()} games, do you want to continue playing? (y/N) > ").lower()) not in ['y', 'n']:
                    pass
                if rerun == 'n': break

            except KeyboardInterrupt:
                print("\nExiting... Dont forget to star the repo ;)")
                time.sleep(1)
                break
            except Exception:
                traceback.print_exc()
                break

if __name__ == "__main__":
    main = Main()
    main.run()

