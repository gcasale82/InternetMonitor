//Simple Internet monitor with GO
package main

import (
	"time"
	"net"
	"fmt"
	"os"
	"log")

func create_log(message string) error {
	       f, err := os.OpenFile("connection.log", os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0644)
        if err != nil {
                log.Fatal(err)
        }   

        //defer to close when you're done with it, not because you think it's idiomatic!
        defer f.Close()

        //set output of logs to f
        log.SetOutput(f)

        //test case
        log.Println(message)
		return err
}
 

func main(){

err := create_log("Starting the script ...")
if err != nil {
	fmt.Println("Error")
}
status := true
tFailed := time.Now()
tRestored := time.Now()

for {
time.Sleep(1 * time.Second)
	if status == true {
 _, err = net.LookupIP("google.com")
    if err != nil {
        create_log("Internet went down ")
		status = false
		tFailed = time.Now()
    }
} else {
_, err := net.LookupIP("google.com")
    if err == nil {
		tRestored = time.Now()
		create_log(fmt.Sprintf(" Internet restored after %v" , tRestored.Sub(tFailed).Seconds()))
		status = true
    }


	}

}

}
