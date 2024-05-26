# Bloxflip-auto-tools
Bloxflip auto tools is the best free bloxflip bot that automatically plays a variety of bloxflip game modes (Mines, Towers, Plinko, Crash)!
## Next update at 50 ⭐
+ Better crash prediction
+ Stop amount for crash

### Features:
- [x] - **Open Source**
- [x] - **Free**
- [x] - **Well Managed**
- [x] - **Supported Game-Modes: Mines, Towers, Plinko, Crash**
- [x] - **Plays Automatically**
- [x] - **Very Customizable**
- [x] - **Display information about the current games**
- [x] - **Built in "predictor" for mines**
- [x] - **Using artificial neural network for crash prediction**

## Setup
1. Install python from python.org
2. Open config.json and setup your stuff (every section is documented in red in the code block under this)
3. Open start.bat or main.py
4. Enjoy
```json
{
    "Token": "", Your bloxflip account token, you get it by opening inspect (right click) and going to console then typing "copy(localStorage.getItem('_DO_NOT_SHARE_BLOXFLIP_TOKEN'))", your token has been copied to your clipboard

    "Bet_Amount": 5, Amount to bet every game (All game modes)
    "Click_Amount": 1, Amount of clicks to click (Mines and Towers)
    "Stop_Amount": 100, Amount of robux to stop at when you hit it (All game modes)
    
    "Mines": {
        "Mines_Amount": 3, Amount of Mines to set every game 
        "Safe_Prediction": false Uses a specific method to click if set to true
    },
    "Towers": {
        "Difficulty": "easy" Difficulty level (easy/normal/hard)
    },
    "Plinko": {
        "Difficulty": "easy", Difficulty level (easy/normal/hard)
        "Row": 8 Amount of plinko rows
    }
}

```

## Preview:
![image](https://github.com/Aspectise/Bloxflip-auto-tools/assets/90333100/bfde9447-baad-4567-958a-0b84e72ffe50)

## Information
This project was fully made by me ([Aspect](https://github.com/Aspectise)). Do not try to sell this or repost it without credits ([LICENSE](https://github.com/Aspectise/Bloxflip-auto-mine/blob/main/LICENSE)) 

## ⭐
If you like this project please start it ⭐ 😊

Bloxflip affiliate: https://bloxflip.com/a/aspectise
## Help
If you need help setting up the bot join the [Discord](https://discord.gg/deathsniper)
