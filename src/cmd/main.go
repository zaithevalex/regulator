package main

import (
	"controller/src"
	"time"
)

func main() {
	src.Run()
	time.Sleep(time.Hour)
}
