package main

import (
	"context"
	"controller/lib"
	db "controller/proto"
	"controller/server"
	"google.golang.org/grpc"
	"google.golang.org/protobuf/types/known/emptypb"
	"net"
	"time"
)

var (
	startTime               time.Time
	timeInterval, timeShift time.Duration

	queue      lib.Queue
	controller lib.Controller
)

type ControllerServer struct {
	db.ControllerServiceServer
}

func init() {
	timeInterval, timeShift = 10*time.Second, 5*time.Second
	startTime = time.Now().Add(timeInterval)

	queue = lib.Queue{
		StartTime: startTime,
	}

	controller = lib.Controller{
		Input:  make(chan *server.Event, server.Capacity),
		Output: make(chan *server.Event),
	}
}

func main() {
	lis, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}

	server := grpc.NewServer()
	db.RegisterControllerServiceServer(server, &ControllerServer{})

	err = server.Serve(lis)
	if err != nil {
		panic(err)
	}
}

func (s *ControllerServer) StoreToController(_ context.Context, _ *emptypb.Empty) (*emptypb.Empty, error) {
	if e := queue.First(); e != nil {
		if e.Time.UnixMilli() < time.Now().UnixMilli() {
			controller.Input <- queue.Pop()
		}
	}

	if queue.StartTime.UnixMilli() < time.Now().Add(timeShift).UnixMilli() {
		queue.Push(timeInterval)
	}

	return nil, nil
}
