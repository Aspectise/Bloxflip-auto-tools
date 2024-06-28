from rgbprint import Color, rgbprint
from datetime import datetime
import os
import ctypes
import shutil

def info(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Color(190, 190, 190)}{timestamp} > {Color(127, 127, 127)}INFO{Color(255, 255, 255)} | {text}")

def won(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Color(190, 190, 190)}{timestamp} > {Color(0, 255, 0)}WON{Color(255, 255, 255)} | {text}")

def success(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Color(190, 190, 190)}{timestamp} > {Color(0, 255, 0)}SUCCESS{Color(255, 255, 255)} | {text}")

def warn(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Color(190, 190, 190)}{timestamp} > {Color(255, 100, 0)}WARNING{Color(255, 255, 255)} | {text}")

def lost(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Color(190, 190, 190)}{timestamp} > {Color(255, 0, 0)}RIP{Color(255, 255, 255)} | {text}")

def error(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Color(190, 190, 190)}{timestamp} > {Color(255, 0, 0)}ERROR{Color(255, 255, 255)} | {text}")

def user_input(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    choice = input(f"{Color(190, 190, 190)}{timestamp} > {Color(0, 128, 255)}INPUT{Color(255, 255, 255)} | {text}").lower()
    return choice

def custom(text, tag, color):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Color(190, 190, 190)}{timestamp} > {Color(*color)}{tag}{Color(255, 255, 255)} | {text}")

def header(banner=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    if os.name == "nt":ctypes.windll.kernel32.SetConsoleTitleW("Bloxflip-Auto-Tools | made by Aspectise")
    VERSION = 7.5
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
    ╔═{"═" * (len(TEXT_IN_BOX) + len(str(VERSION)) + 1)}═╗
    ║ {TEXT_IN_BOX} {str(VERSION)} ║
    ╚═{"═" * (len(TEXT_IN_BOX) + len(str(VERSION)) + 1)}═╝
    """

    OPTIONS: dict[str, str] = {
"01": "Mines",
"02": "Towers",
"03": "Plinko",
"04": "Crash",
"05": "Slides",
"06": "Settings",
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