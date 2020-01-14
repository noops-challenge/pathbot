const http = require("https");

class Maze {
  constructor() {
    this.map = {0: {0: " "}};
    this.x = 0;
    this.y = 0;
    this.minX = -1;
    this.minY = -1;
    this.maxX = 1;
    this.maxY = 1;
  }

  get prettyMap() {
    var output = "";
    for (var x = this.minX; x <= this.maxX; x++) {
      for (var y = this.minY; y <= this.maxY; y++) {
        output += (this.map[x] || {})[y] || " ";
      }
      output += "\n";
    }
    return output;
  }

  directionToOffsets(direction) {
    if (direction == "N") {
      return [0, 1];
    }
    if (direction == "S") {
      return [0, -1];
    }
    if (direction == "E") {
      return [1, 0];
    }
    if (direction == "W") {
      return [-1, 0];
    }
  }

  move(direction) {
    var offsets = this.directionToOffsets(direction);

    this.map[this.x][this.y] = " ";

    this.x += offsets[0];
    this.y += offsets[1];

    if (this.minX >= this.x) this.minX -= 1;
    if (this.maxX <= this.x) this.maxX += 1;
    if (this.minY >= this.y) this.minY -= 1;
    if (this.maxY <= this.y) this.maxY += 1;

    this.map[this.x] = this.map[this.x] || {};
    this.map[this.x][this.y] = "@";
  }

  discover(exits) {
    for (let direction of ["N", "S", "E", "W"]) {
      var newValue = "?";
      if (exits.includes(direction)) {
        newValue = " ";
      } else {
        newValue = String.fromCharCode(9608);
      }

      var offsets = this.directionToOffsets(direction);

      if (! this.map[this.x + offsets[0]]) this.map[this.x + offsets[0]] = {};
      this.map[this.x + offsets[0]][this.y + offsets[1]] = newValue;
    }
  }
}

Number.prototype.mod = function(n) {
  return ((this % n) + n) % n;
};

function turn(currentDirection, newDirectionOffset) {
  const directions = ["W", "S", "E", "N"];
  return directions[
    (directions.indexOf(currentDirection) + newDirectionOffset).mod(
      directions.length
    )
  ];
}

function chooseDirection(direction, exits) {
  // Always follows right wall
  for (let i = -1; i < 3; i++) {
    let newDirection = turn(direction, i);
    if (exits.includes(newDirection)) {
      return newDirection;
    }
  }
}

const httpReq = (url, options = {}, body = "") => {
  return new Promise((resolve, reject) => {
    var request = http
      .request(url, options, res => {
        res.setEncoding("utf8");
        let body = "";
        res.on("data", chunk => (body += chunk));
        res.on("end", () => resolve(body));
      })
      .on("error", reject);

    if (body != "") {
      request.write(body);
    }
    request.end();
  });
};

async function start() {
  var moves = 0;
  var startTime = new Date().getTime();

  var maze = new Maze();

  var result = await httpReq("https://api.noopschallenge.com/pathbot/start", {
    method: "POST"
  });

  result = JSON.parse(result);

  let newUrl = "https://api.noopschallenge.com" + result.locationPath;

  maze.discover(result.exits);

  // Choose first direction
  let direction = result.exits[0];
  for (exit of result.exits) {
    if (result.mazeExitDirection.includes(exit)) {
      direction = exit;
      break;
    }
  }

  while (true) {
    moves += 1;

    maze.move(direction);

    result = JSON.parse(
      await httpReq(
        newUrl,
        {
          method: "POST"
        },
        JSON.stringify({
          direction
        })
      )
    );

    if (result.status == "finished") break;

    maze.discover(result.exits);

    console.log("\x1b[2J" + maze.prettyMap);
    
    direction = chooseDirection(direction, result.exits);

    newUrl = "https://api.noopschallenge.com" + result.locationPath;
  }

  console.log(
    `It took you only ${moves} moves and ${(new Date().getTime() - startTime) /
      1000} seconds to escape the maze!`
  );
}

start().catch(console.error);
