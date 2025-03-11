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

type ControllerServer struct {
	db.PayloadServiceServer
}

func init() {
	startTime = time.Date(
		2025,
		1,
		1,
		0,
		0,
		0,
		0,
		time.UTC)

	controller = server.Controller{
		Length:    1,
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
	controller.Push(startTime.Add())
	return nil, nil
}
