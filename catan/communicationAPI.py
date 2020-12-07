import requests


class CommunicationAPI:

    def __init__(self, is_train_mode):
        self.is_train_mode = is_train_mode

    def get_url(self):
        return 'http://localhost:9080/train' if self.is_train_mode else 'http://localhost:9080'

    def make_get_request(self, relative_url):
        r = requests.get(url=self.get_url() + relative_url)
        data = r.json()
        return data

    def do_action(self, playerID, gameID, action):
        URL = '/doAction?playerID=' + str(playerID) + '&gameID=' + str(gameID) + '&action=' + action
        print(URL)
        response = self.make_get_request('/doAction?playerID=' + str(playerID) + '&gameID=' + str(gameID) + '&action=' + action)
        return response['result']

    def join_game(self, playerID, gameID):
        return self.make_get_request('/game/play?playerID=' + str(playerID) + 'gameID=' + str(gameID))

    def start_training(self, playerID):
        return self.make_get_request('/play?playerID=' + str(playerID) + '&gameID=1')

