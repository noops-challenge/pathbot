package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

type PathbotDirection struct {
	Direction string `json:"direction"`
}

type PathbotLocation struct {
	Status            string   `json:"status"`
	Message           string   `json:"message"`
	Exits             []string `json:"exits"`
	Description       string   `json:"description"`
	MazeExitDirection string   `json:"mazeExitDirection"`
	MazeExitDistance  int      `json:"mazeExitDistance"`
	LocationPath      string   `json:"locationPath"`
}

func main() {
	var location = start()

	explore(location)
}

func start() PathbotLocation {
	return apiPost("/pathbot/start", strings.NewReader("{}"))
}

func explore(location PathbotLocation) {
	reader := bufio.NewReader(os.Stdin)

	for {
		printLocation(location)

		if location.Status == "finished" {
			fmt.Println(location.Message)
			os.Exit(0)
		}

		printPrompt(location.Exits)

		direction, err := reader.ReadString('\n')
		if err != nil {
			panic(err.Error())
		}

		dir := PathbotDirection{Direction: strings.ToUpper(direction[0:1])}

		body, err := json.Marshal(dir)

		if err != nil {
			panic(err.Error())
		}

		location = apiPost(location.LocationPath, bytes.NewBuffer(body))
	}
}

func printPrompt(directions []string) {
	fmt.Println("What direction will you go?")
	fmt.Println(directions)
}

func printLocation(location PathbotLocation) {
	fmt.Println()
	fmt.Println(location.Message)
	fmt.Println(location.Description)
}

func apiPost(path string, body io.Reader) PathbotLocation {
	//domain := "https://api.noopschallenge.com"
	domain := "http://localhost:3004"
	res, err := http.Post(domain+path, "application/json", body)
	if err != nil {
		panic(err.Error())
	}

	return parseResponse(res)
}

func parseResponse(res *http.Response) PathbotLocation {
	var response PathbotLocation
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		panic(err.Error())
	}

	err = json.Unmarshal(body, &response)
	if err != nil {
		panic(err.Error())
	}

	return response
}
