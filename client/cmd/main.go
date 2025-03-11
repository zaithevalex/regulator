package main

import (
	"context"
	db "controller/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/protobuf/types/known/emptypb"
)

func main() {
	ctx := context.Background()

	con, err := grpc.Dial("localhost:8080", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		panic(err)
	}
	defer con.Close()

	for {
		client := db.NewPayloadServiceClient(con)
		_, _ = client.Store(ctx, &emptypb.Empty{})
	}
}
