import os
import json
import codecs
import requests
from dotenv import load_dotenv
load_dotenv()


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def runUpdate():
    url = "https://" + os.environ.get("PANEL_URL") + \
        "/api/application/servers?include=allocations"
    key = "Bearer " + os.environ.get("API_KEY")

    headers = {"Authorization": key}

    response = requests.request("GET", url, headers=headers)

    data = response.json()

    total_pages = data["meta"]["pagination"]["total_pages"]
    current_page = 0

    while(current_page < total_pages):
        for i in range(len(data["data"])):
            # Load the dynamic parts into memory
            uuid = data["data"][i]["attributes"]["uuid"]
            domain = data["data"][i]["attributes"]["name"]
            ip_port = data["data"][i]["attributes"]["relationships"]["allocations"]["data"][0]["attributes"]["ip"] + \
                ":" + str(data["data"][i]["attributes"]["relationships"]
                          ["allocations"]["data"][0]["attributes"]["port"])
            sleep_timeout = 0
            try:
                sleep_timeout = data["data"][i]["attributes"]["container"]["environment"]["SLEEP_TIMEOUT"]
            except:
                pass

            # Introduce the schema and static parts
            file_name = "configs/" + uuid + ".json"
            schema = {
                "timeout": 1000,
                "containerTimeout": 60000,
                "disconnectMessage": "\u00A72\u00A7l{{domain}} \u00A7r\u00A76is now starting up!\n\u00A78Please come back in 30-45 seconds...",
                "offlineStatus": {
                    "versionName": "\u00A7e▶ \u00A76\u00A7lSleeping",
                    "protocolNumber": 0,
                    "maxPlayers": 2,
                    "playersOnline": 2,
                    "motd": "      \u00A7e\u00A7lThe server is currently sleeping...",
                    "playerSamples": [
                        {
                            "name": "\u00A7cServer is Sleeping!",
                            "uuid": "ec561538-f3fd-461d-aff5-086b22154bce"
                        },
                        {
                            "name": "\u00A77\u00A7l~~~~~~~~",
                            "uuid": "ec561538-f3fd-461d-aff5-086b22154bce"
                        },
                        {
                            "name": "You can either start by joining",
                            "uuid": "ec561538-f3fd-461d-aff5-086b22154bce"
                        },
                        {
                            "name": "the server or by starting it ",
                            "uuid": "ec561538-f3fd-461d-aff5-086b22154bce"
                        },
                        {
                            "name": "through the web panel!",
                            "uuid": "ec561538-f3fd-461d-aff5-086b22154bce"
                        },
                        {
                            "name": " ",
                            "uuid": "ec561538-f3fd-461d-aff5-086b22154bce"
                        },
                        {
                            "name": "\u00A7fMade possible by \u00A7a\u00A7l\u00A7oBasilisk Hosting",
                            "uuid": "ec561538-f3fd-461d-aff5-086b22154bce"
                        }
                    ]
                },
                "pterodactyl": {
                    "ServerUUID": "",
                    "PanelURL": os.environ.get("PANEL_URL"),
                    "Key": os.environ.get("API_KEY")
                },
                "domainName": "",
                "proxyTo": ""
            }

            # Load the data into the schema
            schema["pterodactyl"]["ServerUUID"] = uuid
            schema["domainName"] = domain
            schema["proxyTo"] = ip_port
            schema["containerTimeout"] = int(sleep_timeout)

            # Check if file is different
            diff = True
            if os.path.isfile(file_name):
                with open(file_name) as f:
                    orig = json.load(f)
                    if(ordered(orig) == ordered(schema)):
                        diff = False

            if(diff):
                with open(file_name, 'wb') as f:
                    json.dump(schema, codecs.getwriter(
                        'utf-8')(f), ensure_ascii=True)
        current_page += 1


if __name__ == "__main__":
    import time
    while True:
        runUpdate()
        time.sleep(1)

