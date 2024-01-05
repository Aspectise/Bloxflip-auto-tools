import os
try:
    from datetime import datetime
    import random
    import time
    import json
    import cloudscraper
    from rgbprint import gradient_print, Color, rgbprint
except Exception as e:
    os.system("pip insall cloudscraper rgbprint")

# Bloxflip auto tools by Aspect | discord.gg/deathsniper
os.system('cls' if os.name == 'nt' else 'clear')
class Mines:
    def __init__(self, auth, bet_amt, bomb_amt, click_amt, stop_amt):
        self.auth = auth
        self.bet_amt = bet_amt
        self.bomb_amt = bomb_amt
        self.click_amt = click_amt
        self.stop_amt = stop_amt
        self.progress = 0
        self.INFO = f"{Color(127, 127, 127)}INFO{Color(255, 255, 255)} |"
        self.WARNING = f"{Color(255, 165, 0)}WARNING{Color(255, 255, 255)} |"
        self.ERROR = f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} |"
        self.LOST = f"{Color(255, 0, 0)}RIP{Color(255, 255, 255)} |"
        self.WON = f"{Color(0, 255, 0)}WON{Color(255, 255, 255)} |"
        self.scraper = cloudscraper.create_scraper()

    def get_balance(self):
        request = self.scraper.get("https://api.bloxflip.com/user", headers={"x-auth-token": self.auth}).json()
        if "user" not in request:
            input(f"{self.ERROR} Invalid Token. Enter to exit...")
            os._exit(0)
        return request["user"]["wallet"]
    
    def get_username(self):
        request = self.scraper.get("https://api.bloxflip.com/user", headers={"x-auth-token": self.auth}).json()
        if "user" not in request:
            input(f"{self.ERROR} Invalid Token. Enter to exit...")
            os._exit(0)
        return request["user"]["robloxUsername"]

    def start_game(self):
        global game_amt
        while True:
            game_amt_input = input(f'{Color(0, 128, 255)}INPUT{Color(255, 255, 255)} | How many games do you want to play: ')
            if game_amt_input.isdigit() and float(game_amt_input) == int(game_amt_input) and game_amt_input != 0:
                game_amt = int(game_amt_input)
                break
            else:
                print(f"{self.ERROR} Please enter a valid number.")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{self.INFO} Checking Token...")
        self.get_balance()
        os.system('cls' if os.name == 'nt' else 'clear')
        orig_balance = "{:.2f}".format(self.get_balance())
        username = self.get_username()
        print(f"{self.INFO} Logged in as {username} / Balance: {orig_balance}$")
        print(f"{self.INFO} Starting game...\n")
        self.progress = 0
        for game_index in range(1, game_amt + 1):
            print(f"{'-' * 5} Game {game_index} {'-' * 5}")
            self.play_round()
        time.sleep(1)
        final_balance = "{:.2f}".format(self.get_balance())
        print(f"{Color(0, 150, 150)}GAME{Color(255, 255, 255)} Done with all games")
        print(f"{self.INFO} Starting Balance: {orig_balance}$")
        print(f"{self.INFO} New Balance: {final_balance}$\n")
        y_n = input(f"{Color(0, 128, 255)}INPUT{Color(255, 255, 255)} | Do you want to run again? (y/n): ").lower()
        if y_n == "y" or y_n == "yes":
            os.system('cls' if os.name == 'nt' else 'clear')
            self.start_game()
        elif y_n == "n" or y_n == "no":
            print(f"{Color(255, 165, 0)}CYA{Color(255, 255, 255)} | Closing in 5s...")
            time.sleep(5)
            os._exit(0)

    def play_round(self):
        start_game = self.scraper.post("https://api.bloxflip.com/games/mines/create",headers={"x-auth-token": self.auth},json={"betAmount": self.bet_amt, "mines": self.bomb_amt},)
        if start_game.status_code == 400 and start_game.json()["msg"] == "You already have an active mines game!":
            input(f"{self.ERROR} You have an active mines game already. Enter to exit...")
            os._exit(0)
        elif start_game.status_code != 200:
            input(f"{self.ERROR} Unknown error occurred, try again. Enter to exit...")
            os._exit(0)
        round_id = start_game.json()["game"]["uuid"]
        client_seed = start_game.json()["game"]["clientSeed"]
        self.progress += 1
        print(f"{Color(89, 39, 176)}STARTED{Color(255, 255, 255)} | Mines Game started! {Color(200, 200, 200)}({self.progress}/{game_amt}){Color(255, 255, 255)}")
        print(f"{Color(0, 150, 150)}GAME{Color(255, 255, 255)} | Round ID: {round_id}")
        print(f"{Color(0, 150, 150)}GAME{Color(255, 255, 255)} | Client Seed: {client_seed}")
        mines = [f"{Color(255, 255, 255)}X {Color(255, 255, 255)}" for _ in range(25)]
        count = 0
        clicked_positions = set()
        exploded = False
        
        for _ in range(self.click_amt):
            while not exploded:
                a = random.randint(0, 24)
                if a not in clicked_positions:
                    mines[a] = f"{Color(0, 255, 0)}O {Color(255, 255, 255)}"
                    clicked_positions.add(a)
                    choose_mine = self.scraper.post('https://api.bloxflip.com/games/mines/action', headers={'x-auth-token': self.auth}, json={'cashout': False, 'mine': a})
                    click_json = choose_mine.json()
                    if click_json["exploded"] == True:
                        print(f"{Color(255, 50, 50)}UH OH{Color(255, 255, 255)} | Clicked a mine..")
                        exploded = True
                        break
                    count += 1
                    print(f"{self.INFO} Clicked {count} times ({a+1})")
                    break
        print("\n".join(["".join(mines[i:i + 5]) for i in range(0, 25, 5)]))
        time.sleep(0.2)
        if exploded is not True:
            self.cashout()
        else:
            balance = self.get_balance()
            balance = "{:.2f}".format(balance)
            print(f"{self.LOST} You lost / Balance: {balance}$\n")

    def cashout(self):
        try:
            time.sleep(1)
            cashout = self.scraper.post("https://api.bloxflip.com/games/mines/action", headers={"x-auth-token": self.auth}, json={"cashout": True})
        except Exception as e:
            input(f"{self.ERROR} Unknown error occurred trying again: {e}. Enter to exit...")
            os._exit(0)
        winnings = cashout.json()["winnings"]
        profit = winnings - self.bet_amt
        balance = self.get_balance()
        balance = "{:.2f}".format(balance)
        profit = "{:.2f}".format(profit)
        print(f"{self.WON} Profit: {profit}$ / Balance: {balance}$\n")
        if float(balance) <= float(self.stop_amt):
            print(f"{self.WARNING} Your Balance has reached under your minimum stop amount of: {self.stop_amt}$")
            input(f"{self.INFO} Ending turns until further notice. Enter to exit...")
            os._exit(0)

class Towers:
    def __init__(self, auth, bet_amt, difficulty, click_amt, stop_amt):
        self.auth = auth
        self.bet_amt = bet_amt
        self.difficulty = difficulty.lower()
        self.click_amt = click_amt
        self.stop_amt = stop_amt
        self.progress = 0
        self.INFO = f"{Color(127, 127, 127)}INFO{Color(255, 255, 255)} |"
        self.WARNING = f"{Color(255, 165, 0)}WARNING{Color(255, 255, 255)} |"
        self.ERROR = f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} |"
        self.LOST = f"{Color(255, 0, 0)}RIP{Color(255, 255, 255)} |"
        self.WON = f"{Color(0, 255, 0)}WON{Color(255, 255, 255)} |"
        self.scraper = cloudscraper.create_scraper()

    def get_balance(self):
        request = self.scraper.get("https://api.bloxflip.com/user", headers={"x-auth-token": self.auth}).json()
        if "user" not in request:
            input(f"{self.ERROR} Invalid Token. Enter to exit...")
            os._exit(0)
        return request["user"]["wallet"]
    
    def get_username(self):
        request = self.scraper.get("https://api.bloxflip.com/user", headers={"x-auth-token": self.auth}).json()
        if "user" not in request:
            input(f"{self.ERROR} Invalid Token. Enter to exit...")
            os._exit(0)
        return request["user"]["robloxUsername"]

    def start_game(self):
        global game_amt
        while True:
            game_amt_input = input(f'{Color(0, 128, 255)}INPUT{Color(255, 255, 255)} | How many games do you want to play: ')
            if game_amt_input.isdigit() and float(game_amt_input) == int(game_amt_input) and game_amt_input != 0:
                game_amt = int(game_amt_input)
                break
            else:
                print(f"{self.ERROR} Please enter a valid number.")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{self.INFO} Checking Token...")
        self.get_balance()
        os.system('cls' if os.name == 'nt' else 'clear')
        orig_balance = "{:.2f}".format(self.get_balance())
        username = self.get_username()
        print(f"{self.INFO} Logged in as {username} / Balance: {orig_balance}$")
        print(f"{self.INFO} Starting game...\n")
        self.progress = 0
        for game_index in range(1, game_amt + 1):
            print(f"{'-' * 5} Game {game_index} {'-' * 5}")
            self.play_round()
        final_balance = "{:.2f}".format(self.get_balance())
        print(f"{Color(0, 150, 150)}GAME{Color(255, 255, 255)} | Done with all games")
        print(f"{self.INFO} Starting Balance: {orig_balance}$")
        print(f"{self.INFO} New Balance: {final_balance}$\n")
        y_n = input(f"{Color(0, 128, 255)}INPUT{Color(255, 255, 255)} | Do you want to run again? (y/n): ").lower()
        if y_n == "y" or y_n == "yes":
            os.system('cls' if os.name == 'nt' else 'clear')
            self.start_game()
        elif y_n == "n" or y_n == "no":
            print(f"{Color(255, 165, 0)}CYA{Color(255, 255, 255)} | Closing in 5s...")
            time.sleep(5)
            os._exit(0)

    def play_round(self):
        start_game = self.scraper.post("https://api.bloxflip.com/games/towers/create",headers={"x-auth-token": self.auth},json={"betAmount": self.bet_amt, "difficulty": self.difficulty},)
        if start_game.status_code == 400 and start_game.json()["msg"] == "You already have an active mines game!":
            input(f"{self.ERROR} You have an active towers game already. Enter to exit...")
            os._exit(0)
        elif start_game.status_code != 200:
            input(f"{self.ERROR} Unknown error occurred, try again. Enter to exit...")
            os._exit(0)
        round_id = start_game.json()["game"]["uuid"]
        client_seed = start_game.json()["game"]["clientSeed"]
        self.progress += 1
        print(f"{Color(89, 39, 176)}STARTED{Color(255, 255, 255)} | Towers Game started! {Color(200, 200, 200)}({self.progress}/{game_amt}){Color(255, 255, 255)}")
        print(f"{Color(0, 150, 150)}GAME{Color(255, 255, 255)} | Round ID: {round_id}")
        print(f"{Color(0, 150, 150)}GAME{Color(255, 255, 255)} | Client Seed: {client_seed}")
        if self.difficulty.lower() == "normal":
            tower = [[f'{Color(255, 255, 255)}X {Color(255, 255, 255)}', f'{Color(255, 255, 255)}X {Color(255, 255, 255)}'] for _ in range(8)]
            count = 0
            level = -1
            exploded = False
    
            for _ in range(self.click_amt):
                while not exploded:
                    a = random.randint(0, 1)
                    level += 1
                    tower[count][a] = f'{Color(0, 255, 0)}O {Color(255, 255, 255)}'
                    choose_tile = self.scraper.post('https://api.bloxflip.com/games/towers/action', headers={'x-auth-token': self.auth}, json={'cashout': False, 'tile': a, 'towerLevel': level})
                    click_json = choose_tile.json()
                    if click_json["exploded"] == True:
                        print(f"{Color(255, 50, 50)}UH OH{Color(255, 255, 255)} | Clicked a wrong tile..")
                        exploded = True
                        break
                    count += 1
                    print(f"{self.INFO} Clicked {count} times ({a})")
                    break
                
            print("\n".join("".join(row) for row in tower[::-1]))
            time.sleep(0.2)
        else:
            tower = [[f'{Color(255, 255, 255)}X {Color(255, 255, 255)}', f'{Color(255, 255, 255)}X {Color(255, 255, 255)}', f'{Color(255, 255, 255)}X {Color(255, 255, 255)}'] for _ in range(8)]
            count = 0
            level = -1
            exploded = False

            for _ in range(self.click_amt):
                while not exploded:
                    a = random.randint(0, 2)
                    level += 1
                    tower[count][a] = f'{Color(0, 255, 0)}O {Color(255, 255, 255)}'
                    choose_tile = self.scraper.post('https://api.bloxflip.com/games/towers/action', headers={'x-auth-token': self.auth}, json={'cashout': False, 'tile': a, 'towerLevel': level})
                    click_json = choose_tile.json()
                    if click_json["exploded"] == True:
                        print(f"{Color(255, 50, 50)}UH OH{Color(255, 255, 255)} | Clicked a wrong tile..")
                        exploded = True
                        break
                    count += 1
                    print(f"{self.INFO} Clicked {count} times ({a})")
                    break

            print("\n".join("".join(row) for row in tower[::-1]))
            time.sleep(0.2)
        if exploded is not True:
            self.cashout()
        else:
            balance = self.get_balance()
            balance = "{:.2f}".format(balance)
            print(f"{self.LOST} You lost / Balance: {balance}$\n")

    def cashout(self):
        try:
            time.sleep(1)
            cashout = self.scraper.post("https://api.bloxflip.com/games/towers/action", headers={"x-auth-token": self.auth}, json={"cashout": True})
        except Exception as e:
            input(f"{self.ERROR} Unknown error occurred trying again: {e}. Enter to exit...")
            os._exit(0)
        winnings = cashout.json()["winnings"]
        profit = winnings - self.bet_amt
        balance = self.get_balance()
        balance = "{:.2f}".format(balance)
        profit = "{:.2f}".format(profit)
        print(f"{self.WON} Profit: {profit}$ / Balance: {balance}$\n")
        if float(balance) <= float(self.stop_amt):
            print(f"{self.WARNING} Your Balance has reached under your minimum stop amount of: {self.stop_amt}$")
            input(f"{self.INFO} Ending turns until further notice. Enter to exit...")
            os._exit(0)

def main():
    load_config = json.load(open("config.json", "r"))
    while True:
        gamemode = input(f"{Color(0, 128, 255)}INPUT{Color(255, 255, 255)} | What Game Mode do you want to play (1 = Mines | 2 = Towers): ")
        if gamemode.isdigit() and float(gamemode) == int(gamemode) and gamemode in ['1', '2']:
            break
        else:
            print(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Enter a valid Game Mode.")
    os.system('cls' if os.name == 'nt' else 'clear')
    auth_token = load_config["Token"]
    if not auth_token:
        input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | You did not enter a token in config.json. Enter to exit...")
        os._exit(0)

    if int(gamemode) == 1:
        bet_amount = load_config["Mines"]["Bet_Amount"]
        mines_amount = load_config["Mines"]["Mines_Amount"]
        click_amount = load_config["Mines"]["Click_Amount"]
        stop_amount = load_config["Mines"]["Stop_Amount"]
        if not isinstance(bet_amount, int):
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Bet amount must be a valid number. Enter to exit...")
            os._exit(0)
        if bet_amount < 5:
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Bet amount can not be less then 5. Enter to exit...")
            os._exit(0)
        if not isinstance(mines_amount, int):
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Mines amount must be a valid number. Enter to exit...")
            os._exit(0)
        if mines_amount == 0:
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Mines amount can not be 0. Enter to exit...")
            os._exit(0)
        if not isinstance(click_amount, int):
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Click amount must be a valid number. Enter to exit...")
            os._exit(0)
        if click_amount == 0:
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Click amount can not be 0. Enter to exit...")
            os._exit(0)
        if not isinstance(stop_amount, int):
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Stop amount must be a valid number. Enter to exit...")
            os._exit(0)
        os.system("title Bloxflip auto mines by Aspectise ~ discord.gg/deathsniper")
        game = Mines(auth_token, bet_amount, mines_amount, click_amount, stop_amount)
        game.start_game()
    
    if int(gamemode) == 2:
        bet_amount = load_config["Towers"]["Bet_Amount"]
        difficulty = load_config["Towers"]["Difficulty"]
        click_amount = load_config["Towers"]["Click_Amount"]
        stop_amount = load_config["Towers"]["Stop_Amount"]
        if not isinstance(bet_amount, int):
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Bet amount must be a valid number. Enter to exit...")
            os._exit(0)
        if bet_amount < 5:
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Bet amount can not be less then 5. Enter to exit...")
            os._exit(0)
        if difficulty.lower() not in ["easy", "normal", "hard"]:
            input(f'{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Difficulty must be "Easy" or "Normal" or "Hard". Enter to exit...')
            os._exit(0)
        if not isinstance(click_amount, int):
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Click amount must be a valid number. Enter to exit...")
            os._exit(0)
        if click_amount == 0:
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Click amount can not be 0. Enter to exit...")
            os._exit(0)
        if not isinstance(stop_amount, int):
            input(f"{Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | Stop amount must be a valid number. Enter to exit...")
            os._exit(0)
        os.system("title Bloxflip auto towers by Aspectise ~ discord.gg/deathsniper")
        game = Towers(auth_token, bet_amount, difficulty, click_amount, stop_amount)
        game.start_game()


if __name__ == "__main__":
    main()