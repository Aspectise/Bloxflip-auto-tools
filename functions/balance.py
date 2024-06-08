import asyncio

async def get(session):
    async with session.get("https://api.bloxflip.com/user", ssl=False) as response:
        if response.status == 200:
            data = await response.json()
            return data.get("user").get("wallet") + data.get("user").get("bonusWallet")
        else:
            return None
        
def get2(session):
    wallet = asyncio.run(get(session))
    return wallet