from enum import Enum
from random import randint, choice
from copy import copy

E, B1, L, M, B2, START, END = ' ', 'B1', 'L', 'M', 'B2', 'ST', 'END'


class RestaurantEnvironment():
    def __init__(self, initial_state=None):
        if initial_state is None:
            self.__initial_state = [E for n in range(25)]
            self.__initial_state[11] = B1
            self.__initial_state[21] = M
            self.__initial_state[8] = L
            self.__initial_state[17] = B2
            self.__initial_state[0] = START
            self.__initial_state[24] = END
            self.__possible_states = []
            self.playerState = [0, ""]
            self.reward = 0
        else:
            self.__initial_state = copy(initial_state)
            self.__state = self.__initial_state

    def reset(self):
        self.__state = self.__initial_state
        return self.__state

    # Based on playerposition (0 to 24), add a letter to the currentWord
    def calculate_curr_word(self, playerPosition):
        if playerPosition == 11:
            return "B"
        elif playerPosition == 21:
            return "U"
        elif playerPosition == 8:
            return "R"
        elif playerPosition == 17:
            return "G"

    def step(self, playerPosition):
        if (self.calculate_curr_word(playerPosition)) is not None:
            self.playerState[1] += self.calculate_curr_word(playerPosition)
            self.reward += 1
        else:
            self.reward -= 0.1
        self.playerState[0] = playerPosition
        observation = self.__state  # environment is fully observable
        done = self.get_killed_or_live()
        info = {}  # optional debug info
        return observation, done, info

    def render(self):
        BACKGROUND = [
            '  │   │   │   │   ',
            '───┼───┼───┼───┼───',
            '   │   │   │ L │   ',
            '───┼───┼───┼───┼───',
            '   │ B│   │   │   ',
            '───┼───┼───┼───┼───',
            '   │   │ B│   │   ',
            '───┼───┼───┼───┼───',
            '   │ M │   │   │ E '
        ]
        rendering = copy(BACKGROUND)
        for n, S_n in enumerate(self.__state):
            if S_n != E:
                row = 2 * (n // 5)
                col = 4 * (n % 5) + 1
                line = rendering[row]
                rendering[row] = line[:col] + S_n + line[col + 1:]

        for line in rendering:
            print(line)

    # =========================================================
    # public functions for agent to calculate optimal policy
    # =========================================================

    def get_possible_actions(self):
        if self.playerState[0] in (6, 7, 8, 11, 12, 13, 16, 17, 18):
            return [self.playerState[0] + 1, self.playerState[0] - 1, self.playerState[0] - 5, self.playerState[0] + 5]
        elif self.playerState[0] in (1, 2, 3):
            return [self.playerState[0] + 1, self.playerState[0] - 1, self.playerState[0] + 5]
        elif self.playerState[0] in (5, 10, 15):
            return [self.playerState[0] + 5, self.playerState[0] - 5, self.playerState[0] + 1]
        elif self.playerState[0] in (9, 14, 19):
            return [self.playerState[0] + 5, self.playerState[0] - 5, self.playerState[0] - 1]
        elif self.playerState[0] in (21, 22, 23):
            return [self.playerState[0] + 1, self.playerState[0] - 5, self.playerState[0] - 1]
        elif self.playerState[0] == 0:
            return [self.playerState[0] + 1, self.playerState[0] + 5]
        elif self.playerState[0] == 4:
            return [self.playerState[0] - 1, self.playerState[0] + 5]
        elif self.playerState[0] == 20:
            return [self.playerState[0] + 1, self.playerState[0] - 5]
        elif self.playerState[0] == 24:
            return 24

    def get_step_probability(self, new_state, inventory):
        new_states = self.get_possible_actions()
        if new_states.__contains__(new_state):
            if new_state == 8:
                if self.playerState[1] == "BU" and inventory == "R":      # HUGE QUESTION ? -> self.playerState[1] == "" and inventory == "R" return 1/0?
                    return 1
                else:
                    return 0
            elif new_state == 11:
                if self.playerState[1] == "" and inventory == "B":
                    return 1
                else:
                    return 0
            elif new_state == 17:
                if self.playerState[1] == "BUR" and inventory == "G":
                    return 1
                else:
                    return 0
            elif new_state == 21:
                    if self.playerState[1] == "B" and inventory == "U":
                        return 1
                    else:
                        return 0
            elif self.playerState[1] == inventory :
                return 1
            else:
                return 0
        else:
            return 0

    def get_killed_or_live(self):  # B
        # Reward R(s) for every possible state
        # Current word must be stored somewhere else
        # B, BU, BUR, BURG
        if self.playerState[1] != "B" or "BU" or "BUR" or "BURG":
            return False
        return True

    def get_transition_prob(self, action, new_state, old_state=None):
        # returns the Transition Probability P(s'| s, a)
        # with s = old_state, a = action and s' = new_state

        # # if the game is over, no transition can take place
        # if self.is_done(old_state):
        #     return 0.0
        #
        # # the position of the action must be empty
        if self.get_killed_or_live():
            self.reset()
            return 0.0

        # check if game is done
        if not self.get_killed_or_live():
            self.reset()
            return 1.0

        # game is not done: calculate all possible states of the opponent
        possible_new_states = []
        possible_new_states = self.get_possible_actions()
        # for action in possible_new_states:
        #     possible_new_state = copy(state_after_X)
        #     possible_new_state[action] = O
        #     possible_new_states.append(possible_new_state)
        if new_state not in possible_new_states:
            return 0.0

        # transition is possible, apply strategy:
        # random opponent, probability is 1 / (# of E before placing the new O)
        prob = 1 / (len(possible_new_states))
        return prob


class Game():
    # example of creation of an environment in the default state
    mdp = RestaurantEnvironment()
    mdp.reset()
    mdp.render()
    print(mdp.step(11))
    print(mdp.step(21))
    # print(mdp.step(8))
    print(mdp.step(16))
    print(mdp.playerState[0], mdp.playerState[1])
    print(mdp.get_step_probability(17,"G"))
    print('possible (internal) game states:')


game = Game()
