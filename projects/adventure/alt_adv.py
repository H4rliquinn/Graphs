from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random
from ast import literal_eval


# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"
# map_file = "maps/mike.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)

# traversal_path = ['n', 'n']

traversal_path = []
s = Stack()
map = {
  0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
}
# Create visited
visited = set()
# Create oposites list
reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e", 'x': 'x'}

    # player.current_room.id
    # player.current_room.get_exits()
    # player.travel(direction)
    # get_room_in_direction(self, direction)


def find_walls():
    walls = {'n', 's', 'w', 'e'}-set(player.current_room.get_exits())
    # print("WALLS",walls)
    for x in walls:
        map[player.current_room.id][x] = 'X'


def update_records(last_direction):
    # add to map
    map[player.current_room.id][last_direction] = player.current_room.get_room_in_direction(
        last_direction).id
    find_walls()
    player.travel(last_direction)
    map[player.current_room.id] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
    find_walls()
    map[player.current_room.id][reverse_dirs[last_direction]
        ] = player.current_room.get_room_in_direction(reverse_dirs[last_direction]).id
    # add to path
    traversal_path.append(last_direction)


def find_new_room(passed_id):
    recents = set()
    q = Queue()
    q.enqueue((passed_id, []))
    while q.size() > 0:
        curr = q.dequeue()
        curr_room = map[curr[0]]
        direction = curr[1]
        print("CURR",curr_room,direction,curr[0])
        for x in curr_room:
            if curr_room[x] != 'X':
                if curr_room[x] == '?':
                    print("FOUND",direction,x)
                    # direction.append(x)
                    return direction
                elif direction==[] or x !=reverse_dirs[direction[-1]]:
                    print("NOTFOUND",direction,x)
                    new_direction=list(direction)
                    new_direction.append(x)
                    q.enqueue((curr_room[x],new_direction))


last_direction='x'
while True:
    # Add to visited
    visited.add(player.current_room.id)
    # print(player.current_room.id)
    if len(visited)==len(room_graph):
        break
    # Get exits
    next_directions=player.current_room.get_exits()
    if reverse_dirs[last_direction] in next_directions:
        next_directions.remove(reverse_dirs[last_direction])
    # Continue straight if possible
    if last_direction in next_directions and player.current_room.get_room_in_direction(last_direction).id not in visited:
        update_records(last_direction)
    else:
        # Otherwise turn or reorient
        for x in next_directions:
            print("ROOMVIS",map[player.current_room.id],player.current_room.get_room_in_direction(x).id)
            if player.current_room.get_room_in_direction(x).id in visited:
                map[player.current_room.id][x]=player.current_room.get_room_in_direction(x).id
            if map[player.current_room.id][x]!='?':
                    next_directions.remove(x)
            print("NXTDIR",next_directions)
        if len(next_directions)>0:
            last_direction=random.sample(next_directions,1)[0]
            update_records(last_direction)
        else:
            # re-orient
            gotit=find_new_room(player.current_room.id)
            print("GOTIT",gotit,player.current_room.id)
            for i in gotit:
                update_records(i)
                last_direction='x'
            # break

    # Queue explored reverse direction
    print("T_PATH",traversal_path)
    print("MAP",map)
print({*world.rooms.keys()} - {r for r in visited})
    # # print("VISITED",visited)
    # if not_explored:

    #     # print("NXT DIR",next_directions)
    #     #remove previous direction
    #     # print("LAST",last_direction,next_directions)
    #     if last_direction !='x':
    #         next_directions.remove(reverse_dirs[last_direction])
    #         #If not previous room Add to stack // And not visited?
    #     if len(next_directions)>3:
    #         next_directions=['e','w','n','s']
    #     elif len(next_directions)>1:
    #         crystal_ball=oracle(next_directions)
    #         next_directions=[]
    #         for crack in crystal_ball:
    #             next_directions.append(crack[1])
    #     for dir in next_directions:
    #         if player.current_room.get_room_in_direction(dir).id not in visited:
    #             # print(player.current_room.id)
    #             s.push((True,dir,player.current_room.id))
            # else:
            #     print("VISITS",dir,player.current_room.get_room_in_direction(dir).id,s.stack)



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
