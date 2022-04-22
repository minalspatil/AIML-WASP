import matplotlib.pyplot as plt     # for plots
import random                       # for filling dirt randomly
import copy as cp                   # for deep, shallow copying of state lists
import sys                          # inbuilt python methods
import time                         # for running times of BFS and IDDFS
room_size = 4                       # room size
rest_pos = [(0,0)]                  # rest positions
dp = 35                             # dust percentage

class state():
    def __init__(self,room,location,cost,path):
                        # a list of lists, tells position of dirt
        self.room = cp.deepcopy(room)    
                        # a tuple, denoting the current location of the vaccuum cleaner
        self.location = cp.copy(location)
                        # cost incurred since the start state
        self.cost = cost
                        # the path of actions which drove to this state
        self.path = path

#   amount of memory taken by a single node
def node_size(state):
    mem = 0
    temp = 0
    for elem in state.room:
        temp += sys.getsizeof(elem)
    mem += temp
    mem += sys.getsizeof(state.location)
    mem += sys.getsizeof(state.cost)
    mem += sys.getsizeof(state.path)
    return mem

#   the set of all possible actions
actions = {
    0: 'Moving Right',
    1: 'Moving Left',
    2: 'Moving Up',
    3: 'Moving Down',
    4: 'Remove Dirt',
    5: 'Do Nothing',
}

def print_state(st):
    print(f"Size of the Room: {room_size}")
    print(f"Location of Vacuum Cleaner: {st.location}")
    print(f"Current Cost: {st.cost}")
    for row in st.room:
        print(*row)

def next_state(st, action):
    new = state(st.room,st.location,st.cost,st.path)
    if action[0] == 'M':
        new.cost += 2
    elif action == 'S':
        new.cost += 1
    
    if action == 'Remove Dirt':
        new.room[st.location[0]][st.location[1]] = 0
    elif action == 'Moving Up':
        new.location = (max(0,new.location[0]-1), new.location[1])
    elif action == 'Moving Down':
        new.location = (min(room_size-1,new.location[0]+1), new.location[1])
    elif action == 'Moving Right':
        new.location = (new.location[0], min(room_size-1,new.location[1]+1))
    elif action == 'Moving Left':
        new.location = (new.location[0], max(0,new.location[1]-1))
    
    new.path += (action+', ')

    return new

#   returns a room with dirt on 'p' percent randomly chosen points
def dirt_generator(p):
    room = []
    for i in range(room_size):
        room.append([0 for _ in range(room_size)])
    if not p:
        return room
    positions = [i for i in range(room_size*room_size)]
    random.shuffle(positions)
    num_dirt = (p * room_size**2) // 100
    dirt_pos = positions[0:num_dirt+1]
    for pos in dirt_pos:
        column = pos % room_size
        row = pos // room_size
        room[row][column] = 1
    return room

def goal_test(state):
    if state.room == dirt_generator(0):
        return True
    return False

def hashd(state):
    id = 0
    for i in range(room_size**2):
        column = i % room_size
        row = i // room_size
        id = ( id * 2 + st.room[row][column] ) % 100007
    return id

explored = [[] for _ in range(100007)]
frontier = []

def not_explored(st):
    for item in explored[hashd(st)]:
        if item.room == st.room and item.location == st.location:
            return False
    return True

def breadth_first_search(state, analyse=False):
    t1 = time.time()
    max_queue = 0
    nodes = 0
    frontier.append(state)
    while frontier.__len__()!=0:
        new_state = frontier.pop(0)
        nodes += 1  
        explored[hashd(new_state)].append(new_state)
        if goal_test(new_state):
            t2 = time.time()
            if analyse:
                print()
                print("BREADTH FIRST SEARCH ANALYSIS")
                print(f"BFS - Number of nodes generated = {nodes}")
                print(f"BFS - Size of a node = {node_size(new_state)} bytes")
                print(f"BFS - Max size of auxillary queue = {max_queue}")
                print(f"BFS - Action Path = {new_state.path}")
                print(f"BFS - Total Cost = {new_state.cost}")
                print(f"BFS - Total time taken = {round(t2-t1,2)} seconds")
                print()
            return new_state, round(t2-t1,2)
        for y in range(5):
            future_state = next_state(new_state,actions[y])
            if future_state not in frontier and not_explored(future_state):
                frontier.append(future_state)
                max_queue = frontier.__len__() if max_queue < frontier.__len__() else max_queue
    return None

def not_explored_depth(ED, st):
    for item in ED[hashd(st)]:
        if item.room == st.room and item.location == st.location:
            return False
    return True

dls_nodes = 0
max_stack = 0

def depth_limited_search(ED, state, limit):
    global dls_nodes
    dls_nodes += 1
    global max_stack
    max_stack += 1
    if limit < 0:
        return None
    if goal_test(state):
        return state
    ED[hashd(state)].append(state)
    for y in range(5):
        future_state = next_state(state,actions[y])
        if not_explored_depth(ED, future_state):
            result = depth_limited_search(ED, future_state, limit-1)
            if result != None:
                return result       
    return None

def iterative_deepening_search(st, analyse=False):
    t3 = time.time()
    depth = 0
    while True:
        global max_stack
        max_stack = 0
        ED = [[] for _ in range(100007)]
        depth += 1
        temp_st = state(st.room, st.location, st.cost, st.path)
        result = depth_limited_search(ED, temp_st, depth)
        if result != None:
            t4 = time.time()
            if analyse:
                print("ITERATIVE DEEPENING DEPTH FIRST SEARCH ANALYSIS")
                print(f"IDDFS - Number of nodes generated = {dls_nodes}")
                print(f"IDDFS - Size of a node = {node_size(result)} bytes")
                print(f"IDDFS - Max size of auxillary stack = {max_stack}")
                print(f"IDDFS - Action Path = {result.path}")
                print(f"IDDFS - Total Cost = {result.cost}")
                print(f"IDDFS - Total time taken = {round(t4-t3,2)} seconds")
            return result, round(t4-t3,2)       

if __name__ == "__main__":
    st = state(dirt_generator(dp),(0,0),0,'')
    
    print('1. Enter 1 to know the current location and cost of the Vacuum Cleaner')
    print('2. Enter 2 to implement Breadth First Search (BFS)')
    print('3. Enter 3 to implement Iterative Deepening Search (IDDFS)')
    print('4. Enter 4 to perform a comparative analysis of BFS and IDDFS')

    option = int(input("Enter any option from 1 to 4: "))

    if option==1:
        print_state(st)
    
    if option==2:
        stt1, tm1 = breadth_first_search(st, True)

    if option ==3:
        stt2, tm2 = iterative_deepening_search(st, True)

    if option==4:    
        print()
        print("Comparative Analysis")
        print("Comparative Analysis: Memory used in BFS is more than in IDS")

        cost1 = 0
        cost2 = 0
        iterations = 2
        for i in range(iterations):
            ran = state(dirt_generator(dp),(0,0),0,'')
            stt1, tm1 = breadth_first_search(st)
            stt2, tm2 = iterative_deepening_search(st)
            cost1 += stt1.cost
            cost2 += stt2.cost

        print(f"Comparative Analysis: Average path cost for BFS is {cost1/iterations}, and for IDDFS is {cost2/iterations}")

        timelist = []
        for i in range(2,40):
            st = state(dirt_generator(i),(0,0),0,'')
            stt1, tm1 = iterative_deepening_search(st)
            timelist.append(tm1)

        print("Graph")
        plt.plot(timelist)
        plt.ylabel("Time Taken")
        plt.xlabel("Percentage of Dirt")
        plt.axis([0, 50, 0, 15])
        plt.show()
