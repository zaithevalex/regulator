package lib

import (
	"fmt"
	"time"
)

const toMicros = 1000000.0

type (
	Buffer struct {
		Events []*Event
	}

	Controller struct {
		Buf *Buffer

		// OutputSpeed: amount of events per seconds
		OutputSpeed float64
	}

	Event struct {
		Content byte
		Time    time.Time
	}

	EventBlock []*Event
)

func (c *Controller) Input(toControllerChannel chan *Event) {
	for {
		c.Buf.Events = append(c.Buf.Events, <-toControllerChannel)
		fmt.Println("CONTROLLER BUFFER:", c.Buf.Events)
	}
}

func (c *Controller) Push(e *Event) {
	c.Buf.Events = append(c.Buf.Events, e)
}

func (c *Controller) Pop() *Event {
	if len(c.Buf.Events) == 0 {
		return nil
	}

	e := c.Buf.Events[0]
	c.Buf.Events = c.Buf.Events[1:]

	return e
}

func (c *Controller) Output(toNetworkControllerChannel chan *Event) {
	for {
		if len(c.Buf.Events) > 0 {
			time.Sleep(time.Microsecond * time.Duration(c.OutputSpeed*toMicros))
			event := c.Pop()
			toNetworkControllerChannel <- event
			fmt.Printf("EVENT: %p LOADED TO NETWORK\n", event)
		}
	}
}
