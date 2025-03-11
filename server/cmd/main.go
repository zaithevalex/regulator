package main

import (
	"context"
	db "controller/proto"
	"controller/server"
	"google.golang.org/grpc"
	"google.golang.org/protobuf/types/known/emptypb"
	"net"
	"time"
)

var startTime time.Time
var controller server.Controller
var timeInterval, timeShift time.Duration

type ControllerServer struct {
	db.PayloadServiceServer
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
	db.RegisterPayloadServiceServer(server, &ControllerServer{})

	err = server.Serve(lis)
	if err != nil {
		panic(err)
	}
}

func (s *ControllerServer) Store(_ context.Context, _ *emptypb.Empty) (*db.Queue, error) {
	if controller.StartTime.UnixMilli() < time.Now().Add(timeShift).UnixMilli() {
		controller.Push(timeInterval)
	}

	return nil, nil
}
