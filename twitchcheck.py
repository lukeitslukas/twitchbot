import os
import requests
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch

load_dotenv()

client_id = os.getenv("CLIENTID")
client_secret = os.getenv("CLIENTSECRET")

twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])

TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"

API_HEADERS = {
    'Client-ID': client_id,
    'Accept': 'application/vnd.twitchtv.v5+json',
}


def checkuser(user):  # returns true if online, false if not
    userid = twitch.get_users(logins=[user])['data'][0]['id']
    url = TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
    try:
        req = requests.Session().get(url, headers=API_HEADERS)
        jsondata = req.json()
        if 'stream' in jsondata:
            if jsondata['stream'] is not None:
                return jsondata
            else:
                return "empty"
    except Exception as e:
        print("Error checking user: ", e)
        return "empty"
