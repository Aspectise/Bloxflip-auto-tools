def get(session):
    response = session.get("https://api.bloxflip.com/user")
    if response.status_code == 200:
        data = response.json()
        return data.get("user").get("wallet") + data.get("user").get("bonusWallet")
    else:
        return None