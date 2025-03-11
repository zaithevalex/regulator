package lib

import "controller/server"

type Controller struct {
	Capacity int
	Input    chan<- *server.Event
	Output   <-chan *server.Event
}
