package lib

import (
	"time"
)

const (
	Capacity = 50

	Close OutputState = iota
	Open
)

type (
	Buffer struct {
		Capacity int
		Events   []*Event
	}

	Controller struct {
		Buf    *Buffer
		Output OutputState
	}

	Event struct {
		Content byte
		Time    time.Time
	}

	EventBlock []*Event

	OutputState int
)

func (c *Controller) Push(e *Event) {
	c.Buf.Events = append(c.Buf.Events, e)
}

func (c *Controller) Pop() *Event {
	if c.Output == Close {
		return nil
	}

	e := c.Buf.Events[0]
	c.Buf.Events = c.Buf.Events[1:]

	return e
}
