package src

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

	toControllerChannel        chan *lib.Event
	toNetworkControllerChannel chan *lib.Event
	toBacklog                  chan *lib.Event
)

func init() {
	timeInterval, timeShift = 10*time.Second, 5*time.Second
	startTime = time.Now().Add(timeInterval)

	queue = lib.Queue{
		StartTime: startTime,
	}

	controller = lib.Controller{
		Buf: &lib.Buffer{
			Events: make([]*lib.Event, 0),
		},
		OutputSpeed: 4,
	}

	network = lib.Network{
		Buf: &lib.Buffer{
			Events: make([]*lib.Event, 0),
		},
		OutputSpeed: 8,
		WindowSize:  5,
	}

	toControllerChannel = make(chan *lib.Event)
	toNetworkControllerChannel = make(chan *lib.Event)
	toBacklog = make(chan *lib.Event)
}

func Run() {
	go queue.Send(timeInterval, timeShift, toControllerChannel)
	go controller.Input(toControllerChannel)
	go controller.Output(toNetworkControllerChannel)
	go network.Input(toNetworkControllerChannel)
	go network.Output(toBacklog)
	//<-toBacklog
}
