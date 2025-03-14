package lib

import (
	"fmt"
	"time"
)

type Network struct {
	Buf *Buffer

	// OutputSpeed: amount of events per millis
	OutputSpeed float64

	WindowSize int
}

func (network *Network) Input(toNetworkControllerChannel chan *Event) {
	for {
		if len(network.Buf.Events) < network.WindowSize {
			network.Push(<-toNetworkControllerChannel)
			fmt.Println("NETWORK BUFFER:", network.Buf.Events)
		}
	}
}

func (network *Network) Push(e *Event) {
	network.Buf.Events = append(network.Buf.Events, e)
}

func (network *Network) Pop() *Event {
	if len(network.Buf.Events) == 0 {
		return nil
	}

	e := network.Buf.Events[0]
	network.Buf.Events = network.Buf.Events[1:]

	return e
}

func (network *Network) Output(toBacklog chan *Event) {
	for {
		if len(network.Buf.Events) > 0 {
			time.Sleep(time.Microsecond * time.Duration(network.OutputSpeed*toMicros))
			event := network.Pop()
			toBacklog <- event
			fmt.Printf("POP FROM NETWORK BUFFER: %p, TIME.NOW: %v\n", event, time.Now())
		}
	}
}
