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

func (c Controller) Length() int {
	l := 0
	for _, event := range c.Buffer {
		l += len(*event)
	}

	return l
}

func (c *Controller) Pop() *Event {
	if len(c.Buffer) == 0 {
		return nil
	}

	event := &Event{}
	if len(*c.Buffer[0]) != 0 {
		event = (*c.Buffer[0])[0]
		*c.Buffer[0] = (*c.Buffer[0])[1:]
	} else {
		c.Buffer = c.Buffer[1:]
		c.Pop()
	}

	return event
}

func (c *Controller) Push(delta time.Duration) {
	end := c.StartTime.Add(delta)
	c.Buffer = append(c.Buffer, generateEventBlock(c.StartTime, end))
	c.StartTime = end
}
