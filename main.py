import os
import traceback
import cloudscraper
from src import cprint, settings
from rgbprint import Color
from modes import crash, mines, plinko, slides, towers
import time

class Main:
    def __init__(self):
        settings.load_settings(self)
        cprint.header(1)
        self.token = self.settings.get("Token")
        if not self.token:
            cprint.error("Token not found. Please add your token in the config file.")
            os.system("pause")
            os._exit(0)
        self.session = cloudscraper.create_scraper()
        self.session.headers.update({"x-auth-token": self.token})

        cprint.info("Checking Token...")
        self.wallet, self.username, self.user_id = self.verify_token(self.session)
        cprint.info(f"Logged in as {self.username} | Balance: {self.wallet:.2f} R$\n")
        time.sleep(1)

    def verify_token(self, session):
        response = session.get("https://api.bloxflip.com/user")
        if response.status_code == 200:
            data = response.json()
            wallet = data.get("user").get("wallet") + data.get("user").get("bonusWallet")
            username = data.get("user").get("robloxUsername")
            userid = data.get("user").get("robloxId")
            return wallet, username, userid
        else:
            cprint.error(f"Invalid Token.")
            os.system("pause")
            os._exit(0)


    def run(self):
        while True:
            try:
                cprint.header()
                choice = input(f"""{Color(0x20278C)}┌───({Color(255, 255, 255)}{self.username}@root{Color(0x20278C)})─[{Color(255, 255, 255)}~{Color(0x20278C)}]
└──{Color(255, 255, 255)}$ """)
                
                if choice == "exit":
                    break

                if not choice.isdigit():
                    cprint.error(f"Please provide a valid option.")
                    time.sleep(1)
                    continue

                choice = int(choice)
                if f"{choice:02d}" not in [f"{i:02d}" for i in range(7)]:
                    cprint.error(f"Please provide a valid option.")
                    time.sleep(1)
                    continue

                self.lost_streak = 0
                self.win_streak = 0
                self.mines_lg = None

                self.game_mode = {'01': "mines", '02': "towers", '03': "plinko", '04': "crash", '05': "slides", '06': "settings"}.get(f"{choice:02d}")
                if self.game_mode == "settings":
                    settings.change_settings(self)
                    continue

                errors = settings.setup(self)
                if errors:
                    input("Press enter to continue. . .")
                    continue
                while True: 
                    cprint.header(1)
                    try: self.game_amount = int(cprint.user_input(f"How many {self.game_mode.capitalize()} games do you want to play? > ")); break 
                    except ValueError: pass
                
                cprint.header(1)
                if self.game_mode == "mines":
                    mines.start(self, self.session)
                if self.game_mode == "towers":
                    towers.start(self, self.session)
                if self.game_mode == "plinko":
                    plinko.start(self, self.session)
                if self.game_mode == "crash":
                    crash.Crash(self, self.session).connect()
                if self.game_mode == "slides":
                    slides.Slides(self, self.session).connect()
                self.session = cloudscraper.create_scraper()
                self.session.headers.update({"x-auth-token": self.token})
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