package server

import (
	"math/rand"
	"time"
)

const (
	Capacity           = 50
	maxGeneratedEvents = 10
	minRandomLength    = 46
	maxRandomLength    = 1500
)

type (
	Event struct {
		content []byte
		Time    time.Time
	}

	Controller struct {
		Buffer    []*EventBlock
		Length    int
		Capacity  int
		StartTime time.Time
	}

	EventBlock []*Event
)

func generateEventBlock(start, end time.Time) *EventBlock {
	eventBlock := EventBlock{}
	for range rand.Intn(maxGeneratedEvents) {
		eventBlock = append(eventBlock, &Event{
			content: make([]byte, rand.Intn(maxRandomLength-minRandomLength+1)+minRandomLength),
			Time:    time.UnixMilli(rand.Int63n(end.UnixMilli()-start.UnixMilli()) + start.UnixMilli()),
		})
	}

	return &eventBlock
}

func (c *Controller) Push(delta time.Duration) {
	end := c.StartTime.Add(delta)

	c.Buffer = append(c.Buffer, generateEventBlock(c.StartTime, c.StartTime.Add(delta)))
	c.Length++
	c.StartTime = end
}
