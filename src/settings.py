from src import cprint
from rgbprint import Color, rgbprint
import time
import json
import os

def print_settings(settings_data, indent=2, prefix="", is_last_section=False):
    last_key = list(settings_data.keys())[-1]
    for key, value in settings_data.items():
        if key != "Token":
            if isinstance(value, dict):
                cprint.info(f"{' ' * indent}{prefix}{Color(255, 153, 51)}{key}{Color(255, 255, 255)}:")  # Orange subsection heading
                print_settings(value, indent + 2, prefix + "  ", key == last_key)
                if key != last_key:
                    cprint.info("") 
            else:
                cprint.info(f"{' ' * indent}{prefix}{Color(153, 204, 255)}{key}{Color(255, 255, 255)}: {Color(204, 255, 204)}{value}{Color(255, 255, 255)}")

def change_settings(self):
    while True:
        cprint.header(1)
        cprint.info("Current Settings:")
        print_settings(self.settings)

        print("\n")
        cprint.info("Information:")
        cprint.info("  - Enter the full setting path to change (e.g., 'Mines.Mines_Amount', 'Crash.ANN.Enabled')")
        cprint.info("  - Type 'back' to return to the main menu.\n")

        choice = input(f"{Color(0x20278C)}[{Color(255, 255, 255)}Settings{Color(0x20278C)}]{Color(255, 255, 255)}$ ")
        if choice.lower() == 'back':
            break

        keys = [key.lower() for key in choice.split('.')]

        current_setting = self.settings
        for key in keys[:-1]:
            if key in [k.lower() for k in current_setting.keys()]:
                current_setting = current_setting[[k for k in current_setting.keys() if k.lower() == key][0]]
            else:
                cprint.error(f"Invalid setting path: '{choice}'")
                time.sleep(1)
                break

        last_key = keys[-1]
        if isinstance(current_setting, dict) and last_key in [k.lower() for k in current_setting.keys()]:
            try:
                new_value = cprint.user_input(f"Enter new value for '{choice}': ")
                actual_key = [k for k in current_setting.keys() if k.lower() == last_key][0]

                if choice.lower() in ["main.bet_amount", "crash.auto_cashout"]: 
                    try:
                        new_value = int(new_value)
                    except ValueError:
                        new_value = float(new_value)
                elif choice.lower() in ["main.click_amount", "main.stop_amount", "mines.mines_amount", "plinko.row", "main.double_bet.max_double"]:
                    new_value = int(new_value)
                elif choice.lower() in ["towers.difficulty", "plinko.difficulty"]:
                    if new_value.lower() not in ["easy", "normal", "hard"]:
                        raise ValueError("Difficulty must be 'easy', 'normal', or 'hard'")
                    new_value = new_value.lower()
                elif choice.lower() == "crash.ann.model":
                    if new_value.lower() not in ["random_forest", "linear", "svr"]:
                        raise ValueError("Model must be 'random_forest', 'linear', or 'svr'")
                    new_value = new_value.lower()
                elif choice.lower() in ["main.double_bet.enabled", "mines.safe_prediction", "crash.ann.enabled"]:
                    if new_value.lower() not in ["true", "false"]:
                        raise ValueError("Value must be 'true' or 'false'")
                    new_value = new_value.lower() == "true"
                else:
                    raise ValueError("Invalid setting path.")

                current_setting[actual_key] = new_value
                with open("config.json", "w") as f:
                    json.dump(self.settings, f, indent=4)
                load_settings(self) 
                cprint.success(f"Setting '{choice}' updated successfully!")

            except ValueError as e:
                cprint.error(f"Invalid input: {e}")
            except Exception as e:
                cprint.error(f"An error occurred: {e}")
        else:
            cprint.error(f"Invalid setting path: '{choice}'")
        time.sleep(1.5)

def setup(self):
    self.bet_amt = self.settings.get("Main").get("Bet_Amount")
    self.click_amt = self.settings.get("Main").get("Click_Amount")
    self.stop_amt = self.settings.get("Main").get("Stop_Amount")
    self.if_double = self.settings.get("Main").get("Double_Bet").get("Enabled")
    self.max_double = self.settings.get("Main").get("Double_Bet").get("Max_Double")
    self.difficulty = self.settings.get("Towers").get("Difficulty")
    self.difficulty = self.difficulty.lower()
    self.bomb_amt = self.settings.get("Mines").get("Mines_Amount")
    self.safe_pred = self.settings.get("Mines").get("Safe_Prediction")
    self.plinko_difficulty = self.settings.get("Plinko").get("Difficulty")
    self.plinko_row = self.settings.get("Plinko").get("Row")
    self.auto_cashout = self.settings.get("Crash").get("Auto_Cashout")
    self.crash_model = self.settings.get("Crash").get("ANN").get("Model").lower()
    self.ann_enabled = self.settings.get("Crash").get("ANN").get("Enabled")

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
        return True
    return False

def load_settings(self):
    with open("config.json", "r") as f: self.settings = json.load(f)