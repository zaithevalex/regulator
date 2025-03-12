package lib

import (
	"math/rand"
	"slices"
	"time"
)

const (
	maxGeneratedEvents = 10
)

type Queue struct {
	EventBlocks []*EventBlock
	StartTime   time.Time
}

func (c Queue) All() []Event {
	var events []Event
	for _, eventBlock := range c.EventBlocks {
		for _, event := range *eventBlock {
			events = append(events, *event)
		}
	}

	return events
}

func (c Queue) First() *Event {
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

func (c *Queue) Pop() *Event {
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

func (c *Queue) Generate(delta time.Duration) {
	end := c.StartTime.Add(delta)
	c.EventBlocks = append(c.EventBlocks, generateEventBlock(c.StartTime, end))
	c.StartTime = end
}

func generateEventBlock(start, end time.Time) *EventBlock {
	eventBlock := EventBlock{}
	for range rand.Intn(maxGeneratedEvents) {
		eventBlock = append(eventBlock, &Event{
			Content: byte(rand.Intn(128)),
			Time:    time.UnixMilli(rand.Int63n(end.UnixMilli()-start.UnixMilli()) + start.UnixMilli()),
		})
	}

	slices.SortFunc(eventBlock, func(a, b *Event) int {
		if a.Time.UnixMilli() > b.Time.UnixMilli() {
			return 1
		} else if a.Time.UnixMilli() < b.Time.UnixMilli() {
			return -1
		} else {
			return 0
		}
	})
	return &eventBlock
}
