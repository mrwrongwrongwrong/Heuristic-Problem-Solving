import json
# from random import choice
import random
from hps.clients import SocketClient
from time import sleep
import argparse
from copy import deepcopy

HOST = 'localhost'
PORT = 5000
SLOW = False


class NoTippingClient(object):
    def __init__(self, name, is_first):
        self.first_resp_recv = False
        self.name = name
        self.client = SocketClient(HOST, PORT)
        self.client.send_data(
            json.dumps({
                'name': self.name,
                'is_first': is_first
            }))
        response = json.loads(self.client.receive_data())
        self.board_length = response['board_length']
        self.num_weights = response['num_weights']
        self.myWeight = dict()
        for i in range(1, int(self.num_weights) + 1):
            self.myWeight[i] = 1

        self.dp_value = dict()
        self.tp_position_list = []

    def play_game(self):
        response = {}
        while True:
            response = json.loads(self.client.receive_data())
            if 'game_over' in response and response['game_over'] == "1":
                print("Game Over!")
                exit(0)

            self.board_state = list(
                map(int, response['board_state'].strip().split(' ')))

            print(self.board_state)

            # sleeps 2 seconds
            #if SLOW:
            #    sleep(2)

            if response['move_type'] == 'place':
                position, weight = self.place_local(self.board_state)
                self.myWeight[weight] = 0
                self.client.send_data(
                    json.dumps({
                        "position": position,
                        "weight": weight
                    }))
            else:
                position = self.remove_local(self.board_state)
                self.client.send_data(json.dumps({"position": position}))

    def place(self, board_state):
        """
        Inputs:
        current_board_state - array of what weight is at a given position on the board

        Output:
        position (Integer), weight (Integer)
        """

        allPosition = []
        for key, value in self.myWeight.items():
            if value == 1:
                position = self.find_place_position(key, self.board_state)
                if position != -100:
                    allPosition.append((position - 30, key))
        if len(allPosition) == 0:
            choice = (0, 1)
        else:
            choice = random.choice(allPosition)
        self.myWeight[choice[1]] = 0
        print("Added: " + str(choice))
        return choice[0], choice[1]

    def place_local(self, board_state_1):
        #use mylist and opponent's list to calculate the possbile moves
        opponent_possible_torques = []
        my_possible_torques = []
        #board_state_1 = deepcopy(self.board_state)
        board_state = deepcopy(board_state_1)
        #if len(self.myWeight) != 0:
        if self.check_dictonary(self.myWeight) == True:
            mycard = deepcopy(self.myWeight)
            mycard = self.dict_to_list(mycard)
            opponent_card = self.calculate_opponent_list(board_state)
            self.tp_position_list = []
            x= self.dp2(mycard,opponent_card,board_state) #weight
            tp_position_to_play = deepcopy(self.tp_position_list[0]) - 30 #the length is from 0 to 61, however, the actual position is from -30 to +30
            choice = (tp_position_to_play, x)
            #send x to corresponding moves
            print("Added: " + str(choice))
            print('this is DP')
            #return choice[0], choice[1]
            return tp_position_to_play, x
        else:
            local_tp_board = self.board_state
            for y in self.myWeight:
                for j in self.board_state:
                    if j == 0:
                        local_tp_board[j] = y
                        if self.check_balance_local(local_tp_board) == True:
                            #choice = (j,y)
                            print("Added: " + str(choice))
                            #return choice[0], choice[1]
                            return j, y
        #self.myWeight[choice[1]] = 0
        #print("Added: " + str(choice))
        #return choice[0], choice[1]

    def remove(self, board_state):
        """
        Inputs:
        current_board_state - array of what weight is at a given position on the board

        Output:
        position (Integer)
        """
        allPossiblePosition = []
        for i in range(0, 61):
            if self.board_state[i] != 0:
                tempWeight = self.board_state[i]
                self.board_state[i] = 0
                if self.check_balance(self.board_state):
                    allPossiblePosition.append(i - 30)
                self.board_state[i] = tempWeight
        if len(allPossiblePosition) == 0:
            choice = 1
        else:
            choice = random.choice(allPossiblePosition)
        print("Removed:" + str(choice))
        return choice

    def check_balance(self, board_state):
        left_torque = 0
        right_torque = 0
        for i in range(0, 61):
            left_torque += (i - 30 + 3) * self.board_state[i]
            right_torque += (i - 30 + 1) * self.board_state[i]
        left_torque += 3 * 3
        right_torque += 1 * 3
        return left_torque >= 0 and right_torque <= 0

    def find_place_position(self, weight, board_state):
        for i in range(0, 61):
            if self.board_state[i] == 0:
                self.board_state[i] = weight
                if self.check_balance(board_state):
                    self.board_state[i] = 0
                    return i
                self.board_state[i] = 0
        return -100

    def find_place_position_local(self, weight, board_state):
        list = []
        for i in range(0, 61):
            if board_state[i] == 0:
                board_state[i] = weight
                if self.check_balance(board_state):
                    board_state[i] = 0
                    list.append(i)
        return list

    def check_balance_local(self, board_state):
        left_torque = 0
        right_torque = 0
        for i in range(0, 61):
            left_torque += (i - 30 + 3) * board_state[i]
            right_torque += (i - 30 + 1) * board_state[i]
        left_torque += 3 * 3
        right_torque += 1 * 3
        return left_torque >= 0 and right_torque <= 0


    def get_torque_value(self, board_state):
        left_torque = 0
        right_torque = 0
        for i in range(0, 61):
            left_torque += (i - 30 + 3) * board_state[i]
            right_torque += (i - 30 + 1) * board_state[i]
        left_torque += 3 * 3
        right_torque += 1 * 3
        return (left_torque - right_torque)

    def get_hash(self,a,b,x):
        mod=1000000007
        a.sort()
        b.sort()
        hash= self.get_torque_value(x)
        for i in a:
            hash=hash*3214567+i
            hash=hash%mod
        for i in b:
            hash=hash*3214567+i
            hash=hash%mod
        return hash

    def dp(self, card1, card2, stones):
        '''
        print("state:")
        print(card1)
        print(card2)
        print(stones)
        '''

        for x in card1:
            if x==stones:
                '''
                print("state:")
                print(card1)
                print(card2)
                print(stones,x)
                '''
                return x
                # card1.remove(x)

        state_hash = self.get_hash(card1,card2,stones)
        if state_hash in self.dp_value:
            return self.dp_value[state_hash]

        tp_card1=deepcopy(card1)
        tp_card2=deepcopy(card2)

        Winning_Strategy=None
        for x in card1:
            if x>stones:
                continue

            card1=deepcopy(tp_card1)
            card2=deepcopy(tp_card2)
            card1.remove(x)
            #print(state_hash,card1,card2,stones,x)

            res = self.dp(card2, card1, stones-x)
            if res==-1:
                self.dp_value[state_hash]=x
                '''
                print("state:")
                print(tp_card1)
                print(tp_card2)
                print(stones,x)
                '''
                return x
                #card1.remove(x)
        self.dp_value[state_hash]=-1
        '''
        print("state:")
        print(tp_card1)
        print(tp_card2)
        print(stones,-1)
        '''
        return -1

    #torque_value = left_torque - right_torque
    def dp2(self, card1, card2, board_state):

        #for x in card1:
        #    if x==stones:
        #        return x
        state_hash = self.get_hash(card1, card2, board_state)
        if state_hash in self.dp_value:
            return self.dp_value[state_hash]

        tp_card1=deepcopy(card1)
        tp_card2=deepcopy(card2)

        Winning_Strategy=None
        #position_list = []
        #position_to_place = 0
        for x in card1:
            position_list = self.find_place_position_local(x,board_state)
            for j in range(len(position_list)):
                current_board_state = deepcopy(board_state)
                current_board_state[position_list[j]] = x

                if self.check_balance_local(current_board_state) == False: #if flipped
                    continue
                else:
                    self.tp_position_list.append(position_list[j])
            card1=deepcopy(tp_card1)
            card2=deepcopy(tp_card2)
            card1.remove(x)

            res = self.dp2(card2, card1, current_board_state) #torque_value
            if res==-1:
                self.dp_value[state_hash]=x
                return x

        self.dp_value[state_hash]=-1

        return -1

    def calculate_opponent_list(self, board_state_1):
        #common_state = deepcopy(board_state)
        board = dict()
        board_state = deepcopy(board_state_1)
        #opponent_used_list = []
        opponent_card_list = []
        #这步只是在初始化对手的牌
        for i in range(1, int(self.num_weights) + 1):
            opponent_card_list.append(i)

        #for i in range(1, int(self.num_weights) + 1):
        #    self.myWeight[i] = 1
        #整体逻辑：先对board操作，再对opponent_list操作
        #初始化board这个dictionary
        for i in range(len(board_state)):
            board[board_state[i]] = 0

        for i in range(len(board_state)):
            board[board_state[i]] = board[board_state[i]] + 1

        for key, value in self.myWeight.items():
            if value == 0:
                #my_used_card.append(key)
                board[value] = board[value] - 1

        #key 是剩余的棋子，value是使用的次数
        for key, value in board.items():
            if key == 0: # 0 这个weight出现在board上，但是不可能被任何玩家使用
                continue
            else:
                if value != 0:
                    try:
                        opponent_card_list.remove(key)
                    except:
                        pass
        return opponent_card_list

    def dict_to_list(self, dictionary):
        list = []
        for key, value in dictionary.items():
            if dictionary[key] == 1:
                list.append(value)
        return list

    def check_dictonary(self,dictionary):
        for key, value in dictionary.items():
            if value == 1:
                return True
            else:
                return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--first',
                        action='store_true',
                        default=False,
                        help='Indicates whether client should go first')
    parser.add_argument('--slow', action='store_true', default=False)
    parser.add_argument('--ip', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--name', type=str, default="Red Scarf")

    args = parser.parse_args()

    HOST = args.ip
    PORT = args.port
    SLOW = args.slow

    player = NoTippingClient(args.name, args.first)
    player.play_game()
