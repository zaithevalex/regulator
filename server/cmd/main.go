package main

import (
	controller "controller/server"
	db "controller/tools/controller/proto"
	"google.golang.org/grpc"
	"net"
)

func main() {
	lis, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}

	server := grpc.NewServer()
	db.RegisterControllerServiceServer(server, &controller.ControllerServer{})

	err = server.Serve(lis)
	if err != nil {
		panic(err)
	}
}
