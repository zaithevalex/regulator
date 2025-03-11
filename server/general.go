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
		content [][]byte
		Time    time.Time
	}

	Controller struct {
		Buffer   []*Event
		Length   int
		Capacity int
	}
)

func GeneratePayload(amount int) [][]byte {
	eventsAmount := rand.Intn(amount) + 1

	var payloadList [][]byte
	for range eventsAmount {
		payloadList = append(payloadList, make([]byte, rand.Intn(maxRandomLength-minRandomLength+1)+minRandomLength))
	}

	return payloadList
}

func (c *Controller) GenerateTimes(duration time.Duration) {
	payload := GeneratePayload(maxGeneratedEvents)

	c.Buffer = append(c.Buffer, &Event{content: payload})
	c.Buffer[len(c.Buffer)-1].Time = c.Buffer[len(c.Buffer)-2].Time.Add(duration)
	c.Length += len(c.Buffer[len(c.Buffer)-1].content)
}
