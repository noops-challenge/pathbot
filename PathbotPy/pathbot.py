"""
    Module containing
"""
import sys
import time
import json
import random
import urllib.error
import urllib.request
from collections import namedtuple


try:
    from getch import _Getch
    std_input = _Getch()
except ImportError:
    std_input = input
Boundaries = namedtuple('Boundaries', ('min_x', 'min_y', 'max_x', 'max_y'))


def std_interface(map):
    """
    Returns one of: [W,A,S,D], corresponding to [up,left,down,right]
    movement

    :param map: Map object containing information about state of game
    """
    # current_position = map.rover_position
    # move_successful = map.move_successful
    # exit_found = map.exit_found
    direction = std_input().upper()
    return direction


def mprint(message):
    """
    Returns None. Prints messages to console in the form of an online chat.

    :param message: A str message or an object that has a __str__ method.
    """
    to_print = message
    if not isinstance(message, str):
        to_print = "\n" + str(to_print)
    typing_time = random.uniform(0.3, 1.8)
    dot_counter = 4
    start = time.time()
    if isinstance(message, str):
        status = "Typing"
    else:
        status = "Uploading"
    while time.time() - start < typing_time:
        sys.stdout.write("\r")
        if dot_counter > 3:
            sys.stdout.write("-- " + status + ".  ")
            sys.stdout.flush()
            dot_counter = 1
        else:
            sys.stdout.write("-- " + status + "." * dot_counter + "  ")
            sys.stdout.flush()
            dot_counter += 1
        time.sleep(0.2)

    sys.stdout.write("\r")
    sys.stdout.write(" " * 16)
    sys.stdout.flush()

    sys.stdout.write("\r")
    sys.stdout.flush()

    for index, row in enumerate(to_print.split("\n")):
        if index == 0:
            print(row, "\n")
        if index > 0:
            print(" " * 12, end="")
            print(row)


class WebAPI:
    """
        Wrapper class for communicating with server
    """

    BASE_URL = "https://api.noopschallenge.com"

    def __init__(self):
        self.response = None
        self.next_path = None
        self.next_url = None
        self.cache = {}
        self.start()

    def start(self):
        """Return None. Performs first request to server to create game room
        """
        start_url = self.BASE_URL + "/pathbot/start/"
        request_body = json.dumps({}).encode("utf-8")
        request = urllib.request.Request(
            start_url, data = request_body,
            headers={'Content-Type': 'application/json'}
        )
        self.response = json.load(urllib.request.urlopen(request))
        self.response["region_type"] = "0"
        self.next_path = self.response["locationPath"]
        self.next_url = self.BASE_URL + self.next_path
        self.cache[(0,0)] = self.response

    def request_move(self, direction, next_position):
        """
        Returns dict response from server after requesting move. Extra key,
        "region_type" is added to server response. Value for "region_type" is
        "0" for a successful move and "#" for a failed move.

        :param direction: one of: [N,S,E,W]; Indicates direction of movement
        :param next_position: (x,y) coordinates indicating the position you
            intend to move to. These coordinates depend on the nature of
            your map. It is used solely for caching.
        """
        try:
            response = self.cache[next_position]
            if response["region_type"] == "0":
                self.response = response
                self.next_path = response.get("locationPath", self.next_path)
                self.next_url = self.BASE_URL + self.next_path
            return response
        except KeyError:
            pass

        try:
            request_body = json.dumps({"direction": direction}).encode("utf-8")
            request = urllib.request.Request(
                self.next_url, data = request_body,
                headers={'Content-Type': 'application/json'}
            )
            response = json.load(urllib.request.urlopen(request))
            response["region_type"] = "0"
            self.response = response
            self.cache[next_position] = response
            self.next_path = response.get("locationPath", self.next_path)
            self.next_url = self.BASE_URL + self.next_path
        except urllib.error.HTTPError as err:
            response = json.load(err)
            if response["message"] == "Can't go that way":
                response["region_type"] = "#"
                self.cache[next_position] = response
            else:
                print(response)
                raise(err)
        return response


class Map:
    """
        This class represents the map of the rover's world and is implemented
        with a 2x2 matrix. Each element in the matrix can be one of
        four characters only:
            X -> Denotes current position of rover
            # -> Denotes an obstacle
            ? -> Denotes an unexplored location
            0 -> Denotes empty space (rover can move to empty spaces)
        Map expands as rover explores map boundaries.
        Rover coordinates start at (0,0). The positive x and y directions
        are right and up, respectively. The negative x and y directions are
        left and down, respectively.
        Map objects support indexing like so: map[x,y].
    """
    def __init__(self):
        self.api = WebAPI()
        self.matrix = [["?", "?", "?"],
                       ["?", "X", "?"],
                       ["?", "?", "?"]]
        self.rover_position = (0, 0) # (x, y)
        self.boundaries = Boundaries(min_x=-1, min_y=-1, max_x=1, max_y=1)
        self.directions = {"left": "W", "down": "S", "right": "E", "up": "N"}
        self.exit_found = False
        self.exit_distance = None
        self.exit_direction = None
        self.move_successful = True # Indicates whether last move was a success

    def move(self, direction=None):
        """
        Returns a boolean indicating whether the move was a success.

        :param direction: one of: [left,right,up,down]; Indicates direction of
            movement
        """
        old_x, old_y = self.rover_position
        x, y = old_x, old_y
        if direction == "left": x -= 1
        elif direction == "down": y -= 1
        elif direction == "right": x += 1
        elif direction == "up": y += 1

        try:
            region_type = self[x,y]
            at_boundary = False
        except IndexError:
            at_boundary = True
            region_type = "?"

        region_type = self.explore(direction, (x, y), at_boundary)

        if region_type == "0":
            self[x,y] = "X"
            if self.exit_found:
                self[x,y] = "E"
            self[old_x,old_y] = "0"
            self.rover_position = (x, y)
            self.move_successful = True
            return self.move_successful
        self[x, y] = region_type
        self.move_successful = False
        return self.move_successful

    def explore(self, direction, new_position, at_boundary=False):
        """
        Returns a character indicating type of region in the new position.
        "#" indicates an obstacle, "0" indicates empty space.

        :param direction: one of: [left,right,up,down]; Indicates direction of
            movement
        :param new_position: Tuple with coordinates of next position: (x,y)
        :param at_boundary: Boolean indicating if rover is at a boundary
        """
        response = self.api.request_move(self.directions[direction],
                                         new_position)
        region_type = response["region_type"]
        if region_type == "0":
            if response["status"] == "finished":
                self.exit_found = True
                self.exit_distance = 0
            else:
                self.exit_distance = response["mazeExitDistance"]
                self.exit_direction = response["mazeExitDirection"]
        if at_boundary:
            self.expand(direction, region_type)
        return region_type

    def expand(self, direction, region_type):
        """
        Returns None. Expands the self.matrix to reflect new regions and
        recalculates map boundaries.

        :param direction: one of: [left,right,up,down]; Indicates direction of
            movement
        :param region_type: one of: [#, 0]; indicates type of region. "#"
            indicates an obstacle, "0" indicates empty space.
        """
        min_x, min_y, max_x, max_y = self.boundaries

        if direction == "left":
            min_x -= 1
            [row.insert(0, "?") for row in self.matrix]
        elif direction == "down":
            min_y -= 1
            self.matrix.append(["?"] * len(self.matrix[0]))
        elif direction == "right":
            max_x += 1
            [row.append("?") for row in self.matrix]
        elif direction == "up":
            max_y += 1
            self.matrix.insert(0, ["?"] * len(self.matrix[0]))
        self.boundaries = Boundaries(min_x, min_y, max_x, max_y)

    def __str__(self):
        str_representation = " " + "_ " * (len(self.matrix[0])) + "\n"
        for row in self.matrix:
            str_representation += "|" + " ".join(row) + "|" + "\n"
        str_representation += " " + u"\u203E " * (len(self.matrix[0])) + "\n"
        return str_representation

    def __getitem__(self, x_y):
        x, y = self.__resolve_indices(x_y)
        return self.matrix[y][x]

    def __setitem__(self, x_y, new_value):
        x, y = self.__resolve_indices(x_y)
        self.matrix[y][x] = new_value

    def __resolve_indices(self, x_y):
        """
        Returns a tuple (x,y) corresponding to self.matrix indices.
        y is the index for the outer list and x is the index for the
        inner list

        :param x_y: Tuple containing (x,y) position on map.
        """
        x, y = x_y
        x = x - self.boundaries.min_x
        y = self.boundaries.max_y - y
        if x < 0:
            raise IndexError
        if y < 0:
            raise IndexError
        return (x, y)


class ConsoleWorld:
    """
        This class renders the game in your console
    """
    def __init__(self, input_interface=input):
        """
        Returns None. Initiates console world.

        :param input_interface: A callable that returns a string corresponding
            to a user input. Typically, this is python's <input> function, but
            can be replaced.
        """
        self.map = Map()
        self.input_interface = input_interface
        self.directions = {"A": ("left", u"\u2190"), "S": ("down", u"\u2193"),
                           "D": ("right", u"\u2192"), "W": ("up", u"\u2191"),
                           "Q": ("Exit", "Q")}
        self.arrows = {"W": u"\u2190", "N": u"\u2191",
                       "E": u"\u2192", "S": u"\u2193",
                       "NW": u"\u2196", "NE": u"\u2197",
                       "SE": u"\u2198", "SW": u"\u2199"}

    def start(self):
        """Returns None. Initiates the game and prints pre ...
        """
        mprint("16:08:42 -- Hurry up, Engineer!")
        mprint("16:08:39 -- The Curiosity Rover sent to Mars "
               "has gotten lost and needs your help to navigate back to "
               "its launchpad")
        mprint("16:08:38 -- Unfortunately, its cameras are down so it can "
               "only detect close-ranged objects")
        mprint("16:08:34 -- Navigate it back to the launchpad before the "
               "battery runs down")
        mprint("16:08:33 -- Below is a map showing you where it currently is")
        mprint("16:08:28 -- ")
        mprint(self.map)
        mprint("16:08:19 -- The <X> denotes where the Rover is. Areas marked "
               "<?> represent areas you are yet to visit. Areas marked "
               "<0> are places that you can, and have already visited. "
               "And finally, areas marked <#> represent obstacles the "
               "Curiosity cannot overcome. You can move outside the boundaries "
               "of the map, provided there are no obstacles")
        mprint("16:08:17 -- We entrust you to direct it back home. Your "
               "mission begins ... Now!")

        print("Please input the next direction. (W is up, A is left, "
              "S is down and D is right.)")
        self.run_till_end()

    def run_till_end(self):
        """Returns None. Fascilitates user interaction with game
        """
        while True:
            while True:
                print("Direction: ", end="")
                usr_direction = self.input_interface(self.map).upper()
                try:
                    direction = self.directions[usr_direction][0]
                    break
                except KeyError:
                    print("Invalid direction supplied. Valid directions are "
                          "[W,A,S,D]. Press Q to quit")
            if usr_direction == "Q":
                print("\n\nSeems you have to leave :(. Thanks for your time!")
                return

            if not self.input_interface == input:
                print(self.directions[usr_direction][1])
            success = self.map.move(direction)

            if success:
                print("There was a path in the direction specified\n")
            else:
                print("Rover's path was blocked\n")

            self.display_map()
            print(
                "\nLanchpad direction: " +
                 self.arrows.get(str(self.map.exit_direction), "unkown") +
                 " || Launchpad distance: " +
                 (str(self.map.exit_distance) or "unknown")
            )
            if self.map.exit_found:
                print("\n\nAwesome!! You have located the exit and saved the "
                      "Rover\n\n")
                return

    def display_map(self):
        """Returns None. Prints map to the screen
        """
        for row in str(self.map).split("\n"):
            print(" " * 12, end="")
            print(row)


def main():
    game = ConsoleWorld(input_interface=std_interface)
    game.start()
    

if __name__ == "__main__":
    main()
