from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Fetch_url
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
    url = 'https://kitsu.io/api/edge/users/1342153/library-entries?page[limit]=20&page[offset]=0'
    return get_library(url)

@app.get('/search/{anime}')
async def search(anime: str):
    url = 'https://kitsu.io/api/edge/anime?filter[text]='+ anime + '&page[limit]=20&pge[offset]=0'
    return get_searched_anime(url)

@app.post('/paging')
async def paging(text: Fetch_url):
    data = text.dict()
    print(data)
    return get_library(data['url'])

def get_library(url):

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
    return { 'animes': get_animes(res['data']), 'pageLinks': res['links'] }

def get_animes(data):
    arr = []

    for anime in data:
        url = (((anime['relationships'])['anime'])['links'])['related']

        try:
            res = requests.get(url, headers=headers)
        except:
            print(sys.exc_info()[0])
            print("failed to get anime in get_anime")
        else:
            try:
                data = res.json()
                arr.append(data['data'])
            except:
                print(sys.exc_info()[0])
                print("failed parse anime as json in get_anime")

    return arr

def get_searched_anime(url):

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
    print(res['links'])

    return { 'animes': res['data'], 'pageLinks': res['links'] }

