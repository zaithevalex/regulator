package main

import (
	"context"
	db "controller/proto"
	"google.golang.org/grpc"
	"net"
)

type Controller struct {
	db.PayloadServiceServer
}

func main() {
	lis, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}

	server := grpc.NewServer()
	db.RegisterPayloadServiceServer(server, &Controller{})
	err = server.Serve(lis)
	if err != nil {
		panic(err)
	}
}

func (s *Controller) StorePayload(ctx context.Context, packet *db.Packet) (*db.Queue, error) {
	packet.Queue.Content = append(packet.Queue.Content, packet.Content)
	return packet.Queue, nil
}
