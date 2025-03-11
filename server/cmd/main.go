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

var controller server.Controller

type ControllerServer struct {
	db.PayloadServiceServer
}

func init() {
	controller = server.Controller{
		Buffer: []*server.Event{
			{
				Time: time.Date(
					2025,
					1,
					1,
					0,
					0,
					0,
					0,
					time.UTC),
			},
		},
		Length:   1,
		Capacity: server.Capacity,
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
	go func() {
		controller.GenerateTimes(5 * time.Second)
	}()
	time.Sleep(5 * time.Second)
	fmt.Println("Length:", controller.Length, "Capacity:", controller.Capacity, "Buffer:", controller.Buffer[len(controller.Buffer)-1].Time)

	return nil, nil
}
