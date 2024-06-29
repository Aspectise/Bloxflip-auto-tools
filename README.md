# 🚀 Bloxflip-auto-tools  🤖

**Bloxflip auto tools** is the best free Bloxflip bot that automatically plays a variety of game modes (Mines, Towers, Plinko, Crash, Slides)!  

<p align="center">
  <a href="https://github.com/Aspectise/Bloxflip-auto-tools/issues"><img alt="Issues" src="https://img.shields.io/github/issues/Aspectise/Bloxflip-auto-tools?style=for-the-badge"></a>
  <a href="https://github.com/Aspectise/Bloxflip-auto-tools/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Aspectise/Bloxflip-auto-tools?style=for-the-badge"></a>
  <a href="https://github.com/Aspectise/Bloxflip-auto-tools/network/members"><img alt="Forks" src="https://img.shields.io/github/forks/Aspectise/Bloxflip-auto-tools?style=for-the-badge"></a>
  <a href="https://github.com/Aspectise/Bloxflip-auto-tools/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Aspectise/Bloxflip-auto-tools?style=for-the-badge"></a>
</p>

<p align="center">
  <img src="https://github.com/Aspectise/Bloxflip-auto-tools/assets/90333100/ec9b0af4-7af0-4910-aa06-e3a06b52134c" alt="Bloxflip Bot Preview">
</p>

## 🌟 Next Update at 85 Stars 🌟
+ 🔮 Another Mines algorithm
+ ⛏️ Improved Slides algorithm 

## ✨ Features:

-  🆓 **Free and Open Source**
-  😂 **Not a Logger:** Very rare for bloxflip tools.
-  🎮 **Supported Game Modes:** Mines, Towers, Plinko, Crash, Slides
-  ⚙️ **Automatic Gameplay**
-  🔧 **Highly Customizable:** Configure settings to your liking.
-  📈 **Real-time Information:** Track game progress and stats.
-  🧠 **Mines and Slides Algorithm:** Get an edge in Mines and Slides.
-  🤖 **Crash Prediction with ANN:** Try to predict Crash outcomes!

## 🚀 Quick Setup:

1. **Download Python:** [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. **Configure the Bot:** Open `config.json` and enter your Bloxflip token and adjust settings.
3. **Run the Bot:** Double-click `start.bat` (or run `main.py` from your terminal). 
4. **Enjoy!** 🎉

## 📺 Video Setup:

- https://www.youtube.com/watch?v=PAynRn7K4hw

## ⚙️ Detailed Setup Instructions  
Click to expand 👇
<details>
<summary> </summary> 

### Installation
1. **Install python:**
   This project is powered by Python.  Make sure you have it installed:

   - **Download:** Head to [https://www.python.org/downloads/](https://www.python.org/downloads/) and grab the latest version.
   - **Installation:** Run the installer and **check the "Add Python to PATH" box** during setup.
3. **Clone/Download the repository:**
   Choose your preferred method to get the project files:

   - **Git Clone (Recommended for Developers):**
     ```bash
     git clone https://github.com/Aspectise/Bloxflip-auto-tools.git
     cd Bloxflip-auto-tools
     ```

   - **Direct Download (ZIP Archive):**
     [Download](https://github.com/Aspectise/Bloxflip-auto-tools/archive/refs/heads/main.zip) and **extract** the contents to your desired location.
5. **Install dependencies:**
   - **Open a terminal in the repository folder then paste this:**
     ```bash
     pip install -r requirements.txt
     ```
     
   - **Open `start.bat`.**
### Configuration

1. **Obtain your BloxFlip token:**
   - Open the Bloxflip website ([https://bloxflip.com/](https://bloxflip.com/)) and log in.
   - Open your browser's developer console (usually by pressing F12).
   - Navigate to the "Console" tab.
   - Paste and execute the following code:
     ```javascript
     copy(localStorage.getItem('_DO_NOT_SHARE_BLOXFLIP_TOKEN'))
     ```
   - Your token is now copied to your clipboard.

2. **Edit `config.json`:**
   - Open `config.json` thats located in the project directory.
   - Then, customize the values according to the descriptions below:

### Configuration Settings Explained

   - **`Token`:** **(Required)** Your unique Bloxflip account token. Obtain this from your browser's console using the JavaScript code provided above. 
   
   - **`Main` Settings:** These settings apply to all game modes.
      - **`Bet_Amount`:** The initial amount of Robux the bot will bet on each game.
      - **`Click_Amount`:**  (Mines and Towers only) The number of times the bot will click in Mines or select a tower block in Towers.
      - **`Stop_Amount`:**  If the bot's Robux balance reaches this amount, it will stop playing.
      - **`Double_Bet`:** 
          - **`Enabled`:**  If set to `true`, the bot will double its bet after every win and reset to the original `Bet_Amount` on a loss.
          - **`On_Loss`:**  If set to `true`, the bot will double its bet after every lost and reset to the original `Bet_Amount` on a win.
          - **`Max_Double`:** The maximum bet amount the bot will reach when doubling bets. 

   - **`Mines` Settings:** 
      - **`Mines_Amount`:**  The number of mines the bot will place in each Mines game.
      - **`Algorithm`:** The algorithm to use for predictions (options: "random", "safe", "last_game").

   - **`Towers` Settings:**
      - **`Difficulty`:**  Sets the difficulty of the Towers game (options: "easy", "normal", "hard").

   - **`Plinko` Settings:**
      - **`Difficulty`:** Sets the difficulty of the Plinko game (options: "easy", "normal", "hard").
      - **`Row`:**  The number of rows the Plinko board should have.

   - **`Slides` Settings:**
      - **`Opposite_Color`:** If set to `true`, the bot will chose the opposite color of the last slides game.

   - **`Crash` Settings:**
      - **`Auto_Cashout`:**  The multiplier at which the bot will automatically cash out in Crash.
      - **`ANN` (Artificial Neural Network):**
         - **`Enabled`:** If `true`, the bot will use an ANN to try to predict the Crash outcome. 
            **Note:** Crash predictions are not 100% accurate.
         - **`Model`:** The type of ANN model to use for predictions (options: "random_forest", "linear", "svr").

### Running the Bot

```bash
python main.py 
```

### Disclaimer

- This bot is provided for educational purposes only. 
- Using this bot to automate gameplay on BloxFlip may be against their terms of service. 
- Use at your own risk.

</details>


## 🤝 Contributing

Contributions are welcome! If you like this project please consider giving it a star ⭐ 

**⚠️ Important:**  This project is licensed under the [LICENSE](https://github.com/Aspectise/Bloxflip-auto-tools/blob/main/LICENSE) file. Please respect the license terms. Skidding or redistributing this code as your own is not cool. If you want to use parts of the code, give credit where it's due.


## ⭐️ Show Your Support

If you like this project, give it a star! ⭐

**Bloxflip Affiliate Link:** [https://bloxflip.com/a/aspectise](https://bloxflip.com/a/aspectise)


##  📞 Contact

[![Discord](https://img.shields.io/discord/1117281066923872266?style=for-the-badge&logo=discord)](https://discord.gg/deathsniper)
