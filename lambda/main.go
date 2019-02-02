package main

import (
	"fmt"
	"log"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

// ---- types ----
type (
	LexEvent events.LexEvent
)

// ---------------

// ---- factories ----
// ---------------

// ---- functions ----
func main() {
	fmt.Println("Start Lambda function handler")
	lambda.Start(Handler)
}

// ---------------

// ---- methods ----
func Handler(event LexEvent) (interface{}, error) {
	log.Printf("Processing lex event from %s\n", event.UserID)

	// dispatch lex intent
	intentName = event.CurrentIntent.Name
	log.Printf("Processing current intent name %s\n", intentName)
}

// ---------------
