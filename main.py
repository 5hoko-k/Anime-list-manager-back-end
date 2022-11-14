from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
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
    response = requests.get('https://kitsu.io/api/edge/users?filter[name]=kimeko2', headers=headers)
    print("json at get_id")
    res = response.json()
    if res:
        print("res (from id fetch) recieved and parsed as json")

    for user in res['data']:
        print("here's the user id recieved" + user['id'])

    return user['id']

def get_library(id):
    url = 'https://kitsu.io/api/edge/users/{}/library-entries'
    response = requests.get(url.format(id), headers=headers)
    res = response.json()
    if res:
        print("res (from library fetch) recieved and parsed as json")

    return get_animes(res['data'])

def get_animes(data):
    arr = []
    animeURL = (((anime['relationships'])['anime'])['links'])['related']

    for anime in data:
        res = requests.get(animeURL, headers=headers)
        arr.append(res.json())
    return arr


