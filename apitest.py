import requests
import json

requests.packages.urllib3.disable_warnings()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def searchAPI():
    response = requests.get("https://skylines.aero/api/live", headers=headers, timeout=10, verify=False)
    for track in response.json()["tracks"]:
        club = requests.get("https://skylines.aero/api/users/" + str(track["pilot"]["id"]) + "?extended", headers=headers, timeout=10, verify=False).json()["club"]
        if club:
            if club["id"] == 1246: # Akaflieg Club ID 30
                if track["nearestAirport"]["name"] != "Rheinstetten" or track["nearestAirportDistance"] > track["altitude"] * 25:
                    print("Pilot " + str(track["pilot"]["name"]) + "aus gleitbereich")

searchAPI()