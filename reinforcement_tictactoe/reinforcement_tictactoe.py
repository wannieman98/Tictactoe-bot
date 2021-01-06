from numpy.lib.polynomial import poly1d
import numpy as np
import pickle

BOARD_WIDTH = 3
BOARD_HEIGHT = 3

class board:
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
        self.isEnd = False
        self.playerSymbol = 1
        self.p1 = p1 
        self.p2 = p2
        self.boardIndex = None
        self.boardHash = None
        self.availablePositions = []
        self.allPositions = []
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.availablePositions.append((x,y))
                self.allPositions.append((x,y))


    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_WIDTH * BOARD_HEIGHT))
        return self.boardHash

    def winner(self):
        for i in range(BOARD_WIDTH):
            if sum(self.board[i,:]) == 3:
                self.isEnd = True
                return 1
            elif sum(self.board[i,:]) == -3:
                self.isEnd = True
                return -1
        for i in range(BOARD_HEIGHT):
            if sum(self.board[:,i]) == 3:
                self.isEnd = True
                return 1
            elif sum(self.board[:,i]) == -3:
                self.isEnd = True
                return -1
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_HEIGHT)])
        diag_sum2 = sum([self.board[i, BOARD_HEIGHT - i - 1] for i in range(BOARD_HEIGHT)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1
        if self.isEnd == False and not self.availablePositions:
            self.isEnd == True
            return 0
        else:
            return None

    def updateState(self, position: tuple):
        self.board[position] = self.playerSymbol
        self.availablePositions.remove(position)
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    def giveReward(self):
        winner = self.winner()
        
        if winner == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(-1)
        elif winner == -1:
            self.p1.feedReward(-1)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)

    def reset(self):
        self.board = np.zeros((BOARD_WIDTH, BOARD_HEIGHT))
        self.isEnd = False
        self.boardHash = False
        self.availablePositions = []
        self.playerSymbol = 1
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.availablePositions.append((x,y))

    def play(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("레벨 {}".format(i))
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                # check board status if it is end

                win = self.winner()
                if win is not None:
                    # self.showBoard()
                    # ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.availablePositions
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)

                    win = self.winner()
                    if win is not None:
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    # play with human
    def play2(self):
        all_positions = self.allPositions
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions
            p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
            # take action and upate board state
            self.updateState(p1_action)
            self.showBoard()
            # check board status if it is end
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions
                p2_action = self.p2.chooseAction(positions, all_positions)

                self.updateState(p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break

    def showBoard(self):
        token = ''
        # p1: x  p2: o
        for i in range(0, BOARD_WIDTH):
            print('-------------')
            out = '| '
            for j in range(0, BOARD_HEIGHT):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')

class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value
    
    def getHash(self, board):
        boardHash = str(board.reshape(BOARD_WIDTH * BOARD_HEIGHT))
        return boardHash

    def chooseAction(self, positions, current_board, symbol):
        action = None
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
        # print("{} takes action {}".format(self.name, action))
        return action

    # append a hash state
    def addState(self, state):
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def chooseAction(self, positions, all_positions):
        while True:
            input_number = int(input("Input your action position:")) - 1
            action = all_positions[input_number]
            if action in positions:
                return action
            else:
                print("Already taken, please take another action.")


    # append a hash state
    def addState(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        pass

    def reset(self):
        pass


if __name__ == "__main__":
    # training
    p1 = Player("p1")
    p2 = Player("p2")

    st = board(p1, p2)
    print("컴퓨터 진화중...")
    st.play(50000)
    p1.savePolicy()
    p2.savePolicy()

    # play with human
    computer = Player("computer", exp_rate=0)
    computer.loadPolicy("policy_p1")

    human = HumanPlayer("human")

    st = board(computer, human)
    st.play2()
    