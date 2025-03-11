package server

import (
	"math/rand"
	"slices"
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

func (c *Controller) Push(delta time.Duration) {
	end := c.StartTime.Add(delta)
	c.Buffer = append(c.Buffer, generateEventBlock(c.StartTime, end))
	c.StartTime = end
}
