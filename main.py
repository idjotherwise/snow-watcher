import asyncio
import json
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import weather_api
from models.location import Location
from services import openweather_service, report_service
from views import home

api = fastapi.FastAPI()

def configure():
    configure_routing()
    configure_api_keys()
    configure_fake_data()

def configure_api_keys():
    file = Path('settings.json').absolute()
    if not file.exists():
        print(f"WARNING: {file} file not found, you cannot continue, please see settings_template.json")
        raise Exception("settings.json file not found, you cannot continue please see settings_template.json")
    with open('settings.json') as fin:
        settings = json.load(fin)
        openweather_service.api_key = settings.get('api_key')

def configure_fake_data():
    loop = None
    try:
        loop = asyncio.get_running_loop()
        print("got loop!", loop)
    except RuntimeError:
        pass
    if not loop:
        loop = asyncio.get_event_loop()
    try:
        loc = Location(city="Feldkirch", state="Vb", country="AT")
        loop.run_until_complete(report_service.add_report("Shitton of snow today, awsome", loc))
        loop.run_until_complete(report_service.add_report("Bit of windy blow blow, tomorrow", loc))
    except RuntimeError:
        print("Could not import starter data but that's fine, get over it")



def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(weather_api.router)

if __name__ == '__main__':
    configure()
    uvicorn.run('main:api', reload=True)
else:
    configure()