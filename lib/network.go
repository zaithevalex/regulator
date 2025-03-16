package lib

import (
	"fmt"
	"os"
	"time"
)

type Network struct {
	Buf *Buffer

	// Latency: amount of events per millis
	Latency float64

	WindowSize          int
	FullTransmittedData int
}

func (network *Network) Backlog(c *Controller) {
	if c.FullTransmittedData >= network.FullTransmittedData+network.WindowSize {
		c.Out = Open
	} else {
		c.Out = Close
	}
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

func (network *Network) Output(file *os.File) error {
	for {
		if len(network.Buf.Events) > 0 {
			time.Sleep(time.Microsecond * time.Duration(network.Latency*toMicros))
			network.Pop()
			network.FullTransmittedData++
			fmt.Printf("y(t): %d\n", network.FullTransmittedData)

			_, err := file.WriteString(fmt.Sprintf("%d ", time.Now().UnixMilli()))
			if err != nil {
				return err
			}
		}
	}
}
