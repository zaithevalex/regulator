package main

import (
	"context"
	general "controller/client"
	db "controller/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	ctx := context.Background()

	con, err := grpc.Dial("localhost:8080", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		panic(err)
	}
	defer con.Close()

	q := &db.Queue{}
	client := db.NewPayloadServiceClient(con)
	q, err = client.Store(ctx, &db.Packet{Queue: q, Content: general.GeneratePayload()})
	if err != nil {
		panic(err)
	}
}
