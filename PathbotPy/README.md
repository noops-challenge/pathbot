# 👋 Meet PathbotPy

PathbotPy is module consisting of a set of python classes built around the original [Pathbot API](https://github.com/Oracking/pathbot/blob/master/API.md), to facilitate easy visualization and navigation within the maze. To play the game, simply run `python3 pathbot.py` in the **console**. The game will not render properly if you run it from IDLE, and it may misbehave within other editors, similarly. It is built specifically as a console game.

Also remember to resize your console so the game fits nicely.

## 🤖 Building your automated solver for the game

As it stands, there is no automated solver for the maze. However, `ConsoleWorld` was built with this in mind. To replace user interaction with an automated solver you simply need a callable which accepts a Map object, and returns one of ["W","A","S","D"] corresponding to an instruction for the rover to move ["up","left","down","right"]. See further instructions below:

First of all, read the `docstring` for the Map object:

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
        Map objects support indexing like so: map[x,y].
    """
```

Secondly, you need a callable that will accept the map object. After every attempt to move the rover, the callable will be called and the map will be passed to it. It is expected that the callable will return one of the characters [W,A,S,D] to indicate the direction the rover should move in next. In addition, if the callable returns Q, the game will end.

That said, let's create a Solver class in  a file called `solver.py`:

```
    class Solver:
        def __init__(self):
            .
            .
            # Some attributes to store solver's state

        def interface(self, map):
            # Some logic here to determine rover's next move
            .
            .
            .
            return "W" or "A" or "S" or "D"
```

In our `solver.py` we import our `ConsoleWorld` object and proceed as follows:

```
    solver = Solver()
    game = ConsoleWorld(input_interface=solver.interface)
    game.start()
```

And that's it! You have linked your solver to the game world.

### Useful things to note about Map object
The Map object is the only parameter passed to your callable, therefore you have to determine the entire state of the game from your Map object. And there are attributes to help you determine just that. Here are the most important ones:

- `map.rover_position`: Coordinate of the rover's current position
- `map.exit_found`: Boolean indicating whether exit direction was determines
- `map.exit_distance`: Number of moves to get to exit, disregarding obstacles
- `map.exit_direction`: One of [N,S,E,W,NW,NE,SE,SW], indicating direction of exit
- `map.move_successful`: Boolean indicating whether the most recent move was successful.

Also you can index the map with coordinates like so: `region = Map[x,y]`. Therefore, you never have to directly access `map.matrix` and deal with 2 dimensional lists. However, you are always free to do so.

## ✨ TODO

- **Build a GUI**: The game currently runs within the console, which is convenient, but limiting. It is difficult to design beautiful cross-platform console UIs. Therefore, a GUI will have to be built from built-in libraries. Currently looking at using `turtle`.

- **Build an Automated Solver**: No automated solver has yet been built for the game. You may want to try your hands on this. You can scroll up to the section that talks about building your automated solver to learn more about how to proceed.

- **Test Game Accross Multiple Platforms**: Although, most of the console interactions are theoretically cross-platform, this game has only been tested to work on Linux. It will be helpful to test this game
