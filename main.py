from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import sys
from model import Id

app = FastAPI()

origins = [
    "https://anime-manager.vercel.app",
    "http://localhost:5173",
    "localhost:5173"
]

headers = {"Accept": "application/vnd.api+json", "Context-Type": "application/vnd.api+json"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def home():
    return get_library(get_id())

@app.get("/library-data", response_model=Id)
async def get_library(id: Id):
    print("get_library function triggered")
    print(id)


def get_id():
    try:
        response = requests.get('https://kitsu.io/api/edge/users?filter[name]=kimeko2', headers=headers)
    except:
        print(sys.exc_info()[0])
        print("res (from id fetch) NOT recieved")
    else:
        print("json at get_id")
        try:
            res = response.json()
        except:
            print(sys.exc_info()[0])
            print("res (from id fetch) NOT parsed as json")

    for user in res['data']:
        print("here's the user id recieved" + user['id'])

    return user['id']

def get_library(id):
    url = 'https://kitsu.io/api/edge/users/{}/library-entries'

    try:
        response = requests.get(url.format(id), headers=headers)
    except:
        print(sys.exc_info()[0])
        print("res (from library fetch) NOT recieved")
    else:
        try:
            res = response.json()
        except:
            print(sys.exc_info()[0])
            print("res (from library fetch) NOT parsed as json")

    return get_animes(res['data'])

def get_animes(data):
    arr = []
    animeURL = (((anime['relationships'])['anime'])['links'])['related']

    for anime in data:
        try:
            res = requests.get(animeURL, headers=headers)
        except:
            print(sys.exc_info()[0])
            print("failed to get anime in get_anime")
        else:
            try:
                arr.append(res.json())
            except:
                print(sys.exc_info()[0])
                print("failed parse anime as json in get_anime")
                
    return arr


