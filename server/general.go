package server

import (
	"math/rand"
	"slices"
	"time"
)

const (
	Capacity           = 50
	maxGeneratedEvents = 10
)

type (
	Event struct {
		Content byte
		Time    time.Time
	}

	EventBlock []*Event
)

func GenerateEventBlock(start, end time.Time) *EventBlock {
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
