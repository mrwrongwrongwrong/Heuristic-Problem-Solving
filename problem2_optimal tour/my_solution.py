import OptimalTouring as Game
from copy import deepcopy
import math
import numpy as np
#from itertools import chain

from OptimalTouring import OptimalTouring

x = Game.OptimalTouring("sites.txt")


# print(x.send(siteId = 1))

# x.sendMove(siteId = 1)

'''
x.getState()[3][0][4][0][0]   [3][第几个site][4][第几天][开门时间是0，关门时间是1]
x_location = x.getState()[3][i][0]
y_location = x.getState()[3][i][1]
time_required = x.getState()[3][i][2]
value = x.getState()[3][i][3]
open_time = x.getState()[3][i][4][0]
close_time = x.getState()[3][i][4][1]
'''
'''
动态规划 每一天做一次动归，因为第二天可以从新的点开始
动归的初始点可以是1。开始时间最早 2.价值最高 或者可以都做，二选一。或者开始时间最早+30分钟，这其中价值最高的
'''

'''
x = Game.OptimalTouring("sites.txt")
i = 1
while x.getTime() < x.getDay()*1440:
    x.sendMove(siteId=i)
    x.sendMove(delayTime=240)
    i += 1
x.settlement()
'''



def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def num_sites():
    ret = x.readSites("sites.txt")
    return len(ret)

def site_value(current_list, i):
    return current_list[i][3]

def site_time(current_list, i):
    return current_list[i][2]

def get_ratio(current_list):  # 性价比
    ratio_list = []
    for i in range(len(current_list)):
        ratio = current_list[i][3] / current_list[i][2]  # value/time
        ratio_list.append(ratio)
    return ratio_list


def get_average_ratio(current_list):  # 时间与价值的关系
    lst = get_ratio(current_list)
    return sum(lst) / len(lst)


def get_distance(current_list, i, j):
    distance = int(current_list[i][0] + current_list[j][0]) + int(abs(current_list[i][1] - current_list[j][1]))
    return distance


'''
def get_start_point(current_list, id_list): #以ratio高为优先度高
    list = get_ratio(current_list)
    for i in range(len(id_list)):
        list[id_list[i]] = 0 #has been visited
    print(list)
    max_value = max(list)
    max_index = list.index(max_value)
    #return max_index

#print(get_start_point(ret))
get_start_point(ret, [1,2,4])
'''
def get_start_point(current_list, id_list, day):  # 以最早开门为高优先度
    #starting_time = [0, 10000]  # index = 0, the time = 10000
    starting_time = 1440
    for i in range(len(current_list)):
        if any(ele == i for ele in id_list):
            continue
        # print(current_list[i][4][0])
        if site_value(current_list, i ) == 0:
            continue

        if starting_time > current_list[i][4][day][0]:
            starting_time = deepcopy(current_list[i][4][day][0])
            site = deepcopy(i)
        '''
        if current_list[i][4][day][0] < starting_time[1]:
            starting_time[0] = i
            starting_time[1] = current_list[i][4][day][0]
        else:
            continue
    return starting_time[0]  # 返回的是当天初始的点
        '''
    return site


# def get_possible_point(current_list, id_list, time, day):
def get_possible_point(current_list, id_list, current_time, day):
    tp_list = []
    # current_time = x.getTime() - (day * 1440) # the current time during that day
    # current_time = time - (day * 1440)
    start_point = get_start_point(current_list, id_list, day)
    tp_current_list = deepcopy(current_list)
    #tp_current_list.remove(tp_current_list[start_point])
    for i in range(len(tp_current_list)):
        if any(ele == i for ele in id_list):
            continue
        entry_time = current_time + get_distance(tp_current_list, start_point, i)
        # current_time + travel time
        leave_time = entry_time + tp_current_list[i][2]
        if (entry_time >= tp_current_list[i][4][day][0]) and (leave_time <= tp_current_list[i][4][day][1]):
            # 旅行之后刚好能开门，并且stay的时间完后还没关门
            tp_list.append(i)
    return tp_list  # 返回的是还没被访问过的 并且 可行的点

def get_possible_point_with_prior(start_point,current_list, id_list, current_time, day):
    tp_list = []
    site = -1
    distance = 1000000
    for i in range(len(current_list)):
        # if any(item == i for item in id_list):
        #    continue

        #if any(ele == i for ele in id_list):
        #for j in range(len(id_list)):
        #    if i == id_list[j]:
        #        current_list[i][3] == 0
        #        continue

        #print('11111',get_distance(current_list, start_point, i))
        #print('11111',current_time)

        entry_time = current_time + get_distance(current_list, start_point, i)
        # current_time + travel time
        leave_time = entry_time + current_list[i][2]
        if any(ele == i for ele in id_list):
            continue

        if (entry_time >= current_list[i][4][day][0]) and (leave_time <= current_list[i][4][day][1]):
            # 旅行之后刚好能开门，并且stay的时间完后还没关门
            tp_list.append(i)
            if get_distance(current_list, start_point, i) < distance:
                site = i
                distance = get_distance(current_list, start_point, i)
    return tp_list,site  # 返回的是还没被访问过的 并且 可行的点

dp_value_dict = dict()

'''
list_from_previous_day = x.getState()[3]
visited_site_each_day = [[] for row in range(x.getDay()+1)] #list of a list
print('total days',visited_site_each_day)
id_list = [0] # just a list, with no distinguish on days 初始值是0，因为0这个点不存在现实中，只存在循环中，且对应value为0
dp_value = 0
time_left = 1440
optp = [[0 for col in range(int(1440/10)+1)] for row in range(len(list_from_previous_day)+1)]
site_tp = deepcopy(optp) #做一个和optp一摸一样的，专门存储site的matrix
print('size1',np.shape(optp))
'''
def dp(current_time, list_from_previous_day, id_list,visited_site_each_day , day): #starting_site, #id_list is the list with the sites whch have been visited in the previous days
    #dp是输入了三个variables，输出的是一个值，你每次比较的是这个值的大小
    #对参与过的sites，将value设为0，然后再进行动归
    current_list = deepcopy(list_from_previous_day)
    for i in range(len(id_list)):
        current_list[id_list[i]][3] = 0 # set value = 0 for all used sites
        print('test if the value can be set as 0',current_list)
    available_sites = get_possible_point(current_list, id_list, current_time, day)

    #rate = get_average_ratio(available_sites)
    tp_start_point = get_start_point(available_sites, id_list, day)
    start_point = [tp_start_point for col in range(145)]
    print('start',start_point)
    last_start_point = [tp_start_point for col in range(145)]
    travel_stay_cost = [0 for col in range(145)]
    entry_time = [0 for col in range(145)]
    leave_time = [0 for col in range(145)]

    tp_current_list = current_list
    '''
    for i in range(len(available_sites)):
        for j in range(len(available_sites)): #现在我们是三维的动归，二维是travel的cost加价值，另外一维是时间
            for t in range(0,1440,10): #每天的剩余时间从0开始，一直搜索到剩余时间为1440
                #当下时间为1440 减去 剩余时间j
                current_time = 1440 - t
                if t >=(get_distance(current_list,i,j)+ site_time(current_list,j)):
    '''
    length = len(current_list)
    for i in range(1, length): #虽然你开始时site index是从0开始，但是现在是从1开始了
        for t in range(145): #time left
            current_time = 1440 - t*10 #every ten minutes
            travel_stay_cost[t] = get_distance(current_list, i, start_point[t]) + site_time(current_list, i) #redo
            entry_time[t] = current_time + get_distance(tp_current_list, start_point[t], i) #redo
            leave_time[t] = entry_time[t] + tp_current_list[i][2]
            if t*10 >= travel_stay_cost[t]:
                if (entry_time[t] >= tp_current_list[i][4][day][0]) and (leave_time[t] <= tp_current_list[i][4][day][1]):

                    #optp[i][t] = max(optp[i-1][t], optp[i-1][j-roundup(travel_stay_cost)]+ site_value(current_list,i))

                    if optp[i-1][t] >= optp[i-1][int((t*10 - roundup(travel_stay_cost[t]))/10)]+ site_value(current_list,i):#上一个解比当前解优
                        optp[i][t] = optp[i - 1][t]
                        start_point[t] = last_start_point[t]
                        #如果当前的节点没有上一个节点优，那么就什么也不做 start_point也不用更改


                    else:
                        optp[i][t] = optp[i-1][int((t*10 - roundup(travel_stay_cost[t]))/10)]+ site_value(current_list,i) #site_value(current_list,i) 说明是第i个点
                        start_point[t] = i #把当前loop中下个开始的点设为i
                        last_start_point[t] = i
                        site_tp[i][t] = deepcopy(i) #将i存入到我们要输出的matrix中
                        print('the dp matrix',optp[i][t])
                        print('the site_tp matrix', site_tp[i][t])

            else:
                optp[i][t] = optp[i-1][t]

    print('the dp matrix',optp)
    print('the site_tp matrix', site_tp)
    tp_value = 0
    tp_position = [0,0]
    for i in range(len(optp)): #寻找我们需要的那组解，也就是那组list
        for j in range(len(optp[i])):
            if optp[i][j] > tp_value:
                tp_value = optp[i][j]
                tp_position[0] = i
                tp_position[1] = j

    #visited_site_each_day = []
    print(site_tp[tp_position[0]])
    for j in range(len(site_tp[tp_position[0]])): #第tp_position[0]种解中所有的参与过的sites #functions to get unique values
        if (site_tp[tp_position[0]][j] != 0) and (site_tp[tp_position[0]][j] not in visited_site_each_day[day]):
            visited_site_each_day[day].append(site_tp[tp_position[0]][j])
            print(visited_site_each_day[day])
    print('which sites have I visited on day %d'%day, visited_site_each_day[day])

    return visited_site_each_day


def get_availability(current_list,id_list,current_time,day):
    lst = get_possible_point(current_list,id_list,current_time,day)
    temp = -1
    for i in lst:
        if site_value(current_list, i) == 0:
            continue
        else:
            temp = i
    return temp

def get_next_site(current_list,visited_site_each_day,current_time,day):

    id_list = [item for innerlist in visited_site_each_day for item in innerlist]
    lst = get_possible_point(current_list, id_list, current_time, day)

    start_point = get_start_point(current_list, id_list, day)

    for i in range(len(id_list)):
        current_list[id_list[i]][3] = 0  # set value = 0 for all used sites

    temp = -1
    time = 1440
    for i in lst:
        if site_value(current_list, i) == 0:
            continue
        else:
            if time > current_list[i][4][day][0]:
                time = curren
                starting_time = deepcopy(current_list[i][4][day][0])
                site = deepcopy(i)
            temp = i
    return temp

'''
def greedy(site_list, visited_site_each_day, day):
    id_list = [item for innerlist in visited_site_each_day for item in innerlist]

    #get_possible_point(current_list, id_list, current_time, day)
    current_list = deepcopy(site_list)
    for i in range(len(id_list)):
        current_list[id_list[i]][3] = 0  # set value = 0 for all used sites
    current_time = 0
    start_point = get_start_point(site_list, id_list, day)
    visited_site_each_day[day].append(start_point)
    start_time_of_the_day = site_list[start_point][4][day][0] + site_time(current_list, i)
    current_time = start_time_of_the_day
    while (current_time <1440):
        #if there is a viable site,
            #find the less costy site
            #make the site and time
        #else
            #wait for 10 mins

    #stay_site_each_day[day].append(start_time_of_the_day+)
    #current_time = start_time_of_the_day

    travel_stay_cost = get_distance(current_list, i, start_point) + site_time(current_list, i)  # redo
    entry_time = current_time + get_distance(current_list, start_point, i)  # redo
    leave_time = entry_time + current_list[i][2]
    available_sites = get_possible_point(site_list, id_list, current_time, day)
    length = len(current_list)
    for i in range(len(current_list)):  # 虽然你开始时site index是从0开始，但是现在是从1开始了
        if site_value(current_list, i) == 0:
            continue
        if i == start_point:
            continue


        for t in range(145):  # time left
            current_time = 1440 - t * 10  # every ten minutes
            travel_stay_cost[t] = get_distance(current_list, i, start_point[t]) + site_time(current_list, i)  # redo
            entry_time[t] = current_time + get_distance(tp_current_list, start_point[t], i)  # redo
            leave_time[t] = entry_time[t] + tp_current_list[i][2]
            if t * 10 >= travel_stay_cost[t]:
                if (entry_time[t] >= tp_current_list[i][4][day][0]) and (
                        leave_time[t] <= tp_current_list[i][4][day][1]):

                    # optp[i][t] = max(optp[i-1][t], optp[i-1][j-roundup(travel_stay_cost)]+ site_value(current_list,i))

                    if optp[i - 1][t] >= optp[i - 1][int((t * 10 - roundup(travel_stay_cost[t])) / 10)] + site_value(
                            current_list, i):  # 上一个解比当前解优
                        optp[i][t] = optp[i - 1][t]
                        start_point[t] = last_start_point[t]
                        # 如果当前的节点没有上一个节点优，那么就什么也不做 start_point也不用更改


                    else:
                        optp[i][t] = optp[i - 1][int((t * 10 - roundup(travel_stay_cost[t])) / 10)] + site_value(
                            current_list, i)  # site_value(current_list,i) 说明是第i个点
                        start_point[t] = i  # 把当前loop中下个开始的点设为i
                        last_start_point[t] = i
                        site_tp[i][t] = deepcopy(i)  # 将i存入到我们要输出的matrix中
                        print('the dp matrix', optp[i][t])
                        print('the site_tp matrix', site_tp[i][t])

'''
visited_site_each_day = [[1,2],[3]]
visited_site_each_day = [[] for row in range(x.getDay()+1)]
stay_site_each_day = deepcopy(visited_site_each_day)
site_list = x.getState()[3]
id_list = []

def play(x = Game.OptimalTouring("sites.txt")):
    id_list = [-1]
    site_list = x.getState()[3]
    current_list = deepcopy(site_list)
    total_days = x.getDay()
    day = -1

    #x = Game.OptimalTouring("sites.txt")
    #i = 1

    while x.getTime() < x.getDay() * 1440:
        current_time = x.getTime() % 1440
        if x.getTime() % 1440 == 0.0: #begin of the day
            day = day +1
            start_point = get_start_point(site_list, id_list, day)
            #visited_site_each_day[day].append(start_point)
            id_list.append(start_point)
            #print(id_list)
            start_time_of_the_day = site_list[start_point][4][day][0] + site_time(current_list, start_point)
            current_time = 0 + start_time_of_the_day
            id_list.append(start_point)
            current_list[start_point][3] = 0
            x.sendMove(siteId=(start_point+1))
            x.sendMove(delayTime=start_time_of_the_day)

        to_go_list,to_go_site = get_possible_point_with_prior(start_point, current_list, id_list, current_time, day)
        if to_go_list != []: #get_possible_point 已经说明了即是空间上可行（还没去过），也是时间上可行
            #从所有可去的点挑一个最近点去

            x.sendMove(siteId=(to_go_site+1))
            x.sendMove(delayTime=site_time(current_list, to_go_site))
            travel_stay_cost = get_distance(current_list, to_go_site, start_point) + site_time(current_list, to_go_site)
            current_time = current_time + travel_stay_cost
            start_point = to_go_site
            id_list.append(to_go_site)
            current_list[to_go_site][3] = 0

        else: # ready_to_visit == []:
            if current_time < 1390: #时间早于1400
                x.sendMove(delayTime = 10)
                current_time = current_time + 10

            else: #如果当下时间点不够玩任何景点
                delayed_time = 1440 - current_time
                x.sendMove(delayTime=delayed_time) # until midnight
                current_time = 0
                #print(x.getTime() % 1440)
                #print

        current_list = deepcopy(site_list)
        #x.sendMove(siteId=i)
        #x.sendMove(delayTime=240)
        #i += 1
    x.settlement()

ret = x.readSites("sites.txt")

current_list = x.getState()[3]

play(x)


