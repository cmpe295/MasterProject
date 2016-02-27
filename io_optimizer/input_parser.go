package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

func read_file(filename string) {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		// do something
	}
	lines := strings.Split(string(content), "\n")
	fmt.Print(lines[1])
}

func main() {
	read_file("/Users/dyao/Documents/go/src/github.com/DuoYao/MasterProject/logs/io.csv")
}
