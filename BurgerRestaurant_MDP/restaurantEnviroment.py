from enum import Enum
from random import randint, choice
from copy import copy

E, X, O = ' ', 'X', 'O'


E, B1 , L , M , B2, START, END = ' ', 'B1', 'L', 'M','B2', 'ST', 'END'


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
            # start with empty board
        else:
            self.__initial_state = copy(initial_state)  # copy to prevent aliassing
        self.__state = self.__initial_state
        self.__possible_states = []
        # self.__calculate_possible_states(self.__initial_state)
        self.currentWord = ""
        self.curPlayerPos = 0


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
        self.currentWord += self.calculate_curr_word(playerPosition)
        observation = self.__state  # environment is fully observable
        done = self.get_killed_or_live(self)
        info = {}  # optional debug info
        return observation, done, info

    def render(self):
        BACKGROUND = [
            ' S │   │   │   │   ',
            '───┼───┼───┼───┼───',
            '   │   │   │ L │   ',
            '───┼───┼───┼───┼───',
            '   │ B1│   │   │   ',
            '───┼───┼───┼───┼───',
            '   │   │ B2│   │   ',
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

    # def get_possible_states(self):
    #     return self.__possible_states

    def get_possible_actions(self):
        if self.curPlayerPos in (6, 7, 8,11,12,13,16,17,18):
            return [self.curPlayerPos + 1, self.curPlayerPos - 1, self.curPlayerPos - 5, self.curPlayerPos + 5]
        elif self.curPlayerPos in (1,2,3):
            return [self.curPlayerPos + 1, self.curPlayerPos - 1, self.curPlayerPos + 5]
        elif self.curPlayerPos in (5, 10, 15):
            return [self.curPlayerPos + 5, self.curPlayerPos -5, self.curPlayerPos + 1]
        elif self.curPlayerPos in (9, 14, 19):
            return [self.curPlayerPos + 5, self.curPlayerPos - 5, self.curPlayerPos - 1]
        elif self.curPlayerPos in (21, 22, 23):
            return [self.curPlayerPos + 1, self.curPlayerPos - 5, self.curPlayerPos - 1]
        elif self.curPlayerPos == 0:
            return [self.curPlayerPos + 1, self.curPlayerPos + 5]
        elif self.curPlayerPos == 4:
            return [self.curPlayerPos - 1, self.curPlayerPos + 5]
        elif self.curPlayerPos == 20:
            return [self.curPlayerPos + 1, self.curPlayerPos - 5]
        elif self.curPlayerPos == 24:
            return 24


    def get_killed_or_live(self):  # B
        # Reward R(s) for every possible state
        # Current word must be stored somewhere else
          # B, BU, BUR, BURG
        if self.currentWord != "B" or "BU" or "BUR" or "BURG":
            return False
        return True

    def get_transition_prob(self, action, new_state, old_state=None):
        # if old_state is None:
        #     old_state = self.__state
        # # returns the Transition Probability P(s'| s, a)
        # # with s = old_state, a = action and s' = new_state

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
    mdp.curPlayerPos = 0
    print(mdp.curPlayerPos)
    print(mdp.get_possible_actions())
    print('possible (internal) game states:')
    # mdp.get_possible_states()

game = Game()