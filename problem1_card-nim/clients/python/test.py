import sys
import socket
import time
from copy import deepcopy
import math

class Client():
    def __init__(self, port=5000):
        self.socket = socket.socket()
        self.port = port

        self.socket.connect(("localhost", port))

        # Send over the name
        self.socket.send("Python Client".encode("utf-8"))

        # Wait to get the ready message, which includes whether we are player 1 or player 2
        # and the initial number of stones in the form of a string "{p_num} {num_stones}"
        # This is important for calculating the opponent's move in the case where we go second
        init_info = self.socket.recv(1024).decode().rstrip()

        self.player_num = int(init_info.split(" ")[0])
        self.num_stones = int(init_info.split(" ")[1])

        

    def getstate(self):
        '''
        Query the server for the current state of the game and wait until a response is received
        before returning
        '''

        # Send the request
        self.socket.send("getstate".encode("utf-8"))

        # Wait for the response (hangs here until response is received from server)
        state_info = self.socket.recv(1024).decode().rstrip()

        # Currently, the only information returned from the server is the number of stones
        num_stones = int(state_info)

        return num_stones

    def sendmove(self, move):
        '''
        Send a move to the server to be executed. The server does not send a response / acknowledgement,
        so a call to getstate() afterwards is necessary in order to wait until the next move
        '''

        self.socket.send(f"sendmove {move}".encode("utf-8"))


    def generatemove(self, state):
        '''
        Given the state of the game as input, computes the desired move and returns it.
        NOTE: this is just one way to handle the agent's policy -- feel free to add other
          features or data structures as you see fit, as long as playgame() still runs!
        '''

        raise NotImplementedError

    def playgame(self):
        '''
        Plays through a game of Card Nim from start to finish by looping calls to getstate(),
        generatemove(), and sendmove() in that order
        '''

        while True:
            state = self.getstate()

            if int(state) <= 0:
                break

            move = self.generatemove(state)

            self.sendmove(move)

            time.sleep(0.1)

        self.socket.close()


class IncrementPlayer(Client):
    '''
    Very simple client which just starts at the lowest possible move
    and increases its move by 1 each turn
    '''
    def __init__(self, port=5000):
        super(IncrementPlayer, self).__init__(port)
        #self.i = 0
        self.i = 1

        self.last_state = self.num_stones

    def generatemove(self, state):
        to_return = self.i
        self.i += 1

        #rival_move = self.last_state - state
        #print("rival move: {}".format(rival_move))
        #print("state {}".format(state))
        print(type(self.num_stones))
        print(self.num_stones)

        return to_return

class MyPlayer(Client):
    '''
    Your custom solver!
    '''
    def __init__(self, port=5000):
        #super(IncrementPlayer, self).__init__(port)
        super().__init__(port)

        self.my_player_num = self.player_num

        self.my_current_card, self.rival_current_card = self.initialize_card_list(self.num_stones)
        #if self.my_player_num == 1:
        #    move = self.dp(my_current_card, rival_current_card, current_stones)
        #else:
        #    move = self.dp(rival_current_card, my_current_card, current_stones)

        self.dp_value = dict()
        self.index = 0



    def generatemove(self, state):

        move = None
        
        '''
        TODO: put your solver logic here!
        '''
        # turn 1, we check if we are the second player or not, if we are player 1, we play a card. If we are player 2, we initialize player 1's card.
        # 如果第一轮是后手，那就先做这个预处理
        if self.index == 0: #如果是第一轮
            self.current_stones = self.num_stones
            self.index += 1
            if self.player_num == 2:
                self.index += 1
                rival_played = self.num_stones - state
                try:
                    self.rival_current_card.remove(rival_played)
                except:
                    pass
        else: #如果是 第2- 第n 轮
        # 直接计算上轮对手出的牌
            rival_played = self.current_stones - state
            try:
                self.rival_current_card.remove(rival_played)
            except:
                pass


        # 无论先手后手 做完预处理之后 进行这步
        move = self.dp(self.my_current_card, self.rival_current_card, state)
        #state is current stone number
        try:
            self.my_current_card.remove(move)
        except:
            pass

        self.current_stones = state - move
        # the current_stones means the stone number remaining after last turn I played
        return move
        
    #from copy import deepcopy

    #dp_value=dict()

    def get_hash(self,a,b,x):
        mod=1000000007
        a.sort()
        b.sort()
        hash=x
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

    #s=5
    #ub=int((s-1)/3+2)
    #list1 = [x+1 for x in range(ub)]
    #list2 = [x+1 for x in range(ub)]
    #first_remove = dp(list1,list2,s)
    #print(first_remove)

    def initialize_card_list(self, num_stone):
        cardlist1 = []
        cardlist2 = []
        num_card = 1 + math.ceil(num_stone / 3)
        print(num_card)
        for i in range(num_card):  # not num_card -1
            cardlist1.append(i + 1)
            cardlist2.append(i + 1)
            print(i)

        return cardlist1, cardlist2
        

if __name__ == '__main__':
    if len(sys.argv) == 1:
        port = 5000
    else:
        port = int(sys.argv[1])

    # Change IncrementPlayer(port) to MyPlayer(port) to use your custom solver
    client = IncrementPlayer(port)
    #client = MyPlayer(port)
    client.playgame()

