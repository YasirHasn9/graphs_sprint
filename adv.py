from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
'''
class World:
    def __init__(self):
        self.starting_room = None
        self.rooms = {}
        self.room_grid = []
        self.grid_size = 0
'''
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
'''
world class
  def load_graph(self, room_graph):
        num_rooms = len(room_graph)
        rooms = [None] * num_rooms
        grid_size = 1
        for i in range(0, num_rooms):
            x = room_graph[i][0][0]
            grid_size = max(grid_size, room_graph[i][0][0], room_graph[i][0][1])
            self.rooms[i] = Room(f"Room {i}", f"({room_graph[i][0][0]},{room_graph[i][0][1]})",i, room_graph[i][0][0], room_graph[i][0][1])
        self.room_grid = []
        grid_size += 1
        self.grid_size = grid_size
        for i in range(0, grid_size):
            self.room_grid.append([None] * grid_size)
        for room_id in room_graph:
            room = self.rooms[room_id]
            self.room_grid[room.x][room.y] = room
            if 'n' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('n', self.rooms[room_graph[room_id][1]['n']])
            if 's' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('s', self.rooms[room_graph[room_id][1]['s']])
            if 'e' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('e', self.rooms[room_graph[room_id][1]['e']])
            if 'w' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('w', self.rooms[room_graph[room_id][1]['w']])
        self.starting_room = self.rooms[0]
'''
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
'''
this is form the player file 
class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room

        
  
'''
player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

'''
use stack or queue to add room
sets to make sure we visited the room
function for direction ["n" , "s" "e" , "w"]

loop over the rooms 
while there are rooms more the one in the visited 
       get the exits for the player 
       each exit_room in the palyer room contains an exit_room for other room



'''


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


stack = Stack()

# keep track of the visited rooms
visited = set()


# get the direction for each room , an exit_room!.
def directions(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "e":
        return "w"
    elif direction == "w":
        return "e"


# since we have less visited rooms
while len(visited) < len(world.rooms):

    # each room has several exits
    '''
    from the room file 
      def get_exits(self):
        exits = []
        if self.n_to is not None:
            exits.append("n")
        if self.s_to is not None:
            exits.append("s")
        if self.w_to is not None:
            exits.append("w")
        if self.e_to is not None:
            exits.append("e")
        return exits
    '''
    exits = player.current_room.get_exits()
    path = []

    for exit_room in exits:
        # check to make sure room move is valid
        if exit_room is not None:
            # an exit_room is found , the room is not visited
            if player.current_room.get_room_in_direction(exit_room) not in visited:
                # append the exit_room to the path
                path.append(exit_room)
    # the room now is visited , loop over another one.
    visited.add(player.current_room)

    
    # if check to make sure the path is over 0
    if len(path) > 0:
        '''
        make sure there are ways to travel
        use a random integer to randomly choose direction, 
        moves test different,
        stack: -1 to get the last in the list
         '''
        move = random.randint(0, len(path) - 1)
        # insert the element to the top of the stack
        stack.push(path[move])
        '''
        def travel(self, direction, show_rooms = False):
            next_room = self.current_room.get_room_in_direction(direction)
            if next_room is not None:
                self.current_room = next_room
                if (show_rooms):
                    next_room.print_room_description(self)
            else:
                print("You cannot move in that direction.")
        '''
        # player  moves along the path
        player.travel(path[move])
        traversal_path.append(path[move])

    else:
        '''
        check of the there a dead end(no direction)
        then remove the item form the stack
        go opposite or whatever direction is available 
        push the direction to the traversal_path
        '''
        # implement the back tracking if the room leads to a dead end
        deadEnd = stack.pop()
        # pop and remove the top item from the stack
        player.travel(directions(deadEnd))
        # will travel in opposite direction, as per directions
        traversal_path.append(directions(deadEnd))


# **********************************************************
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
