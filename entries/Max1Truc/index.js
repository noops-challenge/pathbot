const http = require("https");

Number.prototype.mod = function(n) {
  return ((this % n) + n) % n;
};

function turn(currentDirection, newDirectionOffset) {
  const directions = ["N", "E", "S", "W"];
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

  var result = await httpReq("https://api.noopschallenge.com/pathbot/start", {
    method: "POST"
  });

  result = JSON.parse(result);

  console.log(result.description);

  let newUrl = "https://api.noopschallenge.com" + result.locationPath;

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

    console.log(result.description);

    if (result.status == "finished") break;

    direction = chooseDirection(direction, result.exits);

    newUrl = "https://api.noopschallenge.com" + result.locationPath;
  }

  console.log(
    `It took you only ${moves} moves and ${(new Date().getTime() - startTime) /
      1000} seconds to escape the maze!`
  );
}

start().catch(console.error);
