package lib

import (
	"controller/server"
	"time"
)

type Queue struct {
	EventBlocks []*server.EventBlock
	StartTime   time.Time
}

func (c Queue) All() []server.Event {
	var events []server.Event
	for _, eventBlock := range c.EventBlocks {
		for _, event := range *eventBlock {
			events = append(events, *event)
		}
	}

	return events
}

func (c Queue) First() *server.Event {
	for len(c.EventBlocks) > 0 {
		if len(*c.EventBlocks[0]) > 0 {
			return (*c.EventBlocks[0])[0]
		} else {
			c.EventBlocks = c.EventBlocks[1:]
		}
	}

	return nil
}

func (c Queue) Length() int {
	l := 0
	for _, event := range c.EventBlocks {
		l += len(*event)
	}

	return l
}

func (c *Queue) Pop() *server.Event {
	for len(c.EventBlocks) > 0 {
		if len(*c.EventBlocks[0]) > 0 {
			event := (*c.EventBlocks[0])[0]
			*c.EventBlocks[0] = (*c.EventBlocks[0])[1:]

			return event
		} else {
			c.EventBlocks = c.EventBlocks[1:]
		}
	}

	return nil
}

func (c *Queue) Push(delta time.Duration) {
	end := c.StartTime.Add(delta)
	c.EventBlocks = append(c.EventBlocks, server.GenerateEventBlock(c.StartTime, end))
	c.StartTime = end
}
