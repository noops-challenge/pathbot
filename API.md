
## pathbot API


### POST /pathbot/start to get started

`POST https://api.noopschallenge.com/pathbot/start`

`HTTP 200`

```
{
  "status": "in-progress",
  "message": "You find yourself in a strange room. You're not sure how you got here but you know you need to escape, somehow.",
  "exits": [ "N", "S" ],
  "description": "You are in a bright long dining room with exits to the North and South. You sense that the maze's exit is to the North, at least 6 rooms away..",
  "mazeExitDirection": "N",
  "mazeExitDistance": 6,
  "locationPath": "/pathbot/rooms/LU62ZaD_SqudPvH3Qt3kJQ"
}
```


### POST to move

`POST https://api.noopschallenge.com/pathbot/rooms/LU62ZaD_SqudPvH3Qt3kJQ`


```
{
 "direction": "N"
}
```

`HTTP 200`

```
{
  "status": "in-progress",
  "message": "You are trapped in a maze",
  "exits": [ "N", "S" ],
  "description": "You are in a chartreuse rectangular storage room with exits to the North and South. You sense that the maze's exit is to the North, at least 5 rooms away..",
  "mazeExitDirection": "N",
  "mazeExitDistance": 5,
  "locationPath": "/pathbot/rooms/OkNMk8D_XfLtYgnicZWzcA"
}
```


### Finding the exit

`POST https://api.noopschallenge.com/pathbot/rooms/RPq3xhL51USGI_iU16alKA`


```
{
 "direction": "N"
}
```

`HTTP 200`

```
{
  "status": "finished",
  "description": "Congratulations! You have escaped the maze."
}
```

