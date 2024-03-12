# import modules
from dotenv import load_dotenv
import os 
import base64
from requests import post, get
import json
from flask import Flask, render_template

load_dotenv() # calls ths "load_dot_env" function to load the .env
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# -- request token --
def get_token():
        # concatenate client_id and client_secret as auth_string
    auth_string = client_id + ":" + client_secret
        # encode it
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)

    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


# -- future request will use this token also --
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    type = "artist"
    limit = 10
    query = f"q={artist_name}&type={type}&limit={limit}"
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    # print(query_url) # see full API URL Query string
    if len(json_result) == 0:
        print("No artist with this name exists..")
        return None
    
    return json_result[0]
    # print(json_result)
    # print(json_result.artist.items[0].name)

token = get_token()
# print('token:', token)
# result = search_for_artist(token, "Taylor Swift")
result = search_for_artist(token, "yeah yeah yeah")

print(result["name"] + ".", "Total Followers:", result["followers"]["total"])
print(result["images"][0]["url"])
print(result)
app = Flask(__name__)


@app.route('/')
def index():
    p = '<p>' + 'I searched for my favorite artist: ' + result["name"] + '<p>'
    p2 = '<p>This is their Spotify profile art.</p>'
    img_html = '<img src="' + result["images"][0]["url"] + '"' + ' alt="Example Image">'

    return 'Welcome to my Spotify API Test. It uses Python & Flask., ' + p + p2 + img_html

if __name__ == '__main__':
    app.run(debug=True)

# ---- Example result ----
# {'artists': 
#         {'href': 'https://api.spotify.com/v1/search?query=Taylor+Swift&type=artist&offset=0&limit=1', 
#         'items': [
#                     {'external_urls': 
#                             {'spotify': 'https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02'}, 
#                             'followers': {'href': None, 
#                                         'total': 103870155}, 
#                     'genres': ['pop'], 
#                     'href': 'https://api.spotify.com/v1/artists/06HL4z0CvFAxyc27GXpf02', 
#                     'id': '06HL4z0CvFAxyc27GXpf02', 
#                     'images': [
#                                 {'height': 640, 
#                                 'url': 'https://i.scdn.co/image/ab6761610000e5eb859e4c14fa59296c8649e0e4', 
#                                 'width': 640}, 
#                                 {'height': 320, 
#                                 'url': 'https://i.scdn.co/image/ab67616100005174859e4c14fa59296c8649e0e4', 
#                                     'width': 320}, 
#                                     {'height': 160,
#                                     'url': 'https://i.scdn.co/image/ab6761610000f178859e4c14fa59296c8649e0e4', 
#                                     'width': 160}
#                             ], 
#                     'name': 'Taylor Swift', 
#                     'popularity': 100, 
#                     'type': 'artist', 
#                     'uri': 'spotify:artist:06HL4z0CvFAxyc27GXpf02'}
#                 ], 
#     'limit': 1, 'next': None, 'offset': 0, 'previous': None, 'total': 1}
# }