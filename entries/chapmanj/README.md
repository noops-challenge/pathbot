
# 1. Pathbot Solver

## 1.1 NOOP Challenge GET and POST functions
These were based on the examples given in the API README

## 1.2 Helper Functions


- `rel_coord` translates a NSEW move into relative (x,y) position
- `move_in_dir` encodes the NSEW move to be used in the `post` function, stores the relative (x,y) position with the Pathbot response



## 1.3 Breadth-first Search

`search` takes a starting map and starts the search for the exit for either infinite (where `iterations=-1`) or a defined number of iterations (i.e. `iterations>-1`)

The starting map can be either:
- `https://api.noopschallenge.com/pathbot/start` the default Pathbot starting url
- `https://api.noopschallenge.com/pathbot//pathbot/rooms/<roomid> ` any response succeeding the Pathbot starting map

`position` will be initially set to (0,0), with all other positions relative to it.
For example a path of NWN would be represented by positions (0,1), (-1,1), and (-1,2).

`visited` is a list of all visited positions

While the search is `'in-progress'`
    
- For the current `position` POST a move to each listed `'exit'`, storing the Pathbot JSONs in `responses` (if not already in).
- Also store these evaluted positions in `visited`
- Check if `'finished'`
- Remove the first entry in `responses` and move to the new first entry in `responses`

## 1.4. ✨Suggested Improvements

Currently, the Breadth-first search will evaluate all solutions in the tree sequntially, without any intelligence. 

I would reccommend improving the movement decision making. Specifically, using the `'direction'` and `'distance'` information provided in the Pathbot response


```python

```
