package main

import (
	"controller/src"
	"os"
	"time"
)

func main() {
	dir, err := os.Getwd()
	if err != nil {
		panic(err)
	}

	xFile, err := os.Create(dir + "/analysis/dataset/x.txt")
	if err != nil {
		panic(err)
	}
	defer xFile.Close()

	yFile, err := os.Create(dir + "/analysis/dataset/y.txt")
	if err != nil {
		panic(err)
	}
	defer yFile.Close()

	src.Run(xFile, yFile)
	time.Sleep(1 * time.Minute)
}
