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
			network.Buf.Events = append(network.Buf.Events, <-toNetworkControllerChannel)
			fmt.Println("network.Buf.Events:", network.Buf.Events, time.Now())
		}
	}
}
