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
        setting_schema = {
            "Main": {
                "Bet_Amount": (int, float),
                "Click_Amount": int,
                "Stop_Amount": int,
                "Double_Bet": {
                    "Enabled": bool,
                    "On_Loss": bool,
                    "Max_Double": (int, float)
                }
            },
            "Mines": {
                "Mines_Amount": int,
                "Algorithm": ["last_game", "safe", "random"]
            },
            "Towers": {
                "Difficulty": ["easy", "normal", "hard"]
            },
            "Plinko": {
                "Difficulty": ["easy", "normal", "hard"],
                "Row": int
            },
            "Slides": {
                "Opposite_Color": bool
            },
            "Crash": {
                "Auto_Cashout": (int, float),
                "ANN": {
                    "Enabled": bool,
                    "Model": ["random_forest", "linear", "svr"]
                }
            }
        }    

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

            keys = choice.split(".")
            current_level = self.settings
            schema_level = setting_schema

            try:
                for i, key in enumerate(keys):
                    matching_key = next((k for k in current_level.keys() if k.lower() == key.lower()), None)
                    if matching_key is None:
                        raise ValueError(f"Invalid setting path: '{choice}'")

                    if i == len(keys) - 1:
                        new_value = cprint.user_input(f"Enter new value for '{choice}': ")
                        expected_type = schema_level[matching_key]

                        if isinstance(expected_type, tuple):
                            if isinstance(expected_type[0], type) and all(isinstance(t, type) for t in expected_type):
                                valid_input = False
                                for t in expected_type:
                                    try:
                                        new_value = t(new_value)
                                        valid_input = True
                                        break
                                    except ValueError:
                                        pass

                                if not valid_input:
                                    if int in expected_type and float in expected_type:
                                        raise ValueError(f"Please enter a number.")
                                    else:
                                        raise ValueError(f"Expected one of: {', '.join([t.__name__ for t in expected_type])}")

                        elif expected_type is bool:
                            if new_value.lower() in ["true"]:
                                new_value = True
                            elif new_value.lower() in ["false"]:
                                new_value = False
                            else:
                                raise ValueError(f"Please enter 'true' or 'false'.")
                        elif isinstance(expected_type, list):
                            if new_value.lower() not in [v.lower() for v in expected_type]:
                                raise ValueError(f"Value must be one of: {', '.join(expected_type)}")
                        else:
                            try:
                                new_value = expected_type(new_value)
                            except ValueError:
                                if expected_type is int:
                                    raise ValueError("Please enter a number.")
                                else:
                                    raise ValueError(f"Please enter a value of type {expected_type.__name__}.") 

                        current_level[matching_key] = new_value
                        with open("config.json", "w") as f:
                            json.dump(self.settings, f, indent=4)
                        load_settings(self)
                        cprint.success(f"Setting '{choice}' updated successfully!")
                        break
                    else:
                        current_level = current_level[matching_key]
                        schema_level = schema_level[matching_key]
            except ValueError as e:
                cprint.error(e)
            except Exception as e:
                cprint.error(f"An error occurred: {e}")
            time.sleep(1.5)

def setup(self):
    settings_main = self.settings.get("Main")
    settings_towers = self.settings.get("Towers")
    settings_mines = self.settings.get("Mines")
    settings_plinko = self.settings.get("Plinko")
    settings_slides = self.settings.get("Slides")
    settings_crash = self.settings.get("Crash")
    settings_ann = settings_crash.get("ANN")

    self.bet_amt = settings_main.get("Bet_Amount")
    self.click_amt = settings_main.get("Click_Amount")
    self.stop_amt = settings_main.get("Stop_Amount")
    self.if_double = settings_main.get("Double_Bet").get("Enabled")
    self.max_double = settings_main.get("Double_Bet").get("Max_Double") 
    self.on_loss = settings_main.get("Double_Bet").get("On_Loss") 
    self.difficulty = settings_towers.get("Difficulty").lower()
    self.bomb_amt = settings_mines.get("Mines_Amount")
    self.mines_algo = settings_mines.get("Algorithm").lower()
    self.op_color = settings_slides.get("Opposite_Color")
    self.plinko_difficulty = settings_plinko.get("Difficulty").lower()
    self.plinko_row = settings_plinko.get("Row")
    self.auto_cashout = settings_crash.get("Auto_Cashout")
    self.crash_model = settings_ann.get("Model").lower()
    self.ann_enabled = settings_ann.get("Enabled")

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