package server

import (
	"context"
	"controller/lib"
	db "controller/tools/controller/proto"
	"google.golang.org/protobuf/types/known/emptypb"
	"time"
)

var (
	startTime               time.Time
	timeInterval, timeShift time.Duration

	queue      lib.Queue
	controller lib.Controller
)

type (
	ControllerServer struct {
		db.ControllerServiceServer
	}
)

func init() {
	timeInterval, timeShift = 10*time.Second, 5*time.Second
	startTime = time.Now().Add(timeInterval)

	queue = lib.Queue{
		StartTime: startTime,
	}

	controller = lib.Controller{
		Buf: &lib.Buffer{
			Events:   make([]*lib.Event, 0),
			Capacity: lib.Capacity,
		},
	}
}

func (s *ControllerServer) StoreToController(_ context.Context, _ *emptypb.Empty) (*emptypb.Empty, error) {
	if e := queue.First(); e != nil {
		if e.Time.UnixMilli() < time.Now().UnixMilli() {
			controller.Buf.Events = append(controller.Buf.Events, queue.Pop())
		}
	}

	if queue.StartTime.UnixMilli() < time.Now().Add(timeShift).UnixMilli() {
		queue.Generate(timeInterval)
	}

	return nil, nil
}
