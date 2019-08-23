
package main

import (
    "fmt"
    "net/http"
    "log"
)

func testHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "this is a test")
}

func main() {
    http.HandleFunc("/", testHandler)
    log.Println("starting server")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
