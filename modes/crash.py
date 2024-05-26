from websocket import WebSocketApp
import threading
import json
from src import cprint
from functions import predict

class Crash:
    def __init__(self, client) -> None:
        self.client = client
        self.joined_game = False
        self.close_conn = False
        self.game_played = 0
        self.cashout_point = None
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
            ws.send("40/crash,")

        if "notify-error" in msg:
            data = json.loads(msg.replace("42/crash,", ""))
            if data[1] == "Your session has expired, please refresh your page!":
                cprint.error("Token is invalid")
            self.close_conn = True
            self.stop_event.set()
            ws.close()

        if "40/crash" in msg:
            ws.send('42/crash,["auth","' + self.client.token + '"]')

        if "\"game-starting\"" in msg:
            if self.game_played == self.client.game_amount:
                self.close_conn = True
                self.stop_event.set()
                ws.close()
            else:
                cprint.info("Crash game is starting...")
                if self.cashout_point is None:
                    if not self.client.ann_enabled:
                        self.cashout_point = self.client.auto_cashout
                    else:
                        self.cashout_point = predict.start(self.client.crash_model)
                        self.cashout_point = float(f"{self.cashout_point:.2f}")
                        cprint.info(f"Next game prediction: {self.cashout_point}x")
                ws.send('42/crash,["join-game",{"autoCashoutPoint":' + str(int(self.cashout_point * 100)) + ', "betAmount":' + str(self.client.bet_amt) + '}]')

        if "\"game-start\"" in msg:
            cprint.info("Crash game in-progress...")

        if "game-join-success" in msg:
            cprint.custom(f"Joined the current crash game on {self.cashout_point}x!", "SUCCESS", (0,255,0))
            self.game_played += 1
            self.joined_game = True

        if "game-end" in msg:
            cprint.info("Crash game ended.")
            if self.joined_game:
                data = json.loads(msg.replace("42/crash,", ""))[1]
                if data.get("crashPoint") < self.cashout_point:
                    cprint.lost(f"Crash game ended at: {data.get('crashPoint')}x | Goal: {self.cashout_point}x\n")
                else:
                    gained = self.client.bet_amt * self.cashout_point
                    cprint.won(f"Crash game ended at: {data.get('crashPoint')}x | Cashed out at: {self.cashout_point}x | Profit: {gained:.2f} R$\n")
            else:
                cprint.info("Did not join this crash game.\n")

            if not self.client.ann_enabled:
                self.cashout_point = self.client.auto_cashout
            else:
                self.cashout_point = predict.start(self.client.crash_model)
                self.cashout_point = float(f"{self.cashout_point:.2f}")
                cprint.info(f"Next game prediction: {self.cashout_point}x")

    def keep_alive(self, ws, interval):
        while not self.stop_event.is_set():
            ws.send("2")
            self.stop_event.wait(interval)

    def on_open(self, _):
        cprint.info("Connected to crash game mode!\n")