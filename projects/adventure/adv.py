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

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = ['n','n','s','s','s','s','n','n','w','w','e','e','e','e'] Cross.
traversal_path = []
#Create visited
visited=set()
# player.current_room.id
# player.current_room.get_exits()
# player.travel(direction)
# get_room_in_direction(direction)

# Create Queue
s=Stack()
#Create oposites list
reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
# add current tuple to queue
s.push((True,'x'))

# while not empty
while s.size()>0:
    # print("Stack",s.stack)
    #pop current
    curr_room=s.pop()
    #get Not_Explored
    not_explored=curr_room[0]
    #get dirction
    last_direction=curr_room[1]
    #Add to visited
    visited.add(player.current_room.id)
    if last_direction !='x':
        #Queue explored reverse direction
        if not_explored:
            s.push((False,reverse_dirs[last_direction]))
        #move
        player.travel(last_direction)
        traversal_path.append(last_direction)
        print("T_PATH",traversal_path)
        print("VISITED",visited)
    if not_explored:
        #Get exits
        next_directions=player.current_room.get_exits()
        # print("NXT DIR",next_directions)
        #remove previous direction
        # print("LAST",last_direction,next_directions)
        if last_direction !='x':
            next_directions.remove(reverse_dirs[last_direction])
            #If not previous room Add to stack // And not visited?
        for dir in next_directions:
            print()
            if player.current_room.get_room_in_direction(dir).id not in visited:
                s.push((True,dir))






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
