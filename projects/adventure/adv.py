from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"
# map_file = "maps/mike.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

traversal_path = []
#Create visited
visited=set()

# Create Queue
s=Stack()
#Create oposites list
reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}

def clear_smoke(unordered):
    while True:
        flag=False
        for i in range(len(unordered)-1):
            if unordered[i]<unordered[i+1]:
                unordered[i],unordered[i+1]=unordered[i+1],unordered[i]
                flag=True
        if flag:
            flag=False
        else:
            break
    return unordered

def oracle(directions):
    retVal=[]
    player2 = Player(player.current_room)
    for last_dir in directions:
        counter=0
        current_dir=last_dir
        player2.current_room=player.current_room
        while True:
            if player2.current_room.get_room_in_direction(current_dir).id not in visited:
                player2.travel(current_dir)
                counter+=1
                next_steps=player2.current_room.get_exits()
                next_steps.remove(reverse_dirs[current_dir])
                if len(next_steps)==1:
                    current_dir=next_steps[0]
                elif len(next_steps)==0:
                    retVal.append((counter,last_dir))
                    break
                else:
                    retVal.append((counter+100,last_dir))
                    break
            else:
                break
    clear_smoke(retVal)
    return retVal

# add current tuple to queue
s.push((True,'x',0))

# while not empty
while s.size()>0:
    #pop current
    curr_room=s.pop()
    #get Not_Explored
    not_explored=curr_room[0]
    #get dirction
    last_direction=curr_room[1]
    #Add to visited
    visited.add(player.current_room.id)
    if len(visited)==500:
        break
    if last_direction !='x':
        #move
        player.travel(last_direction)
        traversal_path.append(last_direction)
        #Queue explored reverse direction
        if not_explored:
            s.push((False,reverse_dirs[last_direction],player.current_room.id))
    if not_explored:
        #Get exits
        next_directions=player.current_room.get_exits()
        #remove previous direction
        if last_direction !='x':
            next_directions.remove(reverse_dirs[last_direction])
            #If not previous room Add to stack // And not visited?
        if len(next_directions)>3:
            next_directions=['e','w','n','s']
        elif len(next_directions)>1:
            crystal_ball=oracle(next_directions)
            next_directions=[]
            for crack in crystal_ball:
                next_directions.append(crack[1])
        for dir in next_directions:
            if player.current_room.get_room_in_direction(dir).id not in visited:
                s.push((True,dir,player.current_room.id))



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
