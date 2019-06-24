
# 👋 Meet Pathbot

Like its cousin Mazebot, Pathbot is always getting lost.

While exploring the deeper subterranean floors of the Noops, Inc. complex, Pathbot came upon a [TI-99/4A] with a collection of 1970s-era text adventure games. Pathbot eventually went back to work on the Noops assembly line, but it just couldn't stop thinking about hunting Wumpuses, avoiding pits, and escaping from the Grue.

Enter one of pathbot's labyrinths and see if you can make it out.


## ✳️ How to play

`POST` to `https://api.noopschallenge.com/pathbot/start` to get started.

Every location in pathbot's many mazes will return you a JSON object with the following fields:

- **status** (string) either "in-progress" or "finished",
- **message** (string) a message for you from Pathbot.
- **exits** (string array) An array containing the available exits (N, S, E, or W).
- **description** A description of the room you are in.
- **mazeExitDirection** (string) The general direction toward the exit from the maze - one of (N, S, E, W, NW, NE, SW, SE).
- **mazeExitDistance** (number). The minimum number of rooms between your current location and the maze exit,
- **locationPath** (string) the API path for the location. POST your next move back to this path.

`POST` to the `locationPath` with the exit you would like to take to move to the next location.

See the [API documentation](./API.md) for more information.

# Starter Kits

## Go interactive client

Pathbot has included a go client that will let you explore its mazes.
Can you write a program that can escape the maze on its own?

# ✨ A few ideas

- **Create an automated solver**: Humans can be pretty good at solving mazes, but they'll never be as fast as a well-tuned computer. Start from the included go program or wriate a program that can escape in another language.

- **Make it graphical**: Each room has a description. Use these descriptions to create a richer playing experience. Add a map of the rooms exlored so far.

- **Make your own text adventure**: Perhaps you want to create your own game, complete with [grues](https://en.wikipedia.org/wiki/Grue_%28monster%29). Start out with [Twine](https://twinery.org/) or write your own engine. Anything is possible!

- **Create an audio adventure**: Try using the [Speech Synthesis API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis) to make an immersive audio experience.

More about Pathbot here: https://noopschallenge.com/challenges/pathbot
