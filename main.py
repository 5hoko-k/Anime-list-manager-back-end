from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import sys

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
    return get_library()

@app.get('/search/{anime}')
async def search(anime: str):
    return get_searched_anime(anime)

def get_library():
    url = 'https://kitsu.io/api/edge/users/1342153/library-entries'

    try:
        response = requests.get(url, headers=headers)
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

    for anime in data:
        try:
            res = requests.get((((anime['relationships'])['anime'])['links'])['related'], headers=headers)
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

def get_searched_anime(anime):
    url = 'https://kitsu.io/api/edge/anime?filter[text]='+ anime

    try:
        response = requests.get(url, headers=headers)
    except:
        print(sys.exc_info()[0])
        print("res (from searched anime fetch) NOT recieved")
    else:
        try:
            res = response.json()
        except:
            print(sys.exc_info()[0])
            print("res (from library fetch) NOT parsed as json")

    print(res['data'])
    return res['data']

