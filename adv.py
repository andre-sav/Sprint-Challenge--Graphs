from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


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


# helper function that will return the path to the last unvisited room
# breadth first traversal
def return_to_unvisited(player):
    qq = []
    visited = set()
    qq.append([player.current_room.id])
    while len(qq) > 0:
        path = qq.pop(0)
        previous = path[-1]
        if previous not in visited:
            visited.add(previous)
            for neighbor in graph[previous]:
                # checks if a neighbor is unknown, in which case it returns the path
                if graph[previous][neighbor] == "unknown":
                    return path
                else:
                    updated_path = list(path)
                    updated_path.append(graph[previous][neighbor])
                    qq.append(updated_path)
    return []

# helper function that will enqueue moves
def queue_moves(player, qq):
    unexplored = []
    exits = graph[player.current_room.id]
    for direction in exits:
        # checks if the direction is unknown and adds to unexplored if so
        if exits[direction] == "unknown":
            unexplored.append(direction)
    if len(unexplored) != 0:
        # if unexplored is not empty add a random direction from the unexplored list to moves
        # because we cannot know where to go, we must guess direction from those available
        qq.append(unexplored[random.randint(0, len(unexplored) - 1)])
    else:
        # calls function to route us back to last location with unvisited exits
        path_to_unvisited = return_to_unvisited(player)
        en_route = player.current_room.id
        # loops through directions to room with unvisited adjacents
        for next_direction in path_to_unvisited:
            # loops through rooms on the way back
            # until directions match then appends to the queue
            for direction in graph[en_route]:
                if graph[en_route][direction] == next_direction:
                    qq.append(direction)

opposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}

player = Player(world.starting_room)

graph = {}

room = {}

# build graph for our path constructor by assigning unknown to every exit in starting room
for exit in player.current_room.get_exits():
    room[exit] = "unknown"

graph[world.starting_room.id] = room

def find_the_way():
    path = []
    moves = []
    # calls helper function to determine first move
    queue_moves(player, moves)
    while len(moves) > 0:
        # loops while moves are in queue
        current_room = player.current_room.id
        next_move = moves.pop(0)
        # activates player object travel function "moving" the player in the queued direction
        player.travel(next_move)
        # appends this movement to our return list
        path.append(next_move)
        # assigns the new current room to variable next_room
        next_room = player.current_room.id
        # links that room id to previous
        graph[current_room][next_move] = next_room
        # if it is not in the graph it will populate it with a dictionary adding the possible exits 
        if next_room not in graph:
            graph[next_room] = {}
            for exit in player.current_room.get_exits():
                graph[next_room][exit] = "unknown"
        # accesses the room we travelled to in the graph in this iteration
        # and links it to the starting room by reversing the travel direction
        graph[next_room][opposite_directions[next_move]] = current_room
        if len(moves) == 0:
            # if no more moves, queues additional
            queue_moves(player, moves)
    
    return path


traversal_path = find_the_way()

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
