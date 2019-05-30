class API(object):

    API_URL = "https://skylines.aero/api/"
    REQUEST_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def __init__(self, requests):
        self.__requests = requests
        self.__requests.packages.urllib3.disable_warnings()
        print("api init")

    def get_live(self):
        return_string = ""
        response = self.__requests.get(API.API_URL + "live", headers=API.REQUEST_HEADER, timeout=10, verify=False).json()
        for track in response["tracks"]:
            club = self.__requests.get("https://skylines.aero/api/users/" + str(track["pilot"]["id"]) + "?extended", headers=API.REQUEST_HEADER, timeout=10, verify=False).json()["club"]
            if club:
                if club["id"] == 30: # Akaflieg Club ID 30
                    return_string += track["pilot"]["name"] + "\n"
        if return_string == "":
            return_string = "Niemand ist heute mit Livetrack geflogen"
        return return_string

    def get_pilots(self, club_id):
        pilots = self.__requests.get("https://skylines.aero/api/users/?club=" + club_id, headers=API.REQUEST_HEADER, timeout=10, verify=False).json()["users"]
        return [pilot["id"] for pilot in pilots]