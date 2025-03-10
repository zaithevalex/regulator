package client

import (
	"math/rand"
	"time"
)

const (
	minRandomLength = 46
	maxRandomLength = 1500
)

func GeneratePayload() []byte {
	length := rand.Intn(maxRandomLength-minRandomLength+1) + minRandomLength
	return make([]byte, length)
}

func GenerateTimes(times *[]time.Duration, endTime time.Duration) {

}
