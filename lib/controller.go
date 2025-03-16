package lib

import (
	"fmt"
	"time"
)

const toMicros = 1000000.0
const (
	Close OutputState = iota
	Open
)

type (
	Buffer struct {
		Events []*Event
	}

	Controller struct {
		Buf *Buffer

		// FullTransmittedData: amount of events per seconds
		FullTransmittedData int
		//
		Out OutputState
	}

	Event struct {
		Content byte
		Time    time.Time
	}

	EventBlock  []*Event
	OutputState int
)

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

func (c *Controller) Receive(toControllerChannel, toNetworkControllerChannel chan *Event) {
	for {
		if c.Out == Open {
			fmt.Printf("x(t): %d\n", c.FullTransmittedData)

			if len(c.Buf.Events) > 0 {
				event := c.Pop()
				toNetworkControllerChannel <- event
				c.FullTransmittedData++
			} else {
				toNetworkControllerChannel <- <-toControllerChannel
				c.FullTransmittedData++
			}
		} else {
			c.Buf.Events = append(c.Buf.Events, <-toControllerChannel)
		}
	}
}
