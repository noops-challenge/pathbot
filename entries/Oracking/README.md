## ✌️ Meet PathbotPy

Firstly, familiarize yourself with [Pathbot](https://github.com/noops-challenge/pathbot/blob/master/README.md) if you haven't already.

PathbotPy is a module consisting of a set of python classes built around the original [Pathbot API](https://github.com/Oracking/pathbot/blob/master/API.md) to facilitate easy visualization and navigation within the maze. To play the game, simply run `python3 pathbot.py` in the **console**. The game will not render properly if you run it from IDLE, and it may misbehave within other editors, similarly. It is built specifically as a console game.

Also remember to resize your console so the game fits nicely.

## 🤖 Building your automated solver for the game

#### Firstly, how easy is it to integrate a solver?
Let's look at an example solver that moves the rover in random directions until the exit is found. We just create a python file in the same folder as `pathbot.py` and write the following in it:

```
    from random import choice
    from pathbot import ConsoleWorld

    def random_solver(map):
        return choice(["W", "A", "S", "D"])

    game = ConsoleWorld(input_interface=random_solver)
    game.start()
```

Now run your file from the terminal and you will see your rover moving on the map.

However, you may want your rover to be a bit wiser and not move in random directions. Below is the information you'll need to create your own automated solver:

#### What do you need to do to integrate your solver?

As it stands, there is no automated solver for the maze. However, `ConsoleWorld` was built with this in mind. To replace user interaction with an automated solver you simply need a callable which accepts a `Map` object and returns one of `["W","A","S","D"]` corresponding to an instruction for the rover to move [up,left,down,right]. See further instructions below.



#### Understanding the `Map` object

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

#### A few more things to note about `Map` object

The entire state of the game can be determined from the `Map` object. Here are the attributes to help you determine that:

- `map.rover_position`: Coordinates of the rover's current position
- `map.exit_found`: Boolean indicating whether the rover has reached launchpad destination.
- `map.exit_distance`: Number of moves to get to exit, disregarding obstacles
- `map.exit_direction`: One of `["N","S","E","W","NW","NE","SE","SW"]`, indicating direction of exit
- `map.move_successful`: Boolean indicating whether the most recent move was successful

Also, you can index the map with coordinates (not indices) like so: `region = Map[x,y]`. Therefore, you never have to directly access `map.matrix` and deal with 2 dimensional array/list and indices. However, you are always free to do so.


#### Creating a `solve` function

As mentioned, all you need to integrate your solver is a callable. After every instruction to move the rover, the callable will be called, and the map will be passed to it. It is expected that the callable will return one of the characters [W,A,S,D] to indicate the next instruction for the rover. In addition, if the callable returns Q, the game will end.

To illustrate, let's create a `solve` function in a `solver.py` file:

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

And that's it! Your `solve` function now controls the rover.


#### Creating a `Solver` class

Alternatively, our callable can be a method of an object, instead of a function. For example, an object with a `solve` method

The advantage of using an object is that the object can hold information about its state, in the form of attributes, after its `solve` method is done executing. This contrasts our original `solve` function, which loses all data of its state after it is done executing.

Lets create a sample `Solver` class:

```
    class Solver:
        def __init__(self):
            # Some attributes to store solver's state
            # .
            # .

        def solve(self, map):
            # Some logic here to determine rover's next move
            # based on state of map
            # .
            # .
            return "W" or "A" or "S" or "D"
```

To connect it to our game, we import `ConsoleWorld` into `solver.py` and proceed as follows:

```
    solver = Solver()
    game = ConsoleWorld(input_interface=solver.solve)
    game.start()
```

## ✨ To Do List

- **Build a GUI**: The game currently runs within the console, which is convenient, but limiting. It is difficult to design beautiful cross-platform console UIs. Therefore, a GUI will have to be built from built-in libraries. Currently looking at using [turtle](https://docs.python.org/3.3/library/turtle.html?highlight=turtle).

- **Build an Automated Solver**: No automated solver has yet been built for the game. You may want to try your hands on this. You can scroll up to the section that talks about building your automated solver to learn more about how to proceed.

- **Test Game Accross Multiple Platforms**: Although most of the console interactions are theoretically cross-platform, this game has only been tested to work on Linux. It will be helpful to test this game on other platforms. Any feedback is appreciated.
