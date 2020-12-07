import random

from agent import Agent
from communicationAPI import CommunicationAPI
from map import Map


class Game:
    def __init__(self, world, agent):
        self.my_cities = []
        self.opp_cities = []
        self.score = 0
        self.opp_score = 0
        self.resources = {'water': 0, 'dust': 0, 'sheep': 0, 'wood': 0, 'wheat': 0, 'clay': 0, 'iron': 0}
        self.my_roads = []
        self.opp_roads = []
        self.map = world
        self.agent = agent
        self.position = None
        self.opp_position = None

    def build_town(self):

        if self.check_build_cities(self.position):
            self.my_cities.append((self.position, 1))
            self.score += 1

            self.resources['sheep'] -= 100
            self.resources['wood'] -= 100
            self.resources['wheat'] -= 100
            self.resources['clay'] -= 100

    def build_road(self):

        if self.check_road():
            (position, end) = self.choose_road(self.position)
            if (position, end) != (None, None):
                self.my_roads.append((position, end))

                self.resources['wood'] -= 100
                self.resources['clay'] -= 100
                return end

        return self.position

    def upgrade_city(self):

        if self.check_upgrade():
            available_cities = [city for city in self.my_cities if city[1] == 1]
            if len(available_cities) != 0:
                city = random.choice(available_cities)

                index = self.my_cities.index(city)
                self.my_cities[index] = (city[0], 2)

                self.resources['wheat'] -= 200
                self.resources['iron'] -= 300

                self.score += 1
                return city[0]

    def empty(self):
        pass

    def move(self):
        available_roads1 = [end for (start, end) in self.my_roads if start == self.position]
        available_roads2 = [start for (start, end) in self.my_roads if end == self.position]
        available_roads = available_roads1 + available_roads2
        if len(available_roads) != 0:
            self.position = random.choice(available_roads)
        return self.position

    def get_neighbours(self, location):
        return self.map.get_neighbours(location)

    def update_resources(self):
        updated_resources = self.map.get_resources(self.my_cities)
        for key in updated_resources:
            self.resources[key] = self.resources[key] + updated_resources[key]

    def check_build_cities(self, position):

        neighbours = self.get_neighbours(position)

        opp_road_counter = 0
        my_road_counter = 0

        # je li tu vec grad
        if (position, 1) in self.my_cities or (position, 2) in self.my_cities\
                or (position, 1) in self.opp_cities or (position, 2) in self.opp_cities:
            return 0

        for neighbour in neighbours:

            # ima li mojih gradova na susjednom raskršću
            if (neighbour, 1) in self.my_cities or (neighbour, 2) in self.my_cities:
                return 0

            # ima li protivnikovih gradova na susjednom raskršću
            if (neighbour, 1) in self.opp_cities or (neighbour, 2) in self.opp_cities:
                return 0

            # idu li iz mene 2 ceste protivnika
            if (position, neighbour) in self.opp_roads or (neighbour, position) in self.opp_roads:
                opp_road_counter += 1

                if opp_road_counter == 2:
                    return 0

            # idu li iz mene moje ceste
            if (position, neighbour) in self.my_roads or (neighbour, position) in self.my_roads:
                my_road_counter += 1

        # ako nisu prva dva grada
        if len(self.my_cities) >= 2:
            # imamo li cestu
            if my_road_counter == 0:
                return 0

            # imamo li dovoljno resursa za grad
            if (self.resources['sheep'] >= 100 and self.resources['wood'] >= 100
                    and self.resources['wheat'] >= 100 and self.resources['clay'] >= 100):
                return 1
            else:
                return 0
    
    def check_upgrade(self):
        enough_resources = self.resources['wheat'] >= 200 and self.resources['iron'] >= 300
        upgraded_cities = len([i for (_, i) in self.my_cities if i == 2])
        return 1 if (enough_resources and (upgraded_cities < len(self.my_cities))) else 0
    
    def is_water(self, start, end):
        return self.map.is_water(start, end)

    def check_road(self):

        neighbours = self.get_neighbours(self.position)
        enough_resources = self.resources['wood'] >= 100 and self.resources['clay'] >= 100

        location_validation = []
        for neighbour in neighbours:
            road_condition = True
            opp_city_condition = True
            opp_roads_condition = True
            water = True

            # ako je tu vec moja cesta
            if (self.position, neighbour) in self.my_roads or (neighbour, self.position) in self.my_roads:
                road_condition = False

            # ako je tu neprijateljeva cesta
            if (self.position, neighbour) in self.opp_roads or (neighbour, self.position) in self.opp_roads:
                road_condition = False

            # ako je tu neprijateljev grad
            if (neighbour, 1) in self.opp_cities or (neighbour, 2) in self.opp_cities:
                opp_city_condition = False

            # ako iz krajnje tocke idu dvije neprijateljeve ceste
            if len([(start, end) for (start, end) in self.opp_roads if start == neighbour or end == neighbour]) >= 2:
                opp_roads_condition = False

            # ako su obje tocke uz vodu
            if self.is_water(self.position, neighbour):
                water = False

            location_validation.append(water and road_condition and opp_roads_condition and opp_city_condition)

        return 1 if enough_resources and any(location_validation) else 0

    def choose_road(self, position):
        neighbours = self.map.get_neighbours(position)
        possible_roads = []

        for neighbour in neighbours:
            if not((position, neighbour) in self.my_roads or (position, neighbour) in self.opp_roads
                   or (neighbour, position) in self.my_roads or (neighbour, position) in self.opp_roads
                   or (neighbour, 1) in self.opp_cities or (neighbour, 2) in self.opp_cities):
                neighbours_neighbours = self.map.get_neighbours(neighbour)
                opponent_roads = 0
                for neighbour2 in neighbours_neighbours:
                    if (neighbour, neighbour2) in self.opp_roads or (neighbour2, neighbour) in self.opp_roads:
                        opponent_roads += 1
                if opponent_roads < 2:
                    possible_roads.append((position, neighbour))
        if len(possible_roads) == 0:
            return None, None

        return random.choice(possible_roads)

    def reset(self):
        self.my_cities = []
        self.opp_cities = []
        self.score = 0
        self.opp_score = 0
        self.resources = {'water': 0, 'dust': 0, 'sheep': 0, 'wood': 0, 'wheat': 0, 'clay': 0, 'iron': 0}
        self.my_roads = []
        self.opp_roads = []
        self.position = None
        self.opp_position = None
        
    def configure_state(self):
        return self.check_build_cities(self.position), self.check_upgrade(), self.check_road()

    def initial_move(self, is_first):
        starting_positions = [24, 25, 26, 27, 28, 42, 43, 58, 57, 71, 70, 69, 68, 67, 53, 52, 37, 38, 39, 40, 41, 54,
                              55, 56]

        position = random.choice(starting_positions)
        neighbour = random.choice(self.map.get_neighbours(position))

        current_resources = [key for key in self.resources.keys() if self.resources[key] != 0]
        new_all_resources = self.map.get_resources([(position, 1)])
        new_resources = [key for key in new_all_resources.keys() if new_all_resources[key] != 0]
        resources = current_resources + new_resources

        if is_first:
            self.position = position
            wanted_resources = len(set(resources)) == 3 and 'dust' not in resources
            while not wanted_resources:
                position = random.choice(starting_positions)
                neighbour = random.choice(self.map.get_neighbours(position))
                resources = self.map.get_resources([(position, 1)])
                resources = [key for key in resources.keys() if resources[key] != 0]
                wanted_resources = len(set(resources)) == 3 and 'dust' not in resources
                self.position = position
        else:
            wanted_resources = len(set(resources)) >= 5
            while self.check_build_cities(position) == 0 or not wanted_resources:
                position = random.choice(range(0, 96))
                neighbour = random.choice(self.map.get_neighbours(position))
                new_all_resources = self.map.get_resources([(position, 1)])
                new_resources = [key for key in new_all_resources.keys() if new_all_resources[key] != 0]
                resources = current_resources + new_resources
                wanted_resources = len(set(resources)) >= 5

        self.my_cities.append((position, 1))
        self.my_roads.append((position, neighbour))
        self.score += 1
        return 'initial ' + str(position) + ' ' + str(neighbour)

    def update_state_after_my_action(self, action):
        new_position = self.position
        if action == 'buildtown':
            self.build_town()
        elif action == 'buildroad':
            new_position = self.build_road()
        elif action == 'upgradetown':
            new_position = self.upgrade_city()
        elif action == 'move':
            new_position = self.move()
        else:
            self.empty()

        return self.configure_state(), new_position

    def update_state_after_opp_action(self, opp_action):
        opp_actions = opp_action.split(' ')
        if opp_actions[0] == 'buildtown':
            self.opp_cities.append((int(opp_actions[1]), 1))
            self.opp_score += 1
        elif opp_actions[0] == 'upgradetown':
            for city in self.opp_cities:
                if city[0] == int(opp_actions[1]):
                    index = self.opp_cities.index(city)
                    self.opp_cities[index] = (city[0], 2)
                    self.opp_score += 1
        elif opp_actions[0] == 'buildroad':
            self.opp_roads.append((int(self.opp_position), int(opp_actions[1])))
        elif opp_actions[0] == 'move':
            self.opp_position = int(opp_actions[1])

        return self.configure_state()

    def initial_move_opponent(self, actions):
        opp_actions = actions.split(' ')
        if opp_actions[0] == 'initial':
            self.opp_cities.append((int(opp_actions[1]), 1))
            self.opp_roads.append((int(opp_actions[1]), int(opp_actions[2])))
            self.opp_score += 1
            self.opp_position = int(opp_actions[1])
            if opp_actions[3] == 'initial':
                self.opp_cities.append((int(opp_actions[4]), 1))
                self.opp_roads.append((int(opp_actions[4]), int(opp_actions[5])))
                self.opp_score += 1
            else:
                self.update_state_after_opp_action(opp_actions[3] + ' ' + opp_actions[4] + ' ' + opp_actions[5])

    def is_terminated(self):
        return self.score == 16 or self.opp_score == 16

    def train(self, file=None):
        agent = Agent(epsilon=0.4, gamma=0.9, alpha=1, file=file)
        communicationAPI = CommunicationAPI(is_train_mode=True)

        playerID = 1 if random.random() < 0.5 else 2
        self.reset()
        response = communicationAPI.start_training(playerID)
        self.map.configure(response)
        self.update_resources()

        if playerID == 1:
            print('Igrač 1')
            self.initial_move_opponent(communicationAPI.do_action(playerID, 1, self.initial_move(is_first=True)))
            self.update_resources()
            communicationAPI.do_action(playerID, 1, self.initial_move(is_first=False))
        else:
            print('Igrač 2')
            communicationAPI.do_action(playerID, 1, self.initial_move(is_first=True))
            self.update_resources()
            self.initial_move_opponent(communicationAPI.do_action(playerID, 1, self.initial_move(is_first=False)))

        print('Jebal ga vrag')
        state = self.configure_state()
        while not self.is_terminated():
            self.update_resources()
            action = agent.get_action(state)
            reward = agent.get_reward(state, action)
            new_state, new_position = self.update_state_after_my_action(action)

            send_action = action
            if action == 'move' or action == 'buildroad' or action == 'upgradetown':
                if new_position is not None:
                    send_action = send_action + ' ' + str(new_position)

            self.update_resources()
            opp_action = communicationAPI.do_action(playerID, 1, send_action)
            new_state = self.update_state_after_opp_action(opp_action)
            agent.update(state, action, new_state, reward)
            state = new_state

        agent.write_to_file()

    def run(self):
        agent = Agent(epsilon=0.1, gamma=0.9, alpha=1, file='qValues.txt')

        playerID = input()
        gameID = input()
        
        communicationAPI = CommunicationAPI(is_train_mode=False)
        response = communicationAPI.join_game(playerID, gameID)
        self.map.configure(response)

        if playerID == 1:
            self.initial_move_opponent(communicationAPI.do_action(playerID, gameID, self.initial_move(is_first=True)))
            self.update_resources()
            communicationAPI.do_action(playerID, 1, self.initial_move(is_first=False))
        else:
            communicationAPI.do_action(playerID, 1, self.initial_move(is_first=True))
            self.update_resources()
            self.initial_move_opponent(communicationAPI.do_action(playerID, gameID, self.initial_move(is_first=False)))

        state = self.configure_state()
        while not self.is_terminated():
            self.update_resources()
            action = agent.get_action(state)
            new_state, new_position = self.update_state_after_my_action(action)

            send_action = action
            if action == 'move' or action == 'buildroad' or action == 'upgradetown':
                if new_position is not None:
                    send_action = send_action + ' ' + str(new_position)

            self.update_resources()
            opp_action = communicationAPI.do_action(playerID, 1, send_action)
            new_state = self.update_state_after_opp_action(opp_action)
            state = new_state


if __name__ == '__main__':
    game = Game(Map(), Agent(epsilon=0.1, gamma=0.9, alpha=1))
    game.train()
                

            
        

            
            

            

            
            




    


    

    