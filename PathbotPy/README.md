# 👋 Meet PathbotPy

PathbotPy is a module consisting of a set of python classes built around the original [Pathbot API](https://github.com/Oracking/pathbot/blob/master/API.md) to facilitate easy visualization and navigation within the maze. To play the game, simply run `python3 pathbot.py` in the **console**. The game will not render properly if you run it from IDLE, and it may misbehave within other editors, similarly. It is built specifically as a console game.

Also remember to resize your console so the game fits nicely.

## 🤖 Building your automated solver for the game

As it stands, there is no automated solver for the maze. However, `ConsoleWorld` was built with this in mind. To replace user interaction with an automated solver you simply need a callable which accepts a `Map` object and returns one of ``["W","A","S","D"]`` corresponding to an instruction for the rover to move [up,left,down,right]. See further instructions below:

Firstly, read the `docstring` for the Map object. This has also been included here for reference:

```
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
        Map objects support indexing like so: map[x,y], where x and y are
        coordinates (not indices). Coordinates can be negative.
    """
```

Secondly, you need a callable that will accept the `map` object. After every instruction to move the rover, the callable will be called, and the map will be passed to it. It is expected that the callable will return one of the characters [W,A,S,D] to indicate the next direction the rover should move in. In addition, if the callable returns Q, the game will end.

To illustrate let's create a solver function in a `solver.py` file:

```
    def solve(map):
        # Some logic over here to determine rover's next instruction
        # based on the state of the Map object.
        # .
        # .
        return "W" or "A" or "S" or "D"
```

To use this interface with our game, we import `ConsoleWorld` into our `solver.py` and proceed as follows:

```
    game = ConsoleWorld(input_interface=solve)
    game.start()
```

And that's it! Your solve function now controls the rover.

Alternatively, our callable can be a method of an object, instead of a function.

Let's assume we want to create a `Solver` class with a `solve` method, instead of our plain `solve` function. This has a couple of advantages, chief of them being the ability of the `Solver` object to persist data after the `solve` method has been called. This is contrary to the function, which loses all variables after it is called.

Our `Solver` class may look something like this:

```
    class Solver:
        def __init__(self):
            .
            .
            # Some attributes to store solver's state

        def solve(self, map):
            # Some logic here to determine rover's next move
            .
            .
            .
            return "W" or "A" or "S" or "D"
```

Next to connect it to our game we import `ConsoleWorld` into `solver.py` and proceed as follows:

```
    solver = Solver()
    game = ConsoleWorld(input_interface=solver.interface)
    game.start()
```


### Useful things to note about Map object
The Map object is the only parameter passed to your callable; therefore, you have to determine the entire state of the game from your `Map` object. There are attributes to help you determine just that. Here are the most important ones:

- `map.rover_position`: Coordinate of the rover's current position
- `map.exit_found`: Boolean indicating whether the rover has reached launchpad destination.
- `map.exit_distance`: Number of moves to get to exit, disregarding obstacles
- `map.exit_direction`: One of `["N","S","E","W","NW","NE","SE","SW"]`, indicating direction of exit
- `map.move_successful`: Boolean indicating whether the most recent move was successful

Also, you can index the map with coordinates (not indices) like so: `region = Map[x,y]`. Therefore, you never have to directly access `map.matrix` and deal with 2 dimensional array/list and indices. However, you are always free to do so.

## ✨ TODO

- **Build a GUI**: The game currently runs within the console, which is convenient, but limiting. It is difficult to design beautiful cross-platform console UIs. Therefore, a GUI will have to be built from built-in libraries. Currently looking at using [turtle](https://docs.python.org/3.3/library/turtle.html?highlight=turtle).

- **Build an Automated Solver**: No automated solver has yet been built for the game. You may want to try your hands on this. You can scroll up to the section that talks about building your automated solver to learn more about how to proceed.

- **Test Game Accross Multiple Platforms**: Although most of the console interactions are theoretically cross-platform, this game has only been tested to work on Linux. It will be helpful to test this game on other platforms. Any feedback is appreciated.
