package main

import (
	"controller/lib"
	"time"
)

var (
	startTime               time.Time
	timeInterval, timeShift time.Duration

	queue      lib.Queue
	controller lib.Controller
	network    lib.Network
)

func main() {
	timeInterval, timeShift = 10*time.Second, 5*time.Second
	startTime = time.Now().Add(timeInterval)

	queue = lib.Queue{
		StartTime: startTime,
	}

	controller = lib.Controller{
		Buf: &lib.Buffer{
			Events: make([]*lib.Event, 0),
		},
		OutputSpeed: 0.002,
	}

	network = lib.Network{
		Buf: &lib.Buffer{
			Events: make([]*lib.Event, 0),
		},
		OutputSpeed: 0.004,
		WindowSize:  5,
	}

	var toControllerChannel, toNetworkControllerChannel = make(chan *lib.Event), make(chan *lib.Event)

	go queue.Send(timeInterval, timeShift, toControllerChannel)
	go controller.Input(toControllerChannel)
	go controller.Output(toNetworkControllerChannel)
	go network.Input(toNetworkControllerChannel)

	time.Sleep(time.Hour)
}
