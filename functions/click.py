def start(session, _type, _data):
    response = session.post(f'https://api.bloxflip.com/games/{_type}/action', json=_data)
    return response.json()