package process

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

type pterodactyl struct {
	Endpoint   string
	Key        string
	ServerName string
}

// NewDocker create a new docker process that manages a container
func NewPtero(url string, api string, serverUUID string) (Process, error) {
	return pterodactyl{
		Endpoint:   url,
		Key:        api,
		ServerName: serverUUID,
	}, nil
}

func (proc pterodactyl) Start() error {
	url := fmt.Sprintf("https://%s/api/client/servers/%s/power", proc.Endpoint, proc.ServerName)
	bearer := fmt.Sprintf("Bearer %s", proc.Key)

	payload := strings.NewReader("{\n  \"signal\":\"start\"\n}")

	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("Authorization", bearer)
	req.Header.Add("content-type", "application/json")

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}

	defer res.Body.Close()
	return nil
}

func (proc pterodactyl) Stop() error {
	url := fmt.Sprintf("https://%s/api/client/servers/%s/power", proc.Endpoint, proc.ServerName)
	bearer := fmt.Sprintf("Bearer %s", proc.Key)

	payload := strings.NewReader("{\n  \"signal\":\"stop\"\n}")

	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("Authorization", bearer)
	req.Header.Add("content-type", "application/json")

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}

	defer res.Body.Close()
	return nil
}

func (proc pterodactyl) IsRunning() (bool, error) {
	url := fmt.Sprintf("https://%s/api/client/servers/%s/power", proc.Endpoint, proc.ServerName)
	bearer := fmt.Sprintf("Bearer %s", proc.Key)

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("Authorization", bearer)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := ioutil.ReadAll(res.Body)

	data := Response{}
	json.Unmarshal(body, &data)

	running := false

	fmt.Printf("%s\n", data.Attributes.Current_State)

	if data.Attributes.Current_State == "running" {
		running = true
	}

	fmt.Println(data.Attributes.Current_State)

	return running, nil
}

type Response struct {
	Object     string
	Attributes Properties
}

type Properties struct {
	Current_State string
	Is_Suspended  bool
	Resources     Usage
}

type Usage struct {
	Memory_Bytes     int
	CPU_Absolute     int
	Disk_Bytes       int
	Network_RX_Bytes int
	Network_TX_Bytes int
}
