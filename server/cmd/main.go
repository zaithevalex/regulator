package main

import (
	"context"
	db "controller/proto"
	"controller/server"
	"fmt"
	"google.golang.org/grpc"
	"google.golang.org/protobuf/types/known/emptypb"
	"net"
	"time"
)

var startTime time.Time
var controller server.Controller
var timeInterval, timeShift time.Duration

type ControllerServer struct {
	db.ControllerServiceServer
}

func init() {
	timeInterval, timeShift = 10*time.Second, 5*time.Second
	startTime = time.Now().Add(timeInterval)

	controller = server.Controller{
		Capacity:  server.Capacity,
		StartTime: startTime,
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
	if e := controller.First(); e != nil {
		if e.Time.UnixMilli() < time.Now().UnixMilli() {
			fmt.Println("E.TIME:", e.Time, controller.First())
			controller.Pop()
		}
	}

	if controller.StartTime.UnixMilli() < time.Now().Add(timeShift).UnixMilli() {
		controller.Push(timeInterval)
	}

	return nil, nil
}
