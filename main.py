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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def home():
    print('The home function triggered')

    return get_library(get_id())

    

@app.get("/library-data", response_model=Id)
async def get_library(id: Id):
    print("get_library function triggered")
    print(id)


def get_id():
    response = requests.get('https://kitsu.io/api/edge/users?filter[name]=kimeko2')
    res = response.json()
    if res:
        print("res (from id fetch) recieved and parsed as json")

    for user in res['data']:
        print("here's the user id recieved" + user['id'])

    return user['id']

def get_library(id):
    url = 'https://kitsu.io/api/edge/users/{}/library-entries'
    response = requests.get(url.format(id))
    res = response.json()
    if res:
        print("res (from library fetch) recieved and parsed as json")

    return get_animes(res['data'])

def get_animes(data):

    arr = []

    for anime in data:
        res = requests.get((((anime['relationships'])['anime'])['links'])['related'])

        print('yeyaaaaaaaaaaaaaaaaaaaa')
        print(res)
        arr.append(res.json())

    return arr


