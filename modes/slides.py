from websocket import WebSocketApp
import threading
import json
from src import cprint
from functions import balance, predict
import traceback

class Slides:
    def __init__(self, client, session) -> None:
        self.client = client
        self.joined_game = False
        self.close_conn = False
        self.game_played = 0
        self.session = session
        self.wallet = None
        self.stop_event = threading.Event()

    def connect(self):
        while True:
            if self.close_conn:
                break
            try:
                wsa = WebSocketApp("wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket", header={'Accept-Encoding': 'gzip, deflate, br','Cache-Control': 'no-cache','Connection': 'Upgrade','Pragma': 'no-cache','Upgrade': 'websocket'}, on_open=self.on_open, on_message=self.on_message)
                wsa.run_forever()
            except Exception as e:
                cprint.error(f"WebSocket connection error: {e}")

    def on_message(self, ws, msg):
        if "pingInterval" in msg:
            threading.Thread(target=self.keep_alive, args=(ws, json.loads(msg.replace("0", ""))["pingInterval"])).start()
            ws.send("40/rouletteV2,")

        if "notify-error" in msg:
            data = json.loads(msg.replace("42/rouletteV2,", ""))
            if data[1] == "Your session has expired, please refresh your page!":
                cprint.error("Token is invalid")
            self.close_conn = True
            self.stop_event.set()
            ws.close()

        if "40/rouletteV2" in msg:
            ws.send('42/rouletteV2,["auth","' + self.client.token + '"]')

        if "\"new-round\"" in msg:
            if self.game_played == self.client.game_amount or (self.wallet and float(self.wallet) <= float(self.client.stop_amt)):
                self.close_conn = True
                self.stop_event.set()
                ws.close()
            else:
                cprint.info("Slides game is starting...")
                self.chosen_color = predict.slides()
                cprint.info(f"Next game prediction: {self.chosen_color}.")
                ws.send(f'42/rouletteV2,{json.dumps(["join-game", {"color": self.chosen_color, "betAmount": self.client.bet_amt}])}')

        if "game-join-success" in msg:
            cprint.custom(f"Joined the current slides game on {self.chosen_color}!", "SUCCESS", (0,255,0))
            self.game_played += 1
            self.joined_game = True

        if "game-rolled" in msg:
            try:
                cprint.info("Slides game ended.")
                if self.joined_game:
                    data = json.loads(msg.replace("42/rouletteV2,", ""))[1]
                    wincolor = data["winningColor"]

                    self.wallet = balance.get(self.session)

                    if self.chosen_color != wincolor:
                        cprint.lost(f"Predicted {self.chosen_color} and was {wincolor}..")
                    else:
                        gained = self.client.bet_amt * 2
                        cprint.won(f"Prediction correct ({self.chosen_color})! Got {gained:.2f} R$!\n")
                else:
                    cprint.info("Did not join this slides game.\n")
            except:
                traceback.print_exc()

    def keep_alive(self, ws, interval):
        while not self.stop_event.is_set():
            ws.send("2")
            self.stop_event.wait(interval)

    def on_open(self, _):
        cprint.info("Connected to slides game mode!\n")