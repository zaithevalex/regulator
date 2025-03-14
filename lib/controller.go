package lib

import (
	"fmt"
	"time"
)

type (
	Buffer struct {
		Events []*Event
	}

	Controller struct {
		Buf *Buffer

		// OutputSpeed: amount of events per millis
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
		//mu.Lock()
		c.Buf.Events = append(c.Buf.Events, <-toControllerChannel)
		fmt.Println("c.Buf.Events:", c.Buf.Events, time.Now())
		//mu.Unlock()
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
		event := c.Pop()

		if event != nil {
			time.Sleep(5 * time.Second)
			toNetworkControllerChannel <- event
			fmt.Printf("EVENT: %p, TIME: %v, NOW: %v\n", event, event.Time, time.Now())
		}
	}
}
