import random


class Action:
    MOVE = 'move'
    BUILD_TOWN = 'buildtown'
    BUILD_ROAD = 'buildroad'
    UPGRADE = 'upgradetown'
    EMPTY = 'empty'


class Agent:

    def __init__(self, epsilon=0.05, gamma=0.9, alpha=1, file=None):
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.qValues = dict()

        if file:
            f = open(file)
            line = f.readline()
            while line != '':
                text = line.split(' ')
                state = (text[0], text[1], text[2])
                action = text[3]
                value = text[4]
                self.set_qValue(state, action, value)
                line = f.readline()

    def get_qValue(self, state, action):
        if (state, action) in self.qValues:
            return self.qValues[(state, action)]

        self.qValues[(state, action)] = 0
        return 0

    def set_qValue(self, state, action, value):
        self.qValues[(state, action)] = value

    def compute_value_from_qValues(self, state):
        actions = self.get_legal_actions(state)
        max_value = None

        if len(actions) == 0:
            print('No actions possible.')
            return 0

        for action in actions:
            value = self.get_qValue(state, action)
            if max_value is None or value > max_value:
                max_value = value
        return max_value

    def compute_action_from_qValues(self, state):
        actions = self.get_legal_actions(state)

        best = None
        best_action = ''

        if len(actions) == 0:
            print('No actions possible.')
            return None

        for action in actions:
            value = self.get_qValue(state, action)
            if best is None or value > best:
                best = value
                best_action = action

        return best_action

    def get_action(self, state):
        legal_actions = self.get_legal_actions(state)
        action = None
        if len(legal_actions) == 0:
            return action

        if random.random() < self.epsilon:
            action = random.choice(legal_actions)
        else:
            action = self.compute_action_from_qValues(state)

        return action

    def update(self, state, action, next_state, reward):
        next_state_qValue = self.compute_value_from_qValues(next_state)
        current_state_qValue = self.get_qValue(state, action)
        value = current_state_qValue + self.alpha * (reward + self.gamma * next_state_qValue - current_state_qValue)
        self.set_qValue(state, action, value)

    def get_legal_actions(self, state):
        legal_actions = []
        if state[0] == 1:
            legal_actions.append(Action.BUILD_TOWN)
        if state[1] == 1:
            legal_actions.append(Action.UPGRADE)
        if state[2] == 1:
            legal_actions.append(Action.BUILD_ROAD)

        legal_actions.append(Action.MOVE)
        legal_actions.append(Action.EMPTY)
        return legal_actions

    def get_reward(self, state, action):
        reward = 0
        positive_reward = 5
        negative_reward = -5

        if state == (0, 0, 0):
            if action == 'move':
                reward += positive_reward
            else:
                reward += negative_reward

        elif state == (0, 0, 1):
            if action == 'buildroad':
                reward += positive_reward
            else:
                reward += negative_reward

        elif state == (0, 1, 0):
            if action == 'upgradetown':
                reward += positive_reward
            else:
                reward += negative_reward

        elif state == (0, 1, 1):
            if action == 'upgradetown':
                reward += positive_reward
            elif action == 'buildroad':
                reward += positive_reward*0.5
            else:
                reward += negative_reward

        elif state == (1, 0, 0):
            if action == 'buildtown':
                reward += positive_reward
            else:
                reward += negative_reward

        elif state == (1, 0, 1):
            if action == 'buildtown':
                reward += positive_reward
            elif action == 'buildroad':
                reward += positive_reward*0.5
            else:
                reward += negative_reward

        elif state == (1, 1, 0):
            if action == 'buildtown' or action == 'upgradetown':
                reward += positive_reward
            else:
                reward += negative_reward

        elif state == (1, 1, 1):
            if action == 'buildtown' or action == 'upgradetown':
                reward += positive_reward
            elif action == 'buildroad':
                reward += positive_reward*0.5
            else:
                reward += negative_reward

        if action == 'empty':
            reward += -10

        return reward

    def write_to_file(self):
        file = open('qValues.txt', 'w')
        for key in self.qValues.keys():
            file.write(str(key[0][0]) + ' ' + str(key[0][1]) + ' ' + str(key[0][2]) + ' ' + str(key[1]) + ' ' + str(self.qValues[key]) + '\n')
